"""
GoogleEarthService — προσαρμοσμένο για EGSA Suite.
Χρησιμοποιεί pyproj απευθείας, χωρίς εξάρτηση από το αρχικό core/models.
"""

from pathlib import Path
from datetime import datetime
from typing import Callable, Optional
import logging
from pyproj import Transformer
from dataclasses import dataclass

from .file_service import FileService
from .http_server import LocalServer
from kml.network_link import generate_network_link_kml
from kml.current_point import generate_current_point_kml
from kml.fly_to import generate_fly_to_point_kml, generate_empty_fly_to_kml
from kml.saved_points import generate_saved_points_kml, append_placemark_to_saved_points
from kml.polygon import generate_polygon_kml

logger = logging.getLogger("egsa_suite.google_earth")


@dataclass
class GEPoint:
    x: float; y: float
    longitude: float; latitude: float
    name: str; view_range: float = 800.0


_EGSA_TO_WGS = Transformer.from_crs("EPSG:2100", "EPSG:4326", always_xy=True)
_WGS_TO_EGSA = Transformer.from_crs("EPSG:4326", "EPSG:2100", always_xy=True)

def _egsa_to_wgs84(x, y):   return _EGSA_TO_WGS.transform(x, y)
def _wgs84_to_egsa(lon, lat): return _WGS_TO_EGSA.transform(lon, lat)


