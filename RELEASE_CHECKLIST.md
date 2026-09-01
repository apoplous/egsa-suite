# Release checklist

Use this before changing a GitHub pre-release to a stable release.

- [ ] `python -m pytest -q` passes.
- [ ] Windows EXE builds from a clean virtual environment.
- [ ] HATT → EGSA87 checked with at least one known control example.
- [ ] Kastellorizo warning is still present unless the record has been authoritatively corrected.
- [ ] EGSA87 point / line / polygon workflows manually checked.
- [ ] SHP single-feature and multipart/multi-feature import checked.
- [ ] SHP export opens correctly in ArcGIS/QGIS and reports EPSG:2100.
- [ ] DXF import/export checked in the target CAD software.
- [ ] Google Earth Pro live integration checked on Windows if available.
- [ ] Version is consistent in `geotoolsgr.py`, `version_info.txt`, `CHANGELOG.md` and build script.
- [ ] `LICENSE`, `THIRD_PARTY_NOTICES.md`, `DATA_SOURCES.md` and `licenses/` are in the release ZIP.
- [ ] `SHA256SUMS.txt` is attached to the GitHub Release.
- [ ] Release notes describe known limitations and any data-table changes.
