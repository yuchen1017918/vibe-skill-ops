---
name: python-package-release
description: Python packaging lifecycle — initial packaging (PEP 621 src-layout migration) through release (cache cleanup, export integrity, env templates, import validation, build, twine check, offline distribution, delivery checklist).
triggers:
  - User asks to "finalize", "package", "release", "build for distribution", "打包", or "prepare for PyPI" on a Python project
  - User asks to "package this project", "make it pip installable", "standardize into a Python package", or "create pyproject.toml"
  - User asks for "PEP 621 src layout migration" or flatten-to-src-layout restructuring
  - User asks for "pre-release audit", "version audit", "bug scan before release", "版本号统一", "全链路静态Bug扫描", "release hardening"
  - User provides a numbered checklist of bugs to scan for across a packaged codebase
  - User asks to "统一版本号", "扫描Bug", or "修复打包问题" on an already-packaged project
  - Any phrase matching "收尾", "打包验证", "发布准备", "离线分发"
---

# Python Packaging Lifecycle

Complete lifecycle: initial packaging (PEP 621 src-layout migration) through release and distribution. Two major sections — first-time packaging of a flat project (Phase 0), then the release/verification pipeline for already-packaged projects (Phases 1–7).

## Phase 0: Initial Packaging — PEP 621 src-layout migration

Use this phase when the project is still flat (no `src/` layout, no `pyproject.toml`, or uses `sys.path.insert()` hacks). Skip to Phase 1 if the project already has `src/<pkg>/` with `pyproject.toml`.

### 0.1 Copy source to new build directory

NEVER modify the original project. Always copy to a new directory:

```bash
cp -a /path/to/original /path/to/build-target
```

### 0.2 Clean runtime artifacts

Remove from the copy only:
- `__pycache__/` directories, `.pytest_cache/`, `.ruff_cache/`, `.mypy_cache/`
- `data/`, `logs/`, `htmlcov/` (runtime outputs)
- `.coverage`, `.vscode/`, `.idea/`
- `old_version/`, legacy directories
- `.env` (keep as `.env.example` template instead)

### 0.3 Create `src/<package>/` structure

```bash
mkdir -p src/<package>
mv config/ crawler/ llm_agent/ storage/ utils/ main.py src/<package>/
```

Package name must be lowercase, PEP-compliant.

### 0.4 Fix ALL internal imports

Every `from <top_pkg> import ...` in a subpackage must become a relative import.

**Rule by file depth (relative to `src/<package>/`):**

| File depth | Old import | New import |
|-----------|-----------|-----------|
| 0 (e.g. `main.py`) | `from config import X` | `from .config import X` |
| 1 (e.g. `crawler/engine.py`) | `from utils import X` | `from ..utils import X` |
| 1 (e.g. `crawler/engine.py`) | `from .base import X` | Keep as-is (already relative) |

**Pitfall: `search_files` regex alternation** — alternation groups like `from (config|crawler|storage|utils) import` return zero results with ripgrep. Search each prefix individually.

To find all imports to fix:
```bash
grep -rn "^from \\(config\\|crawler\\|llm_agent\\|storage\\|utils\\)" src/<package>/ --include="*.py" | grep -v __pycache__ | grep -v "/__init__.py:"
```

Apply fixes with `patch()` — 31+ fixes is normal for a 15-file project. Also remove `sys.path.insert()` hacks from root-level files.

### 0.5 Identify dependencies from imports

Scan imports across ALL .py files — don't rely on `requirements.txt` alone. Check both direct `import`/`from X import` lines and conditional/dynamic imports inside functions.

Runtime deps → `[project].dependencies`
Test/build/tool deps → `[project.optional-dependencies].dev`
Optional features (e.g. Playwright) → separate optional group

### 0.6 Create pyproject.toml

Use the template at `references/pyproject-template.toml`. Key sections:
- `[build-system]`: setuptools>=68.0 + wheel
- `[project]`: name, version, description, readme, license, requires-python, dependencies, optional-dependencies, scripts
- `[project.scripts]`: CLI entry = `<pkg>.cli:main`
- `[tool.setuptools.packages.find]`: where = ["src"]
- `[tool.setuptools.package-data]`: include `*.json`, `*.yaml`, `*.cfg`
- Tool configs (ruff, black, isort, pytest, mypy) go in toml

### 0.7 Create `src/<package>/__init__.py`

Define `__version__`, re-export public API classes only, hide internal `_init_*`, `_ensure_*`, `_check_*` methods.

### 0.8 Create `src/<package>/cli.py`

Use argparse (stdlib, no extra dep). Provide positional URL args, `--file` for batch input, `--concurrency`, `--output`, `--json` flags, `--interactive` mode, `--version`, `--help`.

### 0.9 Create root files

