# PS3 Real-Hardware 60 FPS Patches (Artemis & Memory Hooks)

Bu dizin, gerçek PlayStation 3 donanımı (CFW ve PS3HEN) üzerinde çalışan kare hızı (FPS) kilidi kaldırma yamalarını içerir.

---

## The Last of Us (BCUS98174 — v01.11)

### Yama Detayları
- **Hedef Bellek Adresi:** `0x01571A6F`
- **Orijinal Değer:** `0x02` (30 FPS Sınırı - 2 V-Sync frame)
- **Yama Değeri:** `0x01` (60 FPS Modu) veya `0x00` (Tamamen Kilitsiz / Uncapped)
- **Doğrulayanlar:** Joey85 (PSX-Place Ghidra RE), Nascar1243 (Gerçek Donanım Testleri)

### Donanım Gerçekliği & Performans Notu
1. **Yükleme Ekranında 100 FPS:**  
   Oyun motorundaki yazılımsal 30 FPS sınırı kaldırıldığı için çizilecek poligon yükü olmayan yükleme ekranlarında motor **100 FPS** değerine fırlar.
2. **Oyun İçi (Gameplay) Performansı:**  
   PS3'ün RSX ekran kartı (256 MB GDDR3) 2013 yapımı Naughty Dog grafik motorunun (volumetrik ışıklar, SSAO, MLAA, yapraklar) yükü altında %100 doygunlukta çalışır. Bu nedenle 3D sahnelerde donanım sınırı gereği 25-30 FPS bandında seyreder.
3. **Optimizasyon İpucu:**  
   PS3 Görüntü Ayarlarından 1080p/1080i tiklerini kaldırıp sadece **720p** bırakmak, RSX üzerindeki ölçekleme yükünü hafifleterek kalabalık sahnelerdeki düşüşleri toparlar.

---

## Kurulum (Artemis PS3 ile)

1. [Artemis PS3 Releases](https://github.com/bucanero/ArtemisPS3/releases) adresinden en son `ArtemisPS3-GUI.pkg` dosyasını indirin.
2. PS3'e kurun.
3. `BCUS98174.ncl` dosyasını konsoldaki `/dev_hdd0/game/ARTPS3001/USRDIR/USERLIST/` dizinine kopyalayın.
4. Artemis uygulamasını açın, **Cheats** sekmesinden The Last of Us 60 FPS yamasını seçip **START** ile XMB'ye dönün ve oyunu başlatın.
