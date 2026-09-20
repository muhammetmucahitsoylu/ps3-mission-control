"""
PS3 Mission Control - Blu-ray Phantom Sector Analyzer
Scans installed PS3ISOs for Sony optical disc dummy padding and tail vacancy.
"""

import sys
import os
import io

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import PS3_IP
from core.ps3_client import PS3Client

client = PS3Client()

def analyze_phantom_padding():
    print("================================================================================")
    print("             PS3 BLU-RAY HAYALET DOLGU & SEKTÖR ANALİZÖRÜ                       ")
    print("      (Sony Blu-Ray Dış Kenar Dummy Sektörleri & Kayıpsız Depolama Sınavı)      ")
    print("================================================================================\n")
    print(f"[*] PS3'e bağlanılıyor: {PS3_IP}...")

    try:
        ftp = client.get_ftp(custom_timeout=12)
    except Exception as e:
        print(f"[!] PS3'e bağlanılamadı: {e}")
        return

    iso_dir = "/dev_hdd0/PS3ISO"
    try:
        raw_items = ftp.nlst(iso_dir)
        iso_files = [f.split("/")[-1] for f in raw_items if f.lower().endswith(".iso")]
    except Exception as e:
        print(f"[!] ISO klasörü taranırken hata: {e}")
        ftp.quit()
        return

    print(f"[*] Toplam {len(iso_files)} adet PS3ISO imajı taranıyor...\n")

    total_bytes = 0
    total_phantom_est = 0

    for iso in sorted(iso_files):
        iso_path = f"{iso_dir}/{iso}"
        try:
            sz = ftp.size(iso_path)
            total_bytes += sz
            sz_gb = round(sz / (1024**3), 2)

            # Sample 64KB from the tail of the ISO
            sample_len = 65536
            offset = max(0, sz - sample_len)

            bio = io.BytesIO()
            ftp.retrbinary(f"RETR {iso_path}", bio.write, rest=offset)
            tail = bio.getvalue()

            null_count = tail.count(b"\x00")
            null_ratio = (null_count / len(tail)) * 100 if tail else 0

            has_padding = null_ratio > 90.0
            if has_padding:
                phantom_est = sz * 0.18  # Typical BD dual-layer padding ratio
                total_phantom_est += phantom_est
                print(f"  -> {iso:<30} | Boyut: {sz_gb:5.2f} GB | Kuyruk Boşluk: %{null_ratio:5.1f} | HAYALET DOLGULU (Padding Var)")
                print(f"     [!] Tahmini Boş Sektör Dolgusu: ~{round(phantom_est / (1024**3), 2)} GB")
            else:
                print(f"  -> {iso:<30} | Boyut: {sz_gb:5.2f} GB | Kuyruk Boşluk: %{null_ratio:5.1f} | SIKIŞTIRILMIŞ (Temiz)")

        except Exception as e:
            print(f"  [-] {iso} incelenirken hata: {e}")

    ftp.quit()

    print("\n--------------------------------------------------------------------------------")
    print(f"[+] Toplam Taranan Oyun Verisi        : {round(total_bytes / (1024**3), 2)} GB")
    print(f"[+] Tespit Edilen Hayalet Boş Dolgu    : ~{round(total_phantom_est / (1024**3), 2)} GB")
    print("================================================================================\n")

if __name__ == "__main__":
    analyze_phantom_padding()
