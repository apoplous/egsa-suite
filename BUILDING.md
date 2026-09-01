# Building EGSA Suite on Windows

## Recommended environment

- Windows 10/11 x64
- Python 3.13 or 3.14 x64
- Clean virtual environment

## Automated build

From the repository root:

```bat
build_exe.bat
```

The script:

1. installs `requirements-build.txt`;
2. removes previous `build/`, `dist/` and release staging output;
3. runs PyInstaller using `EGSA_Suite.spec`;
4. creates a release folder containing the EXE, `LICENSE`, `THIRD_PARTY_NOTICES.md`,
   `DATA_SOURCES.md` and `licenses/`;
5. creates a ZIP suitable for attaching to a GitHub Release.

Expected output:

```text
dist/EGSA_Suite.exe
release/EGSA_Suite_v5.4.0-beta.2_Windows_x64/
release/EGSA_Suite_v5.4.0-beta.2_Windows_x64.zip
```

## Before publishing a binary

Run the regression suite first:

```bat
python -m pip install -r requirements-dev.txt
set EGSA_SUITE_NO_SPLASH=1
python -m pytest -q
```

Then launch the produced EXE manually and check at minimum:

- HATT → EGSA87 with a known non-Kastellorizo sheet;
- EGSA87 point and polygon workflows;
- Shapefile import/export;
- DXF import/export;
- Google Earth Pro opening/live link if GE Pro is available;
- About/Help version and license wording.

For public releases, calculate a SHA-256 checksum of the ZIP or EXE and publish it with the release
notes.
