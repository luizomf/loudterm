# Installation and dependency repairs (#3, #4, #5)

## Scope and provenance

The existing fixes in `658d7f6` (Python 3.14 instructions/output location) and
`2ab0b5b` (Cython 3.2.4 isolated-build constraint) are retained, not duplicated.
The reporter in issue #4 subsequently confirmed installation and audio output,
but reported a first-submission history failure. The prompt now creates its
history directory before asking for input, even when audio saving is disabled.
Existing recordings and history are not removed.

PR #3 retains the contributor's optional `mojimoji` extra while keeping Python
3.14 as the minimum. README and example commands use `--extra japanese`,
including on `uv run`; this is not a dependency group or a promise that all
Japanese dependencies are optional. Regeneration with uv 0.12.10 also simplifies
CUDA extra markers; exports still restrict CUDA packages to Linux. No package
versions change in the Japanese-extra repair.

## CVE-2026-9856

Verified sources:

- [GitHub reviewed advisory GHSA-xrqw-3rrv-vx5w](https://github.com/advisories/GHSA-xrqw-3rrv-vx5w):
  affected Transformers versions `<5.10.0`; first patched version `5.10.0`.
- [Upstream fix eaaaf849](https://github.com/huggingface/transformers/commit/eaaaf8494dd5386634ae37d1d122212fdc315be5):
  both tokenizer and processor save paths reject template names whose resolved
  parent escapes the chat-template directory.
- [PyPI 5.10.1 metadata](https://pypi.org/pypi/transformers/5.10.1/json):
  5.10.1 is not yanked. uv reports 5.10.0 as yanked because it was published
  from an outdated main branch, so this project uses a **5.10.1** minimum and lock.

Transformers was transitive through Kokoro, not an existing direct 5.8.0 pin in
`pyproject.toml`. The direct requirement now enforces the security floor for
both uv and pip. Only Transformers changes version in this security update.

Searches of loudterm and installed Kokoro/Misaki found no `save_pretrained`
call. Kokoro uses `AlbertConfig` and `AlbertModel` through `CustomAlbert`;
ordinary text-to-WAV use is not shown to reach the vulnerable save path.
The dependency was nevertheless affected. The advisory's arbitrary-file-write
claim should not be read as evidence that loudterm itself offers a remotely
reachable exploit, or that arbitrary extensionless files can be overwritten:
the affected template path appends `.jinja`.

## Observed validation

On macOS arm64, uv 0.12.10, Python 3.14.4:

- Real prompt input through Prompt Toolkit pipe input reproduced missing history
  on first submission; the regression passes after the directory fix, including
  a second submission preserving the first and with audio saving disabled.
- An offline tokenizer save regression failed on 5.8.0 (no rejection) and passes
  on 5.10.1 (rejection and no escaped canary file).
- `uv run --locked --extra japanese pytest -q`: 2 passed.
- Focused Ruff (`--no-fix`) and Pyright checks for the new tests and prompt pass.
- Default installation/import works without `mojimoji`; the Japanese extra
  installs it, and `misaki.ja` imports plus native full-width conversion pass.
- Default/Japanese locked exports differ by the optional `mojimoji` requirement.
- Fresh-environment locked sync with the Japanese extra installed 114 packages,
  including a real `curated-tokenizers` source build. `pip check` and imports of
  Kokoro, Misaki Japanese, mojimoji and curated-tokenizers passed.
- Both a small ALBERT forward pass and Kokoro's actual `CustomAlbert` wrapper
  forward pass succeed without model downloads.

A first fresh-environment attempt selected Python 3.14.7 and exceeded a
180-second bound during source building; it is not counted as successful.
The subsequent explicit Python 3.14.4 fresh environment succeeded.

Repository-wide checks already report 40 Ruff findings and 9 Pyright errors in
unchanged code. These unrelated issues are not silently fixed as part of this
repair. No new full audio inference, model/dictionary download, device playback,
Windows/Linux installation, or comprehensive vulnerability scan was performed.
The two regressions do not constitute comprehensive application test coverage.
