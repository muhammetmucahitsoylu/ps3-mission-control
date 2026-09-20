"""
PS3 Mission Control - Cyberpunk Web Dashboard
Real-time hardware monitoring, dynamic game launcher, and telemetry HUD over Web/LAN.
"""

import http.server
import socketserver
import urllib.request
import urllib.parse
import json
import re
import os
import sys
import threading
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import CONFIG, PS3_IP, COCKPIT_PORT
from core.ps3_client import PS3Client

client = PS3Client()

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PS3 SUPER SLIM // MISSION CONTROL</title>
    <style>
        :root {
            --bg: #090b10;
            --card-bg: rgba(18, 24, 38, 0.7);
            --border: rgba(0, 242, 254, 0.2);
            --accent: #00f2fe;
            --accent-glow: rgba(0, 242, 254, 0.4);
            --green: #00ff88;
            --yellow: #ffd000;
            --red: #ff3366;
            --text: #e0e6ed;
            --text-muted: #8898aa;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', system-ui, sans-serif; }
        body {
            background: var(--bg);
            color: var(--text);
            min-height: 100vh;
            padding: 20px;
            background-image: radial-gradient(circle at 10% 20%, rgba(0, 242, 254, 0.05) 0%, transparent 40%),
                              radial-gradient(circle at 90% 80%, rgba(0, 255, 136, 0.04) 0%, transparent 40%);
        }
        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 20px;
            background: var(--card-bg);
            border: 1px solid var(--border);
            border-radius: 16px;
            backdrop-filter: blur(10px);
            margin-bottom: 24px;
        }
        .title-group h1 {
            font-size: 24px;
            letter-spacing: 2px;
            color: var(--accent);
            text-transform: uppercase;
        }
        .title-group p {
            color: var(--text-muted);
            font-size: 13px;
            margin-top: 4px;
        }
        .status-badge {
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 8px 16px;
            border-radius: 20px;
            background: rgba(0, 255, 136, 0.1);
            border: 1px solid var(--green);
            color: var(--green);
            font-weight: bold;
            font-size: 14px;
        }
        .status-dot {
            width: 10px;
            height: 10px;
            border-radius: 50%;
            background: var(--green);
            box-shadow: 0 0 10px var(--green);
            animation: pulse 2s infinite;
        }
        @keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.3; } }
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 20px;
            margin-bottom: 24px;
        }
        .card {
            background: var(--card-bg);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 20px;
            backdrop-filter: blur(10px);
            position: relative;
            overflow: hidden;
        }
        .card h3 {
            font-size: 13px;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            color: var(--text-muted);
            margin-bottom: 12px;
        }
        .metric-value {
            font-size: 38px;
            font-weight: 800;
            color: #fff;
            display: flex;
            align-items: baseline;
            gap: 6px;
        }
        .metric-unit {
            font-size: 16px;
            color: var(--text-muted);
            font-weight: normal;
        }
        .progress-track {
            width: 100%;
            height: 8px;
            background: rgba(255,255,255,0.06);
            border-radius: 4px;
            margin-top: 15px;
            overflow: hidden;
        }
        .progress-bar {
            height: 100%;
            border-radius: 4px;
            transition: width 0.5s ease;
        }
        .games-section {
            background: var(--card-bg);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 24px;
            backdrop-filter: blur(10px);
        }
        .section-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
        }
        .games-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
            gap: 16px;
        }
        .game-card {
            background: rgba(255,255,255,0.03);
            border: 1px solid rgba(255,255,255,0.06);
            border-radius: 12px;
            padding: 16px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            transition: all 0.2s ease;
        }
        .game-card:hover {
            border-color: var(--accent);
            transform: translateY(-2px);
            box-shadow: 0 4px 20px rgba(0, 242, 254, 0.15);
        }
        .game-name {
            font-weight: bold;
            font-size: 15px;
            margin-bottom: 6px;
            color: #fff;
        }
        .game-type {
            font-size: 12px;
            color: var(--text-muted);
            margin-bottom: 14px;
        }
        .btn-mount {
            background: linear-gradient(135deg, rgba(0, 242, 254, 0.2), rgba(0, 255, 136, 0.2));
            border: 1px solid var(--accent);
            color: #fff;
            padding: 10px;
            border-radius: 8px;
            cursor: pointer;
            font-weight: 600;
            transition: all 0.2s ease;
            text-align: center;
        }
        .btn-mount:hover {
            background: var(--accent);
            color: #000;
            box-shadow: 0 0 15px var(--accent-glow);
        }
        .actions-row {
            display: flex;
            gap: 12px;
            margin-top: 20px;
            flex-wrap: wrap;
        }
        .btn-action {
            padding: 10px 20px;
            border-radius: 8px;
            background: rgba(255,255,255,0.05);
            border: 1px solid rgba(255,255,255,0.1);
            color: var(--text);
            cursor: pointer;
            font-weight: 600;
            transition: all 0.2s ease;
        }
        .btn-action:hover {
            border-color: var(--accent);
            color: var(--accent);
        }
    </style>
