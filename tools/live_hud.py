"""
PS3 Mission Control - Live Terminal Hardware HUD
Real-time ASCII gauges for CELL/RSX thermals, fan speeds, uptime, and memory.
"""

import time
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import PS3_IP
from core.ps3_client import PS3Client

client = PS3Client()

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def get_color_bar(val, max_val, warn_val, crit_val, unit="°C"):
    pct = min(1.0, max(0.0, val / max_val))
    bar_len = 24
    filled = int(bar_len * pct)
    empty = bar_len - filled

    if val >= crit_val:
        color = "\033[91m"  # Red
    elif val >= warn_val:
        color = "\033[93m"  # Yellow
    else:
        color = "\033[92m"  # Green
    rst = "\033[0m"
    return f"{color}[{'#' * filled}{'-' * empty}] {val} {unit}{rst}"

def render_hud():
    print(f"[*] PS3 Telemetrisi Başlatılıyor... (Hedef: {PS3_IP})")
    time.sleep(0.5)

    try:
        while True:
            stats = client.get_telemetry()
            clear_screen()

            print("================================================================")
            print("         PS3 CANLI DONANIM TELEMETRİSİ (LIVE HUD)              ")
            print("================================================================")

            if not stats["online"]:
                print(f"\n  [!] KONSOLA BAĞLANILAMADI ({PS3_IP})")
                print("  [?] webMAN MOD ve FTP sunucusunun açık olduğundan emin olun.")
                print("  [?] Yeniden denemek için bekleniyor...\n")
                time.sleep(2)
                continue

            cpu_bar = get_color_bar(stats["cpu"], 85, 65, 74)
            rsx_bar = get_color_bar(stats["rsx"], 85, 65, 74)
            fan_bar = get_color_bar(stats["fan"], 100, 50, 75, unit="%")
            ram_mb = round(stats["mem_kb"] / 1024, 2)

            print(f" Hedef IP       : {PS3_IP}")
            print(f" Çalışma Süresi : {stats['uptime']}")
            print(f" Aktif Disk     : {stats['mounted_title']}\n")
            print(f" CELL (CPU)     : {cpu_bar}")
            print(f" RSX  (GPU)     : {rsx_bar}")
            print(f" Fan Hızı       : {fan_bar}")
            print(f" Boş VSH RAM    : \033[96m{ram_mb} MB ({stats['mem_kb']:,} KB)\033[0m")
            print("================================================================")
            print(" Çıkış için CTRL + C tuşlarına basabilirsiniz.")

            time.sleep(1.5)
    except KeyboardInterrupt:
        print("\n[*] Live HUD kapatıldı.")

if __name__ == "__main__":
    render_hud()
