---
name: offline-rag-pipeline
description: Build offline RAG pipelines — local embedding models (HF snapshots), vector DB append strategies, chunking from raw datasets, ChromaDB metadata discovery, hardware-tuned batch encoding. Full offline with zero external network.
---

# Offline RAG Pipeline — Local Embeddings + Vector DB

## When to Load

Load when the user asks to build, modify, or debug an offline RAG pipeline using:
- Local sentence-transformers / HF embedding models (no network)
- ChromaDB (PersistentClient) for vector storage — especially appending to existing collections
- PyArrow / HuggingFace Datasets for reading raw corpora
- Wikipedia dumps, document corpora, or any text datasets that need chunking and indexing
- Hardware-constrained environments (CPU-only, limited RAM)

Also load when the task involves: re-chunking from raw data, appending vectors to an existing collection without deleting old ones, or setting up full-offline HF lockdown.

## Trigger Conditions

Any of these phrases should trigger loading this skill:
- "offline RAG", "离线RAG", "本地向量库", "ChromaDB vector store"
- "bge embedding", "本地嵌入模型", "sentence-transformers local"
- "re-chunk Wikipedia", "重分片", "追加入库", "append vectors"
- "HF offline", "huggingface offline", "全离线", "no network"
- "local HF snapshot", "本地HF快照"

## Core Patterns

### 1. Multi-Layer HF Offline Lockdown (MUST be first, before any HF/hub import)

```
Layer 1: Environment variables — HF_HUB_OFFLINE=1, TRANSFORMERS_OFFLINE=1, HF_DATASETS_OFFLINE=1
Layer 2: Monkey-patch urllib3.connection.HTTPConnection.connect → raise OSError
Layer 3: Monkey-patch requests.Session.request → raise ConnectionError
Layer 4: Monkey-patch socket.create_connection → raise OSError
```

Execute this in a `_lockdown_hf_offline()` function called at module level, BEFORE any `import sentence_transformers` or `import datasets`. This prevents accidental network calls during module import, not just at runtime.

See `references/offline-patterns.md` for the full code block.

### 2. ChromaDB Collection Metadata Discovery

When appending to an EXISTING vector collection, you MUST match its metadata schema. Use sqlite3 to inspect the ChromaDB database directly:

```python
import sqlite3
conn = sqlite3.connect(path_to_chroma.sqlite3)
# Get collection name, dimension
rows = conn.execute('SELECT id, name, dimension FROM collections').fetchall()
# Get metadata schema
schema = json.loads(row['schema_str'])  # reveals expected keys
conn.close()
```

Failure to match the existing metadata schema causes ChromaDB `add()` to fail silently or with obscure errors.

### 3. Append-Only Vector Strategy

When adding new vectors to an existing collection:
- **NEVER** call `collection.delete()` or `client.delete_collection()`
- Use `client.get_collection(name=...)` to get the existing collection
- Use `collection.add(ids=..., embeddings=..., metadatas=..., documents=...)` with NEW unique IDs
- Existing vectors are untouched — ChromaDB's `add()` does not overwrite or delete
- After adding, `collection.count()` reflects old + new total

### 3.5 Text-Hash Deduplication on Append (Avoid Re-Adding Identical Chunks)

When re-chunking the SAME raw data with the SAME parameters, new chunks will be textually identical to existing ones. Blindly appending doubles the vector count with 100% redundancy. Use text hashing to skip duplicates:

**Algorithm:**
1. Before ingestion, load ALL existing document texts from Chroma via `collection.get()` in batches of 5000
2. Compute SHA256 (first 16 hex chars) for each existing document — build a `set` of hashes
3. For each new chunk batch: compute hash → if in set, skip (count as duplicate) → if not, add to set + encode + write to Chroma
4. Store `text_hash` in Chroma metadata for future runs (avoids re-reading documents)

**Key design decisions:**
- SHA256 truncated to 16 hex chars = 2^64 space = negligible collision probability for 100K-scale corpora
- Load hashes ONCE at startup — the hash set lives in ~10MB RAM for 100K entries
- Check hash BEFORE encoding — saves the expensive embedding computation for duplicates
- Write hash to metadata on first add so next run reads metadata (fast) instead of documents (slow)

