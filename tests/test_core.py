from decimal import Decimal
from pathlib import Path

import shapefile
import pytest

from geotoolsgr import (
    CoordinateTransformer,
    HATT_COEFFICIENTS,
    InputParser,
    Point,
    PolygonCalculator,
    ShapefileExporter,
    extract_shapefile_candidates,
    export_dxf_file,
    format_hatt_angle,
    is_epsg2100_prj,
    safe_point_name,
    shapefile_text_encoding,
    load_user_settings,
    save_user_settings,
    configured_default_region,
)
from wgs84_utils import format_wgs84_dms, parse_wgs84_points


def P(name, x, y):
    return Point(name, Decimal(str(x)), Decimal(str(y)))


def test_hatt_dataset_structure():
    assert len(HATT_COEFFICIENTS) == 390
    codes = [item["code"] for item in HATT_COEFFICIENTS.values()]
    assert len(set(codes)) == 387
    assert set(codes) == set(range(1, 388))
    for item in HATT_COEFFICIENTS.values():
        assert len(item["A"]) == 6
        assert len(item["B"]) == 6


def test_katerini_zero_origin_regression():
    tr = CoordinateTransformer()
    tr.set_region("ΚΑΤΕΡΙΝΗ")
    x, y = tr.HATT_to_egsa(Decimal("0"), Decimal("0"))
    d = HATT_COEFFICIENTS["ΚΑΤΕΡΙΝΗ"]
    assert x == Decimal(str(d["A"][0]))
    assert y == Decimal(str(d["B"][0]))


def test_katerini_nonzero_polynomial_regression():
    tr = CoordinateTransformer()
    tr.set_region("ΚΑΤΕΡΙΝΗ")
    x, y = tr.HATT_to_egsa(Decimal("1000"), Decimal("2000"))
    assert x == Decimal("370620.24738000000")
    assert y == Decimal("4458411.29166000000")


def test_parser_accepts_greek_decimal_comma():
    pts, errors = InputParser.parse_points("A 123,45 678,90")
    assert errors == []
    assert pts[0].x == Decimal("123.45")
    assert pts[0].y == Decimal("678.90")


def test_hatt_angle_is_degrees_minutes_not_decimal_degrees():
    assert format_hatt_angle(40.15) == "40°15′"
    assert format_hatt_angle(-1.45) == "−1°45′"


def test_polygon_area_and_self_intersection():
    square = [P("A", 0, 0), P("B", 10, 0), P("C", 10, 10), P("D", 0, 10)]
    bow = [P("A", 0, 0), P("B", 10, 10), P("C", 0, 10), P("D", 10, 0)]
    assert PolygonCalculator.calculate_area(square) == Decimal("100")
    assert not PolygonCalculator.has_self_intersections(square)
    assert PolygonCalculator.has_self_intersections(bow)


def test_epsg2100_prj_parser():
    assert is_epsg2100_prj(ShapefileExporter.PRJ_EPSG_2100)
    assert not is_epsg2100_prj('GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563]],PRIMEM["Greenwich",0],UNIT["degree",0.0174532925199433]]')


def test_shapefile_export_rejects_zero_area(tmp_path: Path):
    pts = [P("A", 400000, 4400000), P("B", 400010, 4400010), P("C", 400020, 4400020)]
    with pytest.raises(ValueError, match="μηδενικό εμβαδόν"):
        ShapefileExporter.export_geometry(pts, str(tmp_path / "bad.shp"))


def test_shapefile_export_rejects_self_intersection(tmp_path: Path):
    pts = [
        P("A", 400000, 4400000),
        P("B", 400100, 4400100),
        P("C", 400000, 4400100),
        P("D", 400100, 4400000),
    ]
    with pytest.raises(ValueError, match="αυτοτομή"):
        ShapefileExporter.export_geometry(pts, str(tmp_path / "bow.shp"))


def test_shapefile_export_roundtrip_polygon(tmp_path: Path):
    pts = [
        P("A", 400000, 4400000),
        P("B", 400100, 4400000),
        P("C", 400100, 4400100),
        P("D", 400000, 4400100),
    ]
    shp = tmp_path / "ok.shp"
    assert ShapefileExporter.export_geometry(pts, str(shp)) == "POLYGON"
    assert shp.exists()
    assert shp.with_suffix(".prj").exists()
    assert shp.with_suffix(".cpg").read_text(encoding="utf-8") == "UTF-8"
    reader = shapefile.Reader(str(shp))
    assert len(reader.shapes()) == 1


