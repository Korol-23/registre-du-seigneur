#!/usr/bin/env python3
"""Le Registre du Seigneur (Rise of Lords) — open this file to start it.

Opens the tool in your browser and saves every change to rol-data.json
in this folder (a daily copy goes to the "sauvegardes" folder, 30 days kept).
Nothing keeps running afterwards: the program stops by itself about a minute
after you close the tab.

Linux: double-click start.py (or right-click > "Run as a Program"), or run  python3 start.py
Only the Python standard library is used: nothing to install.
"""
import datetime
import hashlib
import http.server
import json
import os
import shutil
import socket
import sys
import threading
import webbrowser

# silence the harmless GTK message "Not loading module atk-bridge" printed by some Linux browsers
os.environ.setdefault("NO_AT_BRIDGE", "1")

HERE = os.path.dirname(os.path.abspath(__file__))
PAGE = "registre-du-seigneur.html"
# show each message at once, even when the output is not a terminal (pythonw on Windows has no output at all)
if sys.stdout is not None and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(line_buffering=True)
# identifies this copy of the Registre (its folder) without revealing the folder's path
FOLDER_ID = hashlib.sha256(os.path.realpath(HERE).encode("utf-8")).hexdigest()[:16]
DATA = os.path.join(HERE, "rol-data.json")
BACKUPS = os.path.join(HERE, "sauvegardes")
KEEP_DAYS = 30
PORT = 8765  # the page looks for the calculator here when opened by double-click
MAX_BYTES = 20 * 1024 * 1024
LOCK = threading.Lock()
IDLE_LIMIT = 300      # stop if the page hasn't been heard from for 5 minutes
CLOSE_GRACE = 75      # stop this long after the tab was closed (unless it reopens)
ALIVE = {"last": None, "bye": None}


def touch():
    ALIVE["last"] = datetime.datetime.now().timestamp()
    ALIVE["bye"] = None


def watchdog(server, started):
    import time
    while True:
        time.sleep(5)
        now = datetime.datetime.now().timestamp()
        last = ALIVE["last"] or started
        if ALIVE["bye"] and now - ALIVE["bye"] > CLOSE_GRACE:
            break
        if now - last > IDLE_LIMIT:
            break
    print("Registre ferme : arret du programme.")
    server.shutdown()


def free_port(start=8765):
    for port in range(start, start + 50):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            # same rule as the server itself: a port left in TIME_WAIT by the previous run can be reused
            # (not on Windows, where this option would allow two programs on the same port)
            if os.name != "nt":
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            try:
                s.bind(("127.0.0.1", port))
                return port
            except OSError:
                continue
    raise SystemExit("No free port found between 8765 and 8814.")


