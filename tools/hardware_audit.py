"""
PS3 Mission Control - Comprehensive Hardware & Disk Integrity Audit
Performs concurrent networking, SATA HDD I/O cryptographic hashing, and thermal curve tests.
"""

import ftplib
import urllib.request
import socket
import hashlib
import time
import os
import re
import json
import io
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import PS3_IP, BACKUP_DIR
from core.ps3_client import PS3Client

client = PS3Client()

def run_audit():
    print("================================================================================")
    print("       PS3 ULTIMATE RUTHLESS HARDWARE, STORAGE & INTEGRITY MASTER AUDIT         ")
    print("================================================================================\n")

    # STAGE 1: Concurrent Socket Stress Test
    print("[1/3] webMAN & Ağ Soket Eşzamanlılık Testi...", flush=True)
    burst = 20
    success = 0
    latencies = []
    for _ in range(burst):
        t0 = time.time()
        try:
            req = urllib.request.Request(f"http://{PS3_IP}/cpursx_ps3", headers={"User-Agent": "AuditBot"})
            with urllib.request.urlopen(req, timeout=2.0) as r:
                if r.status == 200:
                    success += 1
                    latencies.append((time.time() - t0) * 1000)
        except Exception:
            pass

    loss = ((burst - success) / burst) * 100
    avg_lat = sum(latencies) / len(latencies) if latencies else 999
    print(f"  -> Paket Başarısı: {success}/{burst} (%{100 - loss:.1f}) | Ort. Tepki: {avg_lat:.1f} ms")

    # STAGE 2: SATA HDD I/O & SHA-256 Check
    print("\n[2/3] Dahili SATA HDD I/O & Kriptografik Doğrulama (SHA-256)...", flush=True)
    try:
        ftp = client.get_ftp(custom_timeout=15)
        test_payload = os.urandom(8 * 1024 * 1024)  # 8 MB
        orig_hash = hashlib.sha256(test_payload).hexdigest()

        # Write test
        t_w0 = time.time()
        ftp.storbinary("STOR /dev_hdd0/tmp/io_benchmark.tmp", io.BytesIO(test_payload))
        write_time = time.time() - t_w0
        write_mbps = round(8 / write_time, 2)

        # Read test
        read_bio = io.BytesIO()
        t_r0 = time.time()
        ftp.retrbinary("RETR /dev_hdd0/tmp/io_benchmark.tmp", read_bio.write)
        read_time = time.time() - t_r0
        read_mbps = round(8 / read_time, 2)

        ftp.delete("/dev_hdd0/tmp/io_benchmark.tmp")
        ftp.quit()

        verified_hash = hashlib.sha256(read_bio.getvalue()).hexdigest()
        integrity_ok = orig_hash == verified_hash

        print(f"  -> Yazma Hızı: {write_mbps} MB/s | Okuma Hızı: {read_mbps} MB/s")
        print(f"  -> SHA-256 Veri Bütünlüğü: {'KUSURSUZ (Eşleşti)' if integrity_ok else 'HATA (Bozulma Var)'}")
    except Exception as e:
        print(f"  [-] HDD Test Hatası: {e}")

    # STAGE 3: Telemetry & Thermal Efficiency
    print("\n[3/3] Donanım Termal ve Çalışma Durumu...", flush=True)
    telemetry = client.get_telemetry()
    if telemetry["online"]:
        print(f"  -> CELL (CPU) : {telemetry['cpu']}°C")
        print(f"  -> RSX  (GPU) : {telemetry['rsx']}°C")
        print(f"  -> Fan Hızı   : %{telemetry['fan']}")
        print(f"  -> Boş RAM    : {round(telemetry['mem_kb'] / 1024, 2)} MB")
        print(f"  -> Uptime     : {telemetry['uptime']}")
    else:
        print("  [-] Telemetri okunamadı.")

    print("\n================================================================================")
    print("                    DONANIM TESTİ TAMAMLANDI                                    ")
    print("================================================================================\n")

if __name__ == "__main__":
    run_audit()
