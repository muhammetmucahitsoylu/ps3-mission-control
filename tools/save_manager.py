"""
PS3 Mission Control - Save Game Backup Manager
Safely synchronizes and backs up save data from all PS3 user profiles to the local backups directory.
"""

import sys
import os
import ftplib

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import PS3_IP, BACKUP_DIR
from core.ps3_client import PS3Client

client = PS3Client()
SAVE_DEST = os.path.join(BACKUP_DIR, "saves")

def download_folder_recursive(ftp, remote_dir, local_dir):
    os.makedirs(local_dir, exist_ok=True)
    items = ftp.nlst(remote_dir)
    count = 0
    for item in items:
        base = item.split("/")[-1]
        if base in [".", ".."]:
            continue
        remote_item = f"{remote_dir}/{base}"
        local_item = os.path.join(local_dir, base)

        try:
            sz = ftp.size(remote_item)
            with open(local_item, "wb") as f:
                ftp.retrbinary(f"RETR {remote_item}", f.write)
            count += 1
        except Exception:
            count += download_folder_recursive(ftp, remote_item, local_item)
    return count

def backup_saves():
    print("================================================================")
    print("         PS3 OYUN KAYIT (SAVE) YEDEKLEME SİSTEMİ                ")
    print("================================================================\n")
    print(f"[*] PS3'e bağlanılıyor: {PS3_IP}...")

    try:
        ftp = client.get_ftp(custom_timeout=10)
    except Exception as e:
        print(f"[!] PS3'e bağlanılamadı: {e}")
        return

    try:
        user_profiles = [u.split("/")[-1] for u in ftp.nlst("/dev_hdd0/home") if u.split("/")[-1] not in [".", ".."]]
    except Exception:
        user_profiles = []

    if not user_profiles:
        print("[!] Konsolda kullanıcı profili tespit edilemedi.")
        ftp.quit()
        return

    print(f"[+] Bulunan Kullanıcı Profilleri: {', '.join(user_profiles)}")
    print(f"[*] PC Hedef Yedekleme Klasörü: {SAVE_DEST}\n")

    total_synced = 0
    for user in user_profiles:
        remote_save_dir = f"/dev_hdd0/home/{user}/savedata"
        try:
            saves = [s.split("/")[-1] for s in ftp.nlst(remote_save_dir) if s.split("/")[-1] not in [".", ".."]]
            if not saves:
                print(f"  [i] Profil {user}: Kayıtlı save dosyası yok.")
                continue

            print(f"  [*] Profil {user}: {len(saves)} adet oyun kaydı yedekleniyor...")
            for s in saves:
                local_save_path = os.path.join(SAVE_DEST, user, s)
                c = download_folder_recursive(ftp, f"{remote_save_dir}/{s}", local_save_path)
                total_synced += c
                print(f"    [+] {s} ({c} dosya) -> Yedeklendi")
        except Exception as e:
            print(f"  [-] Profil {user} taranırken hata: {e}")

    ftp.quit()
    print("\n----------------------------------------------------------------")
    print(f"[+] Yedekleme Tamamlandı! Toplam {total_synced} dosya PC'ye kaydedildi.")
    print(f"[+] Konum: {SAVE_DEST}")
    print("================================================================\n")

    client.send_popup(f"SAVE YEDEKLEME: {total_synced} Dosya PC ye Kaydedildi")

if __name__ == "__main__":
    backup_saves()
