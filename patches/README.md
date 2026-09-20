# PS3 Real-Hardware 60 FPS Patches & Memory Hooks

This directory contains real-hardware framerate unlock patches verified on original PlayStation 3 silicon (CFW and PS3HEN via the Artemis cheat/patch engine).

---

## The Last of Us (BCUS98174 — v01.11)

### Patch Definition
- **Target Memory Address:** `0x01571A6F`
- **Default Byte:** `0x02` (30 FPS cap — 2 V-Sync intervals per frame update at 60Hz)
- **Patched Byte:** `0x01` (60 FPS mode — 1 V-Sync interval) or `0x00` (Uncapped)
- **Verified by:** Joey85 (PSX-Place Ghidra static analysis), Nascar1243 (Hardware testing on CECH-2500 & CECH-4000)

### Technical Analysis: Frametimes & RSX Hardware Limits

1. **Why Loading Screens Hit ~100 FPS:**
   Modifying byte `0x01571A6F` removes the software governor in Naughty Dog's engine loop. When the engine executes with trivial GPU draw calls (e.g. static background rendering during level loading or title card screens), framerates scale freely up to ~100 FPS.

2. **Why 3D Gameplay Remains ~25–30 FPS on PS3 Silicon:**
   - The PS3's **RSX Reality Synthesizer** (500 MHz, 24 Pixel Pipelines, 128-bit bus) possesses only **256 MB of GDDR3 VRAM** (~20.8 GB/s bandwidth).
   - *The Last of Us* uses heavy deferred rendering, multi-pass dynamic lighting, volumetric fog, high-density particle emitters (spores), sub-surface scattering, and Morphological Anti-Aliasing (MLAA).
   - In standard 720p scenes, drawing a single full 3D frame saturates the RSX pipeline for approximately ~33.3 milliseconds ($1000\text{ ms} / 33.3\text{ ms} \approx 30.0\text{ FPS}$).
   - In resource-heavy areas (rain, deep water, multiple infected encounters), frame rendering time climbs to ~40–45 ms, causing the framerate to dip into the 22–25 FPS bracket.
   - **Conclusion:** The software limiter is successfully disabled, but the 2006-era RSX hardware is physically bound by pixel fillrate and memory bandwidth in real 3D scenes.

3. **Performance Optimization Tip:**
   In the PS3 XMB menu, navigate to **Settings → Display Settings → Video Output Settings** and uncheck `1080i` and `1080p`, locking output strictly to **720p**. Bypassing the hardware scaler overhead frees precious rasterization budget on the RSX, smoothing out frame drops during heavy encounters.

---

## Installation via Artemis PS3

1. Download the latest `ArtemisPS3-GUI.pkg` from the [official Artemis releases](https://github.com/bucanero/ArtemisPS3/releases).
2. Install the PKG on your PS3 via **Package Manager → Install Package Files**.
3. Copy `BCUS98174.ncl` into `/dev_hdd0/game/ARTPS3001/USRDIR/USERLIST/`.
4. Launch Artemis from the XMB, open **Cheats**, locate **The Last of Us (BCUS98174)**, select `[Unlock 60 FPS Mode]`, and press **START** to return to XMB.
5. Launch the game; the memory hook is injected into the active process upon startup.
