"""
EGSA Suite – Coordinate Transformation Suite
Version 5.4.0-beta.3 - Public Release Candidate
Author: D.T. 2026

Μετατροπή συντεταγμένων από το τοπικό σύστημα HATT στο ΕΓΣΑ87
με βάση πολυωνυμικό μετασχηματισμό 2ου βαθμού.
"""

# ── Splash screen ─────────────────────────────────────────────────────────────
# Εμφανίζεται ΠΡΙΝ τα βαριά imports, ώστε ο χρήστης να βλέπει κάτι αμέσως.
import tkinter as tk
import sys, os
from pathlib import Path

def _early_icon_path() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys._MEIPASS) / "assets" / "egsa_suite.ico"
    return Path(__file__).resolve().parent / "assets" / "egsa_suite.ico"

def apply_window_icon(window) -> None:
    """Ορίζει το icon του παραθύρου, αν υπάρχει διαθέσιμο .ico αρχείο."""
    try:
        icon_path = _early_icon_path()
        if icon_path.exists():
            window.iconbitmap(default=str(icon_path))
    except Exception:
        pass

def _show_splash() -> tk.Toplevel | None:
    """Δημιουργεί και εμφανίζει το splash window EGSA Suite."""
    try:
        root_hidden = tk.Tk()
        root_hidden.withdraw()
        apply_window_icon(root_hidden)

        splash = tk.Toplevel(root_hidden)
        apply_window_icon(splash)
        splash.overrideredirect(True)
        splash.configure(bg="#0f2d1a")

        W, H = 580, 310
        sw = splash.winfo_screenwidth()
        sh = splash.winfo_screenheight()
        splash.geometry(f"{W}x{H}+{(sw-W)//2}+{(sh-H)//2}")

        c = tk.Canvas(splash, width=W, height=H, bg="#0f2d1a",
                      highlightthickness=0)
        c.pack()

        # ── Λεπτό border όλου του παραθύρου ──────────────────────
        c.create_rectangle(1, 1, W-1, H-1, outline="#2a6e3f", width=1)

        # ════════════════════════════════════════════════════════
        # ΑΡΙΣΤΕΡΟ ΤΜΗΜΑ — Βουνό Ολύμπου + pin  (0..200)
        # ════════════════════════════════════════════════════════
        LW = 200   # πλάτος αριστερής ζώνης

        # Ουρανός (πάνω μισό)
        c.create_rectangle(0, 0, LW, H, fill="#0f2d1a", outline="")

        # Βουνά — τρία επίπεδα για βάθος
        # Πίσω βουνό (πιο ανοιχτό)
        c.create_polygon(
            20,175,  80,70,  140,175,
            fill="#1e5530", outline=""
        )
        # Μεσαίο (κύριος Όλυμπος)
        c.create_polygon(
            0,175,  60,55,  120,175,
            fill="#2a6e3f", outline=""
        )
        # Μπροστινό (σκοτεινότερο)
        c.create_polygon(
            70,175,  130,100,  190,175,
            fill="#235e38", outline=""
        )

        # Χιόνι κορυφής (κύριος Όλυμπος)
        c.create_polygon(
            48,80,  60,55,  72,80,  67,77,  60,63,  53,77,
            fill="#e8f5e9", outline=""
        )
        # Χιόνι μεσαίου
        c.create_polygon(
            122,112,  130,100,  138,112,  135,110,  130,103,  125,110,
            fill="#c8e6c9", outline=""
        )

        # Έδαφος / πεδιάδα
        c.create_rectangle(0, 175, LW, H, fill="#1a4a2e", outline="")
        c.create_line(0, 175, LW, 175, fill="#2a6e3f", width=1)

        # Pin (πάνω από την πεδιάδα, στο μέσο)
        PX, PY = 100, 135   # κορυφή pin
        # Σώμα pin (δάκρυ)
        c.create_oval(PX-14, PY, PX+14, PY+28, fill="#e8f5e9", outline="#c8e6c9", width=1)
        c.create_polygon(
            PX-8, PY+22,  PX, PY+44,  PX+8, PY+22,
            fill="#e8f5e9", outline=""
        )
        # Κέντρο pin
        c.create_oval(PX-6, PY+6, PX+6, PY+18, fill="#2a6e3f", outline="")
        c.create_oval(PX-2, PY+10, PX+2, PY+14, fill="#e8f5e9", outline="")
        # Σκιά
        c.create_oval(PX-10, 178, PX+10, 184, fill="#0f2d1a", outline="")

        # Λεπτή κάθετη διαχωριστική γραμμή
        c.create_line(LW, 20, LW, H-20, fill="#2a6e3f", width=1)

        # ════════════════════════════════════════════════════════
        # ΔΕΞΙ ΤΜΗΜΑ — Κείμενο  (210..W)
        # ════════════════════════════════════════════════════════
        TX = 218   # αρχή κειμένου

        # ── Όνομα εφαρμογής — EGSA (μεγάλο) + Suite (μικρότερο, πράσινο) ──
        c.create_text(TX, 48, text="EGSA",
                      font=("Georgia", 32, "bold"),
                      fill="#e8f5e9", anchor="w")
        c.create_text(TX, 82, text="Suite",
                      font=("Georgia", 26),
                      fill="#2a6e3f", anchor="w")

        # Οριζόντια γραμμή
        c.create_rectangle(TX, 94, W-18, 96, fill="#2a6e3f", outline="")

        # ── Tagline ──
        c.create_text(TX, 112, text="COORDINATE TRANSFORMATION SUITE",
                      font=("Segoe UI", 8),
                      fill="#4a8a5f", anchor="w", )

        # ── Pills: HATT → ΕΓΣΑ'87 → WGS84 ──
        def pill(x, y, w, h, text, r=10):
            c.create_rectangle(x, y, x+w, y+h, fill="#1a4a2e", outline="#2a6e3f", width=1)
            c.create_text(x+w//2, y+h//2+1, text=text,
                          font=("Courier New", 9, "bold"), fill="#8fbc8f")

        def arrow_lbl(x, y):
            c.create_text(x, y, text="→", font=("Segoe UI", 13),
                          fill="#2a6e3f", anchor="w")

        pill(TX,     126, 62, 22, "HATT")
        arrow_lbl(TX+68, 137)
        pill(TX+84,  126, 82, 22, "ΕΓΣΑ '87")
        arrow_lbl(TX+172, 137)
        pill(TX+188, 126, 72, 22, "WGS84")

        # ── Google Earth badge ──
        GE_X, GE_Y = TX, 160
        c.create_rectangle(GE_X, GE_Y, GE_X+148, GE_Y+24,
                           fill="#0f2d1a", outline="#2a6e3f", width=1)

        # Mini GE globe (κύκλοι)
        GX, GY = GE_X+14, GE_Y+12
        c.create_oval(GX-8, GY-8, GX+8, GY+8, fill="#1a6e3f", outline="#4aae7f", width=1)
        c.create_oval(GX-3, GY-3, GX+3, GY+3, fill="#4aae7f", outline="")
        c.create_line(GX, GY-8, GX, GY+8, fill="#4aae7f", width=1)
        c.create_line(GX-8, GY, GX+8, GY, fill="#4aae7f", width=1)

        c.create_text(GE_X+30, GE_Y+12, text="Google Earth",
                      font=("Segoe UI", 10), fill="#8fbc8f", anchor="w")

        # KML live badge
        KL_X = GE_X + 156
        c.create_rectangle(KL_X, GE_Y, KL_X+64, GE_Y+24,
                           fill="#0f2d1a", outline="#2a6e3f", width=1)
        c.create_text(KL_X+32, GE_Y+12, text="KML live",
                      font=("Courier New", 9), fill="#4a7a5f")

        # ── Separator ──
        c.create_line(TX, 196, W-18, 196, fill="#2a6e3f", width=1)

        # ── Loading label ──
        loading_var = tk.StringVar(value="Φόρτωση βιβλιοθηκών...")
        loading_lbl = tk.Label(splash, textvariable=loading_var,
                               bg="#0f2d1a", fg="#8fbc8f",
                               font=("Segoe UI", 9))
        loading_lbl.place(x=TX + (W - TX)//2 + TX//2, y=210, anchor="center")

        # ── Progress bar ──
        BAR_X, BAR_Y = TX, 226
        BAR_W, BAR_H  = W - TX - 18, 7
        c.create_rectangle(BAR_X, BAR_Y, BAR_X+BAR_W, BAR_Y+BAR_H,
                           fill="#1a4a2e", outline="")
        progress_bar = c.create_rectangle(BAR_X, BAR_Y, BAR_X, BAR_Y+BAR_H,
                                          fill="#8fbc8f", outline="")

        # ── Version ──
        c.create_text(TX, 248, text="v5.4.0-beta.3  ·  390 εγγραφές HATT  ·  2026",
                      font=("Segoe UI", 8), fill="#2a6e3f", anchor="w")

        splash.update()

        splash._canvas       = c
        splash._progress_bar = progress_bar
        splash._loading_var  = loading_var
        splash._bar_x        = BAR_X
        splash._bar_y        = BAR_Y
        splash._bar_w        = BAR_W
        splash._bar_h        = BAR_H
        splash._root_hidden  = root_hidden

        return splash
    except Exception:
        return None


def _update_splash(splash, message: str, progress: float) -> None:
    """Ενημερώνει το μήνυμα και την progress bar (progress: 0.0–1.0)."""
    if splash is None:
        return
    try:
        splash._loading_var.set(message)
        x2 = splash._bar_x + int(splash._bar_w * min(progress, 1.0))
        splash._canvas.coords(
            splash._progress_bar,
            splash._bar_x, splash._bar_y,
            x2, splash._bar_y + splash._bar_h
        )
        splash.update()
    except Exception:
        pass


def _close_splash(splash) -> None:
    """Κλείνει το splash window."""
    if splash is None:
        return
    try:
        splash.destroy()
        splash._root_hidden.destroy()
    except Exception:
        pass


# Εμφάνιση splash ΑΜΕΣΩΣ
_splash = None if os.environ.get("EGSA_SUITE_NO_SPLASH") == "1" else _show_splash()
_update_splash(_splash, "Φόρτωση βιβλιοθηκών...", 0.05)
# ─────────────────────────────────────────────────────────────────────────────

from tkinter import filedialog, messagebox, ttk
_update_splash(_splash, "Φόρτωση decimal, shapefile...", 0.15)
from decimal import Decimal, getcontext, ROUND_HALF_UP, InvalidOperation
import shapefile
try:
    import ezdxf
    from ezdxf import units as dxf_units
    DXF_AVAILABLE = True
except ImportError:
    DXF_AVAILABLE = False
import string
import re
import codecs
import json
_update_splash(_splash, "Φόρτωση matplotlib...", 0.30)
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
import math
_update_splash(_splash, "Φόρτωση folium...", 0.45)
import folium
import tempfile
import webbrowser
import atexit
import logging
import traceback
from typing import List, Tuple, Optional
from dataclasses import dataclass
_update_splash(_splash, "Φόρτωση pyproj...", 0.60)
from pyproj import Transformer, CRS
from wgs84_utils import WGS84Point, dms_components_to_decimal, format_wgs84_dms, parse_wgs84_points
import tempfile as _tempfile

_update_splash(_splash, "Φόρτωση Google Earth modules...", 0.75)

# ── PyInstaller path fix ──────────────────────────────────────────────────────
if getattr(sys, 'frozen', False):
    _BASE_DIR = Path(sys._MEIPASS)
else:
    _BASE_DIR = Path(__file__).resolve().parent

if str(_BASE_DIR) not in sys.path:
    sys.path.insert(0, str(_BASE_DIR))

ICON_PATH = _BASE_DIR / "assets" / "egsa_suite.ico"
# ─────────────────────────────────────────────────────────────────────────────

# Google Earth integration
try:
    from services.google_earth_service import GoogleEarthService
    from utils.platform_utils import is_google_earth_installed
    GE_AVAILABLE = True
except ImportError:
    GE_AVAILABLE = False

_update_splash(_splash, "Αρχικοποίηση εφαρμογής...", 0.90)

# Φάκελος εργασίας για GE (στο temp)
_GE_WORK_DIR = Path(_tempfile.gettempdir()) / "egsa_suite_ge"

# ==================== CONFIGURATION ====================

getcontext().prec = 34
APP_VERSION = "5.4.0-beta.3"
DISPLAY_DEC = Decimal("0.01")

# ── Χρωματική παλέτα ─────────────────────────────────────────────────────────
C = {
    "bg":          "#f7f8fa",
    "green_dark":  "#1a4a2e",
    "green_mid":   "#2a6e3f",
    "green_light": "#eaf4ec",
    "blue_btn":    "#1565c0",
    "text":        "#1a1a1a",
    "text_mid":    "#555555",
    "text_dim":    "#999999",
    "border":      "#d0d7de",
    "output_bg":   "#f6f8fa",
    "input_bg":    "#ffffff",
    "white":       "#ffffff",
    "header_fg":   "#e8f5e9",
    "accent":      "#d4edda",
}

def setup_styles(root):
    style = ttk.Style(root)
    style.theme_use("clam")
    style.configure("Modern.TCombobox",
        fieldbackground=C["input_bg"], background=C["white"],
        foreground=C["text"], bordercolor=C["border"],
        arrowcolor=C["green_mid"], padding=(4, 3),
    )
    style.map("Modern.TCombobox",
        fieldbackground=[("readonly", C["input_bg"])],
        bordercolor=[("focus", C["green_mid"])],
    )
# ─────────────────────────────────────────────────────────────────────────────

# Φόρτωση συντελεστών HATT→ΕΓΣΑ87 για όλη την Ελλάδα (390 εγγραφές μετασχηματισμού)
try:
    from hatt_coefficients import HATT_COEFFICIENTS
except ImportError:
    HATT_COEFFICIENTS = {}

# Προεπιλεγμένη περιοχή
DEFAULT_REGION = "ΚΑΤΕΡΙΝΗ"

# Η επίσημη έκδοση ΟΚΧΕ/ΓΥΣ/ΕΜΠ περιέχει αυτή την εγγραφή με τις ίδιες ασυνήθιστες
# σταθερές. Δεν επινοούμε διόρθωση χωρίς authoritative corrigendum/control data.
UNVERIFIED_HATT_REGIONS = {
    "ΝΗΣΟΣ ΜΕΓΙΣΤΗ(ΚΑΣΤΕΛΛΟΡΙΖΟ)": (
        "Οι συντελεστές της συγκεκριμένης εγγραφής επιβεβαιώνονται στην επίσημη έκδοση "
        "ΟΚΧΕ/ΓΥΣ/ΕΜΠ, αλλά παρουσιάζουν σημαντική γεωγραφική ασυνέπεια σε σχέση με το "
        "δηλωμένο κέντρο του φύλλου. Δεν γίνεται αυθαίρετη διόρθωση. Για επαγγελματική ή "
        "διοικητική χρήση απαιτείται ανεξάρτητη επαλήθευση με κατάλληλα επίσημα/γνωστά δεδομένα."
    )
}

def _region_to_decimal_coeffs(region_name: str) -> dict:
    """Μετατρέπει τους float συντελεστές μιας περιοχής σε Decimal."""
    d = HATT_COEFFICIENTS.get(region_name)
    if d is None:
        raise KeyError(f"Άγνωστη περιοχή: {region_name}")
    A, B = d['A'], d['B']
    return {
        'X': {
            'constant': Decimal(str(A[0])),
            'x':        Decimal(str(A[1])),
            'y':        Decimal(str(A[2])),
            'x2':       Decimal(str(A[3])),
            'y2':       Decimal(str(A[4])),
            'xy':       Decimal(str(A[5])),
        },
        'Y': {
            'constant': Decimal(str(B[0])),
            'x':        Decimal(str(B[1])),
            'y':        Decimal(str(B[2])),
            'x2':       Decimal(str(B[3])),
            'y2':       Decimal(str(B[4])),
            'xy':       Decimal(str(B[5])),
        }
    }

# Συντελεστές μετασχηματισμού HATT → EGSA87 (Πιερία / Κατερίνη — προεπιλογή)
TRANSFORM_COEFFICIENTS = _region_to_decimal_coeffs(DEFAULT_REGION) if HATT_COEFFICIENTS else {
    'X': {
        'constant': Decimal("369585.94"),
        'x':  Decimal("0.9996775"),  'y':  Decimal("0.0173122"),
        'x2': Decimal("-1.04E-9"),   'y2': Decimal("1.81E-9"),
        'xy': Decimal("-3.60E-10")
    },
    'Y': {
        'constant': Decimal("4456429.27"),
        'x':  Decimal("-0.0173071"), 'y':  Decimal("0.9996669"),
        'x2': Decimal("1.00E-10"),   'y2': Decimal("2.30E-10"),
        'xy': Decimal("-3.03E-9")
    }
}

# Μηνύματα
MESSAGES = {
    'error_min_points': 'Απαιτούνται τουλάχιστον 3 σημεία.',
    'error_title': 'Λάθος',
    'success_export': 'Το πολύγωνο αποθηκεύτηκε σε EGSA87.',
    'success_title': 'OK'
}

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# ==================== USER SETTINGS ====================

def get_settings_path() -> Path:
    """Επιστρέφει το per-user αρχείο ρυθμίσεων χωρίς να γράφει δίπλα στο EXE."""
    override = os.environ.get("EGSA_SUITE_SETTINGS_DIR")
    if override:
        base = Path(override)
    elif sys.platform == "win32":
        local_app_data = os.environ.get("LOCALAPPDATA")
        base = Path(local_app_data) if local_app_data else (Path.home() / "AppData" / "Local")
        base = base / "EGSA Suite"
    else:
        base = Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config")) / "egsa-suite"
    return base / "settings.json"


def load_user_settings(path: Optional[Path] = None) -> dict:
    """Φορτώνει ρυθμίσεις χρήστη. Κατεστραμμένο/ανύπαρκτο αρχείο αγνοείται με ασφάλεια."""
    settings_path = Path(path) if path is not None else get_settings_path()
    try:
        if not settings_path.exists():
            return {}
        data = json.loads(settings_path.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {}
    except Exception as exc:
        logger.warning("Could not load user settings from %s: %s", settings_path, exc)
        return {}


def save_user_settings(settings: dict, path: Optional[Path] = None) -> Path:
    """Αποθηκεύει atomically τις ρυθμίσεις χρήστη και επιστρέφει το path."""
    settings_path = Path(path) if path is not None else get_settings_path()
    settings_path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = settings_path.with_suffix(settings_path.suffix + ".tmp")
    tmp_path.write_text(
        json.dumps(settings, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    tmp_path.replace(settings_path)
    return settings_path


def configured_default_region(settings: Optional[dict] = None) -> str:
    """Επιστρέφει έγκυρη αποθηκευμένη περιοχή ή την ασφαλή ενσωματωμένη προεπιλογή."""
    data = settings if settings is not None else load_user_settings()
    region = data.get("default_hatt_region") if isinstance(data, dict) else None
    if region in HATT_COEFFICIENTS:
        return region
    return DEFAULT_REGION


# Temporary files cleanup
temp_files = []

def cleanup_temp_files():
    """Διαγραφή προσωρινών αρχείων κατά το κλείσιμο."""
    for f in temp_files:
        try:
            if os.path.exists(f):
                os.unlink(f)
                logger.info(f"Deleted temp file: {f}")
        except Exception as e:
            logger.warning(f"Failed to delete {f}: {e}")

atexit.register(cleanup_temp_files)

# ==================== DATA STRUCTURES ====================

@dataclass
class Point:
    """Αναπαράσταση ενός σημείου με όνομα και συντεταγμένες."""
    name: str
    x: Decimal
    y: Decimal
    
    def to_float_tuple(self) -> Tuple[float, float]:
        """Μετατροπή σε float tuple για plotting."""
        return (float(self.x), float(self.y))

# ==================== CORE LOGIC CLASSES ====================

class CoordinateTransformer:
    """Χειρισμός μετατροπών συντεταγμένων."""

    def __init__(self):
        self.egsa_to_wgs = Transformer.from_crs("EPSG:2100", "EPSG:4326", always_xy=True)
        self.wgs_to_egsa = Transformer.from_crs("EPSG:4326", "EPSG:2100", always_xy=True)
        self._coeffs = TRANSFORM_COEFFICIENTS  # τρέχοντες συντελεστές

    def set_region(self, region_name: str) -> None:
        """Αλλαγή περιοχής HATT — φορτώνει τους αντίστοιχους συντελεστές."""
        self._coeffs = _region_to_decimal_coeffs(region_name)
        logger.info(f"Region set to: {region_name}")

    def HATT_to_egsa(self, x: Decimal, y: Decimal) -> Tuple[Decimal, Decimal]:
        """
        Μετατροπή από HATT σε EGSA87 με πολυωνυμικό μετασχηματισμό 2ου βαθμού.
        Χρησιμοποιεί τους συντελεστές της τρέχουσας περιοχής.
        """
        c = self._coeffs

        X = (c['X']['constant'] +
             c['X']['x']  * x +
             c['X']['y']  * y +
             c['X']['x2'] * x * x +
             c['X']['y2'] * y * y +
             c['X']['xy'] * x * y)

        Y = (c['Y']['constant'] +
             c['Y']['x']  * x +
             c['Y']['y']  * y +
             c['Y']['x2'] * x * x +
             c['Y']['y2'] * y * y +
             c['Y']['xy'] * x * y)

        return X, Y

    def egsa_to_wgs84(self, x: Decimal, y: Decimal) -> Tuple[float, float]:
        """Μετατροπή από EGSA87 σε WGS84 (longitude, latitude)."""
        lon, lat = self.egsa_to_wgs.transform(float(x), float(y))
        return lon, lat

    def wgs84_to_egsa(self, longitude: float, latitude: float) -> Tuple[Decimal, Decimal]:
        """Μετατροπή από WGS84 σε EGSA87."""
        x, y = self.wgs_to_egsa.transform(float(longitude), float(latitude))
        return Decimal(str(x)), Decimal(str(y))


class PolygonCalculator:
    """Υπολογισμοί γεωμετρίας πολυγώνων."""
    
    @staticmethod
    def calculate_area(points: List[Point]) -> Decimal:
        """
        Υπολογισμός εμβαδού πολυγώνου με τον τύπο Shoelace.
        
        Args:
            points: Λίστα σημείων του πολυγώνου
            
        Returns:
            Εμβαδόν σε τετραγωνικά μέτρα
        """
        if len(points) < 3:
            return Decimal("0")
        
        # Κλείσιμο πολυγώνου
        closed_points = points + [points[0]]
        
        area = Decimal("0")
        for i in range(len(closed_points) - 1):
            x1, y1 = closed_points[i].x, closed_points[i].y
            x2, y2 = closed_points[i + 1].x, closed_points[i + 1].y
            area += x1 * y2 - x2 * y1
        
        return abs(area) / 2
    
    @staticmethod
    def calculate_distance(p1: Point, p2: Point) -> Decimal:
        """Υπολογισμός Ευκλείδειας απόστασης μεταξύ δύο σημείων."""
        dx = float(p2.x - p1.x)
        dy = float(p2.y - p1.y)
        return Decimal(str(math.sqrt(dx * dx + dy * dy)))

    @staticmethod
    def _orientation(a: Point, b: Point, c: Point) -> Decimal:
        """Προσανατολισμός τριάδας σημείων (θετικό/αρνητικό/μηδέν)."""
        return (b.x - a.x) * (c.y - a.y) - (b.y - a.y) * (c.x - a.x)

    @staticmethod
    def _on_segment(a: Point, b: Point, c: Point) -> bool:
        """True όταν το c βρίσκεται πάνω στο κλειστό τμήμα a-b."""
        return (min(a.x, b.x) <= c.x <= max(a.x, b.x) and
                min(a.y, b.y) <= c.y <= max(a.y, b.y))

    @classmethod
    def _segments_intersect(cls, a: Point, b: Point, c: Point, d: Point) -> bool:
        o1 = cls._orientation(a, b, c)
        o2 = cls._orientation(a, b, d)
        o3 = cls._orientation(c, d, a)
        o4 = cls._orientation(c, d, b)

        if ((o1 > 0 and o2 < 0) or (o1 < 0 and o2 > 0)) and \
           ((o3 > 0 and o4 < 0) or (o3 < 0 and o4 > 0)):
            return True
        if o1 == 0 and cls._on_segment(a, b, c): return True
        if o2 == 0 and cls._on_segment(a, b, d): return True
        if o3 == 0 and cls._on_segment(c, d, a): return True
        if o4 == 0 and cls._on_segment(c, d, b): return True
        return False

    @classmethod
    def self_intersection_pairs(cls, points: List[Point]) -> List[Tuple[int, int]]:
        """
        Επιστρέφει ζεύγη ακμών που τέμνονται σε κλειστό πολύγωνο.
        Οι γειτονικές ακμές εξαιρούνται, επειδή μοιράζονται νόμιμα μία κορυφή.
        """
        n = len(points)
        if n < 4:
            return []
        intersections = []
        for i in range(n):
            a, b = points[i], points[(i + 1) % n]
            for j in range(i + 1, n):
                if j == i or j == (i + 1) % n or i == (j + 1) % n:
                    continue
                # πρώτη και τελευταία ακμή είναι επίσης γειτονικές
                if i == 0 and j == n - 1:
                    continue
                c, d = points[j], points[(j + 1) % n]
                if cls._segments_intersect(a, b, c, d):
                    intersections.append((i, j))
        return intersections

    @classmethod
    def has_self_intersections(cls, points: List[Point]) -> bool:
        return bool(cls.self_intersection_pairs(points))


class InputParser:
    """Ανάλυση εισόδου χρήστη."""
    
    @staticmethod
    def parse_decimal(s: str) -> Decimal:
        """
        Μετατροπή string σε Decimal με υποστήριξη διαφόρων μορφών.
        
        Args:
            s: String προς μετατροπή
            
        Returns:
            Decimal αριθμός
            
        Raises:
            InvalidOperation: Αν το string δεν είναι έγκυρος αριθμός
        """
        s = s.strip()
        
        # Χειρισμός μικτής χρήσης . και ,
        if ',' in s and '.' in s:
            if s.rfind(',') > s.rfind('.'):
                s = s.replace('.', '').replace(',', '.')
            else:
                s = s.replace(',', '')
        else:
            s = s.replace(',', '.')
        
        return Decimal(s)
    
    @staticmethod
    def smart_split(line: str) -> List[str]:
        """
        Έξυπνο split με δοκιμή διαφόρων διαχωριστών.
        
        Args:
            line: Γραμμή προς ανάλυση
            
        Returns:
            Λίστα με τα μέρη της γραμμής
        """
        for delim in ["\t", ";", " ", ","]:
            if delim in line:
                parts = [p for p in line.split(delim) if p.strip()]
                if len(parts) >= 2:
                    return parts
        return line.split()
    
    @staticmethod
    def parse_points(text: str, auto_names: bool = True) -> Tuple[List[Point], List[str]]:
        """
        Ανάλυση κειμένου σε λίστα σημείων.
        
        Args:
            text: Κείμενο με σημεία (μία γραμμή ανά σημείο)
            auto_names: Αν True, δημιουργεί αυτόματα ονόματα (A, B, C...)
            
        Returns:
            Tuple με (λίστα Points, λίστα errors)
        """
        lines = text.splitlines()
        points = []
        errors = []
        auto_letters = list(string.ascii_uppercase)
        auto_index = 0
        
        for line_num, line in enumerate(lines, 1):
            parts = InputParser.smart_split(line)
            if not parts:
                continue
            
            try:
                # Προσδιορισμός ονόματος και συντεταγμένων
                if len(parts) >= 3:
                    name, x_str, y_str = parts[0], parts[1], parts[2]
                elif len(parts) == 2:
                    x_str, y_str = parts[0], parts[1]
                    if auto_names:
                        name = (auto_letters[auto_index] 
                               if auto_index < len(auto_letters) 
                               else f"A{auto_index}")
                        auto_index += 1
                    else:
                        name = f"P{line_num}"
                else:
                    errors.append(f"Γραμμή {line_num}: Ανεπαρκή δεδομένα")
                    continue
                
                # Μετατροπή συντεταγμένων
                x = InputParser.parse_decimal(x_str)
                y = InputParser.parse_decimal(y_str)
                
                points.append(Point(name=name, x=x, y=y))
                
            except (ValueError, InvalidOperation) as e:
                errors.append(f"Γραμμή {line_num}: Μη έγκυρες συντεταγμένες ({e})")
                logger.warning(f"Parse error at line {line_num}: {e}")
                continue
        
        return points, errors


class ShapefileExporter:
    """Ασφαλής εξαγωγή POINT / POLYLINE / POLYGON σε ΕΓΣΑ87 (EPSG:2100)."""

    PRJ_EPSG_2100 = (
        'PROJCS["GGRS87 / Greek Grid",GEOGCS["GGRS87",'
        'DATUM["Greek_Geodetic_Reference_System-1987",'
        'SPHEROID["GRS_1980",6378137,298.257222101]],'
        'PRIMEM["Greenwich",0],UNIT["degree",0.0174532925199433]],'
        'PROJECTION["Transverse_Mercator"],'
        'PARAMETER["latitude_of_origin",0],'
        'PARAMETER["central_meridian",24],'
        'PARAMETER["scale_factor",0.9996],'
        'PARAMETER["false_easting",500000],'
        'PARAMETER["false_northing",0],UNIT["metre",1]]'
    )

    @staticmethod
    def _validate(points: List[Point]) -> None:
        if not points:
            raise ValueError("Δεν υπάρχουν σημεία για εξαγωγή.")
        coords = [(float(p.x), float(p.y)) for p in points]
        if len(set(coords)) != len(coords):
            raise ValueError("Υπάρχουν διπλότυπες κορυφές. Αφαιρέστε τις πριν την εξαγωγή.")
        for x, y in coords:
            if not (100000 <= x <= 900000 and 3800000 <= y <= 4700000):
                raise ValueError(f"Η συντεταγμένη ({x:.3f}, {y:.3f}) είναι εκτός αναμενόμενων ορίων ΕΓΣΑ87 Ελλάδας.")
        if len(points) >= 3 and PolygonCalculator.has_self_intersections(points):
            raise ValueError(
                "Το πολύγωνο παρουσιάζει αυτοτομή. Ελέγξτε τη σειρά των κορυφών πριν την εξαγωγή."
            )

    @classmethod
    def export_geometry(cls, points: List[Point], filepath: str) -> str:
        cls._validate(points)
        coords = [(float(p.x), float(p.y)) for p in points]
        n = len(coords)

        if n == 1:
            geometry_name = "POINT"
            w = shapefile.Writer(filepath, shapefile.POINT, encoding="utf-8")
        elif n == 2:
            geometry_name = "POLYLINE"
            w = shapefile.Writer(filepath, shapefile.POLYLINE, encoding="utf-8")
        else:
            area = PolygonCalculator.calculate_area(points)
            if area == 0:
                raise ValueError("Το πολύγωνο έχει μηδενικό εμβαδόν.")
            geometry_name = "POLYGON"
            w = shapefile.Writer(filepath, shapefile.POLYGON, encoding="utf-8")

        try:
            w.field("ID", "N", decimal=0)
            w.field("NAME", "C", size=80)
            if n == 1:
                w.point(*coords[0]); w.record(1, points[0].name)
            elif n == 2:
                w.line([coords]); w.record(1, "Γραμμή ΕΓΣΑ87")
            else:
                ring = coords + [coords[0]]
                w.poly([ring]); w.record(1, "Πολύγωνο ΕΓΣΑ87")
        finally:
            w.close()

        base = str(Path(filepath).with_suffix(""))
        Path(base + ".prj").write_text(cls.PRJ_EPSG_2100, encoding="utf-8")
        Path(base + ".cpg").write_text("UTF-8", encoding="utf-8")
        logger.info("Shapefile %s exported: %s", geometry_name, filepath)
        return geometry_name


def is_epsg2100_prj(prj_text: str) -> bool:
    """Αναγνώριση .prj ως GGRS87 / Greek Grid (EPSG:2100) μέσω pyproj."""
    try:
        source = CRS.from_wkt(prj_text)
    except Exception:
        try:
            source = CRS.from_user_input(prj_text)
        except Exception:
            return False
    target = CRS.from_epsg(2100)
    try:
        epsg = source.to_epsg(min_confidence=70)
    except TypeError:
        epsg = source.to_epsg()
    if epsg == 2100:
        return True
    try:
        return source.equals(target, ignore_axis_order=True)
    except TypeError:
        return source.equals(target)


def format_hatt_angle(value) -> str:
    """
    Τα phi0/lam0 του dataset είναι κωδικοποιημένα ως μοίρες.λεπτά
    (π.χ. 40.15 = 40°15′), όχι ως δεκαδικές μοίρες.
    """
    if value is None:
        return "—"
    sign = "−" if float(value) < 0 else ""
    v = abs(float(value))
    degrees = int(v)
    minutes = int(round((v - degrees) * 100))
    if minutes >= 60:
        degrees += minutes // 60
        minutes %= 60
    return f"{sign}{degrees}°{minutes:02d}′"


def safe_point_name(value, fallback: str = "P") -> str:
    """Μετατρέπει external labels σε ένα token συμβατό με το input format της εφαρμογής."""
    text = str(value or "").strip()
    if not text:
        return fallback
    text = re.sub(r"[\s,;]+", "_", text)
    return text.strip("_") or fallback


def shapefile_text_encoding(shp_path: str) -> str:
    """Διαβάζει το .cpg όταν υπάρχει και επιστρέφει Python codec για το DBF."""
    cpg = Path(shp_path).with_suffix(".cpg")
    if not cpg.exists():
        return "utf-8"
    raw = cpg.read_text(encoding="ascii", errors="ignore").strip().strip('"').strip("'")
    key = re.sub(r"[^A-Z0-9]", "", raw.upper())
    aliases = {
        "UTF8": "utf-8",
        "65001": "utf-8",
        "1253": "cp1253",
        "CP1253": "cp1253",
        "WINDOWS1253": "cp1253",
        "ISO88597": "iso8859_7",
        "ISOIR126": "iso8859_7",
    }
    candidate = aliases.get(key, raw or "utf-8")
    try:
        codecs.lookup(candidate)
        return candidate
    except LookupError:
        logger.warning("Unknown Shapefile CPG encoding %r; falling back to UTF-8", raw)
        return "utf-8"


def extract_shapefile_candidates(reader) -> list:
    """
    Μετατρέπει κάθε feature/part ενός pyshp Reader σε ανεξάρτητο candidate.
    Έτσι multipart και multi-feature δεδομένα δεν συγχωνεύονται σιωπηρά.
    """
    field_names = [f[0].upper() for f in reader.fields[1:]]
    name_field = next(
        (i for i, f in enumerate(field_names)
         if f in ('NAME', 'ONOMA', 'LABEL', 'ID', 'DESCR', 'ΠΕΡΙΓΡΑΦΗ')),
        None
    )
    point_types = {1, 11, 21}
    polyline_types = {3, 13, 23}
    polygon_types = {5, 15, 25}
    candidates = []

    for feature_idx, sr in enumerate(reader.shapeRecords(), 1):
        geom = sr.shape
        rec = sr.record
        raw = rec[name_field] if name_field is not None else None
        feature_name = str(raw).strip() if raw not in (None, "") else f"Feature {feature_idx}"
        st = geom.shapeType

        if st in point_types:
            if geom.points:
                candidates.append({
                    "geometry_type": "POINT",
                    "feature_index": feature_idx,
                    "part_index": 1,
                    "feature_name": feature_name,
                    "points": [geom.points[0]],
                    "closed": False,
                })
            continue

        if st not in polyline_types and st not in polygon_types:
            continue

        starts = list(geom.parts) or [0]
        ends = starts[1:] + [len(geom.points)]
        for part_idx, (part_start, part_end) in enumerate(zip(starts, ends), 1):
            pts = list(geom.points[part_start:part_end])
            closed = st in polygon_types
            if len(pts) > 1 and pts[0] == pts[-1]:
                pts = pts[:-1]
                closed = True
            if pts:
                candidates.append({
                    "geometry_type": "POLYGON" if st in polygon_types else "POLYLINE",
                    "feature_index": feature_idx,
                    "part_index": part_idx,
                    "feature_name": feature_name,
                    "points": pts,
                    "closed": closed,
                })
    return candidates


def export_dxf_file(points: List[Point], dxf_path: str, *, include_points: bool = False, include_labels: bool = False) -> dict:
    """
    Εξάγει ΕΓΣΑ87 γεωμετρία σε DXF. Η polyline δημιουργείται πάντα, ενώ POINT/TEXT
    entities προστίθενται μόνο όταν ζητηθούν ρητά από τον χρήστη.
    """
    if not DXF_AVAILABLE:
        raise RuntimeError("Η βιβλιοθήκη ezdxf δεν είναι διαθέσιμη σε αυτή την εγκατάσταση.")
    if len(points) < 2:
        raise ValueError("Για DXF απαιτούνται τουλάχιστον δύο σημεία ώστε να δημιουργηθεί γραμμή.")

    doc = ezdxf.new('R2010')
    doc.units = dxf_units.M
    msp = doc.modelspace()

    layers = ["EGSA_BOUNDARY"]
    doc.layers.add('EGSA_BOUNDARY', color=1)
    if include_points:
        doc.layers.add('EGSA_POINTS', color=5)
        layers.append("EGSA_POINTS")
    if include_labels:
        doc.layers.add('EGSA_LABELS', color=3)
        layers.append("EGSA_LABELS")

    pts = [(float(p.x), float(p.y)) for p in points]
    msp.add_lwpolyline(
        pts,
        close=(len(pts) >= 3),
        dxfattribs={'layer': 'EGSA_BOUNDARY'}
    )

    xs = [xy[0] for xy in pts]
    ys = [xy[1] for xy in pts]
    span = max(max(xs) - min(xs), max(ys) - min(ys))
    txt_h = max(0.5, min(span * 0.015, 5.0)) if span else 1.0

    for point, (x, y) in zip(points, pts):
        if include_points:
            msp.add_point((x, y), dxfattribs={'layer': 'EGSA_POINTS'})
        if include_labels:
            msp.add_text(point.name, dxfattribs={
                'layer': 'EGSA_LABELS',
                'height': txt_h,
                'insert': (x + txt_h * 0.5, y + txt_h * 0.5),
            })

    doc.saveas(dxf_path)
    return {
        "geometry": "κλειστή polyline" if len(pts) >= 3 else "ανοικτή polyline",
        "layers": layers,
        "vertex_count": len(pts),
    }


# ==================== UTILITY FUNCTIONS ====================

def format_display(d: Decimal) -> str:
    """
    Μορφοποίηση Decimal για εμφάνιση με ελληνικό κόμμα.
    
    Args:
        d: Decimal αριθμός
        
    Returns:
        Formatted string
    """
    return f"{d.quantize(DISPLAY_DEC, rounding=ROUND_HALF_UP):f}".replace(".", ",")


def add_context_menu(widget: tk.Text):
    """
    Προσθήκη context menu (δεξί click) σε Text widget.
    
    Args:
        widget: Το Text widget
    """
    menu = tk.Menu(widget, tearoff=0)
    menu.add_command(label="Copy", command=lambda: widget.event_generate("<<Copy>>"))
    menu.add_command(label="Paste", command=lambda: widget.event_generate("<<Paste>>"))
    menu.add_separator()
    menu.add_command(label="Select All", 
                    command=lambda: widget.tag_add("sel", "1.0", "end"))
    
    def popup(event):
        try:
            menu.tk_popup(event.x_root, event.y_root)
        finally:
            menu.grab_release()
    
    widget.bind("<Button-3>", popup)
    
    # Keyboard shortcuts
    def key_handler(event):
        if not (event.state & 0x4):  # Ctrl key
            return None
        if event.keycode == 86:  # V
            widget.event_generate("<<Paste>>")
            return "break"
        if event.keycode == 67:  # C
            widget.event_generate("<<Copy>>")
            return "break"
        if event.keycode == 65:  # A
            widget.tag_add("sel", "1.0", "end")
            return "break"
        return None
    
    widget.bind("<KeyPress>", key_handler)


# ==================== MAIN APPLICATION ====================

class HATTEgsaApp:
    """Κύρια εφαρμογή GUI."""
    
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("EGSA Suite")
        self.root.configure(bg=C["bg"])
        apply_window_icon(self.root)
        setup_styles(root)
        
        # Per-user settings (αποθηκεύονται στο AppData, όχι δίπλα στο portable EXE)
        self.user_settings = load_user_settings()
        self.default_region = configured_default_region(self.user_settings)

        # Core components
        self.transformer = CoordinateTransformer()
        if HATT_COEFFICIENTS:
            self.transformer.set_region(self.default_region)
        self.calculator = PolygonCalculator()
        self.parser = InputParser()
        self.exporter = ShapefileExporter()
        
        # Data storage
        self.HATT_points: List[Point] = []
        self.egsa_points: List[Point] = []
        self.wgs84_points: List[WGS84Point] = []
        
        # UI Variables — δεσμεύονται ρητά στο σωστό root
        self.mode_var = tk.StringVar(master=root, value="HATT")
        self.map_style_var = tk.StringVar(master=root, value="ESRI Satellite")
        self.wgs_direction_var = tk.StringVar(master=root, value="EGSA_TO_WGS")
        self.wgs_format_var = tk.StringVar(master=root, value="decimal")
        self.wgs_lat_hem_var = tk.StringVar(master=root, value="N")
        self.wgs_lon_hem_var = tk.StringVar(master=root, value="E")

        # Camera tracking vars — αρχικοποίηση εδώ ώστε να υπάρχουν πάντα
        self._ge_cam_x_var   = tk.StringVar(master=root, value="—")
        self._ge_cam_y_var   = tk.StringVar(master=root, value="—")
        self._ge_cam_lon_var = tk.StringVar(master=root, value="—")
        self._ge_cam_lat_var = tk.StringVar(master=root, value="—")
        
        # Google Earth Service
        self.ge_service: Optional[GoogleEarthService] = None
        self.ge_window: Optional[tk.Toplevel] = None
        if GE_AVAILABLE:
            try:
                self.ge_service = GoogleEarthService(_GE_WORK_DIR)
                self.ge_service.initialize()
                self.ge_service.set_camera_callback(self._on_ge_camera_update)
                logger.info("GoogleEarthService initialized")
            except Exception as e:
                logger.warning(f"GE service failed to start: {e}")
                self.ge_service = None

        # Shutdown GE service on app close
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

        # Build UI
        self._create_ui()

        logger.info("Application initialized")
    
    def _create_ui(self):
        """Δημιουργία UI components."""
        # Top frame με buttons
        self._create_top_frame()
        
        # Mode selection
        self._create_mode_selection()
        
        # HATT frame
        self.frame_HATT = self._create_HATT_frame()
        
        # EGSA frame
        self.frame_egsa = self._create_egsa_frame()

        # WGS84 frame
        self.frame_wgs84 = self._create_wgs84_frame()
        
        # Footer
        self._create_footer()
        
        # Initialize view
        self._switch_mode()
        self._stabilize_main_window_size()
        self.mode_var.trace_add("write", lambda *args: self._switch_mode())
    
    def _create_top_frame(self):
        """Δημιουργία top frame."""
        top = tk.Frame(self.root, bg=C["green_dark"])
        top.pack(fill="x")

        # Λογότυπο
        tk.Label(top, text="EGSA",
                 font=("Segoe UI", 14, "bold"),
                 bg=C["green_dark"], fg=C["header_fg"]).pack(side="left", padx=(14,0), pady=8)
        tk.Label(top, text=" Suite",
                 font=("Segoe UI", 14),
                 bg=C["green_dark"], fg=C["green_mid"]).pack(side="left", pady=8)

        # Always-on-top
        self.always_on_top_var = tk.BooleanVar(master=self.root, value=False)
        tk.Checkbutton(
            top, text="📌",
            variable=self.always_on_top_var,
            command=self._toggle_always_on_top,
            bg=C["green_dark"], fg=C["header_fg"],
            selectcolor=C["green_dark"],
            activebackground=C["green_dark"], activeforeground=C["header_fg"],
            font=("Segoe UI", 10), bd=0, relief="flat"
        ).pack(side="left", padx=8)

        # Right buttons — flat, λεπτά
        for txt, cmd in [("Οδηγίες", self._show_help), ("About", self._show_about)]:
            tk.Button(top, text=txt, command=cmd,
                      relief="flat", bd=0,
                      bg=C["green_mid"], fg=C["white"],
                      activebackground="#3a8e5f", activeforeground=C["white"],
                      font=("Segoe UI", 9), padx=12, pady=6,
                      cursor="hand2"
                      ).pack(side="right", padx=(0,6), pady=6)

    def _toggle_always_on_top(self):
        """Ενεργοποίηση/απενεργοποίηση 'Πάντα στην κορυφή' για το κύριο παράθυρο."""
        self.root.attributes("-topmost", self.always_on_top_var.get())

    def _create_mode_selection(self):
        """Επιλογή λειτουργίας ως διακριτές, καθαρές καρτέλες."""
        outer = tk.Frame(self.root, bg=C["bg"])
        outer.pack(fill="x", padx=12, pady=(10, 4))

        tk.Label(outer, text="ΛΕΙΤΟΥΡΓΙΑ",
                 font=("Segoe UI", 7, "bold"), fg=C["text_dim"],
                 bg=C["bg"]).pack(anchor="w")

        tab_row = tk.Frame(outer, bg=C["bg"])
        tab_row.pack(fill="x", pady=(4, 0))

        self._mode_buttons = {}
        for txt, val in [
            ("HATT → ΕΓΣΑ87", "HATT"),
            ("Πολύγωνο ΕΓΣΑ87", "egsa"),
            ("ΕΓΣΑ87 ↔ WGS84", "wgs84"),
        ]:
            btn = tk.Button(
                tab_row, text=txt,
                command=lambda v=val: self.mode_var.set(v),
                font=("Segoe UI", 9, "bold"),
                relief="flat", bd=0,
                bg=C["white"], fg=C["green_dark"],
                activebackground=C["green_light"], activeforeground=C["green_dark"],
                highlightthickness=1, highlightbackground=C["border"],
                padx=12, pady=7, cursor="hand2"
            )
            btn.pack(side="left", fill="x", expand=True, padx=(0, 6))
            self._mode_buttons[val] = btn

        # Λεπτή γραμμή separator
        sep = tk.Frame(self.root, bg=C["border"], height=1)
        sep.pack(fill="x", padx=12, pady=(6, 0))

    def _refresh_mode_tabs(self):
        """Οπτική ένδειξη της ενεργής κύριας καρτέλας."""
        selected = self.mode_var.get()
        for value, button in self._mode_buttons.items():
            if value == selected:
                button.config(
                    bg=C["green_dark"], fg=C["white"],
                    activebackground=C["green_mid"], activeforeground=C["white"],
                    highlightbackground=C["green_dark"]
                )
            else:
                button.config(
                    bg=C["white"], fg=C["green_dark"],
                    activebackground=C["green_light"], activeforeground=C["green_dark"],
                    highlightbackground=C["border"]
                )
    
    def _create_HATT_frame(self) -> tk.Frame:
        """Δημιουργία HATT mode frame."""
        frame = tk.Frame(self.root, bg=C["bg"])

        PAD = {"padx": 12}

        # ── Περιοχή HATT ─────────────────────────────────────────────────────
        region_outer = tk.Frame(frame, bg=C["bg"])
        region_outer.pack(fill="x", pady=(10, 4), **PAD)

        tk.Label(region_outer, text="ΦΥΛΛΟ ΧΑΡΤΗ HATT",
                 font=("Segoe UI", 7, "bold"), fg=C["text_dim"],
                 bg=C["bg"]).pack(anchor="w")

        region_row = tk.Frame(region_outer, bg=C["bg"])
        region_row.pack(fill="x", pady=(3, 0))

        # Στο dropdown εμφανίζεται μαζί ο αριθμός φύλλου και η περιοχή,
        # ενώ εσωτερικά διατηρούμε το πραγματικό όνομα-κλειδί του πίνακα.
        if HATT_COEFFICIENTS:
            self._region_display_to_name = {
                f"Φ. {HATT_COEFFICIENTS[name]['code']} — {name}": name
                for name in sorted(HATT_COEFFICIENTS.keys())
            }
        else:
            self._region_display_to_name = {DEFAULT_REGION: DEFAULT_REGION}

        self._region_name_to_display = {
            name: display for display, name in self._region_display_to_name.items()
        }
        default_region = self.default_region if self.default_region in self._region_name_to_display else DEFAULT_REGION
        default_display = self._region_name_to_display.get(default_region, default_region)

        self.region_var = tk.StringVar(master=self.root, value=default_display)
        self.region_combo = ttk.Combobox(
            region_row, textvariable=self.region_var,
            values=list(self._region_display_to_name.keys()),
            width=38, state="readonly",
            style="Modern.TCombobox"
        )
        self.region_combo.set(default_display)
        self.region_combo.pack(side="left", fill="x", expand=True)
        self.region_combo.bind("<<ComboboxSelected>>", self._on_region_changed)

        self.region_code_lbl = tk.Label(
            region_row,
            text=self._region_info_text(default_region),
            font=("Segoe UI", 8), fg=C["text_dim"], bg=C["bg"]
        )
        self.region_code_lbl.pack(side="left", padx=(10, 0))

        preference_row = tk.Frame(region_outer, bg=C["bg"])
        preference_row.pack(fill="x", pady=(4, 0))
        self.default_region_lbl = tk.Label(
            preference_row,
            text=f"Προεπιλογή: {default_display}",
            font=("Segoe UI", 7), fg=C["text_dim"], bg=C["bg"]
        )
        self.default_region_lbl.pack(side="left")
        tk.Button(
            preference_row,
            text="★ Ορισμός ως προεπιλογή",
            command=self._set_current_region_as_default,
            relief="flat", bd=0,
            bg=C["green_light"], fg=C["green_dark"],
            activebackground=C["accent"], activeforeground=C["green_dark"],
            font=("Segoe UI", 7), padx=8, pady=2, cursor="hand2"
        ).pack(side="right")

        # ── Separator ─────────────────────────────────────────────────────────
        tk.Frame(frame, bg=C["border"], height=1).pack(fill="x", padx=12, pady=(6, 0))

        # ── Input ─────────────────────────────────────────────────────────────
        inp_outer = tk.Frame(frame, bg=C["bg"])
        inp_outer.pack(fill="x", pady=(10, 4), **PAD)

        hdr = tk.Frame(inp_outer, bg=C["bg"])
        hdr.pack(fill="x")
        tk.Label(hdr, text="Σημεία εισόδου  ",
                 font=("Segoe UI", 9, "bold"), fg=C["text"],
                 bg=C["bg"]).pack(side="left")
        tk.Label(hdr, text="(Όνομα X Y)  ή  (X Y)  —  μία γραμμή ανά σημείο",
                 font=("Segoe UI", 8), fg=C["text_dim"],
                 bg=C["bg"]).pack(side="left")

        self.HATT_input = tk.Text(
            frame, width=48, height=6,
            font=("Consolas", 9),
            bg=C["input_bg"], fg=C["text"],
            relief="flat", bd=0,
            insertbackground=C["green_mid"],
            selectbackground=C["accent"],
            highlightthickness=1,
            highlightbackground=C["border"],
            highlightcolor=C["green_mid"],
            padx=8, pady=6
        )
        self.HATT_input.pack(fill="x", padx=12)
        add_context_menu(self.HATT_input)

        # Paste / Clear
        btn_row = tk.Frame(frame, bg=C["bg"])
        btn_row.pack(pady=(5, 0), **PAD)
        for txt, cmd in [
            ("📋  Επικόλληση", lambda: self._paste_to(self.HATT_input)),
            ("✕  Καθαρισμός", lambda: self.HATT_input.delete("1.0", tk.END)),
        ]:
            tk.Button(btn_row, text=txt, command=cmd,
                      font=("Segoe UI", 8), relief="flat", bd=0,
                      bg=C["bg"], fg=C["text_mid"],
                      activebackground=C["border"],
                      padx=10, pady=4, cursor="hand2"
                      ).pack(side="left", padx=(0, 6))

        # ── Calculate button ──────────────────────────────────────────────────
        tk.Frame(frame, bg=C["border"], height=1).pack(fill="x", padx=12, pady=(8, 0))

        calc_frame = tk.Frame(frame, bg=C["bg"])
        calc_frame.pack(fill="x", padx=12, pady=8)
        tk.Button(
            calc_frame, text="  ➜   Μετατροπή σε ΕΓΣΑ87  ",
            command=self._calculate_HATT,
            font=("Segoe UI", 10, "bold"),
            fg=C["white"], bg=C["blue_btn"],
            activebackground="#1976d2", activeforeground=C["white"],
            relief="flat", bd=0, pady=8, cursor="hand2"
        ).pack(fill="x")

        # ── Output ───────────────────────────────────────────────────────────
        out_hdr = tk.Frame(frame, bg=C["bg"])
        out_hdr.pack(fill="x", pady=(4, 2), **PAD)
        tk.Label(out_hdr, text="Αποτελέσματα σε ΕΓΣΑ87",
                 font=("Segoe UI", 9, "bold"), fg=C["text"],
                 bg=C["bg"]).pack(side="left")
        tk.Button(out_hdr, text="📄 Αντιγραφή",
                  font=("Segoe UI", 8), relief="flat", bd=0,
                  bg=C["bg"], fg=C["text_dim"],
                  activebackground=C["border"],
                  padx=8, pady=2, cursor="hand2",
                  command=lambda: self._copy_text_to_clipboard(self.HATT_output)
                  ).pack(side="right")

        self.HATT_output = tk.Text(
            frame, width=48, height=8,
            font=("Consolas", 9),
            bg=C["output_bg"], fg=C["text"],
            state="disabled", relief="flat", bd=0,
            highlightthickness=1,
            highlightbackground=C["border"],
            highlightcolor=C["border"],
            padx=8, pady=6
        )
        self.HATT_output.pack(fill="x", padx=12)
        add_context_menu(self.HATT_output)

        # Area labels
        self.lbl_HATT_area = tk.Label(frame, fg=C["green_mid"], bg=C["bg"],
                                       font=("Segoe UI", 8))
        self.lbl_egsa_area = tk.Label(frame, fg=C["green_mid"], bg=C["bg"],
                                       font=("Segoe UI", 8))
        self.lbl_diff      = tk.Label(frame, fg=C["text_mid"],  bg=C["bg"],
                                       font=("Segoe UI", 8))

        # ── Google Earth ──────────────────────────────────────────────────────
        if GE_AVAILABLE:
            ge_frame = tk.Frame(frame, bg=C["bg"])
            ge_frame.pack(fill="x", padx=12, pady=(10, 0))
            tk.Button(
                ge_frame, text="🌍  Άνοιγμα στο Google Earth",
                command=self._open_google_earth_window,
                font=("Segoe UI", 9, "bold"),
                fg=C["white"], bg=C["green_mid"],
                activebackground="#3a8e5f", activeforeground=C["white"],
                relief="flat", bd=0, pady=7, cursor="hand2"
            ).pack(fill="x")

        # ── Actions ───────────────────────────────────────────────────────────
        tk.Frame(frame, bg=C["border"], height=1).pack(fill="x", padx=12, pady=(12, 0))

        act_outer = tk.Frame(frame, bg=C["bg"])
        act_outer.pack(fill="x", padx=12, pady=(8, 10))

        tk.Label(act_outer, text="ΠΡΟΒΟΛΗ · ΕΙΣΑΓΩΓΗ · ΕΞΑΓΩΓΗ",
                 font=("Segoe UI", 7, "bold"), fg=C["text_dim"],
                 bg=C["bg"]).pack(anchor="w", pady=(0, 6))

        # Row 1: Χάρτης
        row1 = tk.Frame(act_outer, bg=C["bg"])
        row1.pack(fill="x", pady=(0, 4))
        tk.Button(row1, text="🗺  Προβολή σε Χάρτη",
                  command=self._preview_map,
                  font=("Segoe UI", 9), relief="flat", bd=0,
                  bg=C["green_light"], fg=C["green_dark"],
                  activebackground=C["accent"],
                  padx=10, pady=5, cursor="hand2"
                  ).pack(side="left", padx=(0, 6))
        style_box = ttk.Combobox(
            row1, textvariable=self.map_style_var,
            values=["OpenStreetMap", "ESRI Satellite", "Google Maps"],
            width=14, state="readonly", style="Modern.TCombobox"
        )
        style_box.set("ESRI Satellite")
        style_box.pack(side="left")

        # Row 2: Προβολή γεωμετρίας
        row2 = tk.Frame(act_outer, bg=C["bg"])
        row2.pack(fill="x", pady=(0, 4))
        tk.Button(row2, text="📐  Σχήμα & Εμβαδό",
                  command=self._preview_polygon,
                  font=("Segoe UI", 8), relief="flat", bd=0,
                  bg=C["green_light"], fg=C["green_dark"],
                  activebackground=C["accent"],
                  padx=8, pady=5, cursor="hand2"
                  ).pack(side="left")

        # Row 3: Εισαγωγή — κοντά μεταξύ τους και χωριστά από τις εξαγωγές
        row3 = tk.Frame(act_outer, bg=C["bg"])
        row3.pack(fill="x", pady=(2, 4))
        tk.Label(row3, text="Εισαγωγή:", font=("Segoe UI", 8),
                 fg=C["text_dim"], bg=C["bg"]).pack(side="left", padx=(0, 6))
        for txt, cmd in [
            ("Shapefile", self._import_shp),
            ("DXF", self._import_dxf),
        ]:
            tk.Button(row3, text=txt, command=cmd,
                      font=("Segoe UI", 8), relief="flat", bd=0,
                      bg=C["input_bg"], fg=C["green_dark"],
                      highlightthickness=1, highlightbackground=C["border"],
                      activebackground=C["green_light"],
                      padx=12, pady=4, cursor="hand2"
                      ).pack(side="left", padx=(0, 5))

        # Row 4: Εξαγωγή
        row4 = tk.Frame(act_outer, bg=C["bg"])
        row4.pack(fill="x", pady=(2, 0))
        tk.Label(row4, text="Εξαγωγή:", font=("Segoe UI", 8),
                 fg=C["text_dim"], bg=C["bg"]).pack(side="left", padx=(0, 6))
        for txt, cmd in [
            ("Shapefile", self._export_shapefile),
            ("DXF", self._export_dxf),
        ]:
            tk.Button(row4, text=txt, command=cmd,
                      font=("Segoe UI", 8), relief="flat", bd=0,
                      bg=C["green_light"], fg=C["green_dark"],
                      activebackground=C["accent"],
                      padx=12, pady=4, cursor="hand2"
                      ).pack(side="left", padx=(0, 5))

        return frame

    def _create_egsa_frame(self) -> tk.Frame:
        """Δημιουργία EGSA mode frame."""
        frame = tk.Frame(self.root, bg=C["bg"])

        PAD = {"padx": 12}

        # ── Input ────────────────────────────────────────────────────────────
        inp_outer = tk.Frame(frame, bg=C["bg"])
        inp_outer.pack(fill="x", pady=(10, 4), **PAD)

        hdr = tk.Frame(inp_outer, bg=C["bg"])
        hdr.pack(fill="x")
        tk.Label(hdr, text="Σημεία εισόδου  ",
                 font=("Segoe UI", 9, "bold"), fg=C["text"],
                 bg=C["bg"]).pack(side="left")
        tk.Label(hdr, text="(Όνομα X Y)  ή  (X Y)  —  μία γραμμή ανά σημείο",
                 font=("Segoe UI", 8), fg=C["text_dim"],
                 bg=C["bg"]).pack(side="left")

        self.egsa_input = tk.Text(
            frame, width=48, height=6,
            font=("Consolas", 9),
            bg=C["input_bg"], fg=C["text"],
            relief="flat", bd=0,
            insertbackground=C["green_mid"],
            selectbackground=C["accent"],
            highlightthickness=1,
            highlightbackground=C["border"],
            highlightcolor=C["green_mid"],
            padx=8, pady=6
        )
        self.egsa_input.pack(fill="x", padx=12)
        add_context_menu(self.egsa_input)

        btn_row = tk.Frame(frame, bg=C["bg"])
        btn_row.pack(pady=(5, 0), **PAD)
        for txt, cmd in [
            ("📋  Επικόλληση", lambda: self._paste_to(self.egsa_input)),
            ("✕  Καθαρισμός", lambda: self.egsa_input.delete("1.0", tk.END)),
        ]:
            tk.Button(btn_row, text=txt, command=cmd,
                      font=("Segoe UI", 8), relief="flat", bd=0,
                      bg=C["bg"], fg=C["text_mid"],
                      activebackground=C["border"],
                      padx=10, pady=4, cursor="hand2"
                      ).pack(side="left", padx=(0, 6))

        tk.Frame(frame, bg=C["border"], height=1).pack(fill="x", padx=12, pady=(8, 0))

        calc_frame = tk.Frame(frame, bg=C["bg"])
        calc_frame.pack(fill="x", padx=12, pady=8)
        tk.Button(
            calc_frame, text="  ➜   Επεξεργασία Πολυγώνου  ",
            command=self._calculate_egsa,
            font=("Segoe UI", 10, "bold"),
            fg=C["white"], bg=C["blue_btn"],
            activebackground="#1976d2", activeforeground=C["white"],
            relief="flat", bd=0, pady=8, cursor="hand2"
        ).pack(fill="x")

        out_hdr = tk.Frame(frame, bg=C["bg"])
        out_hdr.pack(fill="x", pady=(4, 2), **PAD)
        tk.Label(out_hdr, text="Σημεία πολυγώνου",
                 font=("Segoe UI", 9, "bold"), fg=C["text"],
                 bg=C["bg"]).pack(side="left")
        tk.Button(out_hdr, text="📄 Αντιγραφή",
                  font=("Segoe UI", 8), relief="flat", bd=0,
                  bg=C["bg"], fg=C["text_dim"],
                  activebackground=C["border"],
                  padx=8, pady=2, cursor="hand2",
                  command=lambda: self._copy_text_to_clipboard(self.egsa_output)
                  ).pack(side="right")

        self.egsa_output = tk.Text(
            frame, width=48, height=8,
            font=("Consolas", 9),
            bg=C["output_bg"], fg=C["text"],
            state="disabled", relief="flat", bd=0,
            highlightthickness=1,
            highlightbackground=C["border"],
            highlightcolor=C["border"],
            padx=8, pady=6
        )
        self.egsa_output.pack(fill="x", padx=12)
        add_context_menu(self.egsa_output)

        self.lbl_egsa_only = tk.Label(frame, fg=C["green_mid"], bg=C["bg"],
                                       font=("Segoe UI", 8))

        if GE_AVAILABLE:
            ge_frame = tk.Frame(frame, bg=C["bg"])
            ge_frame.pack(fill="x", padx=12, pady=(10, 0))
            tk.Button(
                ge_frame, text="🌍  Άνοιγμα στο Google Earth",
                command=self._open_google_earth_window,
                font=("Segoe UI", 9, "bold"),
                fg=C["white"], bg=C["green_mid"],
                activebackground="#3a8e5f", activeforeground=C["white"],
                relief="flat", bd=0, pady=7, cursor="hand2"
            ).pack(fill="x")

        tk.Frame(frame, bg=C["border"], height=1).pack(fill="x", padx=12, pady=(12, 0))

        act_outer = tk.Frame(frame, bg=C["bg"])
        act_outer.pack(fill="x", padx=12, pady=(8, 10))

        tk.Label(act_outer, text="ΠΡΟΒΟΛΗ · ΕΙΣΑΓΩΓΗ · ΕΞΑΓΩΓΗ",
                 font=("Segoe UI", 7, "bold"), fg=C["text_dim"],
                 bg=C["bg"]).pack(anchor="w", pady=(0, 6))

        row1 = tk.Frame(act_outer, bg=C["bg"])
        row1.pack(fill="x", pady=(0, 4))
        tk.Button(row1, text="🗺  Προβολή σε Χάρτη",
                  command=self._preview_map,
                  font=("Segoe UI", 9), relief="flat", bd=0,
                  bg=C["green_light"], fg=C["green_dark"],
                  activebackground=C["accent"],
                  padx=10, pady=5, cursor="hand2"
                  ).pack(side="left", padx=(0, 6))
        style_box = ttk.Combobox(
            row1, textvariable=self.map_style_var,
            values=["OpenStreetMap", "ESRI Satellite", "Google Maps"],
            width=14, state="readonly", style="Modern.TCombobox"
        )
        style_box.set("ESRI Satellite")
        style_box.pack(side="left")

        row2 = tk.Frame(act_outer, bg=C["bg"])
        row2.pack(fill="x", pady=(0, 4))
        tk.Button(row2, text="📐  Σχήμα & Εμβαδό",
                  command=self._preview_polygon,
                  font=("Segoe UI", 8), relief="flat", bd=0,
                  bg=C["green_light"], fg=C["green_dark"],
                  activebackground=C["accent"],
                  padx=8, pady=5, cursor="hand2"
                  ).pack(side="left")

        row3 = tk.Frame(act_outer, bg=C["bg"])
        row3.pack(fill="x", pady=(2, 4))
        tk.Label(row3, text="Εισαγωγή:", font=("Segoe UI", 8),
                 fg=C["text_dim"], bg=C["bg"]).pack(side="left", padx=(0, 6))
        for txt, cmd in [("Shapefile", self._import_shp), ("DXF", self._import_dxf)]:
            tk.Button(row3, text=txt, command=cmd,
                      font=("Segoe UI", 8), relief="flat", bd=0,
                      bg=C["input_bg"], fg=C["green_dark"],
                      highlightthickness=1, highlightbackground=C["border"],
                      activebackground=C["green_light"],
                      padx=12, pady=4, cursor="hand2"
                      ).pack(side="left", padx=(0, 5))

        row4 = tk.Frame(act_outer, bg=C["bg"])
        row4.pack(fill="x", pady=(2, 0))
        tk.Label(row4, text="Εξαγωγή:", font=("Segoe UI", 8),
                 fg=C["text_dim"], bg=C["bg"]).pack(side="left", padx=(0, 6))
        for txt, cmd in [("Shapefile", self._export_shapefile), ("DXF", self._export_dxf)]:
            tk.Button(row4, text=txt, command=cmd,
                      font=("Segoe UI", 8), relief="flat", bd=0,
                      bg=C["green_light"], fg=C["green_dark"],
                      activebackground=C["accent"],
                      padx=12, pady=4, cursor="hand2"
                      ).pack(side="left", padx=(0, 5))

        return frame

    def _create_wgs84_frame(self) -> tk.Frame:
        """Τρίτη καρτέλα: αμφίδρομη μετατροπή ΕΓΣΑ87 ↔ WGS84."""
        frame = tk.Frame(self.root, bg=C["bg"])
        PAD = {"padx": 12}

        # ── Direction / WGS84 format ─────────────────────────────────────────
        options_outer = tk.Frame(frame, bg=C["bg"])
        options_outer.pack(fill="x", pady=(10, 4), **PAD)

        tk.Label(options_outer, text="ΚΑΤΕΥΘΥΝΣΗ ΜΕΤΑΤΡΟΠΗΣ",
                 font=("Segoe UI", 7, "bold"), fg=C["text_dim"],
                 bg=C["bg"]).pack(anchor="w")

        direction_row = tk.Frame(options_outer, bg=C["bg"])
        direction_row.pack(fill="x", pady=(3, 7))
        self._wgs_direction_buttons = {}
        for text, value in [
            ("ΕΓΣΑ87 → WGS84", "EGSA_TO_WGS"),
            ("WGS84 → ΕΓΣΑ87", "WGS_TO_EGSA"),
        ]:
            button = tk.Button(
                direction_row, text=text,
                command=lambda v=value: self._set_wgs_direction(v),
                font=("Segoe UI", 8, "bold"), relief="flat", bd=0,
                bg=C["white"], fg=C["green_dark"],
                activebackground=C["green_light"], activeforeground=C["green_dark"],
                highlightthickness=1, highlightbackground=C["border"],
                padx=12, pady=5, cursor="hand2"
            )
            button.pack(side="left", fill="x", expand=True, padx=(0, 6))
            self._wgs_direction_buttons[value] = button

        format_row = tk.Frame(options_outer, bg=C["bg"])
        format_row.pack(fill="x")
        tk.Label(format_row, text="Μορφή WGS84:",
                 font=("Segoe UI", 8), fg=C["text_dim"], bg=C["bg"]).pack(side="left", padx=(0, 6))
        for text, value in [
            ("Δεκαδικές μοίρες", "decimal"),
            ("Μοίρες / λεπτά / δευτερόλεπτα", "dms"),
        ]:
            tk.Radiobutton(
                format_row, text=text,
                variable=self.wgs_format_var, value=value,
                command=self._update_wgs84_ui,
                font=("Segoe UI", 8), bg=C["bg"], fg=C["text"],
                selectcolor=C["bg"], activebackground=C["bg"],
                cursor="hand2"
            ).pack(side="left", padx=(0, 12))

        tk.Frame(frame, bg=C["border"], height=1).pack(fill="x", padx=12, pady=(6, 0))

        # ── Input ─────────────────────────────────────────────────────────────
        inp_outer = tk.Frame(frame, bg=C["bg"])
        inp_outer.pack(fill="x", pady=(10, 4), **PAD)

        hdr = tk.Frame(inp_outer, bg=C["bg"])
        hdr.pack(fill="x")
        self.wgs_input_title_var = tk.StringVar(master=self.root)
        self.wgs_input_hint_var = tk.StringVar(master=self.root)
        tk.Label(hdr, textvariable=self.wgs_input_title_var,
                 font=("Segoe UI", 9, "bold"), fg=C["text"],
                 bg=C["bg"]).pack(side="left")
        tk.Label(hdr, textvariable=self.wgs_input_hint_var,
                 font=("Segoe UI", 8), fg=C["text_dim"],
                 bg=C["bg"]).pack(side="left", padx=(8, 0))

        # Το text input παραμένει για ΕΓΣΑ87 και decimal WGS84. Στη χειροκίνητη
        # είσοδο DMS εμφανίζεται αριθμητικός πίνακας ώστε ο χρήστης να μην
        # χρειάζεται να πληκτρολογεί σύμβολα ° ′ ″.
        self.wgs_input_host = tk.Frame(frame, bg=C["bg"])
        self.wgs_input_host.pack(fill="x", padx=12)

        self.wgs_text_input_frame = tk.Frame(self.wgs_input_host, bg=C["bg"])
        self.wgs_input = tk.Text(
            self.wgs_text_input_frame, width=48, height=6,
            font=("Consolas", 9),
            bg=C["input_bg"], fg=C["text"],
            relief="flat", bd=0,
            insertbackground=C["green_mid"],
            selectbackground=C["accent"],
            highlightthickness=1,
            highlightbackground=C["border"],
            highlightcolor=C["green_mid"],
            padx=8, pady=6
        )
        self.wgs_input.pack(fill="x")
        add_context_menu(self.wgs_input)

        self.wgs_dms_input_frame = tk.Frame(self.wgs_input_host, bg=C["bg"])

        # Καθολική επιλογή ημισφαιρίου για όλα τα σημεία του πίνακα.
        hemisphere_card = tk.Frame(
            self.wgs_dms_input_frame, bg=C["green_light"],
            highlightthickness=1, highlightbackground=C["accent"]
        )
        hemisphere_card.pack(fill="x", pady=(0, 7))
        tk.Label(
            hemisphere_card, text="Κατεύθυνση συντεταγμένων",
            font=("Segoe UI", 8, "bold"), fg=C["green_dark"],
            bg=C["green_light"]
        ).pack(side="left", padx=(10, 14), pady=7)

        tk.Label(
            hemisphere_card, text="Latitude",
            font=("Segoe UI", 8), fg=C["text_mid"], bg=C["green_light"]
        ).pack(side="left", padx=(0, 4))
        ttk.Combobox(
            hemisphere_card, textvariable=self.wgs_lat_hem_var,
            values=("N", "S"), width=3, state="readonly",
            style="Modern.TCombobox"
        ).pack(side="left", padx=(0, 14), pady=4)

        tk.Label(
            hemisphere_card, text="Longitude",
            font=("Segoe UI", 8), fg=C["text_mid"], bg=C["green_light"]
        ).pack(side="left", padx=(0, 4))
        ttk.Combobox(
            hemisphere_card, textvariable=self.wgs_lon_hem_var,
            values=("E", "W"), width=3, state="readonly",
            style="Modern.TCombobox"
        ).pack(side="left", pady=4)

        # Ίδιες σταθερές διαστάσεις χρησιμοποιούνται και στις επικεφαλίδες
        # και στις γραμμές, ώστε LATITUDE / LONGITUDE να ευθυγραμμίζονται ακριβώς
        # με τα αντίστοιχα τρία πεδία ανεξάρτητα από γραμματοσειρά/DPI.
        self._dms_name_width_px = 60
        self._dms_group_width_px = 178

        dms_header = tk.Frame(self.wgs_dms_input_frame, bg=C["bg"])
        dms_header.pack(fill="x", padx=5, pady=(0, 4))

        name_header = tk.Frame(
            dms_header, width=self._dms_name_width_px, height=46, bg=C["bg"]
        )
        name_header.pack_propagate(False)
        name_header.pack(side="left", padx=(0, 7))
        tk.Label(
            name_header, text="Σημείο",
            font=("Segoe UI", 7, "bold"), fg=C["text_dim"], bg=C["bg"],
            anchor="center"
        ).pack(fill="both", expand=True)

        def add_dms_header_group(title: str):
            group = tk.Frame(
                dms_header, width=self._dms_group_width_px, height=46,
                bg=C["green_light"],
                highlightthickness=1, highlightbackground=C["accent"]
            )
            group.pack_propagate(False)
            group.pack(side="left", padx=(0, 9))

            tk.Label(
                group, text=title,
                font=("Segoe UI", 8, "bold"),
                fg=C["green_dark"], bg=C["green_light"]
            ).pack(fill="x", pady=(3, 0))

            symbols = tk.Frame(group, bg=C["green_light"])
            symbols.pack(fill="both", expand=True, padx=3, pady=(0, 2))
            for col, symbol in enumerate(("°", "′", "″")):
                symbols.grid_columnconfigure(col, weight=(5, 4, 7)[col], uniform="dms")
                tk.Label(
                    symbols, text=symbol,
                    font=("Segoe UI", 11, "bold"),
                    fg=C["green_dark"], bg=C["green_light"],
                    anchor="center"
                ).grid(row=0, column=col, sticky="nsew", padx=1)
            symbols.grid_rowconfigure(0, weight=1)
            return group

        add_dms_header_group("LATITUDE")
        add_dms_header_group("LONGITUDE")

        dms_body_outer = tk.Frame(
            self.wgs_dms_input_frame, bg=C["output_bg"],
            highlightthickness=1, highlightbackground=C["border"]
        )
        dms_body_outer.pack(fill="x")

        self.wgs_dms_canvas = tk.Canvas(
            dms_body_outer, height=128, bg=C["output_bg"],
            highlightthickness=0, bd=0
        )
        dms_scroll = tk.Scrollbar(
            dms_body_outer, orient="vertical",
            command=self.wgs_dms_canvas.yview
        )
        self.wgs_dms_canvas.configure(yscrollcommand=dms_scroll.set)
        self.wgs_dms_canvas.pack(side="left", fill="both", expand=True)
        dms_scroll.pack(side="right", fill="y")

        self.wgs_dms_inner = tk.Frame(self.wgs_dms_canvas, bg=C["output_bg"])
        self._wgs_dms_window = self.wgs_dms_canvas.create_window(
            (0, 0), window=self.wgs_dms_inner, anchor="nw"
        )
        self.wgs_dms_inner.bind(
            "<Configure>",
            lambda _e: self.wgs_dms_canvas.configure(
                scrollregion=self.wgs_dms_canvas.bbox("all")
            )
        )
        self.wgs_dms_canvas.bind(
            "<Configure>",
            lambda e: self.wgs_dms_canvas.itemconfigure(
                self._wgs_dms_window, width=e.width
            )
        )

        self._wgs_dms_rows = []
        self._add_wgs_dms_row()

        self.wgs_text_controls = tk.Frame(self.wgs_input_host, bg=C["bg"])
        self.wgs_text_controls.pack(pady=(5, 0))
        for txt, cmd in [
            ("📋  Επικόλληση", lambda: self._paste_to(self.wgs_input)),
            ("✕  Καθαρισμός", self._clear_wgs84_fields),
        ]:
            tk.Button(self.wgs_text_controls, text=txt, command=cmd,
                      font=("Segoe UI", 8), relief="flat", bd=0,
                      bg=C["bg"], fg=C["text_mid"],
                      activebackground=C["border"],
                      padx=10, pady=4, cursor="hand2"
                      ).pack(side="left", padx=(0, 6))

        self.wgs_dms_controls = tk.Frame(self.wgs_input_host, bg=C["bg"])
        self.wgs_dms_controls.pack(pady=(5, 0))
        for txt, cmd in [
            ("＋  Νέα γραμμή", self._add_wgs_dms_row),
            ("−  Τελευταία γραμμή", self._remove_last_wgs_dms_row),
            ("✕  Καθαρισμός", self._clear_wgs84_fields),
        ]:
            tk.Button(self.wgs_dms_controls, text=txt, command=cmd,
                      font=("Segoe UI", 8), relief="flat", bd=0,
                      bg=C["bg"], fg=C["text_mid"],
                      activebackground=C["border"],
                      padx=8, pady=4, cursor="hand2"
                      ).pack(side="left", padx=(0, 5))

        tk.Frame(frame, bg=C["border"], height=1).pack(fill="x", padx=12, pady=(8, 0))

        calc_frame = tk.Frame(frame, bg=C["bg"])
        calc_frame.pack(fill="x", padx=12, pady=8)
        self.wgs_calc_text_var = tk.StringVar(master=self.root)
        tk.Button(
            calc_frame, textvariable=self.wgs_calc_text_var,
            command=self._calculate_wgs84,
            font=("Segoe UI", 10, "bold"),
            fg=C["white"], bg=C["blue_btn"],
            activebackground="#1976d2", activeforeground=C["white"],
            relief="flat", bd=0, pady=8, cursor="hand2"
        ).pack(fill="x")

        # ── Output ────────────────────────────────────────────────────────────
        out_hdr = tk.Frame(frame, bg=C["bg"])
        out_hdr.pack(fill="x", pady=(4, 2), **PAD)
        self.wgs_output_title_var = tk.StringVar(master=self.root)
        tk.Label(out_hdr, textvariable=self.wgs_output_title_var,
                 font=("Segoe UI", 9, "bold"), fg=C["text"],
                 bg=C["bg"]).pack(side="left")
        tk.Button(out_hdr, text="📄 Αντιγραφή",
                  font=("Segoe UI", 8), relief="flat", bd=0,
                  bg=C["bg"], fg=C["text_dim"],
                  activebackground=C["border"],
                  padx=8, pady=2, cursor="hand2",
                  command=lambda: self._copy_text_to_clipboard(self.wgs_output)
                  ).pack(side="right")

        self.wgs_output = tk.Text(
            frame, width=48, height=5,
            font=("Consolas", 9),
            bg=C["output_bg"], fg=C["text"],
            state="disabled", relief="flat", bd=0,
            highlightthickness=1,
            highlightbackground=C["border"],
            highlightcolor=C["border"],
            padx=8, pady=6
        )
        self.wgs_output.pack(fill="x", padx=12)
        add_context_menu(self.wgs_output)

        self.lbl_wgs_area = tk.Label(frame, fg=C["green_mid"], bg=C["bg"],
                                     font=("Segoe UI", 8))

        if GE_AVAILABLE:
            ge_frame = tk.Frame(frame, bg=C["bg"])
            ge_frame.pack(fill="x", padx=12, pady=(10, 0))
            tk.Button(
                ge_frame, text="🌍  Άνοιγμα στο Google Earth",
                command=self._open_google_earth_window,
                font=("Segoe UI", 9, "bold"),
                fg=C["white"], bg=C["green_mid"],
                activebackground="#3a8e5f", activeforeground=C["white"],
                relief="flat", bd=0, pady=7, cursor="hand2"
            ).pack(fill="x")

        # ── Same geometry actions, always backed by EGSA87 internally ─────────
        tk.Frame(frame, bg=C["border"], height=1).pack(fill="x", padx=12, pady=(8, 0))
        act_outer = tk.Frame(frame, bg=C["bg"])
        act_outer.pack(fill="x", padx=12, pady=(6, 7))

        tk.Label(act_outer, text="ΠΡΟΒΟΛΗ · ΕΙΣΑΓΩΓΗ · ΕΞΑΓΩΓΗ",
                 font=("Segoe UI", 7, "bold"), fg=C["text_dim"],
                 bg=C["bg"]).pack(anchor="w", pady=(0, 4))

        row1 = tk.Frame(act_outer, bg=C["bg"])
        row1.pack(fill="x", pady=(0, 4))
        tk.Button(row1, text="🗺  Προβολή σε Χάρτη",
                  command=self._preview_map,
                  font=("Segoe UI", 8), relief="flat", bd=0,
                  bg=C["green_light"], fg=C["green_dark"],
                  activebackground=C["accent"],
                  padx=8, pady=4, cursor="hand2"
                  ).pack(side="left", padx=(0, 5))
        style_box = ttk.Combobox(
            row1, textvariable=self.map_style_var,
            values=["OpenStreetMap", "ESRI Satellite", "Google Maps"],
            width=12, state="readonly", style="Modern.TCombobox"
        )
        style_box.set("ESRI Satellite")
        style_box.pack(side="left", padx=(0, 6))
        tk.Button(row1, text="📐  Σχήμα & Εμβαδό",
                  command=self._preview_polygon,
                  font=("Segoe UI", 8), relief="flat", bd=0,
                  bg=C["green_light"], fg=C["green_dark"],
                  activebackground=C["accent"],
                  padx=8, pady=4, cursor="hand2"
                  ).pack(side="left")

        row2 = tk.Frame(act_outer, bg=C["bg"])
        row2.pack(fill="x")
        tk.Label(row2, text="Εισαγωγή:", font=("Segoe UI", 8),
                 fg=C["text_dim"], bg=C["bg"]).pack(side="left", padx=(0, 5))
        for txt, cmd in [("Shapefile", self._import_shp), ("DXF", self._import_dxf)]:
            tk.Button(row2, text=txt, command=cmd,
                      font=("Segoe UI", 8), relief="flat", bd=0,
                      bg=C["input_bg"], fg=C["green_dark"],
                      highlightthickness=1, highlightbackground=C["border"],
                      activebackground=C["green_light"],
                      padx=8, pady=3, cursor="hand2"
                      ).pack(side="left", padx=(0, 4))

        tk.Label(row2, text="Εξαγωγή:", font=("Segoe UI", 8),
                 fg=C["text_dim"], bg=C["bg"]).pack(side="left", padx=(8, 5))
        for txt, cmd in [("Shapefile", self._export_shapefile), ("DXF", self._export_dxf)]:
            tk.Button(row2, text=txt, command=cmd,
                      font=("Segoe UI", 8), relief="flat", bd=0,
                      bg=C["green_light"], fg=C["green_dark"],
                      activebackground=C["accent"],
                      padx=8, pady=3, cursor="hand2"
                      ).pack(side="left", padx=(0, 4))

        self._update_wgs84_ui()
        return frame

    def _set_wgs_direction(self, value: str) -> None:
        self.wgs_direction_var.set(value)
        self._update_wgs84_ui()

    def _refresh_wgs_direction_buttons(self) -> None:
        selected = self.wgs_direction_var.get()
        for value, button in self._wgs_direction_buttons.items():
            if value == selected:
                button.config(
                    bg=C["green_mid"], fg=C["white"],
                    activebackground=C["green_dark"], activeforeground=C["white"],
                    highlightbackground=C["green_mid"]
                )
            else:
                button.config(
                    bg=C["white"], fg=C["green_dark"],
                    activebackground=C["green_light"], activeforeground=C["green_dark"],
                    highlightbackground=C["border"]
                )

    def _update_wgs84_ui(self) -> None:
        """Ενημερώνει τίτλους και εναλλάσσει text/DMS-table input."""
        self._refresh_wgs_direction_buttons()
        direction = self.wgs_direction_var.get()
        fmt = self.wgs_format_var.get()
        use_dms_table = direction == "WGS_TO_EGSA" and fmt == "dms"

        self.wgs_text_input_frame.pack_forget()
        self.wgs_dms_input_frame.pack_forget()
        self.wgs_text_controls.pack_forget()
        self.wgs_dms_controls.pack_forget()

        if use_dms_table:
            self.wgs_dms_input_frame.pack(fill="x")
            self.wgs_dms_controls.pack(pady=(5, 0))
        else:
            self.wgs_text_input_frame.pack(fill="x")
            self.wgs_text_controls.pack(pady=(5, 0))

        if direction == "EGSA_TO_WGS":
            self.wgs_input_title_var.set("Σημεία εισόδου σε ΕΓΣΑ87")
            self.wgs_input_hint_var.set("(Όνομα X Y) ή (X Y)")
            self.wgs_calc_text_var.set("  ➜   Μετατροπή σε WGS84  ")
            self.wgs_output_title_var.set(
                "Αποτελέσματα WGS84 — " +
                ("δεκαδικές μοίρες (Latitude, Longitude)" if fmt == "decimal"
                 else "μοίρες / λεπτά / δευτερόλεπτα")
            )
        else:
            self.wgs_input_title_var.set("Σημεία εισόδου σε WGS84")
            if fmt == "decimal":
                self.wgs_input_hint_var.set("(Όνομα Latitude Longitude) — π.χ. A 40.272123 22.503456")
            else:
                self.wgs_input_hint_var.set("")
            self.wgs_calc_text_var.set("  ➜   Μετατροπή σε ΕΓΣΑ87  ")
            self.wgs_output_title_var.set("Αποτελέσματα σε ΕΓΣΑ87")

    def _add_wgs_dms_row(self) -> None:
        """Προσθέτει μία επεξεργάσιμη γραμμή DMS. Η τελευταία γραμμή επεκτείνει αυτόματα τον πίνακα."""
        index = len(self._wgs_dms_rows)
        row_frame = tk.Frame(self.wgs_dms_inner, bg=C["output_bg"])
        row_frame.pack(fill="x", padx=5, pady=1)

        row = {
            "frame": row_frame,
            "name": tk.StringVar(master=self.root, value=self._auto_point_name(index)),
            "lat_deg": tk.StringVar(master=self.root),
            "lat_min": tk.StringVar(master=self.root),
            "lat_sec": tk.StringVar(master=self.root),
            "lon_deg": tk.StringVar(master=self.root),
            "lon_min": tk.StringVar(master=self.root),
            "lon_sec": tk.StringVar(master=self.root),
        }

        name_holder = tk.Frame(
            row_frame, width=self._dms_name_width_px, height=31,
            bg=C["output_bg"]
        )
        name_holder.pack_propagate(False)
        name_holder.pack(side="left", padx=(0, 7), pady=1)
        name_entry = tk.Entry(
            name_holder, textvariable=row["name"],
            font=("Consolas", 9, "bold"), justify="center",
            bg=C["white"], fg=C["green_dark"],
            relief="flat", bd=0,
            highlightthickness=1,
            highlightbackground=C["border"],
            highlightcolor=C["green_mid"]
        )
        name_entry.pack(fill="both", expand=True, pady=2)

        def add_group(keys, bg):
            group = tk.Frame(
                row_frame, width=self._dms_group_width_px, height=31, bg=bg,
                highlightthickness=1, highlightbackground=C["border"]
            )
            # Τα παιδιά αυτού του frame τοποθετούνται με grid, άρα πρέπει να
            # απενεργοποιηθεί το grid propagation (όχι το pack propagation).
            # Διαφορετικά τα τρία Entry ζητούν το φυσικό τους πλάτος και το
            # LAT/LON group απλώνεται, με αποτέλεσμα να φαίνονται μόνο 3 πεδία
            # συνολικά αντί για 3 + 3.
            group.grid_propagate(False)
            group.pack(side="left", padx=(0, 9), pady=1)

            for col, key in enumerate(keys):
                group.grid_columnconfigure(col, weight=(5, 4, 7)[col], uniform="dms")
                tk.Entry(
                    group, textvariable=row[key],
                    font=("Consolas", 9), justify="center",
                    bg=C["white"], fg=C["text"],
                    relief="flat", bd=0,
                    highlightthickness=1,
                    highlightbackground=C["border"],
                    highlightcolor=C["green_mid"]
                ).grid(row=0, column=col, sticky="nsew", padx=2, pady=3)
            group.grid_rowconfigure(0, weight=1)
            return group

        row["lat_group"] = add_group(("lat_deg", "lat_min", "lat_sec"), C["green_light"])
        row["lon_group"] = add_group(("lon_deg", "lon_min", "lon_sec"), C["green_light"])

        self._wgs_dms_rows.append(row)
        for key in ("lat_deg", "lat_min", "lat_sec", "lon_deg", "lon_min", "lon_sec"):
            row[key].trace_add(
                "write",
                lambda *_args, r=row: self.root.after_idle(
                    lambda: self._ensure_wgs_dms_trailing_row(r)
                )
            )

        self.root.after_idle(
            lambda: self.wgs_dms_canvas.yview_moveto(1.0)
            if hasattr(self, "wgs_dms_canvas") else None
        )

    def _ensure_wgs_dms_trailing_row(self, row: dict) -> None:
        """Όταν αρχίσει να συμπληρώνεται η τελευταία γραμμή, δημιουργεί μία νέα κενή."""
        if not self._wgs_dms_rows or row is not self._wgs_dms_rows[-1]:
            return
        keys = ("lat_deg", "lat_min", "lat_sec", "lon_deg", "lon_min", "lon_sec")
        if any(row[key].get().strip() for key in keys):
            self._add_wgs_dms_row()

    def _remove_last_wgs_dms_row(self) -> None:
        if len(self._wgs_dms_rows) <= 1:
            return
        row = self._wgs_dms_rows.pop()
        row["frame"].destroy()

    def _reset_wgs_dms_rows(self) -> None:
        for row in self._wgs_dms_rows:
            row["frame"].destroy()
        self._wgs_dms_rows.clear()
        self._add_wgs_dms_row()
        self.wgs_dms_canvas.yview_moveto(0.0)

    def _collect_wgs_dms_points(self) -> Tuple[List[WGS84Point], List[str]]:
        """Διαβάζει τις συμπληρωμένες γραμμές του DMS πίνακα και αγνοεί τις τελείως κενές."""
        points: List[WGS84Point] = []
        errors: List[str] = []
        coord_keys = ("lat_deg", "lat_min", "lat_sec", "lon_deg", "lon_min", "lon_sec")

        for row_index, row in enumerate(self._wgs_dms_rows, 1):
            values = [row[key].get().strip() for key in coord_keys]
            if not any(values):
                continue
            name = row["name"].get().strip() or self._auto_point_name(row_index - 1)
            if not all(values):
                errors.append(f"Γραμμή {row_index} ({name}): συμπλήρωσε όλα τα πεδία μοιρών, λεπτών και δευτερολέπτων.")
                continue
            try:
                latitude = dms_components_to_decimal(
                    row["lat_deg"].get(), row["lat_min"].get(), row["lat_sec"].get(),
                    self.wgs_lat_hem_var.get(), "lat"
                )
                longitude = dms_components_to_decimal(
                    row["lon_deg"].get(), row["lon_min"].get(), row["lon_sec"].get(),
                    self.wgs_lon_hem_var.get(), "lon"
                )
                points.append(WGS84Point(name=name, latitude=latitude, longitude=longitude))
            except ValueError as exc:
                errors.append(f"Γραμμή {row_index} ({name}): {exc}")

        return points, errors

    def _clear_wgs84_fields(self) -> None:
        self.wgs_input.delete("1.0", tk.END)
        self._reset_wgs_dms_rows()
        self.wgs_output.config(state="normal")
        self.wgs_output.delete("1.0", tk.END)
        self.wgs_output.config(state="disabled")
        self.HATT_points = []
        self.egsa_points = []
        self.wgs84_points = []
        self._clear_area_labels()

    def _create_footer(self):
        """Footer."""
        footer = tk.Frame(self.root, bg=C["bg"], height=20)
        footer.pack(side="bottom", fill="x")
        tk.Frame(footer, bg=C["border"], height=1).pack(fill="x")
        tk.Label(footer, text="∘ D.T. 2026",
                 fg=C["text_dim"], bg=C["bg"],
                 font=("Segoe UI", 8)
                 ).pack(side="right", padx=10, pady=3)

    def _stabilize_main_window_size(self) -> None:
        """Κρατά σταθερό το κύριο παράθυρο στο μέγεθος της μεγαλύτερης καρτέλας."""
        frames = [self.frame_HATT, self.frame_egsa, self.frame_wgs84]
        selected = self.mode_var.get()
        max_width = 0
        max_height = 0

        # Το root είναι ακόμη κρυφό πίσω από το splash, οπότε η μέτρηση δεν
        # προκαλεί ορατό τρεμόπαιγμα στον χρήστη.
        for candidate in frames:
            for item in frames:
                item.pack_forget()
            candidate.pack(fill="x", pady=5)
            self.root.update_idletasks()
            max_width = max(max_width, self.root.winfo_reqwidth())
            max_height = max(max_height, self.root.winfo_reqheight())

        for item in frames:
            item.pack_forget()
        if selected == "HATT":
            self.frame_HATT.pack(fill="x", pady=5)
        elif selected == "egsa":
            self.frame_egsa.pack(fill="x", pady=5)
        else:
            self.frame_wgs84.pack(fill="x", pady=5)

        self.root.update_idletasks()
        screen_width = max(640, self.root.winfo_screenwidth() - 40)
        screen_height = max(600, self.root.winfo_screenheight() - 80)
        width = min(max_width, screen_width)
        height = min(max_height, screen_height)

        self.root.geometry(f"{width}x{height}")
        self.root.minsize(width, height)

    def _switch_mode(self):
        """Εναλλαγή μεταξύ HATT, EGSA και WGS84 mode."""
        self._clear_area_labels()
        self._refresh_mode_tabs()

        self.frame_HATT.pack_forget()
        self.frame_egsa.pack_forget()
        self.frame_wgs84.pack_forget()

        mode = self.mode_var.get()
        if mode == "HATT":
            self.frame_HATT.pack(fill="x", pady=5)
        elif mode == "egsa":
            self.frame_egsa.pack(fill="x", pady=5)
        else:
            self.frame_wgs84.pack(fill="x", pady=5)
            self._update_wgs84_ui()
    
    def _paste_to(self, widget: tk.Text):
        """Επικόλληση από clipboard."""
        try:
            widget.insert("insert", self.root.clipboard_get())
        except tk.TclError:
            messagebox.showwarning("Προειδοποίηση", 
                                 "Το clipboard είναι κενό.")
    
    def _copy_text_to_clipboard(self, text_widget: tk.Text) -> None:
        """Αντιγράφει όλο το περιεχόμενο ενός Text widget στο clipboard."""
        content = text_widget.get("1.0", tk.END).strip()
        if not content:
            return
        self.root.clipboard_clear()
        self.root.clipboard_append(content)
        logger.info("Αντιγραφή αποτελεσμάτων στο clipboard")

    def _calculate_HATT(self):
        """Υπολογισμός μετατροπής HATT → EGSA87."""
        display_value = self.region_var.get()
        current_region = self._region_display_to_name.get(display_value, display_value)
        if current_region in UNVERIFIED_HATT_REGIONS:
            if not messagebox.askyesno(
                "Ειδική προειδοποίηση HATT",
                UNVERIFIED_HATT_REGIONS[current_region] + "\n\nΝα συνεχιστεί παρ' όλα αυτά;"
            ):
                return
        text = self.HATT_input.get("1.0", tk.END).strip()
        
        # Parse input
        self.HATT_points, errors = self.parser.parse_points(text)
        
        if errors:
            error_msg = "\n".join(errors[:5])  # Εμφάνιση πρώτων 5 σφαλμάτων
            messagebox.showwarning("Προειδοποίηση", 
                                 f"Κάποια σημεία αγνοήθηκαν:\n{error_msg}")
        
        if not self.HATT_points:
            messagebox.showerror(MESSAGES['error_title'], 
                               "Δεν βρέθηκαν έγκυρα σημεία.")
            return
        
        # Transform to EGSA87
        self.egsa_points = []
        for p in self.HATT_points:
            x_egsa, y_egsa = self.transformer.HATT_to_egsa(p.x, p.y)
            self.egsa_points.append(Point(name=p.name, x=x_egsa, y=y_egsa))
        
        # Display results
        self.HATT_output.config(state="normal")
        self.HATT_output.delete("1.0", tk.END)
        for p in self.egsa_points:
            self.HATT_output.insert(tk.END, 
                f"{p.name}\t{format_display(p.x)}\t{format_display(p.y)}\n")
        self.HATT_output.config(state="disabled")
        
        # Update area labels
        self._update_area_labels_HATT()
        
        logger.info(f"Converted {len(self.HATT_points)} points from HATT to EGSA87")
    
    def _calculate_egsa(self):
        """Υπολογισμός με άμεση εισαγωγή EGSA87."""
        text = self.egsa_input.get("1.0", tk.END).strip()
        
        # Parse input
        self.egsa_points, errors = self.parser.parse_points(text)
        self.HATT_points = []  # Clear HATT points
        
        if errors:
            error_msg = "\n".join(errors[:5])
            messagebox.showwarning("Προειδοποίηση", 
                                 f"Κάποια σημεία αγνοήθηκαν:\n{error_msg}")
        
        if not self.egsa_points:
            messagebox.showerror(MESSAGES['error_title'], 
                               "Δεν βρέθηκαν έγκυρα σημεία.")
            return
        
        # Display results
        self.egsa_output.config(state="normal")
        self.egsa_output.delete("1.0", tk.END)
        for p in self.egsa_points:
            self.egsa_output.insert(tk.END, 
                f"{p.name}\t{format_display(p.x)}\t{format_display(p.y)}\n")
        self.egsa_output.config(state="disabled")
        
        # Update area labels
        self._update_area_labels_egsa()
        
        logger.info(f"Processed {len(self.egsa_points)} EGSA87 points")

    def _calculate_wgs84(self):
        """Αμφίδρομη μετατροπή ΕΓΣΑ87 ↔ WGS84 με κοινό EGSA geometry state."""
        text = self.wgs_input.get("1.0", tk.END).strip()
        direction = self.wgs_direction_var.get()
        fmt = self.wgs_format_var.get()

        self.HATT_points = []
        self.egsa_points = []
        self.wgs84_points = []

        if direction == "EGSA_TO_WGS":
            points, errors = self.parser.parse_points(text)
            if errors:
                messagebox.showwarning("Προειδοποίηση", "Κάποια σημεία αγνοήθηκαν:\n" + "\n".join(errors[:5]))
            if not points:
                messagebox.showerror(MESSAGES['error_title'], "Δεν βρέθηκαν έγκυρα σημεία ΕΓΣΑ87.")
                return

            self.egsa_points = points
            for point in points:
                lon, lat = self.transformer.egsa_to_wgs84(point.x, point.y)
                self.wgs84_points.append(WGS84Point(point.name, lat, lon))

            output_lines = []
            for point in self.wgs84_points:
                if fmt == "dms":
                    lat_text = format_wgs84_dms(point.latitude, "lat")
                    lon_text = format_wgs84_dms(point.longitude, "lon")
                else:
                    lat_text = f"{point.latitude:.8f}"
                    lon_text = f"{point.longitude:.8f}"
                output_lines.append(f"{point.name}\t{lat_text}\t{lon_text}")
        else:
            if fmt == "dms":
                wgs_points, errors = self._collect_wgs_dms_points()
            else:
                wgs_points, errors = parse_wgs84_points(text, fmt)
            if errors:
                messagebox.showwarning("Προειδοποίηση", "Κάποια σημεία αγνοήθηκαν:\n" + "\n".join(errors[:5]))
            if not wgs_points:
                messagebox.showerror(MESSAGES['error_title'], "Δεν βρέθηκαν έγκυρα σημεία WGS84.")
                return

            self.wgs84_points = wgs_points
            for point in wgs_points:
                x, y = self.transformer.wgs84_to_egsa(point.longitude, point.latitude)
                self.egsa_points.append(Point(name=point.name, x=x, y=y))

            output_lines = [
                f"{point.name}\t{format_display(point.x)}\t{format_display(point.y)}"
                for point in self.egsa_points
            ]

        self.wgs_output.config(state="normal")
        self.wgs_output.delete("1.0", tk.END)
        self.wgs_output.insert("1.0", "\n".join(output_lines) + "\n")
        self.wgs_output.config(state="disabled")
        self._update_area_labels_wgs84()
        logger.info(
            "Processed %s points in WGS84 tab (%s, %s)",
            len(self.egsa_points), direction, fmt
        )

    def _update_area_labels_wgs84(self):
        """Εμβαδόν του WGS84 workflow υπολογισμένο σωστά στο επίπεδο ΕΓΣΑ87."""
        self._clear_area_labels()
        if len(self.egsa_points) < 3:
            return
        if self.calculator.has_self_intersections(self.egsa_points):
            self.lbl_wgs_area.config(
                text="Προειδοποίηση: το πολύγωνο παρουσιάζει αυτοτομή — το εμβαδόν δεν υπολογίζεται.",
                fg="#b42318"
            )
        else:
            area = self.calculator.calculate_area(self.egsa_points).quantize(DISPLAY_DEC)
            self.lbl_wgs_area.config(
                text=f"Εμβαδόν (υπολογισμένο σε ΕΓΣΑ87): {format_display(area)} m²",
                fg=C["green_mid"]
            )
        self.lbl_wgs_area.pack(anchor="w")

    def _update_area_labels_HATT(self):
        """Ενημέρωση labels εμβαδού για HATT mode με έλεγχο μη έγκυρης γεωμετρίας."""
        self._clear_area_labels()

        if len(self.HATT_points) < 3 or len(self.egsa_points) < 3:
            return

        if self.calculator.has_self_intersections(self.HATT_points):
            self.lbl_diff.config(
                text="Προειδοποίηση: το πολύγωνο HATT παρουσιάζει αυτοτομή — το εμβαδόν δεν υπολογίζεται.",
                fg="#b42318"
            )
            self.lbl_diff.pack(anchor="w")
            return

        area_HATT = self.calculator.calculate_area(self.HATT_points).quantize(DISPLAY_DEC)
        area_egsa = self.calculator.calculate_area(self.egsa_points).quantize(DISPLAY_DEC)

        self.lbl_HATT_area.config(text=f"Εμβαδόν HATT: {format_display(area_HATT)} m²")
        self.lbl_HATT_area.pack(anchor="w")
        self.lbl_egsa_area.config(text=f"Εμβαδόν EGSA87: {format_display(area_egsa)} m²")
        self.lbl_egsa_area.pack(anchor="w")

        diff = (area_egsa - area_HATT).quantize(DISPLAY_DEC)
        if area_HATT == 0:
            self.lbl_diff.config(
                text=f"Διαφορά: {format_display(diff)} m² (ποσοστό μη διαθέσιμο: μηδενικό εμβαδόν HATT)",
                fg=C["text_mid"]
            )
        else:
            pct = ((diff / area_HATT) * 100).quantize(DISPLAY_DEC)
            self.lbl_diff.config(
                text=f"Διαφορά: {format_display(diff)} m² ({format_display(pct)} %)",
                fg=C["text_mid"]
            )
        self.lbl_diff.pack(anchor="w")

    def _update_area_labels_egsa(self):
        """Ενημέρωση labels εμβαδού για EGSA mode."""
        self._clear_area_labels()

        if len(self.egsa_points) >= 3:
            if self.calculator.has_self_intersections(self.egsa_points):
                self.lbl_egsa_only.config(
                    text="Προειδοποίηση: το πολύγωνο παρουσιάζει αυτοτομή — το εμβαδόν δεν υπολογίζεται.",
                    fg="#b42318"
                )
            else:
                area = self.calculator.calculate_area(self.egsa_points).quantize(DISPLAY_DEC)
                self.lbl_egsa_only.config(
                    text=f"Εμβαδόν EGSA87: {format_display(area)} m²",
                    fg=C["green_mid"]
                )
            self.lbl_egsa_only.pack(anchor="w")

    def _clear_area_labels(self):
        """Απόκρυψη όλων των area labels και επαναφορά χρωμάτων."""
        self.lbl_HATT_area.config(fg=C["green_mid"])
        self.lbl_egsa_area.config(fg=C["green_mid"])
        self.lbl_diff.config(fg=C["text_mid"])
        self.lbl_egsa_only.config(fg=C["green_mid"])
        self.lbl_wgs_area.config(fg=C["green_mid"])
        self.lbl_HATT_area.pack_forget()
        self.lbl_egsa_area.pack_forget()
        self.lbl_diff.pack_forget()
        self.lbl_egsa_only.pack_forget()
        self.lbl_wgs_area.pack_forget()
    
    def _preview_map(self):
        """Προβολή σημείων/πολυγώνου σε διαδραστικό χάρτη (Folium)."""
        if not self.egsa_points:
            messagebox.showerror(MESSAGES['error_title'], "Δεν υπάρχουν σημεία.")
            return

        # Convert to WGS84
        coords_wgs = []
        for p in self.egsa_points:
            lon, lat = self.transformer.egsa_to_wgs84(p.x, p.y)
            coords_wgs.append((lat, lon))
        
        # Calculate center
        center_lat = sum(c[0] for c in coords_wgs) / len(coords_wgs)
        center_lon = sum(c[1] for c in coords_wgs) / len(coords_wgs)
        
        style = self.map_style_var.get()

        # ── Google Maps: άνοιγμα στον browser με pin στο πρώτο σημείο ─────────
        if style == "Google Maps":
            first_lat, first_lon = coords_wgs[0]
            url = f"https://www.google.com/maps?q={first_lat:.8f},{first_lon:.8f}"
            webbrowser.open(url)
            logger.info(f"Google Maps opened (pin on '{self.egsa_points[0].name}'): {url}")
            return
        # ─────────────────────────────────────────────────────────────────────

        # Create folium map
        if style == "OpenStreetMap":
            m = folium.Map(location=[center_lat, center_lon],
                          zoom_start=15, tiles="OpenStreetMap")
        elif style == "ESRI Satellite":
            m = folium.Map(location=[center_lat, center_lon],
                          zoom_start=15, tiles=None)
            folium.TileLayer(
                tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
                attr="Esri Satellite",
                name="Satellite",
                control=False
            ).add_to(m)

        n = len(self.egsa_points)

        if n == 1:
            # Μεμονωμένο σημείο → marker με CircleMarker
            folium.CircleMarker(
                coords_wgs[0], radius=8,
                color="red", fill=True, fill_color="blue", fill_opacity=0.7
            ).add_to(m)
        elif n == 2:
            # Δύο σημεία → γραμμή (απόσταση)
            folium.PolyLine(coords_wgs, color="red", weight=2.5).add_to(m)
        else:
            # Τρία+ σημεία → κλειστό πολύγωνο με fill
            folium.PolyLine(
                coords_wgs + [coords_wgs[0]],
                color="red", weight=2, fill=True, fill_color="blue",
                fill_opacity=0.3
            ).add_to(m)

        # Markers με ονόματα (για όλες τις περιπτώσεις)
        for (lat, lon), p in zip(coords_wgs, self.egsa_points):
            folium.Marker(
                [lat, lon],
                icon=folium.DivIcon(
                    html=f"<div style='color:black; font-size:12px; font-weight:bold;'>{p.name}</div>"
                )
            ).add_to(m)

        # Fit bounds — για 1 σημείο χρησιμοποιούμε location αντί fit_bounds
        if n == 1:
            m.location = list(coords_wgs[0])
            m.zoom_start = 16
        else:
            m.fit_bounds(coords_wgs)

        # Save and open
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix='.html')
        temp_files.append(tmp.name)
        m.save(tmp.name)
        webbrowser.open(tmp.name)

        logger.info(f"Map preview opened: {tmp.name}")
    
    def _preview_polygon(self):
        """Προβολή σημείων/γραμμής/πολυγώνου με matplotlib."""
        if not self.egsa_points:
            messagebox.showerror(MESSAGES['error_title'], "Δεν υπάρχουν σημεία.")
            return

        n = len(self.egsa_points)

        # Για 1 σημείο: απλό scatter plot
        # Για 2 σημεία: γραμμή με απόσταση
        # Για 3+: κλειστό πολύγωνο με εμβαδό
        if n >= 3:
            closed = self.egsa_points + [self.egsa_points[0]]
        else:
            closed = self.egsa_points

        xs = [float(p.x) for p in closed]
        ys = [float(p.y) for p in closed]

        plt.figure(f"Προβολή EGSA87 – v{APP_VERSION}")
        plt.plot(xs, ys, marker="o")

        if n >= 3:
            area = self.calculator.calculate_area(self.egsa_points).quantize(DISPLAY_DEC)
            plt.title("Πολύγωνο σε EGSA87")
        elif n == 2:
            dist = self.calculator.calculate_distance(self.egsa_points[0], self.egsa_points[1])
            plt.title(f"Τμήμα σε EGSA87  |  Απόσταση: {format_display(dist)} m")
        else:
            plt.title("Σημείο σε EGSA87")
        
        ax = plt.gca()
        ax.set_aspect("equal", adjustable="datalim")
        ax.ticklabel_format(style='plain', useOffset=False)

        xf = ScalarFormatter(useOffset=False)
        yf = ScalarFormatter(useOffset=False)
        xf.set_scientific(False)
        yf.set_scientific(False)
        ax.xaxis.set_major_formatter(xf)
        ax.yaxis.set_major_formatter(yf)

        # Εμβαδό μόνο για ≥3 σημεία
        if n >= 3:
            ax.text(0.02, 0.02,
                    f"Εμβαδό: {format_display(area)} m²\n(Βορράς ↑)",
                    transform=ax.transAxes, fontsize=10,
                    bbox=dict(facecolor="white", alpha=0.7, edgecolor="none"))
        else:
            ax.text(0.02, 0.02, "(Βορράς ↑)",
                    transform=ax.transAxes, fontsize=10,
                    bbox=dict(facecolor="white", alpha=0.7, edgecolor="none"))

        # Ονόματα σημείων
        for p in self.egsa_points:
            plt.text(float(p.x) + 0.8, float(p.y) - 0.8, p.name, fontsize=10)

        # Αποστάσεις πλευρών — για πολύγωνο όλες οι πλευρές, για 2 σημεία μόνο η μία
        if n >= 3:
            edges = [(self.egsa_points[i], self.egsa_points[(i + 1) % n]) for i in range(n)]
        elif n == 2:
            edges = [(self.egsa_points[0], self.egsa_points[1])]
        else:
            edges = []

        for p1, p2 in edges:
            d = self.calculator.calculate_distance(p1, p2)
            mx = (float(p1.x) + float(p2.x)) / 2
            my = (float(p1.y) + float(p2.y)) / 2
            plt.text(mx + 1, my + 1, f"{format_display(d)} m",
                    fontsize=9,
                    bbox=dict(facecolor="white", alpha=0.6, edgecolor="none"))

        plt.grid(True)
        plt.tight_layout()
        plt.show()

        logger.info("Preview displayed")
    
    def _export_shapefile(self):
        """Εξαγωγή σημείων/γραμμής/πολυγώνου σε Shapefile."""
        if not self.egsa_points:
            messagebox.showerror(MESSAGES['error_title'], "Δεν υπάρχουν σημεία.")
            return
        
        # Ask for file path
        shp_path = filedialog.asksaveasfilename(
            defaultextension=".shp",
            filetypes=[("Shapefile", "*.shp")]
        )
        
        if not shp_path:
            return
        
        try:
            geometry_name = self.exporter.export_geometry(self.egsa_points, shp_path)
            messagebox.showinfo("Εξαγωγή Shapefile",
                f"Η εξαγωγή ολοκληρώθηκε επιτυχώς.\n\n"
                f"Τύπος γεωμετρίας: {geometry_name}\n"
                f"Σύστημα αναφοράς: ΕΓΣΑ87 / EPSG:2100")
        except Exception as e:
            logger.exception("Shapefile export failed")
            messagebox.showerror("Σφάλμα Shapefile", f"Αποτυχία εξαγωγής:\n{e}")

    def _choose_dxf_export_options(self):
        """Modal επιλογές για POINT/TEXT entities στο DXF. Η βασική γεωμετρία εξάγεται πάντα."""
        result = {"value": None}

        win = tk.Toplevel(self.root)
        win.title("Επιλογές εξαγωγής DXF")
        win.configure(bg=C["bg"])
        win.transient(self.root)
        win.resizable(False, False)
        win.grab_set()

        include_points_var = tk.BooleanVar(master=win, value=False)
        include_labels_var = tk.BooleanVar(master=win, value=False)

        body = tk.Frame(win, bg=C["bg"])
        body.pack(fill="both", expand=True, padx=18, pady=16)

        tk.Label(
            body, text="Επιλογές DXF",
            font=("Segoe UI", 11, "bold"), fg=C["text"], bg=C["bg"]
        ).pack(anchor="w")
        tk.Label(
            body,
            text="Η γραμμή / το πολύγωνο εξάγεται πάντα στο layer EGSA_BOUNDARY.",
            font=("Segoe UI", 8), fg=C["text_dim"], bg=C["bg"]
        ).pack(anchor="w", pady=(2, 10))

        tk.Checkbutton(
            body, text="Εξαγωγή ξεχωριστών σημείων κορυφών (POINT)",
            variable=include_points_var,
            bg=C["bg"], fg=C["text"], selectcolor=C["white"],
            activebackground=C["bg"], font=("Segoe UI", 9)
        ).pack(anchor="w", pady=3)

        tk.Checkbutton(
            body, text="Εξαγωγή ονομάτων κορυφών (TEXT)",
            variable=include_labels_var,
            bg=C["bg"], fg=C["text"], selectcolor=C["white"],
            activebackground=C["bg"], font=("Segoe UI", 9)
        ).pack(anchor="w", pady=3)

        buttons = tk.Frame(body, bg=C["bg"])
        buttons.pack(fill="x", pady=(14, 0))

        def confirm():
            result["value"] = (include_points_var.get(), include_labels_var.get())
            win.destroy()

        def cancel():
            result["value"] = None
            win.destroy()

        tk.Button(
            buttons, text="Ακύρωση", command=cancel,
            relief="flat", bg=C["output_bg"], fg=C["text"],
            font=("Segoe UI", 9), padx=12, pady=5
        ).pack(side="right")
        tk.Button(
            buttons, text="Συνέχεια", command=confirm,
            relief="flat", bg=C["green_mid"], fg=C["white"],
            activebackground=C["green_dark"], activeforeground=C["white"],
            font=("Segoe UI", 9, "bold"), padx=14, pady=5
        ).pack(side="right", padx=(0, 8))

        win.protocol("WM_DELETE_WINDOW", cancel)
        win.update_idletasks()
        x = self.root.winfo_rootx() + max(0, (self.root.winfo_width() - win.winfo_reqwidth()) // 2)
        y = self.root.winfo_rooty() + max(0, (self.root.winfo_height() - win.winfo_reqheight()) // 2)
        win.geometry(f"+{x}+{y}")
        self.root.wait_window(win)
        return result["value"]

    def _export_dxf(self):
        """Εξαγωγή DXF με προαιρετικά POINT entities και ονόματα κορυφών."""
        if not self.egsa_points:
            messagebox.showerror(MESSAGES['error_title'], "Δεν υπάρχουν σημεία.")
            return
        if not DXF_AVAILABLE:
            messagebox.showerror("DXF", "Η βιβλιοθήκη ezdxf δεν είναι διαθέσιμη σε αυτή την εγκατάσταση.")
            return
        if len(self.egsa_points) < 2:
            messagebox.showwarning(
                "Εξαγωγή DXF",
                "Για DXF απαιτούνται τουλάχιστον δύο σημεία ώστε να δημιουργηθεί γραμμή."
            )
            return

        options = self._choose_dxf_export_options()
        if options is None:
            return
        include_points, include_labels = options

        dxf_path = filedialog.asksaveasfilename(
            defaultextension=".dxf",
            filetypes=[("AutoCAD DXF", "*.dxf")],
            title="Εξαγωγή σε DXF"
        )
        if not dxf_path:
            return

        try:
            info = export_dxf_file(
                self.egsa_points, dxf_path,
                include_points=include_points,
                include_labels=include_labels,
            )
            messagebox.showinfo(
                "Εξαγωγή DXF",
                f"Η εξαγωγή ολοκληρώθηκε επιτυχώς.\n\n"
                f"Γεωμετρία: {info['geometry']}\n"
                f"Layers: {', '.join(info['layers'])}\n"
                f"Σύστημα: ΕΓΣΑ87 · μονάδες σε μέτρα"
            )
            logger.info(
                "DXF exported: %s points=%s labels=%s",
                dxf_path, include_points, include_labels
            )

        except Exception as e:
            messagebox.showerror("Σφάλμα DXF", f"Αποτυχία εξαγωγής:\n{e}")
            logger.exception("DXF export error")

    @staticmethod
    def _auto_point_name(index: int) -> str:
        letters = 'ΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩ'
        return letters[index] if index < len(letters) else f"P{index + 1}"

    def _choose_dxf_polyline(self, candidates: list, source_name: str):
        """Modal επιλογή polyline όταν ένα DXF περιέχει περισσότερες από μία."""
        if len(candidates) == 1:
            return candidates[0]

        choice = {"value": None}
        win = tk.Toplevel(self.root)
        win.title("Επιλογή γεωμετρίας DXF")
        win.transient(self.root)
        win.grab_set()
        win.resizable(True, True)
        win.geometry("620x360")

        tk.Label(win, text="Βρέθηκαν περισσότερες από μία polylines",
                 font=("Segoe UI", 11, "bold"), fg=C["green_dark"]).pack(anchor="w", padx=14, pady=(14, 2))
        tk.Label(win, text=f"Αρχείο: {source_name}\nΕπίλεξε τη γεωμετρία που θέλεις να εισαγάγεις.",
                 font=("Segoe UI", 9), fg=C["text_mid"], justify="left").pack(anchor="w", padx=14, pady=(0, 10))

        frame = tk.Frame(win)
        frame.pack(fill="both", expand=True, padx=14)
        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side="right", fill="y")
        lb = tk.Listbox(frame, font=("Consolas", 9), yscrollcommand=scrollbar.set, exportselection=False)
        lb.pack(fill="both", expand=True)
        scrollbar.config(command=lb.yview)

        for i, item in enumerate(candidates, 1):
            state = "ΚΛΕΙΣΤΗ" if item["closed"] else "ΑΝΟΙΚΤΗ"
            lb.insert(tk.END, f"{i:>2}. {state:<8}  κορυφές: {len(item['points']):>4}  layer: {item['layer']}")
        lb.selection_set(0)

        def accept():
            selected = lb.curselection()
            if selected:
                choice["value"] = candidates[selected[0]]
                win.destroy()

        controls = tk.Frame(win)
        controls.pack(fill="x", padx=14, pady=12)
        tk.Button(controls, text="Ακύρωση", command=win.destroy,
                  font=("Segoe UI", 9), relief="flat", padx=14, pady=6).pack(side="right")
        tk.Button(controls, text="Εισαγωγή επιλεγμένης", command=accept,
                  font=("Segoe UI", 9, "bold"), bg=C["green_mid"], fg=C["white"],
                  activebackground=C["green_dark"], activeforeground=C["white"],
                  relief="flat", padx=14, pady=6).pack(side="right", padx=(0, 8))
        lb.bind("<Double-Button-1>", lambda _e: accept())
        win.protocol("WM_DELETE_WINDOW", win.destroy)
        self.root.wait_window(win)
        return choice["value"]

    def _import_dxf(self):
        """Εισαγωγή κορυφών από LWPOLYLINE/POLYLINE DXF ως δεδομένα ΕΓΣΑ87."""
        if not DXF_AVAILABLE:
            messagebox.showerror("DXF", "Η βιβλιοθήκη ezdxf δεν είναι διαθέσιμη σε αυτή την εγκατάσταση.")
            return

        dxf_path = filedialog.askopenfilename(
            filetypes=[("AutoCAD DXF", "*.dxf")],
            title="Εισαγωγή κορυφών από DXF"
        )
        if not dxf_path:
            return

        try:
            doc = ezdxf.readfile(dxf_path)
            msp = doc.modelspace()
            candidates = []

            for entity in msp:
                kind = entity.dxftype()
                if kind == 'LWPOLYLINE':
                    pts = [(float(x), float(y)) for x, y, *_ in entity.get_points('xy')]
                    closed = bool(entity.closed)
                elif kind == 'POLYLINE' and not bool(getattr(entity, 'is_3d_polyline', False)):
                    pts = [(float(v.dxf.location.x), float(v.dxf.location.y)) for v in entity.vertices]
                    closed = bool(entity.is_closed)
                else:
                    continue

                if len(pts) > 1 and pts[0] == pts[-1]:
                    pts = pts[:-1]
                    closed = True
                if len(pts) >= 2:
                    candidates.append({
                        "points": pts,
                        "closed": closed,
                        "layer": entity.dxf.layer or "0",
                    })

            if not candidates:
                messagebox.showwarning(
                    "Εισαγωγή DXF",
                    "Δεν βρέθηκε LWPOLYLINE ή 2D POLYLINE με τουλάχιστον δύο κορυφές."
                )
                return

            selected = self._choose_dxf_polyline(candidates, Path(dxf_path).name)
            if selected is None:
                return

            pts = selected["points"]
            xs = [x for x, _ in pts]
            ys = [y for _, y in pts]
            span = max(max(xs) - min(xs), max(ys) - min(ys)) if len(pts) > 1 else 0.0
            label_radius = max(2.0, span * 0.05)

            labels = []
            for entity in msp.query('TEXT MTEXT'):
                try:
                    if entity.dxftype() == 'TEXT':
                        label = entity.dxf.text.strip()
                        pos = entity.dxf.insert
                    else:
                        label = entity.plain_text().strip()
                        pos = entity.dxf.insert
                    if label:
                        labels.append((label, float(pos.x), float(pos.y)))
                except Exception:
                    continue

            used_labels = set()
            named_points = []
            for i, (x, y) in enumerate(pts):
                best = None
                for j, (label, tx, ty) in enumerate(labels):
                    if j in used_labels:
                        continue
                    distance = math.hypot(tx - x, ty - y)
                    if distance <= label_radius and (best is None or distance < best[0]):
                        best = (distance, j, label)
                if best:
                    used_labels.add(best[1])
                    name = safe_point_name(best[2], self._auto_point_name(i))
                else:
                    name = self._auto_point_name(i)
                named_points.append((name, x, y))

            unit_names = {
                0: "χωρίς δήλωση", 1: "ίντσες", 2: "πόδια", 3: "μίλια",
                4: "χιλιοστά", 5: "εκατοστά", 6: "μέτρα", 7: "χιλιόμετρα",
            }
            unit_name = unit_names.get(int(doc.units or 0), f"κωδικός {doc.units}")

            plausible = all(100000 <= x <= 900000 and 3800000 <= y <= 4700000 for _, x, y in named_points)
            warnings = []
            if doc.units not in (0, dxf_units.M):
                warnings.append(f"Το DXF δηλώνει μονάδες: {unit_name}, όχι μέτρα.")
            if not plausible:
                warnings.append("Οι τιμές δεν βρίσκονται όλες στο συνήθες εύρος ΕΓΣΑ87 για την Ελλάδα.")

            confirmation = (
                "Το αρχείο θα εισαχθεί ως ΕΓΣΑ87 (EPSG:2100), με μονάδες σε μέτρα.\n\n"
                f"Κορυφές: {len(named_points)}\n"
                f"Γεωμετρία: {'κλειστή' if selected['closed'] else 'ανοικτή'} polyline\n"
                f"Layer: {selected['layer']}"
            )
            if warnings:
                confirmation += "\n\nΠΡΟΕΙΔΟΠΟΙΗΣΗ:\n• " + "\n• ".join(warnings)
            confirmation += "\n\nΝα συνεχιστεί η εισαγωγή;"
            if not messagebox.askyesno("Επιβεβαίωση εισαγωγής DXF", confirmation):
                return

            lines = "\n".join(f"{name} {x:.3f} {y:.3f}" for name, x, y in named_points)
            if self.mode_var.get() == "wgs84":
                self.wgs_direction_var.set("EGSA_TO_WGS")
                self._update_wgs84_ui()
                self.wgs_input.delete("1.0", tk.END)
                self.wgs_input.insert("1.0", lines)
                next_step = "Πάτησε «Μετατροπή σε WGS84» για μετατροπή και έλεγχο."
            else:
                self.mode_var.set("egsa")
                self._switch_mode()
                self.egsa_input.delete("1.0", tk.END)
                self.egsa_input.insert("1.0", lines)
                next_step = "Πάτησε «Επεξεργασία Πολυγώνου» για υπολογισμό και έλεγχο."

            messagebox.showinfo(
                "Εισαγωγή DXF",
                f"Εισήχθησαν {len(named_points)} κορυφές.\n" + next_step
            )
            logger.info(f"DXF imported: {dxf_path}, vertices={len(named_points)}")

        except Exception as e:
            messagebox.showerror("Σφάλμα DXF", f"Αποτυχία εισαγωγής:\n{e}")
            logger.exception("DXF import error")

    def _choose_shp_geometry(self, candidates: list, source_name: str):
        """Modal επιλογή feature/part όταν ένα Shapefile περιέχει περισσότερες γεωμετρίες."""
        if len(candidates) == 1:
            return candidates[0]

        choice = {"value": None}
        win = tk.Toplevel(self.root)
        win.title("Επιλογή γεωμετρίας Shapefile")
        win.transient(self.root)
        win.grab_set()
        win.resizable(True, True)
        win.geometry("700x390")

        tk.Label(win, text="Βρέθηκαν περισσότερες από μία γεωμετρίες",
                 font=("Segoe UI", 11, "bold"), fg=C["green_dark"]).pack(anchor="w", padx=14, pady=(14, 2))
        tk.Label(win, text=f"Αρχείο: {source_name}\nΕπίλεξε το feature/part που θέλεις να εισαγάγεις. Δεν ενώνονται αυτόματα διαφορετικές γεωμετρίες.",
                 font=("Segoe UI", 9), fg=C["text_mid"], justify="left").pack(anchor="w", padx=14, pady=(0, 10))

        frame = tk.Frame(win)
        frame.pack(fill="both", expand=True, padx=14)
        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side="right", fill="y")
        lb = tk.Listbox(frame, font=("Consolas", 9), yscrollcommand=scrollbar.set, exportselection=False)
        lb.pack(fill="both", expand=True)
        scrollbar.config(command=lb.yview)

        for i, item in enumerate(candidates, 1):
            label = item.get("feature_name", "")
            lb.insert(tk.END,
                f"{i:>2}. {item['geometry_type']:<8} feature:{item['feature_index']:>3} "
                f"part:{item['part_index']:>2} κορυφές:{len(item['points']):>5}  {label}")
        lb.selection_set(0)

        def accept():
            selected = lb.curselection()
            if selected:
                choice["value"] = candidates[selected[0]]
                win.destroy()

        controls = tk.Frame(win)
        controls.pack(fill="x", padx=14, pady=12)
        tk.Button(controls, text="Ακύρωση", command=win.destroy,
                  font=("Segoe UI", 9), relief="flat", padx=14, pady=6).pack(side="right")
        tk.Button(controls, text="Εισαγωγή επιλεγμένης", command=accept,
                  font=("Segoe UI", 9, "bold"), bg=C["green_mid"], fg=C["white"],
                  activebackground=C["green_dark"], activeforeground=C["white"],
                  relief="flat", padx=14, pady=6).pack(side="right", padx=(0, 8))
        lb.bind("<Double-Button-1>", lambda _e: accept())
        win.protocol("WM_DELETE_WINDOW", win.destroy)
        self.root.wait_window(win)
        return choice["value"]

    def _import_shp(self):
        """
        Εισαγωγή μίας ρητά επιλεγμένης γεωμετρίας από Shapefile ως ΕΓΣΑ87.
        Multi-feature και multipart αρχεία δεν συγχωνεύονται ποτέ σιωπηρά.
        """
        shp_path = filedialog.askopenfilename(
            filetypes=[("Shapefile", "*.shp")],
            title="Εισαγωγή από Shapefile"
        )
        if not shp_path:
            return

        try:
            prj_path = Path(shp_path).with_suffix(".prj")
            if prj_path.exists():
                prj_text = prj_path.read_text(encoding="utf-8", errors="ignore")
                if not is_epsg2100_prj(prj_text):
                    if not messagebox.askyesno(
                        "Έλεγχος συστήματος αναφοράς",
                        "Το .prj δεν αναγνωρίστηκε από το pyproj ως ΕΓΣΑ87 / EPSG:2100.\n"
                        "Η εισαγωγή δεν πραγματοποιεί μετασχηματισμό συντεταγμένων.\n\n"
                        "Να συνεχιστεί η εισαγωγή θεωρώντας τις τιμές ως ΕΓΣΑ87;"
                    ):
                        return
            else:
                if not messagebox.askyesno(
                    "Δεν βρέθηκε αρχείο .prj",
                    "Δεν υπάρχει συνοδευτικό .prj. Οι συντεταγμένες θα θεωρηθούν ΕΓΣΑ87.\n\nΝα συνεχιστεί;"
                ):
                    return

            dbf_encoding = shapefile_text_encoding(shp_path)
            r = shapefile.Reader(shp_path, encoding=dbf_encoding, encodingErrors="replace")
            candidates = extract_shapefile_candidates(r)

            if not candidates:
                messagebox.showwarning(
                    "Εισαγωγή Shapefile",
                    "Δεν βρέθηκε υποστηριζόμενη γεωμετρία POINT, POLYLINE ή POLYGON."
                )
                return

            selected = self._choose_shp_geometry(candidates, Path(shp_path).name)
            if selected is None:
                return

            pts = selected["points"]
            extracted = []
            if selected["geometry_type"] == "POINT":
                x, y = pts[0]
                extracted.append((safe_point_name(selected["feature_name"], "P1"), x, y))
            else:
                for i, (x, y) in enumerate(pts):
                    extracted.append((self._auto_point_name(i), x, y))

            plausible = all(100000 <= x <= 900000 and 3800000 <= y <= 4700000 for _, x, y in extracted)
            confirmation = (
                f"Γεωμετρία: {selected['geometry_type']}\n"
                f"Feature: {selected['feature_index']} · Part: {selected['part_index']}\n"
                f"Κορυφές: {len(extracted)}\n"
                "Σύστημα: ΕΓΣΑ87 / EPSG:2100 (χωρίς αυτόματο reprojection)"
            )
            if not plausible:
                confirmation += (
                    "\n\nΠΡΟΕΙΔΟΠΟΙΗΣΗ: Οι τιμές δεν βρίσκονται όλες στο συνήθες εύρος "
                    "ΕΓΣΑ87 για την Ελλάδα."
                )
            confirmation += "\n\nΝα συνεχιστεί η εισαγωγή;"
            if not messagebox.askyesno("Επιβεβαίωση εισαγωγής Shapefile", confirmation):
                return

            lines = "\n".join(f"{n} {x:.3f} {y:.3f}" for n, x, y in extracted)
            if self.mode_var.get() == "wgs84":
                self.wgs_direction_var.set("EGSA_TO_WGS")
                self._update_wgs84_ui()
                self.wgs_input.delete("1.0", tk.END)
                self.wgs_input.insert("1.0", lines)
                next_step = "Πάτησε «Μετατροπή σε WGS84» για μετατροπή και έλεγχο."
            else:
                self.mode_var.set("egsa")
                self._switch_mode()
                self.egsa_input.delete("1.0", tk.END)
                self.egsa_input.insert("1.0", lines)
                next_step = "Πάτησε «Επεξεργασία Πολυγώνου» για υπολογισμό και έλεγχο."

            messagebox.showinfo(
                "Εισαγωγή Shapefile",
                f"Εισήχθησαν {len(extracted)} σημεία από το επιλεγμένο "
                f"{selected['geometry_type']}.\n" + next_step
            )
            logger.info(
                "Shapefile imported: %s feature=%s part=%s vertices=%s",
                shp_path, selected["feature_index"], selected["part_index"], len(extracted)
            )

        except Exception as e:
            messagebox.showerror("Σφάλμα Shapefile", f"Αποτυχία εισαγωγής:\n{e}")
            logger.exception("SHP import error")

    def _region_info_text(self, region: str) -> str:
        """Επιστρέφει τα στοιχεία κέντρου του επιλεγμένου φύλλου HATT."""
        if not HATT_COEFFICIENTS or region not in HATT_COEFFICIENTS:
            return ""
        d = HATT_COEFFICIENTS[region]
        phi_s = format_hatt_angle(d.get('phi0'))
        lam_s = format_hatt_angle(d.get('lam0'))
        return f"φ₀={phi_s}   λ₀={lam_s} από Αθήνα"

    def _set_current_region_as_default(self) -> None:
        """Αποθηκεύει το τρέχον φύλλο HATT ως per-user προεπιλογή."""
        display_value = self.region_var.get()
        region = self._region_display_to_name.get(display_value, display_value)
        if region not in HATT_COEFFICIENTS:
            messagebox.showerror("Προεπιλογή HATT", "Δεν είναι δυνατή η αποθήκευση της επιλεγμένης περιοχής.")
            return

        new_settings = dict(self.user_settings)
        new_settings["default_hatt_region"] = region
        new_settings["default_hatt_code"] = HATT_COEFFICIENTS[region].get("code")
        try:
            settings_path = save_user_settings(new_settings)
        except Exception as exc:
            logger.exception("Could not save default HATT region")
            messagebox.showerror(
                "Προεπιλογή HATT",
                f"Δεν ήταν δυνατή η αποθήκευση της προεπιλογής:\n{exc}"
            )
            return

        self.user_settings = new_settings
        self.default_region = region
        default_display = self._region_name_to_display.get(region, region)
        self.default_region_lbl.config(text=f"Προεπιλογή: {default_display}")
        logger.info("Default HATT region saved: %s (%s)", region, settings_path)
        messagebox.showinfo(
            "Προεπιλογή HATT",
            f"Το φύλλο «{default_display}» ορίστηκε ως προεπιλογή.\n\n"
            "Θα επιλέγεται αυτόματα στην επόμενη εκκίνηση του EGSA Suite."
        )

    def _on_region_changed(self, event=None) -> None:
        """Καλείται όταν ο χρήστης επιλέγει νέο φύλλο HATT."""
        display_value = self.region_var.get()
        region = self._region_display_to_name.get(display_value, display_value)
        try:
            self.transformer.set_region(region)
            # Ενημέρωση κωδικού φύλλου
            self.region_code_lbl.config(text=self._region_info_text(region))
            if region in UNVERIFIED_HATT_REGIONS:
                messagebox.showwarning(
                    "Ειδική προειδοποίηση HATT",
                    UNVERIFIED_HATT_REGIONS[region]
                )
            # Αν υπάρχουν ήδη αποτελέσματα, τα καθαρίζουμε (είναι για την παλιά περιοχή)
            if self.HATT_points:
                self.HATT_output.config(state="normal")
                self.HATT_output.delete("1.0", tk.END)
                self.HATT_output.config(state="disabled")
                self.HATT_points.clear()
                self.egsa_points.clear()
                self._clear_area_labels()
            logger.info(f"Region changed to: {region}")
        except KeyError as e:
            messagebox.showerror("Σφάλμα", f"Άγνωστη περιοχή: {e}")

    def _on_close(self):
        """Κλείσιμο εφαρμογής με καθαρισμό GE service."""
        if self.ge_service:
            try:
                self.ge_service.shutdown()
            except Exception:
                pass
        cleanup_temp_files()
        self.root.destroy()

    def _on_ge_camera_update(self, egsa_x: float, egsa_y: float, lon: float, lat: float):
        """Callback: ενημερώνει τα labels του GE παραθύρου με live ΕΓΣΑ87 συντεταγμένες.
        Καλείται από HTTP thread → χρησιμοποιούμε root.after() για thread-safe UI update."""
        def _update():
            self._ge_cam_x_var.set(f"{egsa_x:.3f}")
            self._ge_cam_y_var.set(f"{egsa_y:.3f}")
            self._ge_cam_lon_var.set(f"{lon:.6f}")
            self._ge_cam_lat_var.set(f"{lat:.6f}")
        self.root.after(0, _update)

    def _open_google_earth_window(self):
        """Ανοίγει ή φέρνει στο προσκήνιο το Google Earth Live παράθυρο."""
        if not self.ge_service:
            messagebox.showerror("Google Earth", 
                "Η υπηρεσία Google Earth δεν είναι διαθέσιμη.\n"
                "Βεβαιωθείτε ότι οι φάκελοι kml/, services/, utils/ βρίσκονται δίπλα στο egsa_suite.py")
            return

        # Αν το παράθυρο υπάρχει ήδη, το φέρνουμε μπροστά
        if self.ge_window and self.ge_window.winfo_exists():
            self.ge_window.lift()
            self.ge_window.focus_force()
            # Στέλνουμε τα τρέχοντα σημεία αν υπάρχουν
            self._ge_send_current_points()
            return

        # Δημιουργία νέου παραθύρου
        win = tk.Toplevel(self.root)
        self.ge_window = win
        win.title("🌍 Google Earth Live – ΕΓΣΑ87")
        win.minsize(380, 500)
        win.resizable(True, True)

        # Τοποθέτηση δεξιά από το κύριο παράθυρο
        main_x = self.root.winfo_x()
        main_y = self.root.winfo_y()
        main_w = self.root.winfo_width()
        win.geometry(f"420x540+{main_x + main_w + 10}+{main_y}")

        # ── Τίτλος ────────────────────────────────────────────────
        title_row = tk.Frame(win)
        title_row.pack(fill="x", padx=12, pady=(12, 0))

        title_col = tk.Frame(title_row)
        title_col.pack(side="left")
        tk.Label(title_col, text="Google Earth Live",
                 font=("Segoe UI", 12, "bold"), fg="#2a6e3f").pack(anchor="w")
        tk.Label(title_col, text="Σύνδεση μέσω KML NetworkLink · HTTP localhost",
                 font=("Segoe UI", 8), fg="#888").pack(anchor="w")

        ge_always_on_top_var = tk.BooleanVar(master=win, value=False)
        tk.Checkbutton(
            title_row, text="📌",
            variable=ge_always_on_top_var,
            command=lambda: win.attributes("-topmost", ge_always_on_top_var.get()),
            font=("Segoe UI", 9)
        ).pack(side="right", anchor="ne")

        ttk.Separator(win, orient="horizontal").pack(fill="x", padx=12, pady=10)

        # ── Status ────────────────────────────────────────────────
        status_frame = tk.Frame(win, bg="#f0f8f0", relief="flat", bd=0)
        status_frame.pack(fill="x", padx=12, pady=(0,4))
        self._ge_status_var = tk.StringVar(master=win, value="Αναμονή σύνδεσης από το Google Earth…")
        self._ge_status_label = tk.Label(status_frame,
                 textvariable=self._ge_status_var,
                 font=("Segoe UI", 9), fg="#8a6d00", bg="#fff8df",
                 wraplength=360, justify="left")
        self._ge_status_label.pack(padx=10, pady=8, anchor="w")

        # Δευτερεύον κουμπί για χειροκίνητο άνοιγμα / επαναποστολή
        action_row = tk.Frame(win)
        action_row.pack(fill="x", padx=12, pady=(0, 4))

        tk.Button(action_row, text="🌍  Ξανάνοιγμα Google Earth",
                  command=lambda: self.ge_service.open_in_google_earth(),
                  bg="#1f6feb", fg="white", font=("Segoe UI", 9),
                  relief="flat", padx=10, pady=4).pack(side="left", padx=(0,6))

        tk.Button(action_row, text="🗺  Google Maps",
                  command=self._open_google_maps_browser,
                  font=("Segoe UI", 9), fg="#1f6feb",
                  relief="flat", cursor="hand2", padx=6, pady=4).pack(side="left")
        tk.Label(action_row, text="(pin στο 1ο σημείο)",
                 font=("Segoe UI", 7), fg="#aaa").pack(side="left", padx=4)

        # ── Αποστολή σημείων ──────────────────────────────────────
        step2 = tk.LabelFrame(win, text=" Σημεία στο Google Earth ",
                               font=("Segoe UI", 9), padx=8, pady=8)
        step2.pack(fill="x", padx=12, pady=4)

        pts_info = tk.Label(step2, text="—", font=("Segoe UI", 9), fg="#444")
        pts_info.pack(anchor="w")
        self._ge_pts_info_label = pts_info

        btn_row = tk.Frame(step2)
        btn_row.pack(pady=(6, 0))

        tk.Button(btn_row, text="📍 Στείλε σημεία στο GE",
                  command=lambda: [self._ge_send_current_points(),
                                   self.root.after(500, self._ge_trigger_fly_to)],
                  bg="#2a6e3f", fg="white", font=("Segoe UI", 9, "bold"),
                  width=20).pack(side="left", padx=4)

        tk.Button(btn_row, text="🗑 Καθαρισμός",
                  command=self._ge_clear_points,
                  width=10).pack(side="left", padx=4)

        # ── Camera Tracking ────────────────────────────────────────
        cam_frame = tk.LabelFrame(win, text=" Camera Tracking – Κέντρο οθόνης GE ",
                                   font=("Segoe UI", 9), padx=8, pady=8)
        cam_frame.pack(fill="x", padx=12, pady=4)

        tk.Label(cam_frame, 
                 text="Καθώς κινείτε τον χάρτη στο Google Earth,\n"
                      "οι ΕΓΣΑ87 συντεταγμένες ενημερώνονται live:",
                 font=("Segoe UI", 9), justify="left").pack(anchor="w")

        grid = tk.Frame(cam_frame)
        grid.pack(anchor="w", pady=(6, 0))

        lbl_style = {"font": ("Segoe UI", 9), "anchor": "w", "width": 12}
        val_style = {"font": ("Consolas", 10, "bold"), "fg": "#1f6feb", "anchor": "w", "width": 16}

        for row, (label, var) in enumerate([
            ("Χ ΕΓΣΑ87:",   self._ge_cam_x_var),
            ("Υ ΕΓΣΑ87:",   self._ge_cam_y_var),
            ("Longitude:",  self._ge_cam_lon_var),
            ("Latitude:",   self._ge_cam_lat_var),
        ]):
            tk.Label(grid, text=label, **lbl_style).grid(row=row, column=0, sticky="w", pady=1)
            tk.Label(grid, textvariable=var, **val_style).grid(row=row, column=1, sticky="w", pady=1)

        ttk.Separator(win, orient="horizontal").pack(fill="x", padx=12, pady=8)

        tk.Label(win, text="Το NetworkLink ανανεώνεται αυτόματα κάθε 1 δευτερόλεπτο.",
                 font=("Segoe UI", 8), fg="#aaa").pack()

        # Αποστολή σημείων αμέσως (polygon/points στη μνήμη)
        self._ge_send_current_points()
        # Άνοιγμα GE
        self.ge_service.open_in_google_earth()
        # FlyTo μετά από 4 δευτερόλεπτα — δίνουμε χρόνο στο GE να φορτώσει το NetworkLink
        self.root.after(4000, self._ge_trigger_fly_to)
        self.root.after(500, self._ge_update_connection_status)

    def _ge_update_connection_status(self):
        """Εμφανίζει πραγματική κατάσταση σύνδεσης βάσει του τελευταίου HTTP poll."""
        if not self.ge_window or not self.ge_window.winfo_exists() or not self.ge_service:
            return
        import time
        age = time.time() - self.ge_service.last_poll_time if self.ge_service.last_poll_time else None
        if age is not None and age < 3.5:
            self._ge_status_var.set(f"✔ Συνδεδεμένο · θύρα {self.ge_service.server.port} · τελευταία ενημέρωση πριν {age:.1f}s")
            self._ge_status_label.config(fg="#2a6e3f", bg="#f0f8f0")
        elif age is not None:
            self._ge_status_var.set("⚠ Η σύνδεση δεν ανανεώνεται. Ελέγξτε το NetworkLink στο Google Earth.")
            self._ge_status_label.config(fg="#9a5700", bg="#fff3df")
        else:
            self._ge_status_var.set("Αναμονή σύνδεσης από το Google Earth…")
            self._ge_status_label.config(fg="#8a6d00", bg="#fff8df")
        self.root.after(1000, self._ge_update_connection_status)

    def _ge_trigger_fly_to(self):
        """Επαναστέλνει το FlyTo μετά από καθυστέρηση ώστε το GE να έχει φορτώσει."""
        if not self.ge_service or not self.egsa_points:
            return
        points = self.egsa_points
        cx = sum(float(p.x) for p in points) / len(points)
        cy = sum(float(p.y) for p in points) / len(points)
        self.ge_service.send_point(cx, cy, "Κέντρο πολυγώνου", fly_to=True)
        logger.info("FlyTo re-triggered after GE load delay")

    def _ge_send_current_points(self):
        """Στέλνει τα τρέχοντα egsa_points στο Google Earth.
        ≥3 σημεία → polygon · 1-2 σημεία → individual saved points."""
        if not self.ge_service:
            return

        points = self.egsa_points
        if not points:
            if hasattr(self, '_ge_pts_info_label'):
                self._ge_pts_info_label.config(
                    text="Δεν υπάρχουν σημεία. Κάνε πρώτα Υπολογισμό.", fg="#cc0000")
            return

        from services.google_earth_service import GEPoint, _egsa_to_wgs84

        self.ge_service.clear_saved_points()

        if len(points) >= 3:
            # Μετατροπή σε GEPoint για τον polygon generator
            ge_points = []
            for p in points:
                lon, lat = _egsa_to_wgs84(float(p.x), float(p.y))
                ge_points.append(GEPoint(
                    x=float(p.x), y=float(p.y),
                    longitude=lon, latitude=lat,
                    name=p.name
                ))
            self.ge_service.send_polygon(ge_points, "Πολύγωνο ΕΓΣΑ87")
            # FlyTo στο κέντρο του πολυγώνου
            cx = sum(float(p.x) for p in points) / len(points)
            cy = sum(float(p.y) for p in points) / len(points)
            self.ge_service.send_point(cx, cy, "Κέντρο πολυγώνου", fly_to=True)
            msg = f"✔  Πολύγωνο {len(points)} κορυφών στάλθηκε στο Google Earth."
        else:
            # 1-2 σημεία → individual points
            for p in points:
                self.ge_service.add_saved_point(float(p.x), float(p.y), p.name)
            first = points[0]
            self.ge_service.send_point(float(first.x), float(first.y), first.name, fly_to=True)
            msg = f"✔  {len(points)} σημεία στάλθηκαν στο Google Earth."

        if hasattr(self, '_ge_pts_info_label'):
            self._ge_pts_info_label.config(text=msg, fg="#2a6e3f")

        logger.info(msg)

    def _ge_clear_points(self):
        """Καθαρισμός saved points από το Google Earth."""
        if self.ge_service:
            self.ge_service.clear_saved_points()
        if hasattr(self, '_ge_pts_info_label'):
            self._ge_pts_info_label.config(text="Τα σημεία καθαρίστηκαν.", fg="#888")

    def _open_google_maps_browser(self):
        """Ανοίγει τα τρέχοντα σημεία στο Google Maps σε browser.
        Δείχνει pin στο πρώτο σημείο (το Google Maps URL API δεν υποστηρίζει
        πολλαπλά custom markers χωρίς My Maps)."""
        if not self.egsa_points:
            messagebox.showwarning("Google Maps", "Δεν υπάρχουν σημεία. Κάνε πρώτα Υπολογισμό.")
            return

        first = self.egsa_points[0]
        lon, lat = self.transformer.egsa_to_wgs84(first.x, first.y)

        # ?q=lat,lon τοποθετεί πραγματικό pin marker στο σημείο
        url = f"https://www.google.com/maps?q={lat:.8f},{lon:.8f}"

        webbrowser.open(url)
        logger.info(f"Google Maps browser opened (pin on '{first.name}'): {url}")

    def _show_about(self):
        """Εμφάνιση συνοπτικών πληροφοριών έκδοσης και τεχνικής ταυτότητας."""
        win = tk.Toplevel(self.root)
        win.title(f"Σχετικά με το EGSA Suite {APP_VERSION}")
        win.geometry("600x520")
        win.minsize(520, 420)

        header = tk.Frame(win, bg=C["green_dark"])
        header.pack(fill="x")
        tk.Label(header, text="EGSA Suite", font=("Segoe UI", 17, "bold"),
                 bg=C["green_dark"], fg=C["header_fg"]).pack(anchor="w", padx=18, pady=(14, 0))
        tk.Label(header, text=f"Έκδοση {APP_VERSION} · Εργαλεία συντεταγμένων HATT / ΕΓΣΑ87 / WGS84",
                 font=("Segoe UI", 9), bg=C["green_dark"], fg="#a8cdb2").pack(anchor="w", padx=18, pady=(2, 14))

        frame = tk.Frame(win, bg=C["white"])
        frame.pack(fill="both", expand=True)
        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side="right", fill="y")
        text = tk.Text(frame, wrap="word", padx=20, pady=18,
                       yscrollcommand=scrollbar.set, font=("Segoe UI", 10),
                       bg=C["white"], fg=C["text"], relief="flat", bd=0)
        text.pack(fill="both", expand=True)
        scrollbar.config(command=text.yview)

        about_text = f"""ΣΚΟΠΟΣ

Το EGSA Suite είναι εφαρμογή υποβοήθησης τεχνικών εργασιών για μετατροπή συντεταγμένων HATT → ΕΓΣΑ87 και ΕΓΣΑ87 ↔ WGS84, διαχείριση κορυφών και ανταλλαγή γεωμετρίας με GIS, CAD και Google Earth.

ΚΥΡΙΕΣ ΔΥΝΑΤΟΤΗΤΕΣ

• Πολυωνυμικός μετασχηματισμός HATT → ΕΓΣΑ87 για 390 εγγραφές μετασχηματισμού (387 κωδικοί φύλλων).
• Εισαγωγή σημείων απευθείας σε ΕΓΣΑ87.
• Αμφίδρομη μετατροπή ΕΓΣΑ87 ↔ WGS84 (EPSG:2100 ↔ EPSG:4326) με δεκαδικές μοίρες ή μοίρες/λεπτά/δευτερόλεπτα.
• Υπολογισμός αποστάσεων και εμβαδού.
• Προβολή σε χάρτη, Google Maps και Google Earth Pro.
• Εισαγωγή και εξαγωγή Shapefile και DXF.
• Ανταλλαγή γεωμετρίας με GIS και CAD, με διατήρηση της σειράς των κορυφών.

ΤΕΧΝΙΚΕΣ ΠΑΡΑΤΗΡΗΣΕΙΣ

Οι εξαγωγές SHP χρησιμοποιούν ΕΓΣΑ87 / EPSG:2100. Τα DXF δεν διαθέτουν αξιόπιστη ενσωματωμένη πληροφορία CRS· κατά την εισαγωγή θεωρούνται συντεταγμένες ΕΓΣΑ87 σε μέτρα και απαιτείται έλεγχος από τον χρήστη.

Οι συντελεστές HATT βασίζονται στην επίσημη έκδοση ΟΚΧΕ/ΓΥΣ/ΕΜΠ. Η ίδια η έκδοση διευκρινίζει ότι τα πολυώνυμα προορίζονται για ένταξη χαρτογραφικών εργασιών και δεν παρέχουν γεωδαιτική ακρίβεια. Η ορθή χρήση εξαρτάται από τη σωστή επιλογή φύλλου και από την ταυτότητα/ποιότητα των αρχικών HATT δεδομένων, ιδίως ως προς την υλοποίηση μετά την τμηματική συνόρθωση των δικτύων μετά το 1963. Το εργαλείο δεν αντικαθιστά επίσημη γεωδαιτική μελέτη, τοπογραφική αποτύπωση ή νομική αξιολόγηση.

ΣΧΕΔΙΑΣΜΟΣ ΚΑΙ ΑΝΑΠΤΥΞΗ

Δημήτρης Τσακνάκης · Δασολόγος
Υλοποίηση και έλεγχος με τη συνδρομή σύγχρονων εργαλείων τεχνητής νοημοσύνης.

ΛΟΓΙΣΜΙΚΟ ΑΝΟΙΧΤΟΥ ΚΩΔΙΚΑ

Η ενσωμάτωση Google Earth KML NetworkLink, τοπικού HTTP server και camera tracking βασίζεται και προσαρμόζει στοιχεία του έργου egsa2ge του dasaki-greece, το οποίο διανέμεται με άδεια MIT. Η σχετική απόδοση πίστωσης και η άδεια διατηρούνται στο THIRD_PARTY_NOTICES.md. Το EGSA Suite διανέμεται ως λογισμικό ανοικτού κώδικα με άδεια MIT.
"""
        text.insert("1.0", about_text)
        text.config(state="disabled")

    def _show_help(self):
        """Εμφάνιση καθαρών, προσανατολισμένων στη ροή εργασίας οδηγιών."""
        win = tk.Toplevel(self.root)
        win.title(f"Οδηγίες χρήσης · EGSA Suite {APP_VERSION}")
        win.geometry("700x620")
        win.minsize(600, 480)

        header = tk.Frame(win, bg=C["green_dark"])
        header.pack(fill="x")
        tk.Label(header, text="Οδηγίες χρήσης", font=("Segoe UI", 15, "bold"),
                 bg=C["green_dark"], fg=C["header_fg"]).pack(anchor="w", padx=18, pady=(13, 0))
        tk.Label(header, text="Βασική ροή: εισαγωγή → υπολογισμός → έλεγχος → εξαγωγή",
                 font=("Segoe UI", 9), bg=C["green_dark"], fg="#a8cdb2").pack(anchor="w", padx=18, pady=(2, 13))

        frame = tk.Frame(win, bg=C["white"])
        frame.pack(fill="both", expand=True)
        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side="right", fill="y")
        text = tk.Text(frame, wrap="word", padx=20, pady=18,
                       yscrollcommand=scrollbar.set, font=("Segoe UI", 10),
                       bg=C["white"], fg=C["text"], relief="flat", bd=0)
        text.pack(fill="both", expand=True)
        scrollbar.config(command=text.yview)

        help_text = """1. ΕΠΙΛΟΓΗ ΛΕΙΤΟΥΡΓΙΑΣ

Μετατροπή HATT → ΕΓΣΑ87
Επίλεξε το σωστό φύλλο HATT από τη λίστα, όπου εμφανίζονται μαζί ο αριθμός φύλλου και η περιοχή. Αν το χρησιμοποιείς συχνά, πάτησε «Ορισμός ως προεπιλογή» ώστε να επιλέγεται αυτόματα στις επόμενες εκκινήσεις του προγράμματος. Έπειτα εισήγαγε τις τοπικές συντεταγμένες και πάτησε «Μετατροπή σε ΕΓΣΑ87».

Δημιουργία πολυγώνου ΕΓΣΑ87
Χρησιμοποίησέ την όταν οι συντεταγμένες είναι ήδη σε ΕΓΣΑ87 ή όταν εισάγονται από Shapefile ή DXF.

ΕΓΣΑ87 ↔ WGS84
Χρησιμοποίησέ την για αμφίδρομη μετατροπή μεταξύ ΕΓΣΑ87 / EPSG:2100 και WGS84 / EPSG:4326. Επίλεξε πρώτα την κατεύθυνση μετατροπής και έπειτα τη μορφή WGS84: δεκαδικές μοίρες ή μοίρες/λεπτά/δευτερόλεπτα.

2. ΜΟΡΦΗ ΕΙΣΟΔΟΥ

Κάθε γραμμή περιέχει:
  Όνομα  X  Y
ή:
  X  Y

Χωρίς όνομα, η εφαρμογή δημιουργεί αυτόματα ονομασίες κορυφών. Υποστηρίζονται κενό, tab και ελληνικές/διεθνείς μορφές δεκαδικών. Έλεγξε πάντοτε τη σειρά X, Y.

Στην καρτέλα ΕΓΣΑ87 ↔ WGS84:
• Για δεκαδικές μοίρες η σειρά εισόδου WGS84 είναι Latitude, Longitude.
• Για μοίρες/λεπτά/δευτερόλεπτα η εισαγωγή γίνεται σε ξεχωριστά αριθμητικά πεδία για °, ′ και ″, χωρίς να χρειάζεται πληκτρολόγηση συμβόλων.
• Η επιλογή N/S για Latitude και E/W για Longitude είναι καθολική και εφαρμόζεται σε όλα τα σημεία του πίνακα.
• Ο πίνακας ξεκινά με μία γραμμή και προσθέτει αυτόματα νέα κενή γραμμή μόλις αρχίσεις να συμπληρώνεις την τελευταία.

3. ΥΠΟΛΟΓΙΣΜΟΣ ΚΑΙ ΕΛΕΓΧΟΣ

• 1 σημείο: σημειακή γεωμετρία.
• 2 σημεία: ανοικτό τμήμα και απόσταση.
• 3 ή περισσότερα: κλειστό πολύγωνο και εμβαδόν.

Χρησιμοποίησε «Σχήμα & Εμβαδό» για οπτικό έλεγχο της σειράς των κορυφών, των πλευρών και του κλεισίματος πριν από κάθε επαγγελματική εξαγωγή. Στη ροή WGS84 η γεωμετρία μετατρέπεται εσωτερικά σε ΕΓΣΑ87 και το εμβαδόν υπολογίζεται σε ΕΓΣΑ87, όχι πάνω στις γεωγραφικές μοίρες.

4. ΧΑΡΤΗΣ ΚΑΙ GOOGLE EARTH

Η προβολή χάρτη μετατρέπει προσωρινά τα δεδομένα σε WGS84. Το Google Earth Live ανοίγει τοπικό KML NetworkLink, εμφανίζει τα σημεία ή το πολύγωνο και ενημερώνει τις συντεταγμένες του κέντρου οθόνης. Η σύνδεση λειτουργεί μόνο όσο παραμένει ανοικτό το EGSA Suite.

5. ΕΙΣΑΓΩΓΗ SHAPEFILE

Η εφαρμογή διαβάζει POINT, POLYLINE και POLYGON. Αν υπάρχουν πολλά features ή multipart γεωμετρίες, ζητά ρητή επιλογή feature/part και δεν τα ενώνει αυτόματα. Το συνοδευτικό .prj ελέγχεται μέσω pyproj. Δεν μετασχηματίζει αυτόματα άγνωστο CRS· επιβεβαίωσε ότι το αρχείο είναι ΕΓΣΑ87 / EPSG:2100.

6. ΕΞΑΓΩΓΗ SHAPEFILE

• 1 σημείο → POINT
• 2 σημεία → POLYLINE
• 3+ σημεία → POLYGON

Δημιουργούνται τα συνοδευτικά .prj και .cpg. Πριν από εξαγωγή polygon ελέγχονται διπλότυπες κορυφές, μηδενικό εμβαδόν, αναμενόμενο εύρος ΕΓΣΑ87 και αυτοτομές.

7. ΕΙΣΑΓΩΓΗ DXF

Η εφαρμογή θεωρεί ότι το DXF περιέχει συντεταγμένες ΕΓΣΑ87 (EPSG:2100) σε μέτρα. Διαβάζονται LWPOLYLINE και 2D POLYLINE. Αν υπάρχουν περισσότερες από μία, εμφανίζεται παράθυρο επιλογής. Τα κοντινά TEXT/MTEXT μπορούν να χρησιμοποιηθούν ως ονόματα κορυφών· διαφορετικά δημιουργούνται αυτόματα.

Αν οι δηλωμένες μονάδες ή το εύρος των τιμών φαίνονται ασυνήθιστα, εμφανίζεται σχετική προειδοποίηση πριν από την εισαγωγή.

8. ΕΞΑΓΩΓΗ DXF

Η βασική γεωμετρία εξάγεται πάντα στο layer EGSA_BOUNDARY ως ανοικτή ή κλειστή LWPOLYLINE. Πριν από την αποθήκευση μπορείς προαιρετικά να προσθέσεις:
• EGSA_POINTS — ξεχωριστά POINT entities στις κορυφές.
• EGSA_LABELS — ονόματα κορυφών ως TEXT.

Οι δύο προαιρετικές επιλογές είναι απενεργοποιημένες από προεπιλογή για καθαρότερο DXF.

9. ΕΠΑΓΓΕΛΜΑΤΙΚΟΣ ΕΛΕΓΧΟΣ

Πριν χρησιμοποιήσεις αποτέλεσμα σε διοικητική, τεχνική ή νομική διαδικασία:
• επιβεβαίωσε το φύλλο HATT,
• έλεγξε CRS και μονάδες,
• επαλήθευσε τουλάχιστον ένα γνωστό σημείο,
• έλεγξε οπτικά τη σειρά και το κλείσιμο των κορυφών,
• κράτησε αντίγραφο των αρχικών δεδομένων.
"""
        text.insert("1.0", help_text)
        text.config(state="disabled")


# ==================== MAIN ====================

def main():
    """Entry point της εφαρμογής."""
    root = tk.Tk()
    root.withdraw()                      # κρύβουμε μέχρι να φορτώσει το UI
    _update_splash(_splash, "Έτοιμο!", 1.0)
    app = HATTEgsaApp(root)
    _close_splash(_splash)               # κλείνει το splash
    root.deiconify()                     # εμφανίζουμε το κύριο παράθυρο
    root.lift()
    root.focus_force()

    try:
        root.mainloop()
    except KeyboardInterrupt:
        logger.info("Application interrupted by user")
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        messagebox.showerror("Κρίσιμο Σφάλμα", 
                           f"Η εφαρμογή αντιμετώπισε πρόβλημα:\n{e}")
    finally:
        cleanup_temp_files()
        logger.info("Application closed")


if __name__ == "__main__":
    main()