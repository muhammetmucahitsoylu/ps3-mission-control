"""
PS3 Mission Control - Ghost Sentinel Background Daemon
Active thermal watchdog, overheating early warning system, and auto-backup guardian.
"""

import time
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import CONFIG, PS3_IP
from core.ps3_client import PS3Client

client = PS3Client()
WARN_TEMP = CONFIG.get("thermal_warning_threshold_c", 70)
CRIT_TEMP = CONFIG.get("thermal_critical_threshold_c", 76)

def run_sentinel():
    print("================================================================")
    print("       PS3 GHOST SENTINEL // CANLI TERMAL VE GÜVENLİK NÖBETÇİSİ ")
    print("================================================================")
    print(f"[*] İzlenen Konsol   : {PS3_IP}")
    print(f"[*] Uyarı Eşiği       : {WARN_TEMP}°C")
    print(f"[*] Kritik Eşik       : {CRIT_TEMP}°C")
    print("================================================================")
    print("Nöbetçi devrede. Çıkmak için CTRL + C yapabilirsiniz.\n")

    last_warn_time = 0
    poll_count = 0

    try:
        while True:
            stats = client.get_telemetry()
            poll_count += 1

            if stats["online"]:
                cpu = stats["cpu"]
                rsx = stats["rsx"]
                max_t = max(cpu, rsx)

                status_line = (
                    f"[{time.strftime('%H:%M:%S')}] "
                    f"CPU: {cpu}°C | RSX: {rsx}°C | Fan: {stats['fan']}% | "
                    f"RAM: {round(stats['mem_kb']/1024, 1)}MB | {stats['mounted_title']}"
                )
                print(status_line)

                # Overheating alerts
                now = time.time()
                if max_t >= CRIT_TEMP and (now - last_warn_time > 30):
                    client.send_popup(f"KRITIK SICAKLIK! CPU: {cpu}C | RSX: {rsx}C")
                    print(f"\033[91m[!] KRİTİK SICAKLIK UYARISI: {max_t}°C!\033[0m")
                    last_warn_time = now
                elif max_t >= WARN_TEMP and (now - last_warn_time > 60):
                    client.send_popup(f"TERMAL UYARI: CPU: {cpu}C | RSX: {rsx}C")
                    print(f"\033[93m[!] Yüksek Sıcaklık Uyarısı: {max_t}°C\033[0m")
                    last_warn_time = now

            else:
                print(f"[{time.strftime('%H:%M:%S')}] [!] Konsol yanıt vermiyor, bekleniyor...")

            time.sleep(3)
    except KeyboardInterrupt:
        print("\n[*] Ghost Sentinel kapatıldı.")

if __name__ == "__main__":
    run_sentinel()
