"""
PS3 Mission Control - Core Client Wrapper
Provides robust webMAN MOD HTTP and FTP client interfaces with auto-recovery.
"""

import urllib.request
import urllib.parse
import ftplib
import socket
import re
import sys
import os

# Ensure config is importable regardless of caller location
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import CONFIG, PS3_IP, HTTP_PORT, FTP_PORT, TIMEOUT

class PS3Client:
    def __init__(self, ip=None, timeout=None):
        self.ip = ip or PS3_IP
        self.timeout = timeout or TIMEOUT

    def get_url(self, path):
        if path.startswith("/"):
            return f"http://{self.ip}:{HTTP_PORT}{path}"
        return f"http://{self.ip}:{HTTP_PORT}/{path}"

    def send_http(self, path, custom_timeout=None):
        url = self.get_url(path)
        req = urllib.request.Request(url, headers={"User-Agent": "PS3MissionControl"})
        t = custom_timeout or self.timeout
        with urllib.request.urlopen(req, timeout=t) as resp:
            return resp.read().decode("utf-8", errors="ignore")

    def send_popup(self, message):
        """Sends an on-screen notification popup to the PS3 screen."""
        try:
            encoded = urllib.parse.quote(str(message))
            self.send_http(f"/popup.ps3?{encoded}")
            return True
        except Exception:
            return False

    def get_telemetry(self):
        """Fetches real-time CPU/RSX temperatures, Fan speed, and free memory."""
        try:
            html = self.send_http("/cpursx.ps3", custom_timeout=2.0)
            cpu_m = re.search(r"CPU:\s*(\d+)", html)
            rsx_m = re.search(r"RSX:\s*(\d+)", html)
            fan_m = re.search(r"FAN SPEED:\s*(\d+)%", html)
            mem_m = re.search(r"MEM:\s*([0-9,]+)\s*KB", html)
            uptime_m = re.search(r"Startup.*?>\s*([0-9:]+)", html)
            title_m = re.search(r"/mount\.ps3/([^\"'<]+)", html)

            return {
                "online": True,
                "cpu": int(cpu_m.group(1)) if cpu_m else 0,
                "rsx": int(rsx_m.group(1)) if rsx_m else 0,
                "fan": int(fan_m.group(1)) if fan_m else 0,
                "mem_kb": int(mem_m.group(1).replace(",", "")) if mem_m else 0,
                "uptime": uptime_m.group(1) if uptime_m else "N/A",
                "mounted_title": title_m.group(1) if title_m else "XMB (Ana Menü)"
            }
        except Exception as e:
            return {
                "online": False,
                "error": str(e),
                "cpu": 0,
                "rsx": 0,
                "fan": 0,
                "mem_kb": 0,
                "uptime": "N/A",
                "mounted_title": "Bağlantı Yok"
            }

    def mount_game(self, game_path):
        """Mounts a game ISO or folder in webMAN MOD."""
        try:
            res = self.send_http(f"/mount.ps3{game_path}")
            return True
        except Exception as e:
            return False

    def unmount(self):
        """Unmounts any currently mounted game image."""
        try:
            self.send_http("/mount.ps3/unmount")
            return True
        except Exception:
            return False

    def trim_ram(self):
        """Flushes VSH heap and socket buffers to free RAM for games."""
        try:
            self.send_http("/mem.ps3")
            self.send_http("/vshmem.ps3")
            return True
        except Exception:
            return False

    def get_ftp(self, custom_timeout=10):
        """Returns an authenticated FTP client instance."""
        ftp = ftplib.FTP(self.ip, timeout=custom_timeout)
        ftp.login()
        return ftp

    def list_installed_games(self):
        """Scans /dev_hdd0/PS3ISO and /dev_hdd0/GAMES dynamically."""
        games = []
        try:
            ftp = self.get_ftp(custom_timeout=5)
            # Scan ISOs
            try:
                for item in ftp.nlst("/dev_hdd0/PS3ISO"):
                    fname = item.split("/")[-1]
                    if fname.lower().endswith(".iso"):
                        clean_title = fname[:-4].replace("_", " ")
                        games.append({
                            "title": clean_title,
                            "type": "PS3ISO",
                            "path": f"/dev_hdd0/PS3ISO/{fname}"
                        })
            except Exception:
                pass

            # Scan Folder games
            try:
                for item in ftp.nlst("/dev_hdd0/GAMES"):
                    fname = item.split("/")[-1]
                    if fname not in [".", ".."]:
                        games.append({
                            "title": fname,
                            "type": "GAMES",
                            "path": f"/dev_hdd0/GAMES/{fname}"
                        })
            except Exception:
                pass

            ftp.quit()
        except Exception:
            pass

        return games
