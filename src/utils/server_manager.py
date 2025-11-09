import os
import threading
import socket
import subprocess
import re
import logging
import json
from flask import Flask, request, jsonify, send_from_directory
from werkzeug.serving import make_server
from typing import Tuple


class ServerManager:

    def __init__(self, host="127.0.0.1", port=5000, log_func=None):
        self.host = host
        self.port = port
        self.log_func = log_func
        self.scheme = "http"  # http or https, decided at start()
        # Static resources now live under src/js
        # BASEDIR -> src
        self.BASEDIR = os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        )
        self.STATIC_DIR = os.path.join(self.BASEDIR, "static")
        self.INDEX_FILE = "index.html"
        self.latest_metadata = None  # New caching mechanism, stores the metadata of the most recent upload
        self.app = self._create_app()
        self._srv = None
        self._thread = None
        # SSL certificate path
        self.cert_path = os.path.join(self.BASEDIR, "configs", "cert.pem")
        self.key_path = os.path.join(self.BASEDIR, "configs", "key.pem")
        self.is_running = False

    def _create_app(self):

        app = Flask(__name__, static_folder=self.STATIC_DIR, static_url_path="")
        manager = self

        @app.route("/get_latest_metadata", methods=["GET"])
        def get_latest_metadata():
            return jsonify(manager.latest_metadata or {})

        @app.route("/api/file_share/upload", methods=["POST"])
        def file_share_upload():
            tab = getattr(self, "ShareTab_instance", None)
            if not tab or not hasattr(tab, "cache_dir"):
                return (
                    jsonify(
                        {"success": False, "error": "No output directory configured"}
                    ),
                    400,
                )
            out_dir = tab.cache_dir
            if not os.path.exists(out_dir):
                os.makedirs(out_dir, exist_ok=True)
            files = request.files.getlist("photos")
            saved = []
            for f in files:
                filename = f.filename
                # Prevent path traversal
                filename = os.path.basename(filename)
                save_path = os.path.join(out_dir, filename)
                try:
                    f.save(save_path)
                    self.log(logging.INFO, f"[UPLOAD] File saved: {save_path}")
                    saved.append(filename)
                except Exception as e:
                    self.log(logging.ERROR, f"[UPLOAD] Failed to save {save_path}: {e}")
                    return jsonify({"success": False, "error": str(e)}), 500
            self.log(logging.INFO, f"[UPLOAD] All files saved to: {out_dir}")

            # Update latest metadata cache
            if len(saved) == 1:
                ext = os.path.splitext(saved[0])[1].lower()
                if ext == ".txt":
                    self.latest_metadata = {"type": "text", "info": [saved[0]]}
                elif ext == ".png":
                    self.latest_metadata = {"type": "draw", "info": [saved[0]]}
                else:
                    self.latest_metadata = {"type": "file", "info": [saved[0]]}
            elif len(saved) > 1:
                self.latest_metadata = {"type": "files", "info": saved}
            else:
                self.latest_metadata = None
            return jsonify({"success": True, "files": saved})

        @app.route("/get_pushed_signature", methods=["GET"])
        def get_pushed_signature():
            if manager.latest_payload:
                payload = manager.latest_payload
                manager.latest_payload = None
                return jsonify(payload)
            else:
                return jsonify({"type": None, "data": None})

        @app.route("/push_signature", methods=["POST"])
        def push_signature():
            try:
                j = request.get_json(force=True)
            except Exception:
                return jsonify({"status": "error", "message": "invalid json"}), 400
            typ = j.get("type")
            data = j.get("data")
            filename = j.get("filename")
            if not typ or not data:
                return (
                    jsonify({"status": "error", "message": "missing type or data"}),
                    400,
                )
            manager.latest_payload = {"type": typ, "data": data, "filename": filename}
            return jsonify({"status": "ok"})

        @app.route("/")
        def index():
            return send_from_directory(manager.STATIC_DIR, manager.INDEX_FILE)

        @app.route("/canvas/size", methods=["GET"])
        def canvas_size():
            # Prefer dynamic size from injected SignatureTab
            tab = getattr(self, "SignatureTab_instance", None)
            if tab is not None:
                try:
                    size = tab.get_canvas_size()
                    return jsonify(size)
                except Exception:
                    pass
            # Fallback default
            return jsonify({"width": 560, "height": 300})

        # Remove upload_signature route, all signatures are stored in memory

        # Remove serve_signature route, all signatures are stored in memory

        # --- File Sharing API ---
        @app.route("/api/file_share/files", methods=["GET"])
        def file_share_list():
            self.log(
                logging.INFO,
                f"[Flask] /api/file_share/files called. manager.ShareTab_instance: {repr(getattr(manager, 'ShareTab_instance', None))}",
            )
            tab = getattr(manager, "ShareTab_instance", None)
            if tab and hasattr(tab, "get_file_list"):
                self.log(
                    logging.INFO,
                    f"[Flask] Calling ShareTab_instance.get_file_list()...",
                )
                return (
                    self.api_file_list(tab.get_file_list()),
                    200,
                    {"Content-Type": "application/json"},
                )
            self.log(
                logging.WARNING,
                f"[Flask] No valid ShareTab_instance or get_file_list not found.",
            )
            return jsonify([])

        @app.route("/api/file_share/download", methods=["GET"])
        def file_share_download():
            filename = request.args.get("filename")
            self.log(
                logging.INFO,
                f"[Flask] /api/file_share/download called. filename: {filename} manager.ShareTab_instance: {repr(getattr(manager, 'ShareTab_instance', None))}",
            )
            tab = getattr(manager, "ShareTab_instance", None)
            if tab and hasattr(tab, "get_file_list"):
                self.log(
                    logging.INFO,
                    f"[Flask] Calling ShareTab_instance.get_file_list({filename})...",
                )
                data = self.api_file_download(tab.get_file_list(), filename)
                if data:
                    from flask import Response

                    response = Response(data, mimetype="application/octet-stream")
                    response.headers["Content-Disposition"] = (
                        f'attachment; filename="{filename}"'
                    )
                    return response
            return jsonify({"error": "File not found"}), 404

        return app

    def start(self):
        if self._srv is not None:
            self.log(logging.INFO, "Server already started")
            return
        ssl_context = None
        if os.path.exists(self.cert_path) and os.path.exists(self.key_path):
            ssl_context = (self.cert_path, self.key_path)
            self.log(
                logging.INFO,
                f"[ServerManager] Using SSL context: {self.cert_path}, {self.key_path}",
            )
            self.scheme = "https"
        else:
            self.log(
                logging.WARNING,
                "[ServerManager] SSL certificate not found, using HTTP mode. Please generate cert.pem and key.pem in the project root directory.",
            )
            self.scheme = "http"
        self._srv = make_server(self.host, self.port, self.app, ssl_context=ssl_context)
        self._thread = threading.Thread(target=self._srv.serve_forever, daemon=True)
        self._thread.start()
        self.is_running = True

    def get_base_url(self) -> str:
        return f"{self.scheme}://{self.host}:{self.port}"

    def stop(self):
        try:
            if self._srv:
                self._srv.shutdown()
        except Exception:
            pass
        self._srv = None
        self._thread = None
        self.is_running = False

    def list_local_ips(self):
        ips = []
        try:
            name = socket.gethostname()
            for res in socket.getaddrinfo(name, None):
                af, _, _, _, sa = res
                if af == socket.AF_INET:
                    addr = sa[0]
                    if not addr.startswith("127.") and addr not in ips:
                        ips.append(addr)
        except Exception:
            pass
        try:
            probe = self._get_local_ip()
            if probe and probe not in ips:
                ips.insert(0, probe)
        except Exception:
            pass
        try:
            if os.name == "nt":
                p = subprocess.run(["ipconfig"], capture_output=True, text=True)
                out = p.stdout or p.stderr or ""
                for m in re.finditer(r"IPv4[^\n:]*:\s*([0-9]+(?:\.[0-9]+){3})", out):
                    a = m.group(1)
                    if not a.startswith("127.") and a not in ips:
                        ips.append(a)
        except Exception:
            pass
        if "127.0.0.1" not in ips:
            ips.append("127.0.0.1")
        return ips

    def _get_local_ip(self) -> str:

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
        except Exception:
            ip = "127.0.0.1"
        finally:
            try:
                s.close()
            except Exception:
                pass
        return ip

    # File saving logic has been removed, signatures are only stored in memory cache

    def test_bind(self, ip: str, port: int) -> Tuple[bool, str]:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.bind((ip, port))
            return True, "Local bind OK"
        except Exception as e:
            return False, f"Local bind FAILED: {e}"
        finally:
            try:
                s.close()
            except Exception:
                pass

    def ping_host(self, ip: str, count: int = 1) -> Tuple[bool, str]:
        try:
            if os.name == "nt":
                cmd = ["ping", "-n", str(count), ip]
            else:
                cmd = ["ping", "-c", str(count), ip]
            p = subprocess.run(cmd, capture_output=True, text=True)
            out = p.stdout or p.stderr or ""
            if "TTL=" in out or "ttl=" in out:
                return True, out
            else:
                return False, out
        except Exception as e:
            return False, str(e)

    def log(self, level: int, msg: str):
        if self.log_func:
            self.log_func(level, msg)

    def get_selected_files_info(self, file_list):
        """
        Get information about the user-selected files (base name, ext, size, mtime) for web display.
        """
        result = []
        for f in file_list:
            f = f.strip()
            if f and os.path.isfile(f):
                stat = os.stat(f)
                base = os.path.basename(f)
                name, ext = os.path.splitext(base)
                result.append(
                    {
                        "name": name,
                        "ext": ext,
                        "size": stat.st_size,
                        "mtime": stat.st_mtime,
                        "full": f,
                    }
                )
        return result

    def api_file_list(self, filelist):
        """
        Used for server API, returns brief information about the selected files (excluding full paths).
        """

        info = self.get_selected_files_info(filelist)
        # Only return safe fields
        return json.dumps(
            [
                {
                    "name": i["name"],
                    "ext": i["ext"],
                    "size": i["size"],
                    "mtime": i["mtime"],
                }
                for i in info
            ]
        )

    def api_file_download(self, filelist, filename):
        """
        Used for server API, downloads the specified file (filename is base name + ext).
        """
        info = self.get_selected_files_info(filelist)
        for i in info:
            if i["name"] + i["ext"] == filename:
                # The server should securely send the file here
                with open(i["full"], "rb") as f:
                    return f.read()
        return None
