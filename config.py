"""
PS3 Mission Control - Unified Configuration & Network Resolver
Zero-hardcoded paths, dynamic IP discovery, and cross-platform compatibility.
"""

import os
import json
import socket

# Base directories
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_CONFIG_FILE = os.path.join(BASE_DIR, "config.json")
EXAMPLE_CONFIG_FILE = os.path.join(BASE_DIR, "config.example.json")

def load_config():
    config = {
        "ps3_ip": os.getenv("PS3_IP", "<PS3_IP>"),
        "webman_http_port": int(os.getenv("PS3_HTTP_PORT", 80)),
        "webman_ftp_port": int(os.getenv("PS3_FTP_PORT", 21)),
        "web_cockpit_port": int(os.getenv("COCKPIT_PORT", 8080)),
        "backup_directory": os.path.join(BASE_DIR, "backups"),
        "request_timeout_sec": 4.0,
        "thermal_warning_threshold_c": 70,
        "thermal_critical_threshold_c": 76
    }
    
    target_file = DEFAULT_CONFIG_FILE if os.path.exists(DEFAULT_CONFIG_FILE) else EXAMPLE_CONFIG_FILE
    if os.path.exists(target_file):
        try:
            with open(target_file, "r", encoding="utf-8") as f:
                file_conf = json.load(f)
                for k, v in file_conf.items():
                    if k == "backup_directory" and not os.path.isabs(v):
                        config[k] = os.path.join(BASE_DIR, v)
                    else:
                        config[k] = v
        except Exception as e:
            print(f"[!] Warning: Failed to parse config file: {e}")
            
    # Ensure backup directory exists
    os.makedirs(config["backup_directory"], exist_ok=True)
    return config

def is_ps3_reachable(ip, port=80, timeout=1.5):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        res = s.connect_ex((ip, port))
        s.close()
        return res == 0
    except Exception:
        return False

# Global configuration instance
CONFIG = load_config()
PS3_IP = CONFIG["ps3_ip"]
HTTP_PORT = CONFIG["webman_http_port"]
FTP_PORT = CONFIG["webman_ftp_port"]
COCKPIT_PORT = CONFIG["web_cockpit_port"]
BACKUP_DIR = CONFIG["backup_directory"]
TIMEOUT = CONFIG["request_timeout_sec"]
