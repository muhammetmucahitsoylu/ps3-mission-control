"""
PS3 Mission Control - System Cleaner & Cache Optimizer
Safely removes stale temporary logs, crash dumps, and browser cache from /dev_hdd0/tmp.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import PS3_IP
from core.ps3_client import PS3Client

client = PS3Client()

def clean_system():
    print("================================================================")
    print("        PS3 SİSTEM ÖNBELLEK & ÇÖP TEMİZLEYİCİ (OPTIMIZER)       ")
    print("================================================================\n")
    print(f"[*] PS3'e bağlanılıyor: {PS3_IP}...")

    try:
        ftp = client.get_ftp(custom_timeout=8)
    except Exception as e:
        print(f"[!] PS3'e bağlanılamadı: {e}")
        return

    tmp_path = "/dev_hdd0/tmp"
    files_deleted = 0
    bytes_freed = 0

    try:
        items = ftp.nlst(tmp_path)
        whitelist = [".", "..", "wm_res", "wm_icons", "game_plugin", "wm_custom_combo"]

        for item in items:
            fname = item.split("/")[-1]
            if fname in whitelist:
                continue

            full_p = f"{tmp_path}/{fname}"
            try:
                sz = ftp.size(full_p)
                ftp.delete(full_p)
                files_deleted += 1
                bytes_freed += sz
                print(f"  [-] Temizlendi: {fname} ({round(sz / 1024, 1)} KB)")
            except Exception:
                pass

    except Exception as e:
        print(f"[!] Tarama hatası: {e}")

    ftp.quit()
    mb_freed = round(bytes_freed / (1024 * 1024), 2)

    print("\n----------------------------------------------------------------")
    print(f"[+] Temizlik Tamamlandı: {files_deleted} adet gereksiz dosya temizlendi.")
    print(f"[+] Geri Kazanılan Disk Alanı: {mb_freed} MB")
    print("================================================================\n")

    client.send_popup(f"TEMIZLIK BITTI: {files_deleted} Dosya Silindi ({mb_freed} MB)")

if __name__ == "__main__":
    clean_system()
