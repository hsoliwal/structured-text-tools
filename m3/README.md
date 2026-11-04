# M3 structured-text donor discovery

This is an **additive, machine-readable candidate index** over the existing
[`data/projects.toml`](../data/projects.toml). It does not change the upstream
catalogue, generated Markdown, command-line tools, or runtime implementation.

The initial candidates are classified only from the existing catalogue
descriptions. **Candidate is not approval.** Every license remains unverified;
no benchmark has been run and no Java/JNI implementation is claimed.

From the checkout root with Python 3.11+ (or Python 3.8+ with `tomli`):

```sh
python3 -m m3.catalogue --check
python3 -m m3.catalogue --category structured-search --operation join
python3 -m m3.catalogue --tag json --format jsonl
python3 -m unittest discover -s tests -p 'test_m3_catalogue.py' -v
```

All repeated filters intersect (AND). Results retain the original
`data/projects.toml` project order, including mixed-case project names.
`jsonl` emits one compact JSON object per line for ingestion into an M3
problem-category index; default `json` emits an array.

## Evaluation and promotion contract

1. Add an existing project name under `[donors.<name>]` in `donors.toml`.
   Use operation/category slugs grounded in its description, not speculative
   performance claims. No upstream entry needs changing.
2. Evaluate the donor's actual source, license and compatibility independently.
   Advancement to `reviewed`, a compatible/incompatible license assessment, or
   `benchmarked` requires evidence URLs. Unknown remains explicitly unknown.
3. For Java/JNI implementation, the Synexia convergence workspace must own the
   Maven/OpenRewrite recipe, tests (including boundary cases), benchmark
   evidence, and public API contract. Promoting an `*-implemented` status
   requires a recipe ID and test evidence URL.
4. Validate with `--check` and the differential tests before proposing a PR.

No donor code is copied by this index. Candidate discovery is offline and
deterministic, without an LLM in the hot path. This is groundwork for later
Java 21/JNI recipe-backed implementations, **not** those implementations.
