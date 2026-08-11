# Offline RAG Pipeline — Reference Code Blocks

## Multi-Layer HF Offline Lockdown

```python
def _lockdown_hf_offline():
    """Call at MODULE LEVEL, before any HF/hub/torch/sentence_transformers import."""
    import os

    # Layer 1: HF environment variables
    os.environ["HF_HUB_OFFLINE"] = "1"
    os.environ["TRANSFORMERS_OFFLINE"] = "1"
    os.environ["HF_DATASETS_OFFLINE"] = "1"
    os.environ["HF_HUB_DISABLE_TELEMETRY"] = "1"
    os.environ["CUDA_VISIBLE_DEVICES"] = ""
    os.environ["OMP_NUM_THREADS"] = "6"
    os.environ["TOKENIZERS_PARALLELISM"] = "false"

    # Layer 2: Block urllib3 HTTPConnection
    try:
        import urllib3.connection
        _orig = urllib3.connection.HTTPConnection.connect
        def _blocked(self): raise OSError("[离线锁死] 外网连接已阻断")
        urllib3.connection.HTTPConnection.connect = _blocked
    except ImportError: pass

    # Layer 3: Block requests Session.request
    try:
        import requests
        _orig = requests.Session.request
        def _blocked(self, method, url, **kw):
            raise requests.exceptions.ConnectionError(f"[离线锁死] {method} {url}")
        requests.Session.request = _blocked
    except ImportError: pass

    # Layer 4: Block socket.create_connection
    try:
        import socket
        _orig = socket.create_connection
        def _blocked(addr, **kw): raise OSError(f"[离线锁死] {addr}")
        socket.create_connection = _blocked
    except ImportError: pass


_lockdown_hf_offline()  # Execute immediately
# NOW safe to import: sentence_transformers, torch, datasets, chromadb, etc.
```

## ChromaDB Metadata Discovery (sqlite3)

```python
import sqlite3, json

conn = sqlite3.connect("path/to/chroma.sqlite3")
cur = conn.cursor()

# Get collection name, ID, dimension
rows = cur.execute("SELECT id, name, dimension FROM collections").fetchall()
for col_id, col_name, col_dim in rows:
    print(f"Collection: name={col_name}, id={col_id}, dim={col_dim}")

# Get metadata schema
row = cur.execute("SELECT schema_str FROM collections WHERE name=?", (col_name,)).fetchone()
schema = json.loads(row[0])
# schema["keys"] contains all valid metadata field names
print("Metadata keys:", list(schema.get("keys", {}).keys()))

# Check embedding count
cnt = cur.execute("SELECT COUNT(*) FROM embeddings").fetchone()[0]
print(f"Embeddings: {cnt}")

conn.close()
```

## Sentence-Transformer Local Loading

```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer(
    "BAAI/bge-small-zh-v1.5",           # or local path: "D:\\hf_cache\\...\\snapshots\\..."
    device="cpu",
    local_files_only=True,               # CRITICAL: blocks all network
)

# FP16 for memory savings
model.half()

# Verify dimension
dim = model.get_sentence_embedding_dimension()  # bge-small = 512
```

## Atomic File Write Pattern (pickle + json)

```python
import pickle, json
from pathlib import Path

def save_atomic(data, path: Path, is_json=False):
    tmp = path.with_suffix(".tmp")
    if is_json:
        tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    else:
        with open(tmp, "wb") as f:
            pickle.dump(data, f, protocol=pickle.HIGHEST_PROTOCOL)
    tmp.replace(path)
```

## Batch Encoding with GC

```python
import gc
import torch

def encode_batches(model, texts, batch_size=64):
    embeddings = []
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i+batch_size]
        with torch.no_grad():
            emb = model.encode(batch, normalize_embeddings=True, show_progress_bar=False)
        embeddings.extend(emb.tolist())
        if (i // batch_size) % 10 == 0:
            gc.collect()
    return embeddings
```

