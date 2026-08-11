# Python Async / HTTP Client Pitfalls

## aiohttp 3.13+ — `get_encoding()` before body read

**Symptom:** `"Cannot compute fallback encoding of a not yet read body"`

**Root cause:** In aiohttp 3.13+, `ClientResponse.get_encoding()` tries body-based
charset detection (chardet) when no Content-Type charset header exists. Calling
it before `await response.text()` means the body hasn't been read yet — crash.

**Fix — always read body first, then get encoding:**

```python
# WRONG (crashes on aiohttp 3.13+):
result.encoding = response.get_encoding() or 'utf-8'
html = await response.text()

# RIGHT:
html = await response.text()
result.html = html
# Use response.charset first (header-only, safe), fall back to get_encoding()
result.encoding = response.charset or response.get_encoding() or 'utf-8'
```

**Affected versions:** aiohttp >= 3.13.0 (confirmed 3.13.5)

## Python 3.10+ — `asyncio.get_event_loop()` deprecated

**Symptom:** `DeprecationWarning` or unpredictable behavior in `__del__` methods.

**Fix:**

```python
# WRONG (deprecated since 3.10, may break in 3.12+):
loop = asyncio.get_event_loop()
if loop.is_running():
    loop.create_task(self.close())

# RIGHT:
try:
    loop = asyncio.get_running_loop()
    loop.create_task(self.close())
except RuntimeError:
    # No running loop — can't async-close from __del__
    pass
```

`get_running_loop()` raises `RuntimeError` when no loop is running, which is
the correct behavior for `__del__` cleanup (just skip if no loop).

## Python 3.14 — `lxml` no wheel

Python 3.14 often lacks wheels for `lxml`. `beautifulsoup4` falls back to
built-in `html.parser` automatically — `lxml` is optional. Don't block
installation on it.

## `content_length` — use byte length, not character length

```python
# WRONG (counts characters, breaks on CJK):
result.content_length = len(html)

# RIGHT (counts bytes, matches HTTP Content-Length semantics):
result.content_length = len(html.encode())
```