See `references/offline-patterns.md` for the complete `_load_existing_hashes()`, `_text_hash()`, and `_dedup_batch()` implementations.

### 4. Hardware-Aware Batch Encoding

For CPU-only inference with limited RAM:
- Set `OMP_NUM_THREADS` = physical core count (not hyperthreads)
- Use FP16 half-precision: `model.half()` to halve memory per embedding
- Encode in sub-batches (64 per encode call) with periodic `gc.collect()`
- Use `torch.no_grad()` context for encoding
- Batch size for ChromaDB writes is separate from encode batch size — typically 240 for 16GB RAM

### 5. Chunking from Arrow/HF Datasets

When source data is an Arrow dataset saved via `datasets.save_to_disk()`:
- Files are Arrow IPC **Stream** format (magic bytes `FFFF FFFF`), NOT Parquet and NOT Arrow File format
- **DO NOT** use `pyarrow.dataset.dataset(path)` — it will misidentify as Parquet and crash with "Parquet magic bytes not found"
- **DO NOT** use `pyarrow.ipc.open_file()` — it needs `ARROW1` magic (File format)
- Use `pyarrow.ipc.open_stream()` (Stream format) with a memory map for efficiency
- Fallback: `datasets.load_from_disk(path)` works reliably if the library is installed
- Iterate with `table.slice(start, end).to_pydict()` to avoid loading all text into memory
- Sliding window: for each article text, chunk with `(chunk_size, chunk_overlap)`
- Short texts (< chunk_size): single chunk
- Long texts: `for start in range(0, len(text), chunk_size - overlap)`
- Save chunks as `pickle.dump(chunks, file)` with atomic write (write to .tmp, then rename)

### 6. Checkpoint/Resume for Long-Running Vector Ingestion

For ingesting 100K+ vectors (hours-long process):
- Use a JSON checkpoint file: `{"total_processed": N, "last_chunk_index": M, "pkl_hash": "..."}`
- Save checkpoint after every successful Chroma batch write
- On script restart, read checkpoint and skip already-processed chunks
- Use atomic write for checkpoint: write to .tmp, then `Path.replace()`
- Delete checkpoint file when ingestion completes

**Smart Resume with pkl Hash Validation (CRITICAL for REBUILD workflow):**
When the script supports both `REBUILD_CHUNK_ONLY=True` (re-chunk + ingest) and restart-after-interrupt, the checkpoint alone is insufficient — re-chunking produces a brand-new pkl whose chunk indices don't match the old checkpoint. Solution:

1. When saving pkl, also write a `.pkl.hash` file: `hashlib.sha256(pkl_bytes).hexdigest()[:16]`
2. Save this hash in every checkpoint entry as `pkl_hash`
3. On restart with `REBUILD_CHUNK_ONLY=True`, check: does pkl exist? does `.pkl.hash` exist? does the checkpoint's `pkl_hash` match the current `.pkl.hash`?
   - **Match** → skip chunk rebuild entirely, resume ingestion from checkpoint
   - **Mismatch** → delete old pkl + old checkpoint → rebuild chunks → start ingestion from 0
4. This means a crash during ingestion is fully recoverable: just re-run the script and it auto-resumes. Only re-chunking (changing CHUNK_SIZE, adding new raw data) requires manual cleanup of the pkl files.

See `references/offline-patterns.md` for the complete `_get_pkl_hash()`, smart resume logic, and atomic hash file write.

### 7. Progress Visualization (tqdm + ANSI + Logging Bridge)

For long-running pipelines, bare log lines are insufficient. Layer in:

**tqdm progress bars** for chunking and embedding phases:
```python
from tqdm import tqdm
pbar = tqdm(total=total_items, desc="  入库进度", unit="块",
            bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}]")
# In loop:
pbar.update(batch_count)
pbar.set_postfix(total=f"{total_vectors:,}", rate=f"{rate:.1f}/s")
pbar.close()  # MUST close on error paths too
```

**tqdm fallback** (pip not installed): provide a minimal drop-in class that mimics `tqdm` API with plain-text progress. Check `HAS_TQDM` flag at module level.

