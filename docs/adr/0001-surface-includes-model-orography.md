# Surface downloads include model orography

Deterministic ICON surface downloads store model elevation and model surface pressure. Ensemble downloads omit both. The curated `heidiVars` selector is removed, and the test D2 schedule is the full surface download.

The curated selector existed to skip eleven heavier single-level fields. Keeping it meant a second writer and a separate spatial index. One surface download is the schedule that was chosen. Ensembles already fetch the same pressure field under sea-level pressure, so they stay without a second copy and without a model-elevation series. The test host may run one surface download on the previous binary, which stores those eleven fields and not the two orography fields, before the binary that includes them is installed.