class GoogleEarthService:
    def __init__(self, work_dir: Path) -> None:
        self.work_dir = work_dir
        self.work_dir.mkdir(parents=True, exist_ok=True)
        self.log_file = work_dir / "ge_debug.log"
        self.last_poll_time = 0.0

        # Dedicated logger: δεν βασίζεται σε δεύτερο logging.basicConfig(),
        # το οποίο αγνοείται όταν η κύρια εφαρμογή έχει ήδη handlers.
        logger.setLevel(logging.DEBUG)
        log_path = str(self.log_file.resolve())
        if not any(
            isinstance(h, logging.FileHandler) and getattr(h, "baseFilename", None) == log_path
            for h in logger.handlers
        ):
            handler = logging.FileHandler(self.log_file, encoding="utf-8")
            handler.setLevel(logging.DEBUG)
            handler.setFormatter(logging.Formatter(
                '%(asctime)s [%(levelname)s] %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            ))
            logger.addHandler(handler)
        logger.propagate = False
        logger.info("--- EGSA Suite GE Service Started ---")

        self.file_service = FileService(work_dir)
        self.network_link_path = work_dir / "egsa87_live_link.kml"
        self.server = LocalServer(port=8000, service=self)

        self.current_point: Optional[GEPoint] = None
        self.current_point_timestamp: str = ""
        self.fly_to_point: Optional[GEPoint] = None
        self.saved_points_kml_content: str = generate_saved_points_kml()
        self.polygon_kml_content: str = ""
        self.camera_lon: float = 0.0
        self.camera_lat: float = 0.0
        self.on_camera_update_callback: Optional[Callable[[float, float, float, float], None]] = None

    def initialize(self) -> None:
        self.file_service.ensure_work_dir()
        self.server.start()
        self.file_service.write_kml(self.network_link_path, self._generate_stub_link())
        logger.info(f"NetworkLink: {self.network_link_path}")

    def shutdown(self) -> None:
        self.server.stop()
        logger.info("--- GE Service Stopped ---")

    def set_camera_callback(self, cb: Callable[[float, float, float, float], None]) -> None:
        self.on_camera_update_callback = cb

    # ── Public API ───────────────────────────────────────────────────────────

    def send_point(self, egsa_x: float, egsa_y: float, name: str, fly_to: bool = True) -> None:
        lon, lat = _egsa_to_wgs84(egsa_x, egsa_y)
        pt = GEPoint(x=egsa_x, y=egsa_y, longitude=lon, latitude=lat, name=name)
        self.current_point = pt
        self.current_point_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if fly_to:
            self.fly_to_point = pt

    def add_saved_point(self, egsa_x: float, egsa_y: float, name: str) -> None:
        lon, lat = _egsa_to_wgs84(egsa_x, egsa_y)
        pt = GEPoint(x=egsa_x, y=egsa_y, longitude=lon, latitude=lat, name=name)
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.saved_points_kml_content = append_placemark_to_saved_points(
            self.saved_points_kml_content, pt, ts)
        self.current_point = pt
        self.current_point_timestamp = ts

    def send_polygon(self, points: list, name: str = "Πολύγωνο ΕΓΣΑ87") -> None:
        self.polygon_kml_content = generate_polygon_kml(points, name)
        self.saved_points_kml_content = generate_saved_points_kml()

    def clear_saved_points(self) -> None:
        self.saved_points_kml_content = generate_saved_points_kml()
        self.polygon_kml_content = ""

    def open_in_google_earth(self) -> None:
        from utils.platform_utils import open_path
        open_path(self.network_link_path)

    # ── HTTP callbacks ───────────────────────────────────────────────────────

    def update_all_kmls(self, point=None) -> None:
        if point is not None:
            self.current_point = point
            self.current_point_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.fly_to_point = None

    def clear_fly_to(self) -> None:
        self.fly_to_point = None

    def trigger_fly_to(self, point) -> None:
        self.current_point = point
        self.current_point_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.fly_to_point = point

    def on_camera_updated(self, lon: float, lat: float) -> None:
        self.camera_lon = lon
        self.camera_lat = lat
        if self.on_camera_update_callback:
            try:
                x, y = _wgs84_to_egsa(lon, lat)
                self.on_camera_update_callback(x, y, lon, lat)
            except Exception as e:
                logger.error(f"Transform error: {e}")

    # ── KML generators (καλούνται από HTTP server) ───────────────────────────

    def generate_live_network_link(self) -> str:
        return generate_network_link_kml(f"http://127.0.0.1:{self.server.port}")

    def get_current_point_kml(self) -> str:
        if self.current_point:
            return generate_current_point_kml(self.current_point, self.current_point_timestamp)
        return ""

    def get_fly_to_kml(self) -> str:
        if self.fly_to_point:
            kml = generate_fly_to_point_kml(
                self.fly_to_point.longitude, self.fly_to_point.latitude,
                self.fly_to_point.view_range)
            self.fly_to_point = None
            return kml
        return generate_empty_fly_to_kml()

    def get_saved_points_kml(self) -> str:
        if self.polygon_kml_content:
            return self.polygon_kml_content
        return self.saved_points_kml_content

    def get_camera_target_kml(self) -> str:
        if self.camera_lon == 0.0 and self.camera_lat == 0.0:
            return ""
        try:
            x, y = _wgs84_to_egsa(self.camera_lon, self.camera_lat)
            desc = (f"WGS84: {self.camera_lon:.6f}, {self.camera_lat:.6f}"
                    f"&lt;br/&gt;ΕΓΣΑ87: {x:.3f}, {y:.3f}")
        except Exception:
            desc = "Εκτός ορίων"
        return f"""<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
<Document>
  <Placemark>
    <name>Κέντρο Οθόνης</name>
    <description><![CDATA[{desc}]]></description>
    <Style><IconStyle><scale>0</scale></IconStyle><LabelStyle><scale>0</scale></LabelStyle></Style>
    <Point><coordinates>{self.camera_lon},{self.camera_lat},0</coordinates></Point>
  </Placemark>
</Document>
</kml>"""

    def _generate_stub_link(self) -> str:
        return f"""<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
  <NetworkLink>
    <name>ΕΓΣΑ87 Live Link</name>
    <open>1</open>
    <Link><href>http://127.0.0.1:{self.server.port}/live_link.kml</href></Link>
  </NetworkLink>
</kml>"""