**ANSI color codes** for stage banners, status indicators, and retrieval results. Always detect terminal support via Windows Console API (`ENABLE_VIRTUAL_TERMINAL_PROCESSING`) or `isatty`. Provide a `c(text, color)` wrapper that returns plain text if colors unsupported. Use `Ansi.BOLD`, `Ansi.GREEN`, `Ansi.YELLOW`, `Ansi.CYAN`, `Ansi.DIM`, etc.

**TqdmLogHandler**: A custom `logging.Handler` that routes all log output through `tqdm.write()` so log lines don't overwrite or corrupt the progress bar:
```python
class TqdmLogHandler(logging.Handler):
    def emit(self, record):
        msg = self.format(record)
        tqdm.write(msg, file=sys.stdout, end="\n")
```

**Stage banners**: Use `═` / `━` borders with colored titles to visually separate the 4 stages (chunking, model load, ingestion, retrieval test). Print a summary dashboard at the end showing: total vectors, old vs new split, elapsed time, average rate.

**Python 3.11 note**: f-string expressions cannot contain backslashes. Avoid `f"{c(\"...\", Ansi.DIM)}"` with escaped quotes inside the `{}`. Extract strings to variables first: `hint = "..."; print(f"{c(hint, Ansi.DIM)}")`.

See `references/offline-patterns.md` for complete copy-paste code blocks (HF lockdown, ChromaDB sqlite3 inspection, atomic file writes, batch encoding, Chroma append with retry, Arrow chunking, checkpoint/resume, disk check, Ollama RAG Q&A loop).

See `templates/wiki_rag_rebuild_append.py` for a complete, production-tested, drop-in single-file script template for Wikipedia RAG with rebuild+append workflow.

## Pitfalls

- **Wrong metadata keys**: ChromaDB schema is strict. Inspect existing collection via sqlite3 BEFORE writing code. In this project, the keys were `article_title`, `source_url`, `original_index` — not the intuitive `title`, `url`, `chunk_index`.
- **Wrong collection name**: The ChromaDB folder UUID is NOT the collection name. Use sqlite3 to query the `name` column. In this project, it was `wikipedia_knowledge`.
- **Mismatched embedding dimensions**: bge-small-zh-v1.5 = 512-dim. bge-base-zh-v1.5 = 768-dim. Verify the existing collection's `dimension` column matches the model.
- **HF lock too late**: If `import sentence_transformers` happens before the lockdown function, the library may already cache DNS lookups. Execute lockdown at module level, before any ML imports.
- **Network timeouts on Windows**: Configuring HF_HUB_OFFLINE alone is insufficient — Windows sockets can still timeout on background DNS/connect. The full 4-layer monkey-patch is the only reliable solution.
- **OOM on encode**: Encoding 100K+ texts at once will OOM. Always batch encode with gc.collect() every ~10 batches.
- **Arrow IPC format mismatch (CRITICAL)**: `.arrow` files from `datasets.save_to_disk()` are Arrow IPC **Stream** format (magic bytes `FFFF FFFF`), NOT File format (`ARROW1` magic) and NOT Parquet. `pyarrow.dataset.dataset()` will crash with "Parquet magic bytes not found". `pyarrow.ipc.open_file()` will crash with "Not an Arrow file". Must use `pyarrow.ipc.open_stream()` or fall back to `datasets.load_from_disk()`. The safe pattern: try `open_stream`, catch → try `load_from_disk`, catch → raise clear error.

## Workflow Checklist

1. Inspect existing ChromaDB via sqlite3: collection name, dimension, metadata keys, embedding count
2. Inspect embedding model snapshot: confirm dimension matches, confirm all files present (model.safetensors, config.json, tokenizer.json, etc.)
3. Set hardware params: OMP_NUM_THREADS, batch sizes, FP16
4. Lock down HF offline — 4 layers, at module level
5. Chunk from raw data (or load existing pkl)
6. Load model with `local_files_only=True` and `device="cpu"`
7. Append vectors in batches with checkpoint + retry + gc
8. Run retrieval test to verify old + new vectors
9. Clean up checkpoint file
