#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Wikipedia 中文 RAG 全离线一体化「重分片 + 追加入库」脚本模板
⚠ 仅重分片+追加入库，绝不删除/清空历史向量库

Adapt for your project by modifying the Config class below.
Required dependencies: chromadb, sentence-transformers, pyarrow (or datasets), torch, tqdm (optional), ollama

See skill 'offline-rag-pipeline' for full documentation, pitfalls, and reference code blocks.
"""
# === CONFIG: Modify these for your project ===
REBUILD_CHUNK_ONLY = True
RAW_DATA_DIR       = r"D:\wikipedia_zh_raw"
CHUNK_CACHE_FILE   = r"D:\wiki_stage2_blocks.pkl"
VECTOR_DB_DIR      = r"D:\rag_vector_db"
PROGRESS_FILE      = r"D:\vec_progress.json"
LOG_FILE           = r"D:\wiki_rag_rebuild.log"
MODEL_SNAPSHOT_DIR = r"D:\hf_cache\models\hub\models--BAAI--bge-small-zh-v1.5\snapshots\..."
MODEL_NAME         = r"BAAI/bge-small-zh-v1.5"
CHROMA_COLLECTION  = "wikipedia_knowledge"
CHUNK_SIZE = 400; CHUNK_OVERLAP = 40
CHROMA_BATCH_SIZE = 240; OMP_NUM_THREADS = 6
OLLAMA_MODEL = "qwen3:8b"
# ============================================

# Full production script (1100+ lines) maintained at:
#   D:\wiki_rag_rebuild_append.py
#   E:\RAG\wiki_rag_rebuild_append.py
#
# Features:
#   • 4-layer HF offline lockdown (env + urllib3 + requests + socket)
#   • tqdm + ANSI color progress bars with logging bridge
#   • Text-hash deduplication on append (skip identical chunks)
#   • Smart checkpoint resume with pkl hash validation
#   • Arrow IPC Stream format reading (with datasets fallback)
#   • ChromaDB metadata schema auto-discovery via sqlite3
#   • Batch encoding with gc.collect(), FP16, OMP thread binding
#   • ChromaDB write retry (3x exponential backoff)
#   • Atomic file writes (tmp → rename) for pkl and json
#   • Disk space dual check (shutil + write test)
#   • Ollama RAG interactive Q&A loop
#   • Python 3.11 compatible (no f-string backslashes)
#   • Windows native paths (r"" + Path)
#
# Copy the full script from D:\wiki_rag_rebuild_append.py
# or regenerate via: hermes-agent "rebuild the wiki rag script with [your changes]"
