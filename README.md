# Batman Arkham City GOTY - Cheat Engine project

Core features user-tested. In v5, the user also reports a phone countdown holding around 58-59 seconds and one-shot Batarang results. Remaining variants and table-only timer tests are documented. Archive prepared 2026-10-07 from surviving project artifacts and conversation test reports.

Start with [v6, the current requested table](tables/recommended/v6/Batman Arkham City GOTY - Original v6.CT). It removes Gameplay / Time while keeping the existing core, phone-race, and challenge features. Code and simulated regression checks passed; this is not a claim that every challenge feature has been gameplay-tested.

## Navigation

| What you want | Where to look |
| --- | --- |
| Recommended versus historical versions | [Version catalog](catalog/VERSIONS.md) |
| Features by version, category, purpose, and code type | [Filterable CSV](catalog/features.csv) / [JSON](catalog/features.json) |
| Confirmed tests, incomplete features, and known bugs | [Project status](docs/STATUS_AND_TESTING.md) |
| What changed and why | [Development history](docs/HISTORY.md) |
| How to load and test safely | [Safety and setup](docs/SAFETY_AND_SETUP.md) |
| Source attribution and exclusions | [Provenance](docs/PROVENANCE.md) |
| Integrity checks | [SHA-256 manifest](CHECKSUMS.sha256) |

## Organization

- tables/recommended: selected baseline, not a promise that every feature is verified.
- tables/history: superseded original files retained for comparison.
- tables/experiments: incomplete or abandoned changes, clearly labeled.
- development/work: available original research and source files. Extensions identify Python (.py), PowerShell (.ps1), and Lua (.lua); table-embedded code is classified in the feature catalog.
- docs: project-specific decisions, gameplay evidence, known limitations, and safety guidance.
- catalog: machine-readable and human-readable indexes; these let you sort/filter without renaming source artifacts.

The catalogs are inventories, not automatic gameplay validation. See the status document for actual evidence. Original .CT files are copied byte-for-byte; development sources are retained where available. No game binaries, private dumps, dependency packages, or third-party reference tables are included.

Latest build: v6. The removed story-play-time freeze, 1.5x speed, and 0.5x slow motion remain available only in historical versions. See [v6 notes](docs/version-notes/Batman%20Arkham%20City%20GOTY%20-%20Original%20v6%20NOTES.md). A proposed one-key Riddler helper is [feasibility research only](docs/RIDDLER_FEASIBILITY.md), not an implemented cheat.

Suggested GitHub issue labels: status:confirmed, status:partial, status:untested, status:abandoned, type:bug, type:feature, area:combat, area:survival, area:gadgets, area:teleport, area:timers, code:lua, code:auto-assembler, code:python, code:powershell. These are suggestions, not labels already created on GitHub.
