# Changelog

## 5.6.0 — 2026-09-22

### Added
- DXF export now allows selecting the target AutoCAD/DXF version: **2000, 2004, 2007, 2010, 2013 or 2018**.
- AutoCAD 2010 / `R2010` remains the default, preserving the previous export behaviour when the user does not change the selection.
- Regression tests verify that each selectable version is written correctly and can be read back as an `LWPOLYLINE`.

### Compatibility / safety
- Existing DXF geometry behaviour is unchanged: `EGSA_BOUNDARY` remains the base polyline layer, while POINT and TEXT vertex options remain independent and optional.
- DXF R12 is intentionally not offered because it would require a separate legacy `POLYLINE` export path instead of the existing `LWPOLYLINE`.
- HATT coefficients, HATT → EGSA87 transformation logic, EGSA87 ↔ WGS84, Shapefile handling, Google Earth integration and map-provider behaviour are unchanged.
- OpenStreetMap remains removed from the map selector; ESRI Satellite and Google Maps remain available.


## 5.5.0 — 2026-09-22

**First stable release.** This release adds a dedicated EGSA87 ↔ WGS84 workflow and consolidates
the three main application modes into a more consistent desktop UI.

### Added
- New third main tab for bidirectional **EGSA87 ↔ WGS84** conversion (`EPSG:2100 ↔ EPSG:4326`).
- WGS84 input/output in decimal degrees and degrees/minutes/seconds (DMS).
- Numeric DMS entry table with separate Latitude/Longitude groups, global N/S and E/W selectors,
  automatic addition of a new row, and validation of degree/minute/second ranges.
- WGS84 workflows reuse the existing EGSA87 geometry state for map preview, polygon/area,
  Google Earth, Shapefile and DXF operations.
- Regression coverage for EGSA87/WGS84 round trips and decimal/DMS parsing/formatting.

### Changed
- Replaced the old main-mode radio buttons with clearer tab-like mode selectors.
- Unified the common **Preview / Import / Export** toolbox layout across HATT, EGSA87 and WGS84.
- Stabilized the main window size using the largest dynamic WGS84/DMS layout so changing modes
  does not cause abrupt resizing or hide the bottom toolbox.
- Updated in-app About/Help text and public documentation for the WGS84 workflow.
- Windows build workflow now also watches `wgs84_utils.py`.

### Compatibility / safety
- The HATT → EGSA87 polynomial formula and the audited HATT coefficient dataset are **unchanged**
  from `v5.4.0-beta.3`.
- Existing HATT and direct-EGSA87 calculation paths remain unchanged; the new WGS84 workflow is
  additive.
- Automated regression suite: **24 tests** on the release candidate build.

## 5.4.0-beta.3 — 2026-09-02

**Critical HATT coefficient data-correction release.** Users of beta.1/beta.2 should replace those
builds with beta.3 before performing new HATT → EGSA87 conversions.

### Fixed
- Re-audited the HATT coefficient dataset against the official O.K.X.E. / ΓΥΣ / ΕΜΠ publication.
- Corrected material transcription errors inherited from a legacy spreadsheet, including wrong
  exponents, signs and individual digits in affected records. Confirmed corrections include
  Agrinio, Athens-Elefsis/Thiva/Chalkida group, Anatoliki Ydra/Ydra, Dyt. Irakleia/Ios/Shoinousa,
  Erythrai, Echinades/Atokos, Zakynthos, Thermi/Thessaloniki/Kilkis/Lahanas, Kandyla/Nemea, Lamia,
  Mesolongi and Kasos.
- Preserved the official printed precision of unusually large but legitimate quadratic terms for
  Akra Paximadi/Gavrion (north), Vartholomio, Anafi and Paxoi.
- The Kastellorizo constants remain unchanged: the anomalous values are confirmed by the official
  publication itself, so the existing explicit warning remains the safe behaviour.

### Verification / documentation
- Added regression checks for canonical corrected coefficients.
- Added a dataset-wide magnitude guard for second-degree terms to catch exponent-transcription
  errors of the type found during this audit.
- Updated `DATA_SOURCES.md` to use the official ΓΥΣ/ΟΚΧΕ/ΕΜΠ publication as the canonical source
  and to document the official limitations of the transformation.
- Updated application/build metadata to `v5.4.0-beta.3`.
- Added a dedicated EGSA Suite application icon for the window, taskbar and packaged Windows EXE.

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
