# Contributing

Contributions that improve correctness, interoperability with Greek GIS/CAD workflows, tests or
clear documentation are welcome.

For transformation-data changes, please include:

1. the authoritative or independently verifiable source;
2. the exact record(s) changed;
3. at least one regression/control-point test when possible;
4. a short explanation of the expected accuracy or limitation.

For code changes, run:

```bash
python -m pip install -r requirements-dev.txt
python -m pytest -q
```

Please avoid committing `build/`, `dist/`, virtual environments, caches or generated logs.
