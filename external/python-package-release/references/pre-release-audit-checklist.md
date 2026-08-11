# Pre-Release Audit Patterns (SmartCrawl Session)

Concrete patterns from a full-codebase pre-release audit session. Use as checklist + pattern reference.

## Version Standardization Workflow

1. Grep all files for version patterns (vX.Y, X.Y.Z in strings, badges, docstrings, config):
   ```bash
   grep -rn "v*\.*\\|\"*\.*\.*\\"" --include="*.py" --include="*.md" --include="*.toml" --include="*.txt" src/ tests/ docs/
   ```
2. Categorize: project version vs dependency versions (pytest>=7.4.0, twine>=4.0.0 are NOT project version)
3. Batch patch: `__version__` in `__init__.py`, `pyproject.toml [project] version`, README badges, docstrings, `.env` header comments, CLI print statements, log messages, smoke test headers
4. `replace_all=True` when same string appears multiple times in one file (e.g., docstring + print banner in run.py)
5. Verify: re-run grep, expect zero hits

## Config Type Safety (`_safe_int/_safe_float/_safe_bool`)

**Problem**: `int(os.getenv("KEY", default))` crashes when env var is set to empty string or non-numeric value.

**Fix**: Define local helper functions inside `_load_from_env()`:

```python
def _safe_int(key: str, default: int) -> int:
    val = os.getenv(key)
    if val is None:
        return default
    try:
        return int(val)
    except (ValueError, TypeError):
        return default

def _safe_float(key: str, default: float) -> float:
    val = os.getenv(key)
    if val is None:
        return default
    try:
        return float(val)
    except (ValueError, TypeError):
        return default

def _safe_bool(key: str, default: bool) -> bool:
    val = os.getenv(key)
    if val is None:
        return default
    return val.lower() in ("true", "1", "yes", "on")
```

Replace ALL raw `int(os.getenv(...))`, `float(os.getenv(...))`, and `.lower()=="true"` calls with these safe wrappers.

## Config Manager Thread Safety

```python
import threading

class ConfigManager:
    def __init__(self, ...):
        self._load_lock = threading.Lock()
    
    def load(self) -> SpiderConfig:
        with self._load_lock:
            # all env loading + hardware probe + validation
        return self.config
```

## pyproject.toml License Fix (PEP 621)

`license = {text = "MIT"}` → `license = "MIT"` (deprecated table format in setuptools>=77)

## sys.path Removal

Remove all `sys.path.insert(0, ...)` hacks from run.py, test files, and spider_core.py.
After removal, verify imports work via relative imports.
If `project_root = Path(__file__).parent` is still needed for file I/O paths (saving markdown results, etc.), keep only the variable definition.
Also remove unused `import sys` in files where sys was only used for `sys.path.insert`.

## Generic Exception Handling Audit

Search for:
```bash
grep -rn "except Exception:" --include="*.py" src/
```

For each match:
- Add `self.logger.error(f"...", exc_info=True)` to log full traceback
- If the exception is swallowed silently (no logging at all), that's a critical bug
- Narrow to specific exception types where possible (e.g., `aiohttp.ClientError` instead of `Exception`)
- For cleanup/resource-close blocks: use `logger.warning()` with `exc_info=True` instead of `pass`

## Retry Decorator Hard Upper Limit

**Problem**: `async_retry(max_retries=N)` accepts any integer — passing 1000000 causes near-infinite retry loops.

**Fix**: Add a module-level constant and clamp at decorator entry:

```python
# Near top of module, after RetryError class definition
MAX_RETRIES_HARD_LIMIT = 100

def async_retry(max_retries: int = 3, ...) -> Callable:
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            actual_max_retries = min(max_retries, MAX_RETRIES_HARD_LIMIT)
            if max_retries > MAX_RETRIES_HARD_LIMIT and logger:
                logger.warning(
                    f"max_retries={max_retries} 超过硬上限 {MAX_RETRIES_HARD_LIMIT}，已截断"
                )
            for attempt in range(actual_max_retries + 1):
                # ... use actual_max_retries throughout
```

Replace ALL `max_retries` references inside the wrapper body with `actual_max_retries` to maintain consistency.

## Pagination Max-Iteration Guard

**Problem**: `PaginationAgent.find_next_page()` has no upper bound — a site with circular or misdetected pagination causes infinite crawling.

**Fix**: Add `max_pages` constructor parameter + `_page_count` counter, checked at entry of every `find_next_page` call:

```python
class PaginationAgent:
    def __init__(self, ollama_client, enable_llm=True, max_pages=50):
        self.max_pages = max_pages
        self._page_count = 0

    async def find_next_page(self, current_url, html_content):
        # Hard limit check at method entry
        if self._page_count >= self.max_pages:
            self.logger.warning(f"已达最大分页限制 {self.max_pages}，停止分页")
            return None, {"method": "limit", "confidence": 1.0, "candidates": []}
        # ... existing logic ...
        # Increment at EVERY return point that yields a next URL:
        self._page_count += 1
        return candidates[0], decision
```

