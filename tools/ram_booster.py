"""
PS3 Mission Control - RAM Booster & VSH Memory Turbo
Flushes lwIP networking socket queues and frees VSH heap memory for optimal gaming headroom.
"""

import sys
import os
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import PS3_IP
from core.ps3_client import PS3Client

client = PS3Client()

def boost_ram():
    print("================================================================")
    print("          PS3 DERİN VSH & SİSTEM RAM OPTİMİZATÖRÜ               ")
    print("================================================================\n")

    before = client.get_telemetry()
    if not before["online"]:
        print(f"[!] PS3'e ulaşılamadı ({PS3_IP}).")
        return

    b_ram_kb = before["mem_kb"]
    print(f"[*] İşlem Öncesi Boş VSH RAM: {b_ram_kb:,} KB ({round(b_ram_kb/1024, 2)} MB)")
    print("[*] 1. Aşama: lwIP TCP soket tamponları boşaltılıyor...")
    client.trim_ram()
    time.sleep(1.0)

    print("[*] 2. Aşama: VSH arayüz dinamik önbelleği (Heap) taranıyor...")
    client.trim_ram()
    time.sleep(1.0)

    after = client.get_telemetry()
    a_ram_kb = after["mem_kb"]
    diff = a_ram_kb - b_ram_kb

    print("\n----------------------------------------------------------------")
    print(f"[+] Tamamlandı! Mevcut Boş RAM: {a_ram_kb:,} KB ({round(a_ram_kb/1024, 2)} MB)")
    if diff > 0:
        print(f"[+] Kazanılan Ek Bellek: +{diff:,} KB (+{round(diff/1024, 2)} MB)")
    else:
        print("[+] RAM tamponları zaten tertemiz ve oyun için en üst seviyede.")
    print("================================================================\n")

    client.send_popup(f"RAM TURBO: {round(a_ram_kb/1024, 2)} MB Bos Bellek")

if __name__ == "__main__":
    boost_ram()