- `README.md`: install, quickstart, API ref, CLI usage
- `LICENSE`: MIT
- `.gitignore`: venv, dist, cache, logs, data, IDE files
- `.env.example`: template config (copy from original `.env`, strip credentials)

### 0.10 Packaging pitfalls

- **Config file swap**: If original project has main module code in `__init__.py` and re-exports in `config.py` (or vice versa), swap them to standard: `__init__.py` = re-exports, `config.py` = implementation.
- **LLMResponse import**: If `__init__.py` re-exports `LLMResponse` but sub-module's `__init__.py` doesn't export it, you'll get ImportError. Check all intermediate `__init__.py` files.
- **Playwright optional**: Conditionally imported via `importlib.util.find_spec`. Put in `[project.optional-dependencies]`, not core deps.

## Phase 1: Cache & Artifact Cleanup

```bash
# Delete dev caches at project root
rm -rf .pytest_cache .ruff_cache .vscode .coverage .mypy_cache

# Recursively delete __pycache__ directories under src/
find src/ -type d -name '__pycache__' -exec rm -rf {} +

# Delete build artifacts
rm -rf build/ dist/ *.egg-info/ src/*.egg-info/
```

PITFALL: Build tools (pip install -e, python -m build) will regenerate __pycache__ and egg-info. Always re-run this step AFTER builds, before final delivery.

## Phase 2: Module Export Integrity Check

The most common packaging bug: top-level `__init__.py` imports something that a sub-module's `__init__.py` doesn't export.

**Procedure:**
1. Read the top-level `src/<pkg>/__init__.py` — note every name imported from each sub-module
2. For each sub-module, read `src/<pkg>/<sub>/__init__.py` — verify every imported name is actually exported
3. If a name is imported from `.submodule` but missing in that submodule's `__init__.py`, add the import and update `__all__`
4. Verify version number matches expected

**Common gaps to check:**
- Enum classes and type aliases defined alongside core classes (like `AntiCrawlLevel`, `CrawlMode` defined in `base_crawler.py` but not re-exported)
- Response/data wrapper classes (like `LLMResponse` used externally but omitted from agent `__init__.py`)
- Utility helpers that consumers need

Use `search_files` with pattern matching to confirm where each class/name is defined, then patch the sub-module `__init__.py`.

## Phase 3: Environment Template Generation

1. Copy source `.env` to `.env.example` in the package root
2. Strip all real credentials, API keys, specific model names, host addresses
3. Replace with placeholders like `<your-ollama-model>` or `<your-api-key>`
4. Keep all non-sensitive config fields and their default values
5. Verify `.gitignore` contains `.env` (so real `.env` stays out, `.env.example` is tracked)

## Phase 4: Import Validation

**Quick check:**
```bash
python -c "import sys; sys.path.insert(0, 'src'); import <pkg>; print('OK')"
```

PITFALL: This quick check only validates top-level `__init__.py` imports. If a class body in a submodule uses a typing construct (`Optional`, `List`, `Union`, etc.) that isn't imported, the crash happens later when the full import chain is exercised. Always run a DEEP import check that reaches into every submodule's classes:

```bash
python -c "
import sys; sys.path.insert(0, 'src')
from <pkg> import <main_class>, <other_exports>
# Also import deeply to trigger class-body evaluation:
from <pkg>.<sub> import <ClassWithAnnotations>
from <pkg>.<sub2> import <AnotherClass>
print('Deep import validation passed')
"
```

If a crash happens at `from .spider_core import SmartSpider`, trace the full chain: `__init__.py → spider_core → submodule/__init__.py → specific_file`. See `references/pre-release-audit-checklist.md` "Type Annotation Import Completeness" for the detection pattern.

**Full export validation** — import every name from `__all__`:
```python
import sys; sys.path.insert(0, 'src')
import <pkg>
from <pkg> import (
    # copy every name from __all__
)
print(f'All {len(<pkg>.__all__)} exports validated')
```

PITFALL: If this fails with `ImportError: cannot import name 'X' from '<pkg>.<sub>'`, return to Phase 2 — the sub-module's `__init__.py` is missing the export.

## Phase 5: Build & Install Verification

### 5.0 Quick-Start: 4-Phase Pipeline Template

For end-to-end release runs (validate → clean → build → verify → snapshot), use the
full pipeline template at `references/packaging-pipeline-template.md`. This covers:
pre-flight validation, artifact cleanup, build execution, and a structured 4-layer
post-build verification chain — all in one run with a deliverable snapshot output.

### 5.1 Editable install
```bash
pip install -e .
```

### 5.2 CLI verification (if entry_points defined)
```bash
<cli-name> --version
<cli-name> --help
```

### 5.3 Build tools + distribution build
```bash
pip install build twine wheel
python -m build
```

