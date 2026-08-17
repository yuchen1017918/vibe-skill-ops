#!/usr/bin/env python3
"""全家桶健康检查 — 合并/废弃/发布前必跑。

检查项:
1. frontmatter 完整性(name/description/闭合)
2. 活跃 skill 的 related_skills 零引用 deprecated
3. 活跃 skill 触发词冲突(同一触发词被 2+ skill 使用)
4. 触发词集合 Jaccard 重叠 ≥25% 的 skill 对
5. related_skills 引用目标存在性(区分 family 内 / external 快照 / 悬空)
6. 计数口径(L3 四类分布 + hub + deprecated)

用法:
  python3 verify-family-health.py [family_dir] [external_dir]

默认 family_dir=~/.hermes/skills/vibe-coding-family,
external_dir=仓库 external/(可选, 用于区分 external 快照引用)。
"""
import os
import re
import sys
import collections

FAMILY = sys.argv[1] if len(sys.argv) > 1 else os.path.expanduser("~/.hermes/skills/vibe-coding-family")
EXTERNAL = sys.argv[2] if len(sys.argv) > 2 else ""

errors, warnings = [], []

# ---------- 读取 ----------
skills = {}
for d in sorted(os.listdir(FAMILY)):
    p = os.path.join(FAMILY, d, "SKILL.md")
    if not os.path.isdir(os.path.join(FAMILY, d)) or not os.path.exists(p):
        continue
    text = open(p, encoding="utf-8").read()
    fm_m = re.search(r"^---\n(.*?)\n---\n", text, re.S)
    fm = fm_m.group(1) if fm_m else ""
    name = re.search(r"^name:\s*(\S+)", fm, re.M)
    desc_m = re.search(r"^description:\s*(.*?)(?=\n[a-z0-9_-]+:|\n---)", text, re.S | re.M)
    desc = re.sub(r"\s+", " ", desc_m.group(1).strip()) if desc_m else ""
    typ = re.search(r"type:\s*(\w+)", text[:1500])
    trig = re.search(r"触发词[:：]([^\n。]+)", desc)
    rel_m = re.search(r"related_skills:\s*\[([^\]]*)\]", text)
    rels = [x.strip().strip('"\'') for x in re.split(r"[,\s]+", rel_m.group(1)) if x.strip()] if rel_m else []
    skills[d] = {
        "fm_ok": bool(name) and bool(desc_m),
        "type": typ.group(1) if typ else ("hub" if "hub" in d else "?"),
        "trigs": [x.strip() for x in trig.group(1).split("、")] if trig else [],
        "rels": rels,
        "dep": "deprecated" in text[:800].lower(),
    }

# ---------- 1. frontmatter ----------
for d, v in skills.items():
    if not v["fm_ok"]:
        errors.append(f"{d}: frontmatter 缺 name/description")

# ---------- 2. 活跃引用 deprecated ----------
dep_names = {d for d, v in skills.items() if v["dep"]}
print(f"deprecated 名单: {sorted(dep_names)}")
for d, v in skills.items():
    if v["dep"]:
        continue
    hits = [r for r in v["rels"] if r in dep_names]
    if hits:
        errors.append(f"{d}: related_skills 引用 deprecated {hits}")

# ---------- 3. 触发词冲突 ----------
active = {d: v for d, v in skills.items() if not v["dep"]}
trig_owner = collections.defaultdict(list)
for d, v in active.items():
    for t in v["trigs"]:
        trig_owner[t].append(d)
for t, owners in trig_owner.items():
    if len(owners) >= 2:
        warnings.append(f"触发词 '{t}' 冲突: {owners}")

# ---------- 4. Jaccard 重叠 ----------
keys = list(active.keys())
for i in range(len(keys)):
    for j in range(i + 1, len(keys)):
        a, b = set(active[keys[i]]["trigs"]), set(active[keys[j]]["trigs"])
        if not a or not b:
            continue
        inter = a & b
        if inter and len(inter) / len(a | b) >= 0.25:
            warnings.append(f"触发词重叠 {keys[i]} ↔ {keys[j]}: {sorted(inter)}")

# ---------- 5. 引用存在性 ----------
ext_set = set(os.listdir(EXTERNAL)) if EXTERNAL and os.path.isdir(EXTERNAL) else set()
family_set = set(skills.keys())
for d, v in skills.items():
    for r in v["rels"]:
        if r not in family_set:
            if r in ext_set:
                warnings.append(f"{d}: 引用 external 快照 '{r}'(检查仓库 external/ 是否同步)")
            else:
                warnings.append(f"{d}: 引用悬空 '{r}'(既不在 family 也不在 external)")

# ---------- 6. 计数口径 ----------
types = collections.Counter(v["type"] for v in active.values())
n_active, n_dep = len(active), len(dep_names)
print(f"计数: {n_active} 活跃({dict(types)})+ {n_dep} deprecated = {n_active + n_dep} 总数")
print(f"触发词总数: {sum(len(v['trigs']) for v in active.values())}")

# ---------- 输出 ----------
print(f"\n{'='*50}\n错误 {len(errors)} / 警告 {len(warnings)}")
for e in errors:
    print("  ❌", e)
for w in warnings:
    print("  ⚠️ ", w)
sys.exit(1 if errors else 0)
