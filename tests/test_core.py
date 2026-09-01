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
    format_hatt_angle,
    is_epsg2100_prj,
    safe_point_name,
    shapefile_text_encoding,
)


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
