# language: Python, file: app.py, target: Windows 10
import os
import sys
import time
import urllib.request
import json
import threading
import subprocess
from core.server import DownloadManagerRouter, start_background_server

def forward_arg_to_running_instance(arg_str):
    try:
        payload = json.dumps({"url": arg_str, "kind": "auto"}).encode("utf-8")
        req = urllib.request.Request(
            "http://127.0.0.1:6800/api/prompt_download",
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=2.5) as resp:
            if resp.status == 200:
                return True
    except Exception:
        return False
    return False

def create_tray_icon(window_ref, router):
    try:
        import pystray
        from PIL import Image, ImageDraw

        ico_file = router.base_dir / "icons" / "app_icon.ico"
        img = Image.open(ico_file) if ico_file.exists() else Image.new("RGB", (64, 64), color=(37, 99, 235))
        d = ImageDraw.Draw(img)
        d.polygon([(36, 10), (16, 36), (30, 36), (26, 54), (48, 28), (34, 28)], fill=(255, 255, 255))

        def on_show(icon, item):
            if window_ref.get("win"):
                try:
                    window_ref["win"].show()
                    window_ref["win"].restore()
                except Exception:
                    subprocess.Popen(["cmd", "/c", "start", "http://127.0.0.1:6800/"])
            else:
                subprocess.Popen(["cmd", "/c", "start", "http://127.0.0.1:6800/"])

        def on_open_folder(icon, item):
            os.startfile(str(router.download_dir))

        def on_quit(icon, item):
            icon.stop()
            router.aria2.shutdown()
            os._exit(0)

        menu = pystray.Menu(
            pystray.MenuItem("Open IDM By Rashid", on_show, default=True),
            pystray.MenuItem("Open Downloads Folder", on_open_folder),
            pystray.MenuItem("Exit Completely", on_quit)
        )
        icon = pystray.Icon("IDMByRashid", img, "IDM By Rashid — 16x, 4K & Magnet Ready", menu)
        threading.Thread(target=icon.run, daemon=True).start()
        return icon
    except Exception:
        return None

def main():
    cli_arg = sys.argv[1].strip() if len(sys.argv) > 1 else ""

    # If IDM By Rashid is already running, pass the clicked Magnet / .torrent straight to it and bring window up!
    if cli_arg and forward_arg_to_running_instance(cli_arg):
        return

    router = DownloadManagerRouter()
    start_background_server(router, port=6800)
    time.sleep(0.4)

    if cli_arg:
        forward_arg_to_running_instance(cli_arg)

    create_tray_icon(router.window_ref, router)

    try:
        import webview
        win = webview.create_window(
            "IDM By Rashid — Pro High-Speed Download Manager",
            "http://127.0.0.1:6800/",
            width=1280,
            height=800,
            min_size=(1020, 640),
            background_color="#F8FAFC"
        )
        router.window_ref["win"] = win
        webview.start()
    except Exception:
        subprocess.Popen(["cmd", "/c", "start", "msedge", "--app=http://127.0.0.1:6800/"])
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            pass
    finally:
        router.aria2.shutdown()

if __name__ == "__main__":
    main()
