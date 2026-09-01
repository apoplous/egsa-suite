# HATT transformation data and provenance

## What the application contains

`hatt_coefficients.py` contains **390 HATT transformation records corresponding to 387 numeric
sheet codes**. Each record stores a sheet centre (`phi0`, `lam0`) and two sets of six coefficients
for a second-degree HATT → EGSA87 polynomial.

The polynomial form used by EGSA Suite is:

```text
E = A0 + A1*x + A2*y + A3*x² + A4*y² + A5*x*y
N = B0 + B1*x + B2*y + B3*x² + B4*y² + B5*x*y
```

The general method is documented in Greek mapping/cadastral material. Article 5 of Decision
71154/95 describes HATT → EGSA87 conversion using second-degree polynomials and states that the
numerical coefficients were published in a special edition by O.K.X.E. and the Hellenic Military
Geographical Service with the collaboration of NTUA:

https://www.nomoskopio.gr/a_71154_95_1_5.php

That article was later repealed; it is cited here as historical documentation of the method and the
origin of the coefficient tables, not as a statement of current legal applicability.

A 2012 public discussion records a table of coefficients circulated by Prof. Kostas Katsampalos,
then a member of the O.K.X.E. board, following an O.K.X.E. board decision:

https://forum.ubuntu-gr.org/viewtopic.php?f=6&t=22817&start=50

## Important notation detail

The `phi0` and `lam0` fields in the inherited table use **degrees.minutes notation**, not decimal
degrees. For example `40.15` means **40°15′**. Longitude values refer to the historical Athens
prime-meridian convention used by the HATT sheet system. EGSA Suite v5.4 displays this explicitly
instead of showing these values as decimal degrees.

## Known unverified record: Kastellorizo

The record `ΝΗΣΟΣ ΜΕΓΙΣΤΗ(ΚΑΣΤΕΛΛΟΡΙΖΟ)` is intentionally **not silently trusted** in the public
release candidate. Its published constants are:

```text
A0 = 721683.24
B0 = 4014622.76
```

A geographic sanity check shows a very large inconsistency between the declared sheet centre and
these constants, unlike the other records. The same values also appear in historical public copies
of the table, so EGSA Suite does **not** alter them without a primary authoritative correction.
Instead the application displays a warning before conversion with this record.

If an official corrected table or verified control points become available, this record should be
updated only together with a regression test and a citation to the source.

## Professional-use warning

The polynomial transformation is an aid for legacy mapping workflows. Accuracy depends on the
correct HATT sheet, the datum/realisation of the source coordinates and the quality of the source
material. Results intended for administrative, cadastral, surveying or legal use should be checked
against known control points and the applicable official specifications.
