import os

# Importing geotoolsgr must not create a Tk splash window during automated tests.
os.environ.setdefault("EGSA_SUITE_NO_SPLASH", "1")