def daily_backup():
    """Copy the current data file to sauvegardes/rol-data-YYYY-MM-DD.json once per day."""
    if not os.path.exists(DATA):
        return
    os.makedirs(BACKUPS, exist_ok=True)
    target = os.path.join(BACKUPS, "rol-data-%s.json" % datetime.date.today().isoformat())
    if not os.path.exists(target):
        shutil.copy2(DATA, target)
        olds = sorted(f for f in os.listdir(BACKUPS) if f.startswith("rol-data-") and f.endswith(".json"))
        for f in olds[:-KEEP_DAYS]:
            try:
                os.remove(os.path.join(BACKUPS, f))
            except OSError:
                pass


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=HERE, **kw)

    def log_message(self, fmt, *args):  # keep the window quiet
        pass

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def _origin_ok(self):
        # Refuse writes coming from any other website open in the browser.
        origin = self.headers.get("Origin")
        host = self.headers.get("Host", "")
        return origin in ("http://" + host,) and host.split(":")[0] in ("127.0.0.1", "localhost")

    def _send_json(self, code, obj):
        body = json.dumps(obj).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        path = self.path.split("?")[0]
        if path == "/":
            self.send_response(302)
            self.send_header("Location", "/" + PAGE)
            self.end_headers()
            return
        if path == "/api/info":
            return self._send_json(200, {"app": "registre", "page": PAGE, "folder": FOLDER_ID})
        if path == "/api/ping":
            touch()
            return self._send_json(200, {"ok": True})
        if path == "/api/hello.js":
            body = ("window.__ROLC_SERVER__=%s;" % json.dumps({"page": PAGE, "folder": FOLDER_ID})).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/javascript")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        if path == "/api/data":
            with LOCK:
                if os.path.exists(DATA):
                    with open(DATA, "r", encoding="utf-8") as f:
                        try:
                            data = json.load(f)
                        except ValueError:
                            return self._send_json(500, {"error": "rol-data.json is damaged; restore one from the sauvegardes folder"})
                else:
                    data = {"app": "rol-calc", "version": 1, "profiles": {}}
            return self._send_json(200, data)
        return super().do_GET()

    def do_POST(self):
        if self.path.split("?")[0] == "/api/bye":
            if self._origin_ok():
                ALIVE["bye"] = datetime.datetime.now().timestamp()
            return self._send_json(200, {"ok": True})
        if self.path.split("?")[0] != "/api/data":
            return self._send_json(404, {"error": "not found"})
        if not self._origin_ok():
            return self._send_json(403, {"error": "forbidden"})
        length = int(self.headers.get("Content-Length") or 0)
        if length <= 0 or length > MAX_BYTES:
            return self._send_json(413, {"error": "bad size"})
        raw = self.rfile.read(length)
        try:
            data = json.loads(raw.decode("utf-8").lstrip("﻿"))
            if data.get("app") != "rol-calc" or not isinstance(data.get("profiles"), dict):
                raise ValueError
        except (ValueError, AttributeError, UnicodeDecodeError):
            return self._send_json(400, {"error": "not calculator data"})
        touch()
        with LOCK:
            daily_backup()
            tmp = DATA + ".tmp"
            with open(tmp, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=1)
                f.flush()
                os.fsync(f.fileno())
            os.replace(tmp, DATA)  # atomic: the file is never half-written
        return self._send_json(200, {"ok": True})


class Server(http.server.ThreadingHTTPServer):
    def handle_error(self, request, client_address):
        # the browser closed a connection early (tab closed or reloaded): nothing to report
        if isinstance(sys.exc_info()[1], (BrokenPipeError, ConnectionResetError, ConnectionAbortedError)):
            return
        super().handle_error(request, client_address)


def running_here():
    """Port of a Registre already running from THIS folder, or None.
    Another program, an older version or a copy in another folder on the same port is left alone:
    this one then takes the next free port."""
    import urllib.request
    for port in range(PORT, PORT + 10):
        try:
            with urllib.request.urlopen("http://127.0.0.1:%d/api/info" % port, timeout=0.5) as r:
                info = json.loads(r.read().decode("utf-8"))
            if info.get("folder") == FOLDER_ID and info.get("page") == PAGE:
                return port
        except Exception:
            continue
    return None


def main():
    if not os.path.exists(os.path.join(HERE, PAGE)):
        sys.exit("%s must be in the same folder as start.py" % PAGE)
    port = running_here()
    if port:
        url = "http://127.0.0.1:%d/%s" % (port, PAGE)
        print("Deja en marche : " + url)
        webbrowser.open(url)
        return
    port = free_port(PORT)
    if port != PORT:
        print("(le port %d est pris par un autre programme ou un autre Registre : port %d utilise)" % (PORT, port))
    url = "http://127.0.0.1:%d/%s" % (port, PAGE)
    server = Server(("127.0.0.1", port), Handler)
    print("Le Registre du Seigneur (Rise of Lords)")
    print("  Page   : " + url)
    print("  Donnees: " + DATA)
    print("Le programme s'arrete tout seul environ une minute apres la fermeture de l'onglet.")
    threading.Thread(target=watchdog, args=(server, datetime.datetime.now().timestamp()), daemon=True).start()
    if "--no-browser" not in sys.argv:
        threading.Timer(0.6, lambda: webbrowser.open(url)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