def test_multipart_and_multifeature_shp_are_separate_candidates(tmp_path: Path):
    shp = tmp_path / "multi.shp"
    w = shapefile.Writer(str(shp), shapeType=shapefile.POLYGON, encoding="utf-8")
    w.field("NAME", "C", size=40)
    ring1 = [(400000, 4400000), (400010, 4400000), (400010, 4400010), (400000, 4400000)]
    ring2 = [(400100, 4400100), (400110, 4400100), (400110, 4400110), (400100, 4400100)]
    ring3 = [(400200, 4400200), (400210, 4400200), (400210, 4400210), (400200, 4400200)]
    w.poly([ring1, ring2])
    w.record("multipart")
    w.poly([ring3])
    w.record("single")
    w.close()

    candidates = extract_shapefile_candidates(shapefile.Reader(str(shp), encoding="utf-8"))
    assert len(candidates) == 3
    assert [(c["feature_index"], c["part_index"]) for c in candidates] == [(1, 1), (1, 2), (2, 1)]
    assert all(c["geometry_type"] == "POLYGON" for c in candidates)


def test_safe_external_point_name():
    assert safe_point_name("Κορυφή Α, 1") == "Κορυφή_Α_1"


def test_shapefile_cpg_cp1253(tmp_path: Path):
    shp = tmp_path / "greek.shp"
    shp.touch()
    shp.with_suffix(".cpg").write_text("1253", encoding="ascii")
    assert shapefile_text_encoding(str(shp)) == "cp1253"


def test_user_settings_roundtrip_and_default_region(tmp_path: Path):
    settings_file = tmp_path / "settings.json"
    saved = {"default_hatt_region": "ΚΑΤΕΡΙΝΗ", "default_hatt_code": HATT_COEFFICIENTS["ΚΑΤΕΡΙΝΗ"]["code"]}
    assert save_user_settings(saved, settings_file) == settings_file
    loaded = load_user_settings(settings_file)
    assert loaded == saved
    assert configured_default_region(loaded) == "ΚΑΤΕΡΙΝΗ"


def test_invalid_saved_hatt_region_falls_back_to_builtin_default():
    assert configured_default_region({"default_hatt_region": "ΔΕΝ ΥΠΑΡΧΕΙ"}) == "ΚΑΤΕΡΙΝΗ"


def test_dxf_export_options_control_points_and_labels(tmp_path: Path):
    pytest.importorskip("ezdxf")
    import ezdxf

    pts = [P("A", 400000, 4400000), P("B", 400100, 4400000), P("C", 400100, 4400100)]

    clean_path = tmp_path / "clean.dxf"
    info = export_dxf_file(pts, str(clean_path))
    assert info["layers"] == ["EGSA_BOUNDARY"]
    doc = ezdxf.readfile(clean_path)
    msp = doc.modelspace()
    assert len(msp.query("LWPOLYLINE")) == 1
    assert len(msp.query("POINT")) == 0
    assert len(msp.query("TEXT")) == 0

    full_path = tmp_path / "full.dxf"
    info = export_dxf_file(pts, str(full_path), include_points=True, include_labels=True)
    assert info["layers"] == ["EGSA_BOUNDARY", "EGSA_POINTS", "EGSA_LABELS"]
    doc = ezdxf.readfile(full_path)
    msp = doc.modelspace()
    assert len(msp.query("POINT")) == 3
    assert len(msp.query("TEXT")) == 3


