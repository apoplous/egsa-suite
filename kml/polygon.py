"""
Δημιουργία KML πολυγώνου από λίστα GEPoint.
Χρησιμοποιείται όταν υπάρχουν ≥3 σημεία.
"""

from xml.sax.saxutils import escape


def generate_polygon_kml(points, name: str = "Πολύγωνο ΕΓΣΑ87") -> str:
    """
    Δημιουργεί KML με:
    - έναν Polygon (outline + ημιδιαφανές fill)
    - ένα Placemark ανά κορυφή με το όνομά της
    - LookAt στο κέντρο του πολυγώνου

    Args:
        points: λίστα GEPoint
        name:   όνομα του Document
    """
    if len(points) < 3:
        return ""

    # Κέντρο (για LookAt)
    center_lon = sum(p.longitude for p in points) / len(points)
    center_lat = sum(p.latitude  for p in points) / len(points)

    # Εκτίμηση view_range από το μέγεθος του πολυγώνου
    lon_span = max(p.longitude for p in points) - min(p.longitude for p in points)
    lat_span = max(p.latitude  for p in points) - min(p.latitude  for p in points)
    span_deg = max(lon_span, lat_span)
    # Κατά προσέγγιση: 1 μοίρα ≈ 111 km → view_range σε μέτρα
    view_range = max(500.0, span_deg * 111_000 * 1.6)

    # Συντεταγμένες πολυγώνου (κλειστός δακτύλιος)
    coords = "\n                ".join(
        f"{p.longitude:.10f},{p.latitude:.10f},0" for p in points
    )
    # Κλείσιμο δακτυλίου
    first = points[0]
    coords += f"\n                {first.longitude:.10f},{first.latitude:.10f},0"

    # Placemarks κορυφών
    vertex_placemarks = ""
    for p in points:
        safe_name = escape(p.name)
        desc = (
            f"Χ ΕΓΣΑ87: {p.x:.3f}&lt;br/&gt;"
            f"Υ ΕΓΣΑ87: {p.y:.3f}&lt;br/&gt;"
            f"Lon: {p.longitude:.8f}&lt;br/&gt;"
            f"Lat: {p.latitude:.8f}"
        )
        vertex_placemarks += f"""
    <Placemark>
      <name>{safe_name}</name>
      <description>{desc}</description>
      <styleUrl>#vertexStyle</styleUrl>
      <Point>
        <coordinates>{p.longitude:.10f},{p.latitude:.10f},0</coordinates>
      </Point>
    </Placemark>"""

    safe_doc_name = escape(name)

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
<Document>
  <name>{safe_doc_name}</name>

  <LookAt>
    <longitude>{center_lon:.10f}</longitude>
    <latitude>{center_lat:.10f}</latitude>
    <altitude>0</altitude>
    <range>{view_range:.2f}</range>
    <tilt>0</tilt>
    <heading>0</heading>
  </LookAt>

  <!-- Στυλ πολυγώνου -->
  <Style id="polygonStyle">
    <LineStyle>
      <color>ff0000ff</color>
      <width>2.5</width>
    </LineStyle>
    <PolyStyle>
      <color>330000ff</color>
    </PolyStyle>
  </Style>

  <!-- Στυλ κορυφών -->
  <Style id="vertexStyle">
    <IconStyle>
      <scale>0.9</scale>
      <Icon>
        <href>http://maps.google.com/mapfiles/kml/paddle/blu-circle.png</href>
      </Icon>
    </IconStyle>
    <LabelStyle>
      <scale>0.8</scale>
    </LabelStyle>
  </Style>

  <!-- Πολύγωνο -->
  <Placemark>
    <name>{safe_doc_name}</name>
    <styleUrl>#polygonStyle</styleUrl>
    <Polygon>
      <outerBoundaryIs>
        <LinearRing>
          <coordinates>
                {coords}
          </coordinates>
        </LinearRing>
      </outerBoundaryIs>
    </Polygon>
  </Placemark>

  <!-- Κορυφές -->{vertex_placemarks}

</Document>
</kml>
"""