## ChromaDB Append with Retry + Fallback (Never Delete)

```python
import chromadb
import time

def get_or_create_collection(db_path, name):
    """Get existing collection or create if missing. NEVER deletes."""
    client = chromadb.PersistentClient(path=str(db_path))
    try:
        collection = client.get_collection(name=name)
        log(f"现有集合 '{name}' 已包含 {collection.count()} 条向量 (保留不删)")
    except Exception:
        log(f"集合 '{name}' 不存在, 创建新集合")
        collection = client.create_collection(name=name)
    return client, collection


def chroma_add_with_retry(collection, ids, embeddings, metadatas, documents,
                          max_retries=3, delay=2.0):
    """ChromaDB写入, 失败自动重试 (指数退避)"""
    for attempt in range(1, max_retries + 1):
        try:
            collection.add(
                ids=ids,
                embeddings=embeddings,
                metadatas=metadatas,
                documents=documents,
            )
            return
        except Exception as e:
            if attempt < max_retries:
                log(f"[Chroma写入重试 {attempt}/{max_retries}] {e}")
                time.sleep(delay * attempt)
            else:
                raise RuntimeError(
                    f"Chroma写入失败 (已重试{max_retries}次): {e}"
                ) from e
```

## Text-Hash Deduplication for Append (Avoid Re-Adding Identical Chunks)

```python
import hashlib
from typing import List, Dict, Tuple, Set

def _text_hash(text: str) -> str:
    """SHA256 truncated to 16 hex chars — 2^64 namespace, negligible collision risk."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def _load_existing_hashes(collection, fetch_batch: int = 5000) -> Set[str]:
    """
    Load all existing document hashes from a Chroma collection.
    Reads metadata['text_hash'] if present (fast path from prior runs),
    else computes hash from documents (first-time path, slower).
    """
    total = collection.count()
    if total == 0:
        return set()

    log(f"Loading {total:,} existing hashes for dedup...")
    hash_set: Set[str] = set()

    for offset in range(0, total, fetch_batch):
        limit = min(fetch_batch, total - offset)
        result = collection.get(
            limit=limit, offset=offset,
            include=["documents", "metadatas"],
        )
        docs = result.get("documents", [])
        metas = result.get("metadatas", [])

        for doc, meta in zip(docs, metas):
            h = (meta or {}).get("text_hash", "")
            if h:
                hash_set.add(h)
            elif doc:
                hash_set.add(_text_hash(doc))

    log(f"Loaded {len(hash_set):,} unique hashes")
    return hash_set


def _dedup_batch(batch_chunks: List[Dict], existing_hashes: Set[str]
                 ) -> Tuple[List[Dict], int]:
    """
    Filter duplicates: compute text hash, skip if already in set.
    New hashes are added to existing_hashes in-place.
    Writes text_hash into each chunk dict for later metadata storage.
    Returns: (unique_chunks, skipped_count)
    """
    unique = []
    skipped = 0
    for c in batch_chunks:
        h = _text_hash(c["text"])
        if h in existing_hashes:
            skipped += 1
            continue
        existing_hashes.add(h)
        c["text_hash"] = h
        unique.append(c)
    return unique, skipped
```

**Usage in ingestion loop:**
```python
existing_hashes = _load_existing_hashes(collection)

for batch in chunk_batches:
    unique, skipped = _dedup_batch(batch, existing_hashes)
    if not unique:
        continue  # entire batch was duplicates

    texts = [c["text"] for c in unique]
    embeddings = encode(texts)
    metadatas = [{
        "text_hash": c["text_hash"],  # ← store for future fast-path
        # ... other fields ...
    } for c in unique]
    collection.add(ids=ids, embeddings=embeddings,
                   metadatas=metadatas, documents=texts)
```

**Why hash before encoding?** Embedding is expensive (CPU/GPU time). If a chunk is a duplicate, we want to skip it *before* running the model, not after.