def test_official_hatt_coefficient_corrections_regression():
    # Canonical values checked against the official OKXE / GYS / NTUA printed tables.
    checks = [
        ("ΑΓΡΙΝΙΟΝ", "B", 1, -0.0277237),
        ("ΑΘΗΝΑ-ΕΛΕΥΣΙΣ", "B", 4, -3e-10),
        ("ΑΘΗΝΑ-ΕΛΕΥΣΙΣ", "B", 5, -7.6e-10),
        ("ΑΘΗΝΑ-ΕΛΕΥΣΙΣ (φ.119)", "B", 4, -3e-10),
        ("ΑΘΗΝΑ-ΕΛΕΥΣΙΣ (φ.119)", "B", 5, -7.6e-10),
        ("ΑΝΑΤΟΛΙΚΗ ΥΔΡΑ", "A", 0, 452679.92),
        ("ΥΔΡΑ", "A", 0, 452679.92),
        ("ΔΥΤ.ΗΡΑΚΛΕΙΑ", "A", 5, -3e-11),
        ("ΙΟΣ", "A", 5, -3e-11),
        ("ΣΧΟΙΝΟΥΣΑ", "A", 5, -3e-11),
        ("ΕΡΥΘΡΑΙ", "B", 5, -2.36e-9),
        ("ΕΧΙΝΑΔΕΣ", "B", 1, -0.032857),
        ("ΝΗΣΟΣ ΑΤΟΚΟΣ", "B", 1, -0.032857),
        ("ΖΑΚΥΝΘΟΣ", "B", 5, -6.94e-9),
        ("ΘΕΡΜΗ", "B", 2, 0.9996386),
        ("ΘΕΣΣΑΛΟΝΙΚΗ", "B", 2, 0.9996386),
        ("ΚΙΛΚΙΣ", "B", 2, 0.9996386),
        ("ΛΑΧΑΝΑΣ", "B", 2, 0.9996386),
        ("ΚΑΝΔΗΛΑ", "A", 3, -1.53e-9),
        ("ΝΕΜΕΑ", "A", 3, -1.53e-9),
        ("ΛΑΜΙΑ", "A", 2, 0.0168119),
        ("ΜΕΣΟΛΟΓΓΙΟΝ", "A", 3, -4.19e-9),
        ("ΜΕΣΟΛΟΓΓΙΟΝ", "A", 4, 4.25e-9),
        ("ΝΗΣΟΣ ΚΑΣΟΣ", "B", 3, -4.6e-10),
        ("ΧΑΛΚΙΣ", "B", 4, -3e-10),
        ("ΧΑΛΚΙΣ", "B", 5, -7.6e-10),
    ]
    for region, side, index, expected in checks:
        assert HATT_COEFFICIENTS[region][side][index] == expected, (region, side, index)

def test_hatt_quadratic_coefficients_have_plausible_magnitude():
    # The official table contains legitimate terms up to about 4.93e-8. Values >= 1e-7 are a
    # strong indication of a lost exponent digit (the exact failure mode found in the legacy XLS).
    limit = 1e-7
    for name, item in HATT_COEFFICIENTS.items():
        for side in ("A", "B"):
            for index in (3, 4, 5):
                value = item[side][index]
                assert abs(value) < limit, (name, side, index, value)


def test_official_high_order_precision_regression():
    assert HATT_COEFFICIENTS["ΑΚΡΑ ΠΑΞΙΜΑΔΙ"]["A"][4] == -40.85e-9
    assert HATT_COEFFICIENTS["ΑΚΡΑ ΠΑΞΙΜΑΔΙ"]["B"][4] == 49.28e-9
    assert HATT_COEFFICIENTS["ΒΑΡΘΟΛΟΜΙΟΝ"]["B"][5] == -12.05e-9
    assert HATT_COEFFICIENTS["ΝΗΣΟΣ ΑΝΑΦΗ"]["A"][5] == -12.44e-9
    assert HATT_COEFFICIENTS["ΝΗΣΟΙ ΠΑΞΟΙ"]["B"][5] == -14.85e-9


def test_egsa_wgs84_roundtrip_regression():
    tr = CoordinateTransformer()
    original_x = Decimal("369585.94")
    original_y = Decimal("4456429.27")
    lon, lat = tr.egsa_to_wgs84(original_x, original_y)
    roundtrip_x, roundtrip_y = tr.wgs84_to_egsa(lon, lat)
    # PROJ's forward/inverse EPSG operation is not mathematically exact to the
    # sub-millimetre after the datum/projection pipeline; centimetre-level
    # round-trip tolerance is ample for detecting axis/order or CRS mistakes.
    assert abs(roundtrip_x - original_x) < Decimal("0.01")
    assert abs(roundtrip_y - original_y) < Decimal("0.01")


def test_wgs84_decimal_parser_accepts_google_and_greek_decimal_styles():
    points, errors = parse_wgs84_points(
        "A 40.27212345, 22.50345678\nB 40,27222345 22,50355678",
        "decimal",
    )
    assert errors == []
    assert len(points) == 2
    assert points[0].latitude == pytest.approx(40.27212345)
    assert points[0].longitude == pytest.approx(22.50345678)
    assert points[1].latitude == pytest.approx(40.27222345)
    assert points[1].longitude == pytest.approx(22.50355678)


def test_wgs84_dms_format_and_parser_roundtrip():
    latitude = 40.27212345
    longitude = 22.50345678
    lat_dms = format_wgs84_dms(latitude, "lat")
    lon_dms = format_wgs84_dms(longitude, "lon")
    points, errors = parse_wgs84_points(f"A {lat_dms} {lon_dms}", "dms")
    assert errors == []
    assert len(points) == 1
    assert points[0].latitude == pytest.approx(latitude, abs=3e-7)
    assert points[0].longitude == pytest.approx(longitude, abs=3e-7)
