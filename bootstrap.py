# language: Python 3.11, file: bootstrap.py
# run once inside "IDM By Rashid":   python bootstrap.py
# rerun safe: existing files are skipped. use --force to overwrite.

import sys
import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parent

FILES = {
    # --- top level ---
    "README.md": """# IDM By Rashid

Personal download manager. Phased build.

- Phase 0: skeleton, window, logging, settings. (done)
- Phase 1: HTTP engine, segmented + resume, CLI testable.
- Phase 2: torrents (libtorrent).
- Phase 3: yt-dlp routing for video sites.
- Phase 4: browser extension + native messaging.
- Phase 5: packaging to .exe.
""",

    "requirements.txt": """PySide6>=6.6
httpx>=0.27
""",

    "run.py": """# language: Python 3.11, file: run.py
from app.main import main
if __name__ == "__main__":
    raise SystemExit(main())
""",

    ".gitignore": """.venv/
__pycache__/
*.pyc
data/
build/
dist/
*.spec
""",

    # --- package markers ---
    "app/__init__.py": "",
    "app/core/__init__.py": "",
    "app/download/__init__.py": "",
    "app/ui/__init__.py": "",
    "app/assets/.gitkeep": "",
    "data/.gitkeep": "",

    # --- core ---
    "app/core/logger.py": '''# language: Python 3.11, file: app/core/logger.py
import logging
from pathlib import Path

LOG_DIR = Path(__file__).resolve().parents[2] / "data"
LOG_DIR.mkdir(parents=True, exist_ok=True)

def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger
    logger.setLevel(logging.DEBUG)

    fh = logging.FileHandler(LOG_DIR / "app.log", encoding="utf-8")
    fh.setFormatter(logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s"))

    ch = logging.StreamHandler()
    ch.setFormatter(logging.Formatter("[%(levelname)s] %(name)s: %(message)s"))

    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger
''',

    "app/core/settings.py": '''# language: Python 3.11, file: app/core/settings.py
import json
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[2] / "data"
SETTINGS_FILE = DATA_DIR / "settings.json"

DEFAULTS = {
    "download_dir": str(DATA_DIR / "downloads"),
    "max_connections": 8,
    "theme": "dark",
}

def load() -> dict:
    if SETTINGS_FILE.exists():
        try:
            return {**DEFAULTS, **json.loads(SETTINGS_FILE.read_text("utf-8"))}
        except Exception:
            pass
    return dict(DEFAULTS)

def save(cfg: dict) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    SETTINGS_FILE.write_text(json.dumps(cfg, indent=2), "utf-8")
''',

    # --- download engine (stub — phase 1 fills this) ---
    "app/download/engine.py": '''# language: Python 3.11, file: app/download/engine.py
# Phase 1 will implement segmented + resumable HTTP downloads here.
# Kept as a stub so imports work and the folder is real.

class DownloadEngine:
    """Placeholder. Phase 1 replaces this with a real engine."""

    def __init__(self) -> None:
        self.jobs: list = []

    def add(self, url: str) -> None:
        raise NotImplementedError("engine lands in phase 1")
''',

    # --- ui ---
    "app/ui/window.py": '''# language: Python 3.11, file: app/ui/window.py
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QListWidget, QLabel
)
from app.core import settings
from app.core.logger import get_logger

log = get_logger(__name__)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("IDM By Rashid — Phase 0")
        self.resize(900, 560)

        self.cfg = settings.load()

        root = QWidget()
        layout = QVBoxLayout(root)

        bar = QHBoxLayout()
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("paste a URL (not wired yet — phase 1)")
        self.add_btn = QPushButton("Add")
        bar.addWidget(self.url_input, 1)
        bar.addWidget(self.add_btn)
        layout.addLayout(bar)

        self.jobs = QListWidget()
        self.jobs.addItem("(no downloads yet — engine lands in phase 1)")
        layout.addWidget(self.jobs, 1)

        self.status = QLabel(f"download dir: {self.cfg['download_dir']}")
        layout.addWidget(self.status)

        self.setCentralWidget(root)
        log.info("main window constructed")
''',

    # --- entry point ---
    "app/main.py": '''# language: Python 3.11, file: app/main.py
import sys
from PySide6.QtWidgets import QApplication
from app.ui.window import MainWindow
from app.core.logger import get_logger

log = get_logger(__name__)

def main() -> int:
    log.info("dlm starting")
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    return app.exec()

if __name__ == "__main__":
    raise SystemExit(main())
''',
}

DIRS = [
    "app", "app/core", "app/download", "app/ui", "app/assets", "data",
]


def write_file(path: Path, content: str, force: bool) -> str:
    if path.exists() and not force:
        return f"skip   {path.relative_to(ROOT)}"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return f"write  {path.relative_to(ROOT)}"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true",
                    help="overwrite existing files")
    args = ap.parse_args()

    print(f"bootstrap root: {ROOT}\n")

    for d in DIRS:
        (ROOT / d).mkdir(parents=True, exist_ok=True)
        print(f"mkdir  {d}")

    print()
    for rel, content in FILES.items():
        print(write_file(ROOT / rel, content, args.force))

    print("\ndone. next:")
    print("  python -m venv .venv")
    if sys.platform.startswith("win"):
        print(r"  .venv\Scripts\activate")
    else:
        print("  source .venv/bin/activate")
    print("  pip install -r requirements.txt")
    print("  python run.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())