</head>
<body>
    <div class="header">
        <div class="title-group">
            <h1>PS3 // Mission Control</h1>
            <p>Canlı Donanım Telemetrisi & Oyun Yönetim Kokpiti &bull; IP: <span id="ps3-ip">...</span></p>
        </div>
        <div class="status-badge" id="status-badge">
            <div class="status-dot"></div>
            <span id="status-text">BAĞLANIYOR...</span>
        </div>
    </div>

    <div class="grid">
        <div class="card">
            <h3>CELL / CPU Sıcaklığı</h3>
            <div class="metric-value"><span id="cpu-temp">--</span><span class="metric-unit">°C</span></div>
            <div class="progress-track"><div class="progress-bar" id="cpu-bar" style="width: 0%; background: var(--green);"></div></div>
        </div>

        <div class="card">
            <h3>RSX / GPU Sıcaklığı</h3>
            <div class="metric-value"><span id="rsx-temp">--</span><span class="metric-unit">°C</span></div>
            <div class="progress-track"><div class="progress-bar" id="rsx-bar" style="width: 0%; background: var(--green);"></div></div>
        </div>

        <div class="card">
            <h3>Fan Hızı</h3>
            <div class="metric-value"><span id="fan-speed">--</span><span class="metric-unit">%</span></div>
            <div class="progress-track"><div class="progress-bar" id="fan-bar" style="width: 0%; background: var(--accent);"></div></div>
        </div>

        <div class="card">
            <h3>Boş VSH RAM</h3>
            <div class="metric-value"><span id="ram-free">--</span><span class="metric-unit">MB</span></div>
            <div class="progress-track"><div class="progress-bar" id="ram-bar" style="width: 70%; background: #a855f7;"></div></div>
        </div>
    </div>

    <div class="games-section">
        <div class="section-header">
            <div>
                <h2>Yüklü Oyun Kütüphanesi</h2>
                <p style="color: var(--text-muted); font-size: 13px; margin-top: 4px;">Aktif Takılı Disk: <strong id="mounted-game" style="color: var(--accent);">XMB (Ana Menü)</strong></p>
            </div>
            <div class="actions-row">
                <button class="btn-action" onclick="unmountGame()">Diski Çıkar (Unmount)</button>
                <button class="btn-action" onclick="trimRam()">RAM Turbo (Trim)</button>
                <button class="btn-action" onclick="sendCustomPopup()">TV'ye Bildirim Gönder</button>
            </div>
        </div>

        <div class="games-grid" id="games-container">
            <p style="color: var(--text-muted);">Oyunlar taranıyor...</p>
        </div>
    </div>

    <script>
        function updateColor(temp, elem, bar) {
            elem.innerText = temp;
            bar.style.width = Math.min(100, Math.max(0, (temp / 85) * 100)) + '%';
            if (temp >= 74) bar.style.background = 'var(--red)';
            else if (temp >= 65) bar.style.background = 'var(--yellow)';
            else bar.style.background = 'var(--green)';
        }

        async function fetchStats() {
            try {
                const res = await fetch('/api/stats');
                const data = await res.json();
                document.getElementById('ps3-ip').innerText = data.ip;
                if (data.online) {
                    document.getElementById('status-text').innerText = 'KONSOL ÇEVRİMİÇİ';
                    document.getElementById('status-badge').style.borderColor = 'var(--green)';
                    document.getElementById('status-badge').style.color = 'var(--green)';
                    updateColor(data.cpu, document.getElementById('cpu-temp'), document.getElementById('cpu-bar'));
                    updateColor(data.rsx, document.getElementById('rsx-temp'), document.getElementById('rsx-bar'));
                    document.getElementById('fan-speed').innerText = data.fan;
                    document.getElementById('fan-bar').style.width = data.fan + '%';
                    document.getElementById('ram-free').innerText = (data.mem_kb / 1024).toFixed(2);
                    document.getElementById('mounted-game').innerText = data.mounted_title || 'XMB (Ana Menü)';
                } else {
                    document.getElementById('status-text').innerText = 'KONSOL ÇEVRİMDIŞI';
                    document.getElementById('status-badge').style.borderColor = 'var(--red)';
                    document.getElementById('status-badge').style.color = 'var(--red)';
                }
            } catch (e) {
                console.error(e);
            }
        }

        async function fetchGames() {
            try {
                const res = await fetch('/api/games');
                const games = await res.json();
                const container = document.getElementById('games-container');
                if (games.length === 0) {
                    container.innerHTML = '<p style="color: var(--text-muted);">Hiç ISO veya klasör oyunu bulunamadı.</p>';
                    return;
                }
                container.innerHTML = '';
                games.forEach(g => {
                    const card = document.createElement('div');
                    card.className = 'game-card';
                    card.innerHTML = `
                        <div>
                            <div class="game-name">${g.title}</div>
                            <div class="game-type">${g.type}</div>
                        </div>
                        <button class="btn-mount" onclick="mountGame('${encodeURIComponent(g.path)}')">Konsola Tak (Mount)</button>
                    `;
                    container.appendChild(card);
                });
            } catch (e) {
                console.error(e);
            }
        }

        async function mountGame(path) {
            await fetch('/api/mount?path=' + path);
            fetchStats();
        }

        async function unmountGame() {
            await fetch('/api/unmount');
            fetchStats();
        }

        async function trimRam() {
            await fetch('/api/trim_ram');
            alert('RAM Önbelleği temizlendi!');
            fetchStats();
        }

        async function sendCustomPopup() {
            const msg = prompt('TV ekranında çıkacak mesajı yazın:');
            if (msg) {
                await fetch('/api/popup?msg=' + encodeURIComponent(msg));
            }
        }

        fetchStats();
        fetchGames();
        setInterval(fetchStats, 2000);
    </script>