## Arrow Dataset Chunking (Sliding Window)

**WARNING**: `.arrow` files from `datasets.save_to_disk()` are Arrow IPC **Stream** format — NOT Parquet, NOT Arrow File format. Use `open_stream()` not `open_file()` and NOT `pyarrow.dataset()`.

```python
import pyarrow.ipc as ipc
import pickle, gc
from pathlib import Path

def build_chunks_from_arrow(arrow_dir, chunk_size=400, chunk_overlap=40):
    """Read Arrow IPC Stream dataset, sliding-window chunk, return list[dict]."""
    arrow_file = Path(arrow_dir) / "data-00000-of-00001.arrow"

    # Try Stream format first, fall back to datasets.load_from_disk
    try:
        with ipc.open_stream(ipc.memory_map(str(arrow_file))) as reader:
            table = reader.read_all()
    except Exception as e1:
        try:
            from datasets import load_from_disk
            dataset = load_from_disk(str(arrow_dir))
            table = dataset.data.table
        except ImportError:
            raise RuntimeError(
                f"Cannot read Arrow file. Install: pip install datasets. Error: {e1}"
            ) from e1

    total = table.num_rows
    chunks = []
    chunk_id = 0

    for batch_start in range(0, total, 100):
        batch_end = min(batch_start + 100, total)
        data = table.slice(batch_start, batch_end - batch_start).to_pydict()
        for i in range(len(data["id"])):
            text = data["text"][i]
            if not text or not isinstance(text, str):
                continue

            if len(text) <= chunk_size:
                chunks.append({
                    "id": data["id"][i],
                    "title": data["title"][i],
                    "url": data["url"][i],
                    "text": text,
                    "chunk_id": chunk_id,
                })
                chunk_id += 1
            else:
                start = 0
                while start < len(text):
                    end = min(start + chunk_size, len(text))
                    chunk_text = text[start:end]
                    if chunk_text.strip():
                        chunks.append({
                            "id": data["id"][i],
                            "title": data["title"][i],
                            "url": data["url"][i],
                            "text": chunk_text,
                            "chunk_id": chunk_id,
                        })
                        chunk_id += 1
                    start += (chunk_size - chunk_overlap)

    return chunks, chunk_id
```

## Checkpoint / Resume for Long Ingestion (with pkl Hash Validation)

