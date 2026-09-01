# Changelog

## 5.4.0-beta.2 — 2026-09-01

Small usability release following the first public beta.

### Added
- Users can set any HATT sheet as their personal default; the selection is stored outside the portable EXE in the per-user settings directory and restored automatically on the next launch.
- DXF export now presents explicit options for separate vertex POINT entities and vertex-name TEXT labels. The base `EGSA_BOUNDARY` polyline is always exported; optional layers are off by default for a cleaner DXF.
- Added regression tests for per-user settings persistence and DXF export options.

### Changed
- Updated application/build metadata to `v5.4.0-beta.2`.

## 5.4.0-beta.1 — 2026-09-01

Public-release hardening of the v5.3 codebase.

### Fixed
- Prevented division by zero when a HATT polygon has zero area.
- Added self-intersection detection; invalid polygons no longer report/export a misleading area.
- Replaced heuristic `.prj` string matching with `pyproj.CRS` validation for EPSG:2100.
- Shapefile import no longer silently concatenates multiple features or ignores multipart geometry;
  the user explicitly selects the feature/part to import.
- Shapefile DBF text now respects common `.cpg` encodings (including Greek CP1253/ISO-8859-7).
- External SHP/DXF vertex labels are normalized before being placed in the text-input parser.
- Reworked Google Earth logging to use a dedicated file handler instead of a second
  `logging.basicConfig()` call.
- Corrected HATT sheet-centre display from apparent decimal degrees to degrees/minutes notation.
- Added explicit warning/confirmation for the unverified Kastellorizo HATT coefficient record.
- Unified public version information.

### Repository / release engineering
- Added MIT license and third-party attribution/license copies.
- Added data provenance notes and known-data warning.
- Added runtime/build/development dependency files with supported version ranges.
- Added `.gitignore` and removed generated build/cache artifacts from the release source tree.
- Added automated regression tests and GitHub Actions CI for Python 3.13/3.14 on Windows.
- Added a release-packaging build script that keeps license notices beside the executable.

## 5.3 — 2026

- HATT sheet code shown inside the selection list (`Φ. <number> — <region>`).
- Updated help/about text and v5.3 UI labels.
