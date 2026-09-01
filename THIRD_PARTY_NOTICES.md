# Third-party notices

EGSA Suite is open-source software, but it also uses or adapts third-party open-source components.
This file is informational and does not replace the license texts in `licenses/`.

## egsa2ge

The Google Earth KML NetworkLink, local HTTP-server and camera-tracking integration in EGSA Suite
is based in part on and adapts ideas/code from **egsa2ge** by Ioannis Maras & Georgios Maras:

- Project: https://github.com/dasaki-greece/egsa2ge
- License: MIT
- Upstream copyright: Copyright (c) 2026 Ioannis Maras & Georgios Maras
- Full license copy: `licenses/egsa2ge-MIT.txt`

## Runtime libraries

The source version declares these direct runtime dependencies. Their upstream license files are
included under `licenses/` for convenient redistribution with binary releases.

- pyshp — MIT — `licenses/pyshp-LICENSE.txt`
- pyproj — MIT — `licenses/pyproj-LICENSE.txt`
- PROJ data/library license used by pyproj — `licenses/PROJ-LICENSE.txt`
- Matplotlib — Matplotlib license — `licenses/matplotlib-LICENSE.txt`
- Folium — MIT — `licenses/folium-LICENSE.txt`
- ezdxf — MIT — `licenses/ezdxf-LICENSE.txt`

Binary builds produced by PyInstaller can also include transitive dependencies and data files.
Anyone redistributing a modified binary should review the licenses of the exact dependency set used
for that build.
