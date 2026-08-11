# Packaging Pipeline Template — 4-Phase End-to-End Release

Drop-in orchestration prompt for executing a complete Python package release
end-to-end: pre-flight validation, artifact cleanup, build, and post-build verification.
Generalized from the SmartCrawl v1.0.0 packaging session.

## When to Use

- Releasing a new version of an already-packaged project (src-layout, pyproject.toml)
- You have a cross-session snapshot (PAST_RUN_SNAPSHOT) from prior audit/fix work
- You want a single run that validates, builds, verifies, and outputs a deliverable snapshot

## Pipeline Structure

Four sequential phases, one at a time:

### Phase 1: Pre-Flight Validation (read-only)

Four checks:
1. **Version consistency**: grep all version strings in __init__.py, pyproject.toml, README,
   docs/, CLI output strings, test files — confirm all match target version, no old residuals
2. **Bug fix ledger**: spot-check key patterns from the snapshot's bug fix table are present
   (safe type wrappers, thread locks, exception logging, input validation, etc.)
3. **Test import risk**: scan tests/ for legacy `sys.path.insert()` or non-package-prefixed
   imports that would break after packaging
4. **File permissions**: verify project files are readable/writable (no Windows read-only locks)

Output: structured PASS/FAIL report. If any section fails, stop and list remediation steps.

### Phase 2: Artifact Cleanup

```bash
# Check and clean old distributions
rm -f dist/*.whl dist/*.tar.gz
rm -rf build/
rm -rf src/*.egg-info/
```

Also run `find . -name "*.whl" -o -name "*.tar.gz"` to catch any stragglers.

### Phase 3: Build

```bash
cd /path/to/project
pip install -q build setuptools wheel
python -m build
```

Verify: `ls -lh dist/` should show exactly one `.whl` and one `.tar.gz` with correct version.

### Phase 4: Post-Build Verification (4 layers)

Layer 1 — Static version from source:
```bash
python -c "import sys; sys.path.insert(0, 'src'); from <pkg> import __version__; print(__version__)"
```

Layer 2 — Editable install + CLI:
```bash
pip install -e . && <cli-name> --version
```

Layer 3 — Wheel force-reinstall:
```bash
pip install ./dist/<pkg>-<version>-py3-none-any.whl --force-reinstall && <cli-name> --version
```

Layer 4 — Core module imports:
```bash
python -c "
from <pkg> import <sub1>, <sub2>, <sub3>, <sub4>, <sub5>
# Also import key classes from each subpackage
from <pkg>.<sub1>.<module> import <KeyClass>
# Verify CLI validation if applicable
print('All core modules imported successfully')
"
```

### Final Deliverable

Output a snapshot file (`BUILD_SNAPSHOT_v<version>.md`) with:

1. Pre-flight summary (version state, bug fix state, import state, permissions)
2. Cleanup log (what was deleted, or "zero residuals")
3. Dist artifacts table (filename, type, size)
4. Full terminal output of all 4 verification layers
5. Delivery conclusion: PASS/FAIL with distribution commands

```markdown
===== <Project> v<version> 打包交付快照（可跨对话存档）
...
【5. 交付结论】
✅ <Project> v<version> 打包构建+校验全部通过
❌ 打包校验失败，缺陷清单：XXX
===== 打包快照存档结束 =====
```

## Pitfalls

- **WSL paths**: On WSL, project paths use `/mnt/c/` or `/mnt/d/` mounts. Pip install from these
  paths works normally but may be slower than native Linux paths.
- **`python -m build` regenerates caches**: After build, `build/` and `*.egg-info/` reappear.
  Clean them before final delivery snapshot.
- **Editable install shadowing**: If `pip install -e .` is run before `pip install ./dist/*.whl`,
  the wheel install may appear to succeed but `pip show <pkg>` still points to the editable
  location. Always use `--force-reinstall` for the wheel install.
- **Cross-session snapshots**: If the pre-flight audit was done in a prior session, embed the
  snapshot as `PAST_RUN_SNAPSHOT` at the top of the pipeline prompt.
