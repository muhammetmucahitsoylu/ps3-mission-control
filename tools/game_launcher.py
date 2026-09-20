"""
PS3 Mission Control - Interactive Game Launcher
Dynamically scans installed PS3 games (ISO and folders) and mounts with one keystroke.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import PS3_IP
from core.ps3_client import PS3Client

client = PS3Client()

def launch_cli():
    print("================================================================")
    print("             PS3 ETKİLEŞİMLİ OYUN BAŞLATICI                     ")
    print("================================================================\n")
    print(f"[*] PS3'teki oyunlar taranıyor ({PS3_IP})...")

    games = client.list_installed_games()
    if not games:
        print("[!] Konsolda oyun bulunamadı veya bağlantı kurulamadı.")
        return

    print(f"\n[+] Toplam {len(games)} adet oyun tespit edildi:\n")
    for i, g in enumerate(games, 1):
        print(f"  [{i}] {g['title']} ({g['type']})")

    print("\n  [0] Çıkış")
    print("  [U] Takılı Diski Çıkar (Unmount)\n")

    try:
        choice = input("Başlatmak istediğiniz oyunun numarasını girin: ").strip()
        if choice == "0":
            return
        elif choice.upper() == "U":
            client.unmount()
            client.send_popup("DISK CIKARILDI (UNMOUNTED)")
            print("[+] Disk çıkarıldı.")
            return

        idx = int(choice) - 1
        if 0 <= idx < len(games):
            selected = games[idx]
            print(f"\n[*] '{selected['title']}' takılıyor (Mounting)...")
            client.mount_game(selected["path"])
            client.send_popup(f"OYUN TAKILDI: {selected['title']}")
            print(f"[+] '{selected['title']}' başarıyla takıldı! TV ekranında disk simgesini görebilirsiniz.")
        else:
            print("[!] Geçersiz numara seçildi.")
    except Exception as e:
        print(f"[!] Hata: {e}")

if __name__ == "__main__":
    launch_cli()