</body>
</html>
"""

class MissionControlHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        query = urllib.parse.parse_qs(parsed.query)

        if path == "/" or path == "/index.html":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(HTML_TEMPLATE.encode("utf-8"))

        elif path == "/api/stats":
            stats = client.get_telemetry()
            stats["ip"] = client.ip
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(stats).encode("utf-8"))

        elif path == "/api/games":
            games = client.list_installed_games()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(games).encode("utf-8"))

        elif path == "/api/mount":
            game_path = urllib.parse.unquote(query.get("path", [""])[0])
            if game_path:
                client.mount_game(game_path)
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"status": "ok"}')

        elif path == "/api/unmount":
            client.unmount()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"status": "ok"}')

        elif path == "/api/trim_ram":
            client.trim_ram()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"status": "ok"}')

        elif path == "/api/popup":
            msg = urllib.parse.unquote(query.get("msg", [""])[0])
            if msg:
                client.send_popup(msg)
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"status": "ok"}')

        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        pass  # Suppress HTTP server console logs for clean UI

def start_server(port=COCKPIT_PORT):
    print("================================================================")
    print(f"       PS3 MISSION CONTROL // CYBERPUNK WEB KOKPİTİ           ")
    print("================================================================")
    print(f"[*] Hedef PS3 IP : {PS3_IP}")
    print(f"[+] PC Tarayıcı  : http://localhost:{port}")
    print(f"[+] Mobil / Ağ   : http://0.0.0.0:{port}")
    print("================================================================")
    print("Kapatmak için CTRL + C yapabilirsiniz.\n")

    with socketserver.TCPServer(("", port), MissionControlHandler) as httpd:
        httpd.serve_forever()

if __name__ == "__main__":
    start_server()
