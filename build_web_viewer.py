"""
=============================================================================
Interactive 3D Web Viewer Suite for Indonesian Banknotes (1992 Series)
=============================================================================
Generates:
  1. index.html - Multi-model 3D web viewer with model switcher
  2. viewer_standalone.html - Standalone zero-install viewer with embedded Base64 models
  3. serve.py - One-click local HTTP server
=============================================================================
"""

import os
import base64

ROOT_DIR = r"E:\blender-gemini\rupiah_banknotes"
WEB_DIR  = os.path.join(ROOT_DIR, "web_viewer")
os.makedirs(WEB_DIR, exist_ok=True)

GLB_100      = os.path.join(ROOT_DIR, "rupiah_100.glb")
GLB_500      = os.path.join(ROOT_DIR, "rupiah_500.glb")
GLB_SHOWCASE = os.path.join(ROOT_DIR, "rupiah_showcase.glb")

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Indonesian Banknotes 1992 Series | 3D Interactive Numismatic Studio</title>
  <script type="module" src="https://ajax.googleapis.com/ajax/libs/model-viewer/3.4.0/model-viewer.min.js"></script>
  <style>
    :root {
      --bg-dark: #0f1115;
      --panel-bg: rgba(20, 24, 32, 0.88);
      --accent: #d97706;
      --accent-pinisi: #ea580c;
      --accent-orangutan: #15803d;
      --text: #f3f4f6;
      --text-dim: #9ca3af;
      --border: rgba(255, 255, 255, 0.12);
    }
    
    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      -webkit-font-smoothing: antialiased;
    }
    
    body {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      background: var(--bg-dark);
      color: var(--text);
      overflow: hidden;
      width: 100vw;
      height: 100vh;
      display: flex;
      flex-direction: column;
    }
    
    /* Top Header Bar */
    header {
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      height: 64px;
      background: linear-gradient(180deg, rgba(15, 17, 21, 0.95) 0%, rgba(15, 17, 21, 0.3) 100%);
      backdrop-filter: blur(16px);
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 24px;
      z-index: 100;
      border-bottom: 1px solid var(--border);
    }
    
    .brand {
      display: flex;
      align-items: center;
      gap: 14px;
    }
    
    .brand-logo {
      font-size: 14px;
      font-weight: 800;
      letter-spacing: 2px;
      color: #ffffff;
      background: rgba(255, 255, 255, 0.1);
      border: 1px solid rgba(255, 255, 255, 0.25);
      padding: 4px 10px;
      border-radius: 4px;
    }
    
    .brand-model {
      font-size: 16px;
      font-weight: 700;
      letter-spacing: 0.5px;
      color: var(--text);
    }
    
    .brand-subtitle {
      font-size: 11px;
      color: var(--text-dim);
      letter-spacing: 0.5px;
    }

    /* Model Selection Switcher Tabs */
    .model-tabs {
      display: flex;
      gap: 6px;
      background: rgba(0, 0, 0, 0.4);
      padding: 4px;
      border-radius: 24px;
      border: 1px solid var(--border);
    }
    
    .tab-btn {
      background: transparent;
      border: none;
      color: var(--text-dim);
      padding: 6px 16px;
      border-radius: 18px;
      font-size: 12px;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.2s ease;
    }
    
    .tab-btn:hover {
      color: #fff;
    }
    
    .tab-btn.active {
      background: var(--accent);
      color: #fff;
      box-shadow: 0 2px 10px rgba(217, 119, 6, 0.4);
    }

    /* 3D Model Viewer Canvas */
    model-viewer {
      width: 100%;
      height: 100%;
      background: radial-gradient(circle at 50% 45%, #1f2530 0%, #0d0f14 85%);
      --progress-bar-color: var(--accent);
      --progress-bar-height: 4px;
    }

    /* Floating UI Controls Toolbar */
    .controls-panel {
      position: absolute;
      bottom: 24px;
      left: 50%;
      transform: translateX(-50%);
      background: var(--panel-bg);
      backdrop-filter: blur(20px);
      border: 1px solid var(--border);
      border-radius: 30px;
      padding: 8px 16px;
      display: flex;
      align-items: center;
      gap: 8px;
      box-shadow: 0 16px 36px rgba(0, 0, 0, 0.5);
      z-index: 100;
    }
    
    .btn {
      background: rgba(255, 255, 255, 0.06);
      color: var(--text);
      border: 1px solid var(--border);
      padding: 8px 14px;
      border-radius: 20px;
      font-size: 12px;
      font-weight: 600;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 6px;
      transition: all 0.2s ease;
      white-space: nowrap;
    }
    
    .btn:hover {
      background: rgba(255, 255, 255, 0.15);
      border-color: rgba(255, 255, 255, 0.3);
      transform: translateY(-1px);
    }
    
    .btn.active {
      background: var(--accent);
      border-color: var(--accent);
      color: #ffffff;
      box-shadow: 0 0 12px rgba(217, 119, 6, 0.4);
    }
    
    .divider {
      width: 1px;
      height: 20px;
      background: var(--border);
      margin: 0 4px;
    }

    /* Side Info Card */
    .info-card {
      position: absolute;
      top: 80px;
      right: 24px;
      background: var(--panel-bg);
      backdrop-filter: blur(16px);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 16px;
      width: 280px;
      box-shadow: 0 12px 28px rgba(0, 0, 0, 0.4);
      z-index: 90;
      font-size: 12px;
      line-height: 1.6;
    }
    
    .info-title {
      font-weight: 700;
      font-size: 13px;
      color: #fff;
      margin-bottom: 10px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      border-bottom: 1px solid var(--border);
      padding-bottom: 6px;
    }
    
    .spec-row {
      display: flex;
      justify-content: space-between;
      padding: 4px 0;
      border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    .spec-label {
      color: var(--text-dim);
    }
    
    .spec-val {
      font-weight: 600;
      color: #fff;
      text-align: right;
    }
    
    /* Help Hint */
    .help-hint {
      position: absolute;
      bottom: 24px;
      left: 24px;
      font-size: 11px;
      color: var(--text-dim);
      background: rgba(0,0,0,0.4);
      padding: 6px 12px;
      border-radius: 16px;
      pointer-events: none;
    }

    @media (max-width: 768px) {
      .info-card { display: none; }
      .controls-panel { width: 92%; overflow-x: auto; justify-content: flex-start; }
      header { flex-direction: column; height: auto; padding: 12px; gap: 8px; }
    }
  </style>
</head>
<body>

  <header>
    <div class="brand">
      <div class="brand-logo">BANK INDONESIA</div>
      <div>
        <div class="brand-model" id="header-title">Uang Kertas 100 Rupiah (1992)</div>
        <div class="brand-subtitle" id="header-subtitle">Perahu Pinisi &bull; Anak Gunung Krakatau</div>
      </div>
    </div>
    
    <div class="model-tabs">
      <button class="tab-btn active" id="tab-100" onclick="switchModel('100')">100 Rupiah (Pinisi)</button>
      <button class="tab-btn" id="tab-500" onclick="switchModel('500')">500 Rupiah (Orangutan)</button>
      <button class="tab-btn" id="tab-showcase" onclick="switchModel('showcase')">Both Notes (Showcase)</button>
    </div>
  </header>

  <model-viewer
    id="banknote-viewer"
    src="{SRC_100}"
    camera-controls
    auto-rotate
    rotation-per-second="18deg"
    camera-orbit="0deg 85deg 0.28m"
    min-camera-orbit="auto auto 0.12m"
    max-camera-orbit="auto auto 0.8m"
    field-of-view="30deg"
    shadow-intensity="1.5"
    shadow-softness="0.7"
    exposure="1.05"
    environment-image="neutral"
    ar
  >
  </model-viewer>

  <div class="info-card" id="info-card">
    <div class="info-title">
      <span id="card-denomination">100 RUPIAH</span>
      <span style="color: var(--accent); font-size: 11px;">EMISI 1992</span>
    </div>
    <div class="spec-row">
      <span class="spec-label">Obverse (Front)</span>
      <span class="spec-val" id="card-obverse">Perahu Pinisi</span>
    </div>
    <div class="spec-row">
      <span class="spec-label">Reverse (Back)</span>
      <span class="spec-val" id="card-reverse">Anak Gn. Krakatau</span>
    </div>
    <div class="spec-row">
      <span class="spec-label">Watermark</span>
      <span class="spec-val" id="card-watermark">Ki Hajar Dewantara</span>
    </div>
    <div class="spec-row">
      <span class="spec-label">Dimensions</span>
      <span class="spec-val" id="card-dims">136 × 67 mm</span>
    </div>
    <div class="spec-row">
      <span class="spec-label">Printer</span>
      <span class="spec-val">Perum Peruri</span>
    </div>
    <div class="spec-row">
      <span class="spec-label">Substrate</span>
      <span class="spec-val">100% Cotton Rag Paper</span>
    </div>
  </div>

  <div class="controls-panel">
    <button class="btn active" id="btn-front" onclick="showFront()">Front Obverse</button>
    <button class="btn" id="btn-back" onclick="showBack()">Back Reverse</button>
    <button class="btn" id="btn-macro" onclick="macroZoom()">Macro Close-Up</button>
    
    <div class="divider"></div>
    
    <button class="btn active" id="btn-rotate" onclick="toggleRotate()">Auto Rotate</button>
    <button class="btn" id="btn-reset" onclick="resetView()">Reset</button>
  </div>

  <div class="help-hint">
    Drag to Orbit &bull; Right-Click to Pan &bull; Scroll to Zoom
  </div>

  <script>
    const viewer = document.getElementById('banknote-viewer');
    const btnRotate = document.getElementById('btn-rotate');

    const models = {
      '100': {
        src: '{SRC_100}',
        title: 'Uang Kertas 100 Rupiah (1992)',
        subtitle: 'Perahu Pinisi • Anak Gunung Krakatau',
        denom: '100 RUPIAH',
        obverse: 'Perahu Pinisi',
        reverse: 'Anak Gn. Krakatau',
        watermark: 'Ki Hajar Dewantara',
        dims: '136 × 67 mm',
        orbit: '0deg 85deg 0.28m'
      },
      '500': {
        src: '{SRC_500}',
        title: 'Uang Kertas 500 Rupiah (1992)',
        subtitle: 'Orangutan • Rumah Adat Kalimantan Timur',
        denom: '500 RUPIAH',
        obverse: 'Orangutan (Pongo)',
        reverse: 'Rumah Adat Kaltim',
        watermark: 'H.O.S. Tjokroaminoto',
        dims: '140 × 67.4 mm',
        orbit: '0deg 85deg 0.29m'
      },
      'showcase': {
        src: '{SRC_SHOWCASE}',
        title: 'Koleksi Uang Kertas 1992 (Duo)',
        subtitle: '100 Rupiah & 500 Rupiah Numismatic Showcase',
        denom: '100 & 500 RUPIAH',
        obverse: 'Pinisi & Orangutan',
        reverse: 'Krakatau & Rumah Adat',
        watermark: 'Dewantara & Tjokroaminoto',
        dims: 'Full 1992 Duo Set',
        orbit: '0deg 65deg 0.35m'
      }
    };

    let currentModelKey = '100';

    function switchModel(key) {
      currentModelKey = key;
      const data = models[key];
      
      // Update UI Tabs
      document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
      document.getElementById('tab-' + key).classList.add('active');
      
      // Update Headers and Card
      document.getElementById('header-title').textContent = data.title;
      document.getElementById('header-subtitle').textContent = data.subtitle;
      document.getElementById('card-denomination').textContent = data.denom;
      document.getElementById('card-obverse').textContent = data.obverse;
      document.getElementById('card-reverse').textContent = data.reverse;
      document.getElementById('card-watermark').textContent = data.watermark;
      document.getElementById('card-dims').textContent = data.dims;
      
      // Switch Model
      viewer.src = data.src;
      viewer.cameraOrbit = data.orbit;
      viewer.fieldOfView = '30deg';
    }

    function showFront() {
      viewer.cameraOrbit = '0deg 85deg 0.28m';
      viewer.fieldOfView = '30deg';
    }

    function showBack() {
      viewer.cameraOrbit = '180deg 85deg 0.28m';
      viewer.fieldOfView = '30deg';
    }

    function macroZoom() {
      viewer.cameraOrbit = '-25deg 75deg 0.14m';
      viewer.fieldOfView = '22deg';
    }

    function toggleRotate() {
      viewer.autoRotate = !viewer.autoRotate;
      btnRotate.classList.toggle('active', viewer.autoRotate);
    }

    function resetView() {
      const data = models[currentModelKey];
      viewer.cameraOrbit = data.orbit;
      viewer.fieldOfView = '30deg';
      if (!viewer.autoRotate) toggleRotate();
    }
  </script>
</body>
</html>
"""

def generate_web_viewers():
    print(f"[Web Viewer] Generating viewer files in {WEB_DIR}...")
    
    # 1. Standard index.html referencing relative GLB files
    index_html = HTML_TEMPLATE.replace("{SRC_100}", "../rupiah_100.glb")
    index_html = index_html.replace("{SRC_500}", "../rupiah_500.glb")
    index_html = index_html.replace("{SRC_SHOWCASE}", "../rupiah_showcase.glb")
    
    index_path = os.path.join(WEB_DIR, "index.html")
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(index_html)
    print(f"  -> Created {index_path}")
    
    # 2. Standalone viewer with embedded Base64 data URIs
    def get_base64_uri(file_path):
        if os.path.exists(file_path):
            with open(file_path, "rb") as f:
                b64 = base64.b64encode(f.read()).decode('ascii')
            return f"data:model/gltf-binary;base64,{b64}"
        return ""
    
    uri_100 = get_base64_uri(GLB_100)
    uri_500 = get_base64_uri(GLB_500)
    uri_showcase = get_base64_uri(GLB_SHOWCASE)
    
    if uri_100 and uri_500:
        standalone_html = HTML_TEMPLATE.replace("{SRC_100}", uri_100)
        standalone_html = standalone_html.replace("{SRC_500}", uri_500)
        standalone_html = standalone_html.replace("{SRC_SHOWCASE}", uri_showcase if uri_showcase else uri_100)
        
        standalone_path = os.path.join(WEB_DIR, "viewer_standalone.html")
        with open(standalone_path, "w", encoding="utf-8") as f:
            f.write(standalone_html)
        print(f"  -> Created {standalone_path} (Standalone with Base64 embedded)")
    else:
        print("[Notice] GLB models not ready yet for standalone embedding.")

    # 3. Simple local server script
    serve_py = """import http.server
import socketserver
import os
import webbrowser

PORT = 8080
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

print(f"Starting Indonesian Banknotes 3D Web Viewer at http://localhost:{PORT}/index.html")
webbrowser.open(f"http://localhost:{PORT}/index.html")

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\\nServer stopped.")
"""
    serve_path = os.path.join(WEB_DIR, "serve.py")
    with open(serve_path, "w", encoding="utf-8") as f:
        f.write(serve_py)
    print(f"  -> Created {serve_path}")

if __name__ == "__main__":
    generate_web_viewers()