## Degraded Text Extraction Fallback

**Problem**: When `DataExtractor.extract()` catches `Exception` (LLM JSON parse failure), it just sets `result.error` with no recovery. Content is lost.

**Fix**: After catching the exception, try a regex-based fallback that extracts fields from `<meta>` tags and JSON-LD blocks:

```python
def _degraded_text_extraction(self, content, schema):
    """LLM失败时基于正则从meta/JSON-LD提取字段作为降级方案"""
    import re
    result = {}
    if not isinstance(schema, dict) or len(schema) > 10:
        return None  # Only handle simple schemas
    for field, hint in schema.items():
        if not isinstance(field, str):
            continue
        # meta tag extraction
        meta_pattern = rf'<meta[^>]+(?:name|property)=["\']{re.escape(field)}["\'][^>]+content=["\']([^"\']+)["\']'
        meta_match = re.search(meta_pattern, content, re.IGNORECASE)
        if meta_match:
            result[field] = meta_match.group(1).strip()
            continue
        # JSON-LD extraction
        jsonld_pattern = rf'"{re.escape(field)}"\s*:\s*"([^"]*)"'
        jsonld_match = re.search(jsonld_pattern, content, re.IGNORECASE)
        if jsonld_match:
            result[field] = jsonld_match.group(1).strip()
    return result if result else None
```

Call it from the `except` block:
```python
except Exception as e:
    result.success = False
    result.error = str(e)
    self.logger.error(f"数据提取异常: {e}")
    # Degraded fallback
    try:
        degraded = self._degraded_text_extraction(content, schema)
        if degraded:
            result.success = True
            result.data = degraded
            result.error = ""
            self.logger.info("已降级为文本模式提取数据")
    except Exception:
        pass
```

## LLMResponse Null-Safe Field Access

**Problem**: `generate_json()` calls `response.content.strip()` — if content is `None` (empty API response), this throws `AttributeError`.

**Fix**: Add null check alongside success check:
```python
# Before: if not response.success:
# After:
if not response.success or not response.content:
    continue
```
The `not response.content` guards against both `None` and empty string.

## Type Annotation Import Completeness

**Problem**: Code fixes that add new methods with type annotations (e.g., `Optional[Dict[str, Any]]`) but don't update the import block. The method exists and the package imports fine at the top level, but crashes when Python evaluates the class body or `inspect.signature()` touches the annotations.

**Symptom**:
```
NameError: name 'Optional' is not defined
```
at the method signature line when the class body is first loaded or annotations are accessed.

**Root cause (real example)**: `_degraded_text_extraction()` return type uses `Optional[Dict[str, Any]]` but `from typing import Any, Dict` doesn't include `Optional`. The package-level import passes, but the first consumer that actually loads `DataExtractor` (via `spider_core → llm_agent → data_extractor`) hits the NameError.

**Detection**: After any code fix that adds/modifies method signatures, grep the file for typing constructs used in annotations and verify they're all in the import line:

```bash
# Find all typing constructs used in annotations
grep -oP '->\s*\K\w+(?=\[)' path/to/file.py
grep -oP ':\s*\K\w+(?=\[)' path/to/file.py

# Compare against what's imported
grep 'from typing import' path/to/file.py
```

**Common missing imports**: `Optional`, `List`, `Union`, `Callable`, `Tuple`, `TypeVar`

**Automated catch**: `ruff check --select F821` catches undefined names, including those in annotations. However, if `from __future__ import annotations` is present (PEP 604, deferred evaluation), F821 won't fire until annotation evaluation. On Python 3.14+ with PEP 649, annotations are evaluated lazily when first accessed via `inspect.signature()` or `typing.get_type_hints()`.

**Root-cause import chain**: When a crash happens at `from .spider_core import SmartSpider`, trace the full import chain: `__init__.py → spider_core → llm_agent/__init__.py → data_extractor`. Any typing import gap anywhere in this chain will fail only when the full chain is exercised.

## Priority Classification

| Level | Label | Examples |
|-------|-------|----------|
| Category A - 严重阻断运行 | Crash-on-start, import errors, type conversion crashes with bad env vars | `int(os.getenv(...))` without try-except, missing imports, sys.path.insert hacks |
| Category B - 边界异常崩溃 | Edge-case crashes, resource leaks, race conditions | Thread-unsafe singletons, bare `except: pass` with no logging, unclosed sessions |
| Category C - 功能逻辑缺陷 | Works but wrong/incomplete in some cases | Missing max-iteration guards, no URL validation, unbounded caches, no degraded fallbacks |
| Category D - 规范兼容性问题 | PEP violations, deprecation warnings, linter errors | license table format, unused imports, missing `__all__` exports, argparse validation gaps |

## Verification Command

After all fixes:
```bash
python -c "import sys; sys.path.insert(0, 'src'); from <pkg> import __version__; print(f'Version: {__version__}')"
pip install -e . && <cli-name> --version
```
