#!/usr/bin/env python3
"""转换全家桶 skills 为 DeepSeek Harness 格式。

规则(依据 deepseek-ai/deepseek-harness docs/subsystems/skills.zh.md):
- name: kebab-case(保留原值, 全家桶已合规)
- description: 模型路由文本, ≤500 字符(DSH catalogDescriptionMaxLength 默认 500)
- 其他 frontmatter 键解析为 metadata(DSH 不认 metadata.hermes, 但保留无害)
- deprecated 的 skill 不转换(文件保留在 Hermes 版, 不进 DSH 版)
- 正文原样保留(DSH 全文加载), references/scripts 一并拷贝

用法: python3 convert-dsh.py <src_family_dir> <dst_dir>
"""
import os
import re
import sys
import shutil

SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.expanduser("~/.hermes/skills/vibe-coding-family")
DST = sys.argv[2] if len(sys.argv) > 2 else "deepseek-harness/vibe-coding-family"

DESC_LIMIT = 500
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")

def parse_frontmatter(text):
    """返回 (frontmatter_dict, body_start_index)。支持 | 块与单行。"""
    if not text.startswith("---\n"):
        return {}, 0
    end = text.find("\n---", 4)
    if end < 0:
        return {}, 0
    fm = text[4:end]
    body_start = end + 4  # 跳过 \n---
    # 解析成简单的 key: value 列表(块用 | 时收集后续缩进行)
    lines = fm.split("\n")
    entries = []
    cur_key = None
    cur_val = []
    for ln in lines:
        if not ln.strip():
            continue
        m = re.match(r"^([a-zA-Z0-9_-]+):\s*(.*)$", ln)
        if m and not ln.startswith((" ", "\t")):
            if cur_key:
                entries.append((cur_key, "\n".join(cur_val)))
            cur_key, rest = m.group(1), m.group(2)
            cur_val = [rest] if rest.strip() else []
        else:
            cur_val.append(ln.strip())
    if cur_key:
        entries.append((cur_key, "\n".join(cur_val)))
    d = {}
    for k, v in entries:
        d[k] = v
    return d, body_start

def compress_description(desc, name):
    """压缩 description 到 ≤500 字符: 保首句 + 触发词 + 负触发词 + 类型。始终单行化。"""
    desc = desc.strip()
    if len(desc) > DESC_LIMIT:
        # 提取关键段
        trig = ""
        m = re.search(r"触发词[:：]([^\n。]+)", desc)
        if m:
            trig = m.group(1).strip()[:200]
        neg = ""
        m = re.search(r"负触发词[:：]([^\n。]+)", desc)
        if m:
            neg = "不适用: " + m.group(1).strip()[:100]
        typ = ""
        m = re.search(r"metadata:\s*\n\s*hermes:\s*\n\s*type:\s*(\w+)", desc) or \
            re.search(r"type[:：]\s*(\w+)", desc)
        if m:
            typ = m.group(1)
        # 首句(去版本历史等)
        first = re.split(r"[。\n]", desc)[0].strip()
        parts = [first]
        if trig:
            parts.append("触发: " + trig)
        if neg:
            parts.append(neg)
        if typ:
            parts.append("类型: " + typ)
        out = "；".join(parts)
        if len(out) > DESC_LIMIT:
            out = out[:DESC_LIMIT - 1].rstrip() + "…"
    else:
        out = desc
    # 单行化(DSH 目录 XML 转义渲染, 换行无意义且占字符)
    out = re.sub(r"\s+", " ", out).strip()
    return out

def convert_skill(src_dir, dst_dir, name):
    os.makedirs(dst_dir, exist_ok=True)
    src_skill = os.path.join(src_dir, "SKILL.md")
    if not os.path.exists(src_skill):
        return None
    with open(src_skill, encoding="utf-8") as f:
        text = f.read()
    fm, body_start = parse_frontmatter(text)
    if not fm.get("name") or not fm.get("description"):
        return None
    desc = fm["description"].strip()
    # metadata 块可能是 YAML 嵌套, 先整体从原文提取 description
    m = re.search(r"description:\s*\|?\s*(.*?)(?=\n[a-z-]+:|\n---)", text, re.S)
    if m:
        desc = m.group(1).strip()
    new_desc = compress_description(desc, name)
    # 提取 hermes type
    typ = ""
    m = re.search(r"type:\s*(\w+)", text[:400])
    if m:
        typ = m.group(1)
    ver = fm.get("version", "1.0.0")
    body = text[body_start:].lstrip("\n")
    new_fm = f"---\nname: {name}\ndescription: {new_desc}\nfamily-type: {typ or 'tool'}\nfamily-version: {ver}\n---\n\n"
    with open(os.path.join(dst_dir, "SKILL.md"), "w", encoding="utf-8") as f:
        f.write(new_fm + body)
    # 拷贝资源目录
    for sub in ("references", "scripts", "templates", "assets"):
        s = os.path.join(src_dir, sub)
        if os.path.isdir(s):
            d = os.path.join(dst_dir, sub)
            if os.path.exists(d):
                shutil.rmtree(d)
            shutil.copytree(s, d)
    return len(new_desc)

def main():
    if os.path.exists(DST):
        shutil.rmtree(DST)
    os.makedirs(DST, exist_ok=True)
    converted, skipped_dep, skipped_bad = 0, 0, 0
    over = []
    for entry in sorted(os.listdir(SRC)):
        src_dir = os.path.join(SRC, entry)
        if not os.path.isdir(src_dir) or not NAME_RE.match(entry):
            continue
        # 跳过 deprecated(描述含 ⚠️ deprecated / 已合并标记)
        p = os.path.join(src_dir, "SKILL.md")
        if os.path.exists(p):
            with open(p, encoding="utf-8") as f:
                head = f.read(800)
            if "deprecated" in head.lower():
                skipped_dep += 1
                continue
        dst_dir = os.path.join(DST, entry)
        r = convert_skill(src_dir, dst_dir, entry)
        if r is None:
            skipped_bad += 1
            if os.path.isdir(dst_dir):
                shutil.rmtree(dst_dir)
            continue
        converted += 1
        if r > DESC_LIMIT:
            over.append((entry, r))
    print(f"✅ 转换完成: {converted} 个 skill → {DST}")
    print(f"跳过 deprecated: {skipped_dep}, 跳过格式异常: {skipped_bad}")
    if over:
        print(f"⚠️ 仍超 500 字符: {over}")
    else:
        print("✅ 所有 description ≤ 500 字符")

if __name__ == "__main__":
    main()