```python
import json, hashlib, pickle
from pathlib import Path

# ── Save pkl with hash file for later validation ──
def save_chunks_to_pkl(chunks, pkl_path: Path):
    """Save chunks + .pkl.hash file for smart resume."""
    data = pickle.dumps(chunks, protocol=pickle.HIGHEST_PROTOCOL)
    tmp = pkl_path.with_suffix(".tmp")
    tmp.write_bytes(data)

    # Verify
    with open(tmp, "rb") as f:
        verified = pickle.load(f)
    assert len(verified) == len(chunks), "Corrupt pkl"

    tmp.replace(pkl_path)

    # Write hash file for checkpoint matching
    pkl_hash = hashlib.sha256(data).hexdigest()[:16]
    hash_path = pkl_path.with_suffix(".pkl.hash")
    hash_path.write_text(pkl_hash)


def _get_pkl_hash(pkl_path: Path) -> str:
    """Read .pkl.hash file, empty string if missing."""
    hash_path = pkl_path.with_suffix(".pkl.hash")
    return hash_path.read_text().strip() if hash_path.exists() else ""


# ── Checkpoint with pkl hash ──
def save_checkpoint(progress_file: Path, total_processed: int,
                    last_chunk_index: int, pkl_hash: str, **extra):
    cp = {
        "total_processed": total_processed,
        "last_chunk_index": last_chunk_index,
        "pkl_hash": pkl_hash,
    }
    cp.update(extra)
    tmp = progress_file.with_suffix(".tmp")
    tmp.write_text(json.dumps(cp, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp.replace(progress_file)


def load_checkpoint(progress_file: Path, pkl_path: Path) -> dict:
    """Load checkpoint. If pkl_hash mismatch → reset to 0 (chunks changed)."""
    empty = {"total_processed": 0, "last_chunk_index": -1}
    if not progress_file.exists():
        return empty

    try:
        cp = json.loads(progress_file.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, KeyError):
        return empty

    # Validate: checkpoint must match current pkl
    cp_hash = cp.get("pkl_hash", "")
    cur_hash = _get_pkl_hash(pkl_path)
    if cp_hash and cur_hash and cp_hash != cur_hash:
        log(f"⚠ Chunks changed (cp={cp_hash[:8]}... ≠ pkl={cur_hash[:8]}...), reset")
        return empty

    return cp


# ── Smart resume in main flow ──
def should_rebuild(pkl_path: Path, progress_file: Path) -> bool:
    """True = need to rebuild chunks. False = can resume from checkpoint."""
    if not pkl_path.exists():
        return True
    if not progress_file.exists():
        return True

    pkl_hash = _get_pkl_hash(pkl_path)
    try:
        cp = json.loads(progress_file.read_text(encoding="utf-8"))
    except Exception:
        return True

    return cp.get("pkl_hash", "") != pkl_hash
    # If hashes match → chunks unchanged, safe to resume
    # If mismatch → chunks were rebuilt, must start from 0


# Usage in ingest loop:
checkpoint = load_checkpoint(progress_file, pkl_path)
start_idx = checkpoint["last_chunk_index"] + 1

for batch_start in range(start_idx, len(all_chunks), batch_size):
    batch_end = min(batch_start + batch_size, len(all_chunks))
    # ... encode + add ...
    save_checkpoint(progress_file, total_processed, batch_end - 1,
                    pkl_hash=_get_pkl_hash(pkl_path),
                    total_skipped=total_skipped)

# When complete:
progress_file.unlink(missing_ok=True)
```

## Disk Space Dual Check

```python
import shutil
from pathlib import Path

def check_disk_space(target_dir: Path, min_free_gb=10.0) -> bool:
    """Layer 1: shutil space check. Layer 2: write test."""
    # Layer 1
    usage = shutil.disk_usage(str(target_dir))
    free_gb = usage.free / (1024 ** 3)
    if free_gb < min_free_gb:
        log(f"[磁盘不足] {free_gb:.1f}GB < {min_free_gb}GB")
        return False

    # Layer 2: actual write test
    test_file = target_dir / ".disk_write_test.tmp"
    try:
        test_file.write_bytes(b"test")
        test_file.unlink()
        return True
    except Exception as e:
        log(f"[磁盘写入测试失败] {e}")
        return False
```

## Ollama RAG Q&A Loop (with ChromaDB retrieval)

```python
import ollama

def rag_qa_loop(model, collection, ollama_model="qwen3:8b"):
    """Interactive RAG Q&A: retrieve → build prompt → Ollama answer."""
    ollama_client = ollama.Client(host="http://127.0.0.1:11434")

    while True:
        query = input("问题 (exit退出) > ").strip()
        if query.lower() in ("exit", "quit", "q"):
            break
        if not query:
            continue

        # Retrieve top-K
        q_emb = model.encode([query], normalize_embeddings=True)
        results = collection.query(
            query_embeddings=q_emb.tolist(),
            n_results=5,
        )
        docs = results["documents"][0]

        # Build RAG prompt
        context = "\n\n---\n\n".join(
            f"[参考{i+1}]\n{d}" for i, d in enumerate(docs)
        )
        prompt = f"根据参考文档回答。\n{context}\n---\n问题: {query}\n中文回答:"

        resp = ollama_client.chat(
            model=ollama_model,
            messages=[{"role": "user", "content": prompt}],
        )
        answer = resp.message.content  # SDK ≥0.1.46
        print(f"\n{answer}\n")
```