PITFALL: `nh3` (pulled by `twine`) is a large native wheel that downloads slowly on some connections. Use `pip install --default-timeout=120` or background install with longer timeout.

### 5.4 Distribution integrity check
```bash
twine check dist/*
```
Both `.whl` and `.tar.gz` must PASS.

### 5.5 Whl install + import verification
```bash
pip install --force-reinstall --no-deps dist/<pkg>-*.whl
python -c "from <pkg> import <main_class>, __version__; print(f'OK: {__version__}')"
```

PITFALL: Skip `--no-deps` if dependencies aren't pre-installed. Use `--force-reinstall` to ensure the wheel is actually loaded (not the stale editable install).

## Phase 6: Offline Distribution Commands

Output these commands (don't execute unless user asks):
```bash
# Internet-connected machine: export deps
pip download <pkg> -d ./offline-packages

# Air-gapped machine: install from offline cache
pip install --no-index --find-links ./offline-packages <pkg>

# Or direct wheel install
pip install ./<pkg>-X.Y.Z-py3-none-any.whl
```

## Phase 7: Delivery Checklist

Final output must include:
1. Clean directory tree (only core distribution files)
2. Per-phase verification results (pass/fail with details)
3. Three complete operation command sets: local dev, offline/air-gapped, PyPI upload
4. Clear separation: completed deliverables vs. optional publishing steps
5. Any deprecation warnings noted (e.g., setuptools license TOML table → string migration)

## Phase 8: Pre-Release Audit — Version Standardization & Bug Hardening

After packaging is complete but before final delivery, run a systematic audit to catch version inconsistencies, config bugs, exception handling gaps, and packaging compliance issues. See `references/pre-release-audit-checklist.md` for the full checklist and code patterns. For audits too large to complete in one session (25+ bugs, 10+ files), use the cross-session snapshot pattern in `references/cross-session-snapshot-pattern.md` to persist progress with category-based sub-agent sharding.

### 8.1 Version Standardization

Grep the entire codebase for old version strings, categorize (project version vs dependency versions), then batch-replace. Use `replace_all=True` when the same string appears in multiple places within one file. Verify with a clean grep run afterward.

### 8.2 Config Type Safety

Replace all `int(os.getenv(...))` / `float(os.getenv(...))` / `.lower()=="true"` with safe wrappers that catch `ValueError` on empty/malformed env vars. The `_safe_int/_safe_float/_safe_bool` pattern (defined locally inside `_load_from_env()`) prevents crashes when environment variables are set to empty strings or non-numeric values.

### 8.3 Thread Safety for Config Managers

Wrap `ConfigManager.load()` in `threading.Lock` to prevent race conditions when multiple consumers read config concurrently.

### 8.4 Exception Handling Audit

Search for all `except Exception:` blocks. Add `logger.error(f"...", exc_info=True)` to preserve full tracebacks. Replace bare `except: pass` with specific exception types and at minimum a debug log.

### 8.5 Packaging Compliance

- `license = {text = "MIT"}` → `license = "MIT"` (PEP 621, setuptools>=77 deprecation)
- Remove all `sys.path.insert(0, ...)` hacks from source and test files
- Verify `pyproject.toml [project.scripts]` entry points match actual CLI functions
- Confirm `requires-python >=3.10` matches codebase (no 3.14-only features)

### 8.6 Type Annotation Import Completeness

When a code fix adds a new method with type annotations containing constructs not previously used in the file (e.g., `Optional[X]`, `List[X]`, `Union[X, Y]`), verify the import line(s) cover every construct. The package-level import will pass, but the first consumer that loads the class body hits `NameError`.

Detection: after all fixes, run `ruff check --select F821` on modified files. See `references/pre-release-audit-checklist.md` "Type Annotation Import Completeness" for the full pattern and import-chain tracing technique.

## Pitfalls

- **Build regenerates caches**: After `python -m build`, `__pycache__/` directories and `build/`, `*.egg-info/` reappear. Always re-clean before final directory tree output.
- **pip timeout on slow deps**: `twine` pulls `nh3` (~800KB native wheel) which can time out on 15s default. Use `--default-timeout=120` or background mode.
- **Editable install shadowing**: After `pip install -e .`, running `pip install ./dist/*.whl` may not actually switch to the wheel. Use `--force-reinstall` and verify with `pip show <pkg>`.
- **License deprecation**: `pyproject.toml` with `license = {text = "MIT"}` (TOML table) triggers SetuptoolsDeprecationWarning in setuptools>=77. Fix by changing to `license = "MIT"` (string). Current builds still succeed but should be fixed for future compatibility.

## Reference

- `references/smartcrawl-session.md` — Packaging session example with export fixes, verification output, and deprecation notes.
- `references/pre-release-audit-checklist.md` — Full pre-release audit checklist: version standardization, config safety, thread safety, exception handling patterns.