## tqdm Progress + ANSI Colors + Logging Bridge

**tqdm import with fallback (no pip = plain-text):**
```python
try:
    from tqdm import tqdm as _tqdm_base
    HAS_TQDM = True
    class tqdm(_tqdm_base):
        def __init__(self, *args, **kwargs):
            kwargs.setdefault("ncols", min(shutil.get_terminal_size().columns, 120))
            kwargs.setdefault("ascii", False)
            super().__init__(*args, **kwargs)
except ImportError:
    HAS_TQDM = False
    # Minimal tqdm-like class for plain-text progress fallback
    class tqdm:
        def __init__(self, iterable=None, total=None, desc="", unit="", **kw):
            self.iterable = iterable
            self.total = total if total else (len(iterable) if iterable else 0)
            self.desc = desc; self.unit = unit; self.n = 0; self._start = time.time()
        def __iter__(self):
            for item in self.iterable: yield item; self.update(1)
            self.close()
        def update(self, n=1):
            self.n += n
            if self.total > 0:
                pct = self.n * 100 / self.total; e = time.time() - self._start
                r = self.n / e if e > 0 else 0; eta = (self.total - self.n) / r if r > 0 else 0
                bar = "█" * int(30 * self.n / self.total) + "░" * (30 - int(30 * self.n / self.total))
                sys.stdout.write(f"\r{self.desc} |{bar}| {self.n}/{self.total} ({pct:.1f}%) [{r:.1f}{self.unit}/s, ETA:{eta:.0f}s]   ")
                sys.stdout.flush()
        def set_description(self, desc): self.desc = desc
        def set_postfix(self, **kw): pass
        def close(self):
            if self.total > 0: sys.stdout.write("\n"); sys.stdout.flush()
```

**ANSI color detection + wrapper (Windows Console API):**
```python
class Ansi:
    RESET="\033[0m"; BOLD="\033[1m"; DIM="\033[2m"
    RED="\033[91m"; GREEN="\033[92m"; YELLOW="\033[93m"
    BLUE="\033[94m"; MAGENTA="\033[95m"; CYAN="\033[96m"
    @staticmethod
    def supports_color():
        if os.name == "nt":
            try:
                import ctypes; k = ctypes.windll.kernel32
                m = ctypes.c_ulong(); h = k.GetStdHandle(-11)
                k.GetConsoleMode(h, ctypes.byref(m))
                m.value |= 0x0004; k.SetConsoleMode(h, m)
                return True
            except: return False
        return hasattr(sys.stdout, "isatty") and sys.stdout.isatty()

COLOR = Ansi.supports_color()
def c(text, color): return f"{color}{text}{Ansi.RESET}" if COLOR else text
```

**TqdmLogHandler — routes logging through tqdm.write so bars aren't corrupted:**
```python
class TqdmLogHandler(logging.Handler):
    def emit(self, record):
        msg = self.format(record)
        if HAS_TQDM:
            _tqdm_base.write(msg, file=sys.stdout, end="\n")
        else:
            sys.stdout.write(msg + "\n"); sys.stdout.flush()
```

**Usage in ingestion loop:**
```python
pbar = tqdm(total=len(chunks), initial=start_idx,
            desc="  入库进度", unit="块",
            bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}] {postfix}")
for batch in batches:
    # ... process ...
    pbar.update(count)
    pbar.set_postfix(total=f"{total:,}", rate=f"{rate:.1f}/s", skip=f"{skipped:,}")
pbar.close()  # MUST close on error paths too
```

**Python 3.11 caveat**: f-string expressions cannot contain backslashes. Avoid:
```python
# BROKEN on Python 3.11:
print(f"  {c(\"text with quotes\", Ansi.DIM)}")
# FIX: extract to variable
hint = "text with quotes"
print(f"  {c(hint, Ansi.DIM)}")
```
