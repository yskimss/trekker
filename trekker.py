# trekker.py - Pythonista 3용 트래킹 + 고도/상승 동적 전환 + GPX 배지 클릭 이동 + 기록 시 진행방향 자동회전 + 나침반/십자선 3초 표시 + 거리 척도 + GPX 고도 프로파일 + 기록 중 5초 간격 진행방향 회전 + 회전 방향 보정 + GPS 노이즈 제거/곡선 보정 + 상단 방위 바 + 상단 UI 높이 축소 + 고도 그래프 위치 점 (v4.20)
import ui, location, math, os, time, datetime, json, urllib.request, threading, sys, socket
import dialogs, console, sound
import http.server
import urllib.parse
import xml.etree.ElementTree as ET

try:
    import background
except ImportError:
    background = None

try:
    import photos
except ImportError:
    photos = None

try:
    import motion
except ImportError:
    motion = None

SAVE_DIR = os.path.join(os.path.expanduser('~/Documents'), 'treks')
CONFIG_PATH = os.path.join(SAVE_DIR, 'trek_config.json')
LOG_PATH = os.path.join(SAVE_DIR, 'trek_debug.txt')

try:
    os.makedirs(SAVE_DIR, exist_ok=True)
except Exception:
    pass

MAX_ACCURACY = 30       # m, 이보다 부정확한 좌표는 기록 안 함
MIN_STEP = 5            # m, 이보다 적게 움직이면 기록 안 함
ALT_THRESHOLD = 3       # m, 고도 노이즈 필터
AUTOSAVE_SEC = 60
TRACK_HEADING_SEC = 5   # s, 기록 중 진행 방향(지도 회전 기준)을 갱신하는 간격
TRACK_HEADING_DIST = 10 # m, 현재 위치와 이만큼 이전 위치를 이은 선으로 방향 계산
# ---- GPS 노이즈 제거 설정
START_MAX_ACCURACY = 20 # m, 기록 첫 점은 이보다 정확할 때만 채택 (MAX_ACCURACY는 이후 점에 적용)
FAST_SPEED_MPS = 10.0   # m/s, 1초에 10m 이상 같은 '단시간 장거리 이동'은 GPS 튐으로 보고 곡선 보정
SPIKE_GAIN = 0.1        # 튐으로 보인 좌표를 반영하는 비율 (작을수록 예측 곡선을 더 따라감)
JUMP_CONFIRM = 3        # 튐으로 보였던 좌표가 연속 N회 비슷한 곳이면 실제 이동으로 인정
JUMP_LINK_M = 30        # m, 위 연속 판정 시 직전 후보 좌표와의 최대 거리
KF_PROCESS_NOISE = 3.0  # m/s, 칼만 필터 프로세스 노이즈 (클수록 반응 빠름, 작을수록 부드러움)
CURVE_SMOOTH = 0.5      # 0~1, 기록된 점을 앞뒤 점의 중간 쪽으로 당기는 정도 (곡선화 강도)
CURVE_SMOOTH_FAST = 0.85  # 단시간 장거리 구간에 쓰는 곡선화 강도
STILL_SPEED_MPS = 0.25  # m/s, GPS 속도가 이보다 낮으면 정지로 보고 좌표를 갱신하지 않음
SERVER_PORT = 0
TOP_INSET = 44          # 상태바(노치) 높이

# ---------------------------------------------------------------- 설정 파일 로드
def load_config():
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            pass
    return {}

CONFIG = load_config()
VWORLD_KEY = CONFIG.get('vworld_key', '').strip()

try:
    MAG_DECLINATION = float(CONFIG.get('declination', -8.0))
except Exception:
    MAG_DECLINATION = -8.0

HEADING_STATE = {'on': False}

# ---------------------------------------------------------------- 로거 설정
def dlog(msg):
    try:
        os.makedirs(SAVE_DIR, exist_ok=True)
        timestamp = datetime.datetime.now().strftime('%m-%d %H:%M:%S')
        log_line = '%s %s\n' % (timestamp, msg)
        with open(LOG_PATH, 'a', encoding='utf-8') as f:
            f.write(log_line)
            f.flush()
            os.fsync(f.fileno())
    except Exception as e:
        print("Log error:", e)

dlog("=== 트레커 앱 시작됨 (v4.20) ===")

def enable_fault():
    try:
        import faulthandler
        with open(LOG_PATH, 'a', encoding='utf-8') as f:
            faulthandler.enable(file=f)
    except Exception:
        pass

def run_on_main(fn):
    try:
        ui.delay(fn, 0)
    except Exception:
        try:
            fn()
        except Exception:
            pass

# ---------------------------------------------------------------- 지도 및 레이어 선택 HTML
MAP_HTML = """<!DOCTYPE html><html><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.css">
<script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.js"></script>
<!-- 지도 회전 플러그인 (leaflet-rotate) CDN -->
<script src="https://unpkg.com/leaflet-rotate@0.2.8/dist/leaflet-rotate.js"></script>
<style>
  html, body, #map {
    height: 100%; width: 100%; margin: 0; background: #1c1c1e;
    -webkit-tap-highlight-color: transparent;
  }
  #layer-container {
    position: absolute; top: 29px; left: 12px; right: 12px; z-index: 99999;
    display: flex; flex-direction: column; align-items: flex-end;
    touch-action: manipulation; pointer-events: none;
  }
  #layer-toggle-btn, #layer-box, #gpx-name-badge, #gpx-elev { pointer-events: auto; }
  
  #top-right-group {
    display: flex; align-items: center; gap: 8px; width: 100%;
  }
  /* GPX 정보 영역: [고도 프로파일 40%][GPX명 60%] (지도 선택 버튼 왼쪽) */
  #gpx-info {
    flex: 1 1 0; min-width: 0; display: flex; justify-content: flex-end;
    align-items: center; gap: 8px; pointer-events: none;
  }
  #gpx-elev {
    display: none; position: relative; width: calc(40% - 4px); height: 38px; box-sizing: border-box;
    padding: 4px 6px; background: rgba(30,30,30,0.95);
    border: 1px solid rgba(255,255,255,0.3); border-radius: 8px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.5);
  }
  #gpx-elev.show { display: block; }
  #gpx-elev svg { display: block; }
  #elev-svg { position: absolute; left: 6px; right: 6px; top: 4px; bottom: 4px; }
  #elev-svg svg { width: 100%; height: 100%; }
  /* 십자선(지도 중심)이 GPX선 근처일 때 고도 그래프 위 해당 위치를 가리키는 점 */
  #elev-cursor { position: absolute; left: 6px; right: 6px; top: 4px; bottom: 4px; display: none; pointer-events: none; }
  #elev-dot {
    position: absolute; width: 10px; height: 10px; margin: -7px 0 0 -7px;
    box-sizing: content-box; border-radius: 50%; background: #ffffff; border: 2px solid #0a84ff;
    box-shadow: 0 0 0 2px rgba(10,132,255,0.35), 0 1px 4px rgba(0,0,0,0.7);
  }
  .elev-none { display: block; text-align: center; color: #8e8e93; font-size: 11px; line-height: 28px; }
  
  #gpx-name-badge {
    background: rgba(30,30,30,0.95); color: #0a84ff; border: 1px solid rgba(255,255,255,0.3);
    padding: 0 8px; border-radius: 8px; font-size: 14px; font-weight: bold;
    box-shadow: 0 4px 12px rgba(0,0,0,0.5);
    width: calc(60% - 4px); height: 38px; line-height: 36px; box-sizing: border-box;
    text-align: center; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
    display: none;
    cursor: pointer; touch-action: manipulation; -webkit-appearance: none;
  }
  #gpx-name-badge.show { display: block; }

  #layer-toggle-btn {
    background: rgba(30,30,30,0.95); color: white; border: 1px solid rgba(255,255,255,0.3);
    padding: 10px 14px; border-radius: 8px; font-size: 14px; font-weight: bold;
    cursor: pointer; box-shadow: 0 4px 12px rgba(0,0,0,0.5);
    -webkit-appearance: none; touch-action: manipulation; white-space: nowrap;
  }
  #layer-box {
    margin-top: 6px; background: rgba(30,30,30,0.95); padding: 8px; border-radius: 8px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.5); display: none; flex-direction: column; gap: 6px;
    max-height: 260px; overflow-y: auto; border: 1px solid rgba(255,255,255,0.15);
  }
  #layer-box.show { display: flex; }
  .layer-btn {
    background: #3a3a3c; color: white; border: none; padding: 10px 14px;
    font-size: 13px; font-weight: bold; border-radius: 6px; text-align: left; cursor: pointer;
    display: flex; justify-content: space-between; align-items: center; gap: 12px;
    -webkit-appearance: none; touch-action: manipulation; width: 100%;
  }
  .layer-btn.active { background: #0a84ff; }
  .badge { font-size: 10px; padding: 2px 6px; border-radius: 4px; background: rgba(0,0,0,0.4); }

  #bottom-right-controls {
    position: absolute; bottom: 16px; right: 12px; z-index: 99999;
    display: flex; flex-direction: column; align-items: flex-end; gap: 8px;
    touch-action: manipulation;
  }
  
  #compass-btn {
    background: #000000; border: 1px solid rgba(255,255,255,0.25);
    width: 44px; height: 44px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    cursor: pointer; box-shadow: 0 4px 12px rgba(0,0,0,0.6);
    -webkit-appearance: none; touch-action: manipulation;
    padding: 0;
  }

  #weather-box {
    background: #0d0d0d; border: 1px solid rgba(255,255,255,0.18);
    width: 44px; padding: 6px 0 8px 0; border-radius: 22px;
    display: none; flex-direction: column; align-items: center; justify-content: center;
    box-shadow: 0 4px 12px rgba(0,0,0,0.65); color: #ffffff;
    cursor: pointer; touch-action: manipulation; -webkit-appearance: none;
  }
  #weather-box.pinned {
    border-color: #0a84ff;
    box-shadow: 0 0 0 2px rgba(10,132,255,0.45), 0 4px 12px rgba(0,0,0,0.65);
  }
  #wx-icon { 
    display: flex; align-items: center; justify-content: center;
    width: 30px; height: 30px; line-height: 0; margin-bottom: 4px;
  }
  #wx-temp { 
    font-size: 16px; font-weight: 900; line-height: 1; 
    letter-spacing: -0.5px; margin-left: 2px;
  }
  #wx-bar {
    width: 26px; height: 3.5px; background: #4b89f3; 
    border-radius: 2px; margin: 5px 0 4px 0;
  }
  #wx-dust {
    font-size: 11px; font-weight: 700; color: #a1a1a6; 
    line-height: 1.1; letter-spacing: -0.5px;
  }

  #compass-btn.active {
    border-color: #0a84ff;
    box-shadow: 0 0 0 2px rgba(10,132,255,0.45), 0 4px 12px rgba(0,0,0,0.6);
  }
  .heading-icon { background: none !important; border: none !important; pointer-events: none; }

  #diff-wrap { position: relative; display: none; }
  #diff-wrap.show { display: block; }
  #diff-btn {
    background: #000000; border: 1px solid rgba(255,255,255,0.25);
    width: 44px; height: 44px; border-radius: 50%;
    display: flex; flex-direction: column; align-items: center; justify-content: center;
    cursor: pointer; box-shadow: 0 4px 12px rgba(0,0,0,0.6);
    -webkit-appearance: none; touch-action: manipulation;
    padding: 0; color: #8e8e93;
  }
  #diff-lv { font-size: 10px; font-weight: 900; line-height: 1; margin-top: 2px; }
  #diff-panel {
    display: none; position: absolute; right: 52px; top: 0; white-space: nowrap;
    background: rgba(30,30,30,0.95); color: white; padding: 10px 12px; border-radius: 8px;
    border: 1px solid rgba(255,255,255,0.15); box-shadow: 0 4px 12px rgba(0,0,0,0.5);
    font-size: 12px; line-height: 1.7; pointer-events: none;
  }
  #diff-panel.show { display: block; }

  #loc-btn {
    background: rgba(30,30,30,0.95); border: 1px solid rgba(255,255,255,0.3);
    width: 44px; height: 44px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    cursor: pointer; box-shadow: 0 4px 12px rgba(0,0,0,0.5);
    -webkit-appearance: none; touch-action: manipulation;
    padding: 0;
  }
  #layer-info-badge {
    background: rgba(30,30,30,0.9); color: #0a84ff; border: 1px solid rgba(255,255,255,0.2);
    padding: 6px 12px; border-radius: 6px; font-size: 12px; font-weight: bold;
    box-shadow: 0 2px 8px rgba(0,0,0,0.4); pointer-events: none;
  }

  /* 화면 중앙 투명 나침반 오버레이 (사이즈 4/5로 축소: 256px) */
  #screen-compass-overlay {
    position: absolute; top: 50%; left: 50%; width: 256px; height: 256px;
    transform: translate(-50%, -50%); pointer-events: none; z-index: 999;
    opacity: 0; transition: opacity 0.3s ease;
  }
  #screen-compass-overlay.show { opacity: 1; }
  #screen-compass-ring {
    width: 100%; height: 100%; position: relative;
    transform-origin: center center;
  }

  /* 지도 이동(드래그) 시 화면 중앙에 잠시 표시되는 가는 십자선 */
  #center-cross {
    position: absolute; top: 50%; left: 50%; width: 64px; height: 64px;
    transform: translate(-50%, -50%); pointer-events: none; z-index: 999;
    opacity: 0; transition: opacity 0.3s ease;
  }
  #center-cross.show { opacity: 1; }

  /* 현재위치 버튼 옆 거리 척도 (투명 배경, 검은 글자) */
  #loc-row { display: flex; align-items: center; gap: 10px; }
  #scale-bar {
    background: transparent; color: #000000; pointer-events: none;
    font-size: 13px; font-weight: 800; line-height: 1.1;
    text-shadow: 0 0 3px rgba(255,255,255,0.9), 0 0 2px rgba(255,255,255,0.9);
  }
  #scale-label { display: flex; justify-content: space-between; padding: 0 1px; }
  #scale-line {
    height: 6px; margin-top: 2px; width: 60px;
    border-left: 2px solid #000000; border-right: 2px solid #000000; border-bottom: 2px solid #000000;
    box-sizing: border-box; filter: drop-shadow(0 0 1.5px rgba(255,255,255,0.9));
  }
</style>
</head><body>
<div id="map"></div>

<div id="screen-compass-overlay">
  <div id="screen-compass-ring">
    <svg width="256" height="256" viewBox="0 0 256 256">
      <circle cx="128" cy="128" r="115" fill="none" stroke="#000000" stroke-width="2" opacity="0.85"/>
      <circle cx="128" cy="128" r="16" fill="rgba(0,0,0,0.08)" stroke="#000000" stroke-width="1.2" opacity="0.75"/>
      <line x1="128" y1="112" x2="128" y2="144" stroke="#000000" stroke-width="1.2" opacity="0.75"/>
      <line x1="112" y1="128" x2="144" y2="128" stroke="#000000" stroke-width="1.2" opacity="0.75"/>
      <g stroke="#000000" stroke-width="1.2" opacity="0.85" id="ticks-container"></g>
      <text x="128" y="55" font-size="28" font-weight="900" fill="#000000" text-anchor="middle">북</text>
      <text x="202" y="137" font-size="28" font-weight="900" fill="#000000" text-anchor="middle">동</text>
      <text x="128" y="221" font-size="28" font-weight="900" fill="#000000" text-anchor="middle">남</text>
      <text x="54" y="137" font-size="28" font-weight="900" fill="#000000" text-anchor="middle">서</text>
      <text x="128" y="76" font-size="16" font-weight="800" fill="#000000" opacity="0.95" text-anchor="middle">0</text>
      <text x="172" y="67" font-size="15" font-weight="800" fill="#000000" opacity="0.95" text-anchor="middle">30</text>
      <text x="203" y="99" font-size="15" font-weight="800" fill="#000000" opacity="0.95" text-anchor="middle">60</text>
      <text x="203" y="170" font-size="15" font-weight="800" fill="#000000" opacity="0.95" text-anchor="middle">120</text>
      <text x="172" y="202" font-size="15" font-weight="800" fill="#000000" opacity="0.95" text-anchor="middle">150</text>
      <text x="84" y="202" font-size="15" font-weight="800" fill="#000000" opacity="0.95" text-anchor="middle">210</text>
      <text x="53" y="170" font-size="15" font-weight="800" fill="#000000" opacity="0.95" text-anchor="middle">240</text>
      <text x="53" y="99" font-size="15" font-weight="800" fill="#000000" opacity="0.95" text-anchor="middle">300</text>
      <text x="84" y="67" font-size="15" font-weight="800" fill="#000000" opacity="0.95" text-anchor="middle">330</text>
    </svg>
  </div>
</div>

<div id="center-cross">
  <svg width="64" height="64" viewBox="0 0 64 64">
    <g stroke="#ffffff" stroke-width="3" opacity="0.55" stroke-linecap="round">
      <line x1="4" y1="32" x2="60" y2="32"/>
      <line x1="32" y1="4" x2="32" y2="60"/>
    </g>
    <g stroke="#000000" stroke-width="1.2" opacity="0.9" stroke-linecap="round">
      <line x1="4" y1="32" x2="60" y2="32"/>
      <line x1="32" y1="4" x2="32" y2="60"/>
    </g>
  </svg>
</div>

<div id="layer-container">
  <div id="top-right-group">
    <div id="gpx-info">
      <div id="gpx-elev">
        <div id="elev-svg"></div>
        <div id="elev-cursor"><div id="elev-dot"></div></div>
      </div>
      <div id="gpx-name-badge" ontouchend="onGpxBadgeClick(event)" onclick="onGpxBadgeClick(event)" title=""></div>
    </div>
    <button id="layer-toggle-btn" ontouchend="toggleLayerBox(event)" onclick="toggleLayerBox(event)">🗺️ 지도 선택</button>
  </div>
  <div id="layer-box">
    <button class="layer-btn active" id="btn-opentopo" ontouchend="switchLayer('opentopo', 'Topo (오프라인)', this, event)" onclick="switchLayer('opentopo', 'Topo (오프라인)', this, event)"><span>Topo (오프라인)</span><span class="badge" style="background:#30d158;">오프라인</span></button>
    <button class="layer-btn" id="btn-opentopo-online" ontouchend="switchLayer('opentopo_online', 'Topo (온라인)', this, event)" onclick="switchLayer('opentopo_online', 'Topo (온라인)', this, event)"><span>Topo (온라인)</span><span class="badge">온라인</span></button>
    <button class="layer-btn" id="btn-esri" ontouchend="switchLayer('esri', 'Esri (위성)', this, event)" onclick="switchLayer('esri', 'Esri (위성)', this, event)"><span>Esri (위성)</span><span class="badge">온라인</span></button>
    <button class="layer-btn" id="btn-cyclosm" ontouchend="switchLayer('cyclosm', 'CyclOSM (등산)', this, event)" onclick="switchLayer('cyclosm', 'CyclOSM (등산)', this, event)"><span>CyclOSM (등산)</span><span class="badge">온라인</span></button>
    __VWORLD_BUTTONS__
  </div>
</div>

<div id="bottom-right-controls">
  <div id="diff-wrap">
    <div id="diff-panel"></div>
    <button id="diff-btn" ontouchend="toggleDiffPanel(event)" onclick="toggleDiffPanel(event)" title="경로 난이도">
      <svg width="24" height="17" viewBox="0 0 24 17">
        <polygon points="1,16 9,2 14,10 17,6 23,16" fill="currentColor" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/>
      </svg>
      <span id="diff-lv">Lv1</span>
    </button>
  </div>
  <div id="weather-box" ontouchend="onWeatherClick(event)" onclick="onWeatherClick(event)" title="지도 중심 날씨">
    <span id="wx-icon"></span>
    <span id="wx-temp">-</span>
    <span id="wx-bar"></span>
    <span id="wx-dust">미세</span>
  </div>

  <button id="compass-btn" ontouchend="onCompassClick(event)" onclick="onCompassClick(event)" title="정북으로 복귀">
    <svg id="compass-svg" width="36" height="36" viewBox="0 0 36 36">
      <circle cx="18" cy="18" r="18" fill="#000000"/>
      <g id="dial-group" transform="rotate(0, 18, 18)">
        <g stroke="#8e8e93" stroke-width="2" stroke-linecap="round">
          <line x1="31" y1="18" x2="34" y2="18"/>
          <line x1="18" y1="31" x2="18" y2="34"/>
          <line x1="5" y1="18" x2="2" y2="18"/>
        </g>
        <g stroke="#8e8e93" stroke-width="2" stroke-linecap="round" opacity="0.55">
          <line x1="27.2" y1="8.8" x2="29.3" y2="6.7"/>
          <line x1="27.2" y1="27.2" x2="29.3" y2="29.3"/>
          <line x1="8.8" y1="27.2" x2="6.7" y2="29.3"/>
          <line x1="8.8" y1="8.8" x2="6.7" y2="6.7"/>
        </g>
        <text x="18" y="9.5" font-size="9" font-weight="900" fill="#ffffff" text-anchor="middle">N</text>
        <polygon points="18,14 24,27 18,23 12,27" fill="#ff5a36" stroke="#ff5a36" stroke-width="1" stroke-linejoin="round"/>
      </g>
    </svg>
  </button>

  <div id="loc-row">
  <div id="scale-bar">
    <div id="scale-label"><span id="scale-text">20m</span><span>0</span></div>
    <div id="scale-line"></div>
  </div>
  <button id="loc-btn" ontouchend="onLocBtnClick(event)" onclick="onLocBtnClick(event)" title="내 위치로 이동">
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
      <circle cx="12" cy="12" r="7" stroke="#ffffff" stroke-width="2"/>
      <line x1="12" y1="2" x2="12" y2="6" stroke="#ffffff" stroke-width="2" stroke-linecap="round"/>
      <line x1="12" y1="18" x2="12" y2="22" stroke="#ffffff" stroke-width="2" stroke-linecap="round"/>
      <line x1="2" y1="12" x2="6" y2="12" stroke="#ffffff" stroke-width="2" stroke-linecap="round"/>
      <line x1="18" y1="12" x2="22" y2="12" stroke="#ffffff" stroke-width="2" stroke-linecap="round"/>
    </svg>
  </button>
  </div>
  <div id="layer-info-badge">🗺️ Topo (오프라인)</div>
</div>

<script>
var PORT = __PORT__;
var map = L.map('map', {
  zoomControl: false, 
  attributionControl: false,
  rotate: true,
  touchRotate: true,
  rotateControl: false
}).setView([37.5665, 126.978], 15);

var proxyBase = 'http://127.0.0.1:' + PORT + '/proxy/';
var vworldKey = '__VWORLD_KEY__';

var layers = {
  'opentopo': L.tileLayer(proxyBase + 'opentopo/{z}/{x}/{y}.png', {maxZoom:17, keepBuffer: 8, updateWhenIdle: false}),
  'opentopo_online': L.tileLayer('https://tile.opentopomap.org/{z}/{x}/{y}.png', {maxZoom:17}),
  'esri': L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {maxZoom:19}),
  'cyclosm': L.tileLayer('https://{s}.tile-cyclosm.openstreetmap.fr/cyclosm/{z}/{x}/{y}.png', {maxZoom:20, subdomains:['a','b','c']})
};

if (vworldKey) {
  layers['vworld_base'] = L.tileLayer('https://api.vworld.kr/req/wmts/1.0.0/' + vworldKey + '/Base/{z}/{y}/{x}.png', {maxZoom:19});
  layers['vworld_sat'] = L.tileLayer('https://api.vworld.kr/req/wmts/1.0.0/' + vworldKey + '/Satellite/{z}/{y}/{x}.jpeg', {maxZoom:19});
}

var currentLayer = layers['opentopo'];
currentLayer.addTo(map);

L.DomEvent.disableClickPropagation(document.getElementById('layer-container'));
L.DomEvent.disableScrollPropagation(document.getElementById('layer-container'));
L.DomEvent.disableClickPropagation(document.getElementById('bottom-right-controls'));

function toggleLayerBox(e) {
  if (e) { e.preventDefault(); e.stopPropagation(); }
  document.getElementById('layer-box').classList.toggle('show');
}

var lastLat = 0, lastLon = 0;
var lastTouchTime = 0;

function onLocBtnClick(e) {
  if (e) { e.preventDefault(); e.stopPropagation(); }
  var now = Date.now();
  if (now - lastTouchTime < 300) return;
  lastTouchTime = now;

  if (lastLat && lastLon) {
    map.setView([lastLat, lastLon], Math.max(map.getZoom(), 16));
    if (wxCenterMode) {
      wxCenterMode = false;
      document.getElementById('weather-box').classList.remove('pinned');
      fetchWeatherAt(lastLat, lastLon);
    }
  }
}

var headingMode = false, headingRaw = null, hMarker = null, isRecording = false;
var hdCont = 0, hdInit = false, lastCompassTouch = 0;
var compassHideTimer = null;

function generateTicks() {
  var container = document.getElementById('ticks-container');
  if (!container) return;
  var html = '';
  for (var deg = 0; deg < 360; deg += 6) {
    var rad = deg * Math.PI / 180;
    var isMajor = (deg % 30 === 0);
    var rOuter = 115;
    var rInner = isMajor ? 99 : 105;
    var strokeW = isMajor ? 2.0 : 1.2;
    
    var x1 = 128 + rOuter * Math.sin(rad);
    var y1 = 128 - rOuter * Math.cos(rad);
    var x2 = 128 + rInner * Math.sin(rad);
    var y2 = 128 - rInner * Math.cos(rad);
    
    html += '<line x1="' + x1.toFixed(1) + '" y1="' + y1.toFixed(1) + '" x2="' + x2.toFixed(1) + '" y2="' + y2.toFixed(1) + '" stroke="#000000" stroke-width="' + strokeW + '"/>';
  }
  container.innerHTML = html;
}
window.addEventListener('DOMContentLoaded', generateTicks);

var HD_HTML = '<div id="hd-rot" style="width:160px;height:160px;transform-origin:80px 80px;transition:transform 0.12s linear;opacity:0;">'
  + '<svg width="160" height="160" viewBox="0 0 160 160">'
  + '<defs><radialGradient id="hdg" gradientUnits="userSpaceOnUse" cx="80" cy="80" r="70">'
  + '<stop offset="0.15" stop-color="#2f9bff" stop-opacity="0.9"/>'
  + '<stop offset="0.6" stop-color="#0a84ff" stop-opacity="0.5"/>'
  + '<stop offset="1" stop-color="#0a84ff" stop-opacity="0.05"/></radialGradient></defs>'
  + '<path d="M72.6,70.5 L36.9,24.8 A70,70 0 0 1 123.1,24.8 L87.4,70.5 A12,12 0 0 0 72.6,70.5 Z" fill="url(#hdg)"/>'
  + '<line x1="72.6" y1="70.5" x2="36.9" y2="24.8" stroke="#5ac8fa" stroke-opacity="0.85" stroke-width="1.5" stroke-linecap="round"/>'
  + '<line x1="87.4" y1="70.5" x2="123.1" y2="24.8" stroke="#5ac8fa" stroke-opacity="0.85" stroke-width="1.5" stroke-linecap="round"/>'
  + '<polygon points="80,54 88,69 72,69" fill="#ff3b30" stroke="#ffffff" stroke-width="1" stroke-linejoin="round"/>'
  + '</svg></div>';

function updateHeadingAngle() {
  if (!hMarker || headingRaw === null) return;
  var el = document.getElementById('hd-rot');
  if (!el) return;
  var screenAngle = headingRaw + mapCW();
  if (!hdInit) {
    hdCont = screenAngle;
    hdInit = true;
  } else {
    var d = (((screenAngle - hdCont) % 360) + 540) % 360 - 180;
    hdCont += d;
  }
  el.style.transform = 'rotate(' + hdCont + 'deg)';
  el.style.opacity = 1;
}

function updateScreenCompass() {
  var bearing = (map.getBearing ? map.getBearing() : 0) || 0;
  var ring = document.getElementById('screen-compass-ring');
  if (ring) {
    ring.style.transform = 'rotate(' + mapCW() + 'deg)';
  }
}

function showScreenCompassTemporarily() {
  var overlay = document.getElementById('screen-compass-overlay');
  if (!overlay) return;
  updateScreenCompass();
  hideCrosshairNow();   // 나침반이 나오면 십자선은 즉시 숨김
  overlay.classList.add('show');
  if (compassHideTimer) clearTimeout(compassHideTimer);
  compassHideTimer = setTimeout(function() {
    overlay.classList.remove('show');
  }, 3000);
}

function setHeading(h) {
  headingRaw = h;
  if (headingMode) {
    if (map.setBearing) {
      map.setBearing(headToBearing(h));
    }
  }
  updateHeadingAngle();
  updateScreenCompass();
}

function createCone() {
  if (hMarker) return;
  hdInit = false;
  hMarker = L.marker(me.getLatLng(), {
    icon: L.divIcon({className: 'heading-icon', html: HD_HTML, iconSize: [160, 160], iconAnchor: [80, 80]}),
    interactive: false, keyboard: false, zIndexOffset: 1000
  }).addTo(map);
}

function removeCone() {
  if (hMarker) { map.removeLayer(hMarker); hMarker = null; }
}

function setHeadingMode(on) {
  headingMode = on;
  var btn = document.getElementById('compass-btn');
  if (on) {
    btn.classList.add('active');
    headingRaw = null;
    if (!isRecording) createCone();
    if (lastLat && lastLon) {
      map.setView([lastLat, lastLon], Math.max(map.getZoom(), 17), {animate: false});
    }
  } else {
    btn.classList.remove('active');
    removeCone();
  }
  try {
    fetch('http://127.0.0.1:' + PORT + '/hmode?on=' + (on ? 1 : 0)).catch(function() {});
  } catch (err) {}
}

function onCompassClick(e) {
  if (e) { e.preventDefault(); e.stopPropagation(); }
  var now = Date.now();
  if (now - lastCompassTouch < 300) return;
  lastCompassTouch = now;
  quietUntil = now + 600;   // 나침반 버튼으로 정북 복귀할 때도 중앙 나침반 생략

  var inBounds = false;
  if (lastLat && lastLon) {
    var latLng = L.latLng(lastLat, lastLon);
    inBounds = map.getBounds().contains(latLng);
  }

  var noFix = !(lastLat && lastLon);
  if (noFix || !inBounds) {
    if (headingMode) {
      setHeadingMode(false);
    }
    map.setBearing(0);
    updateScreenCompass();
    return;
  }

  if (!headingMode) {
    setHeadingMode(true);
  } else {
    setHeadingMode(false);
    map.setBearing(0);
    updateScreenCompass();
  }
}

// 거리 척도: 화면 중심 위도 기준 (회전과 무관)
var SCALE_STEPS = [1, 2, 5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000, 50000, 100000, 200000, 500000, 1000000];
function updateScale() {
  var line = document.getElementById('scale-line');
  var txt = document.getElementById('scale-text');
  if (!line || !txt) return;
  var lat = map.getCenter().lat;
  var mpp = 156543.03392 * Math.cos(lat * Math.PI / 180) / Math.pow(2, map.getZoom());
  if (!(mpp > 0)) return;
  var maxM = mpp * 100;   // 최대 100px
  var pick = SCALE_STEPS[0];
  for (var i = 0; i < SCALE_STEPS.length; i++) {
    if (SCALE_STEPS[i] <= maxM) pick = SCALE_STEPS[i];
  }
  line.style.width = Math.max(20, Math.round(pick / mpp)) + 'px';
  txt.innerText = pick >= 1000 ? (pick / 1000) + 'km' : pick + 'm';
}
map.on('zoom moveend zoomend', updateScale);
updateScale();

// 기록 시작/재개 시 진행 방향 up 자동 회전 켜기, 종료 시 정북 복귀
var autoSession = false;          // 시작 버튼으로 자동 회전 중인 상태
var quietUntil = 0;               // 이 시각 전까지는 프로그램 회전에도 중앙 나침반을 띄우지 않음
var fingerDown = false, fingerUntil = 0;

// 두 손가락이 닿아 있는 동안(또는 직후)만 '손가락 회전'으로 간주
document.addEventListener('touchstart', function(e) {
  if (e.touches && e.touches.length >= 2) fingerDown = true;
}, {capture: true, passive: true});
function onFingerEnd(e) {
  if (!e.touches || e.touches.length < 2) {
    if (fingerDown) fingerUntil = Date.now() + 400;
    fingerDown = false;
  }
}
document.addEventListener('touchend', onFingerEnd, {capture: true, passive: true});
document.addEventListener('touchcancel', onFingerEnd, {capture: true, passive: true});
function isFingerRotating() {
  return fingerDown || Date.now() < fingerUntil;
}

// 지도 드래그 이동 시 중앙 십자선을 3초간 표시
var crossHideTimer = null;
function hideCrosshairNow() {
  var el = document.getElementById('center-cross');
  if (el) el.classList.remove('show');
  if (crossHideTimer) { clearTimeout(crossHideTimer); crossHideTimer = null; }
}
function hideCompassNow() {
  var ov = document.getElementById('screen-compass-overlay');
  if (ov) ov.classList.remove('show');
  if (compassHideTimer) { clearTimeout(compassHideTimer); compassHideTimer = null; }
}
function showCrosshairTemporarily() {
  var el = document.getElementById('center-cross');
  if (!el) return;
  hideCompassNow();     // 십자선이 나오면 나침반은 즉시 숨김
  el.classList.add('show');
  if (crossHideTimer) clearTimeout(crossHideTimer);
  crossHideTimer = setTimeout(function() {
    el.classList.remove('show');
  }, 3000);
}
map.on('drag', showCrosshairTemporarily);

function autoHeading(on) {
  autoSession = !!on;
  if (on) {
    if (!headingMode) setHeadingMode(true);
  } else {
    if (headingMode) setHeadingMode(false);
    map.setBearing(0);
    updateScreenCompass();
  }
}

// leaflet-rotate가 setBearing(θ)로 지도를 시계/반시계 중 어느 쪽으로 돌리는지 자동 판별
//  HEAD_SIGN = -1 : 지도가 시계방향으로 θ만큼 회전 (진행방향 h가 위로 오려면 setBearing(-h))
//  HEAD_SIGN = +1 : 지도가 반시계방향으로 θ만큼 회전 (setBearing(h))
var HEAD_SIGN = -1;
var rotateDetecting = false;
function detectRotateDirection() {
  try {
    var pane = map._rotatePane;
    if (!map.setBearing || !pane) return;
    var old = (map.getBearing ? map.getBearing() : 0) || 0;
    rotateDetecting = true;
    map.setBearing(90);
    var t = window.getComputedStyle(pane).transform;
    map.setBearing(old);
    rotateDetecting = false;
    var m = (t || '').match(/matrix(3d)?\\(([^)]+)\\)/);
    if (m) {
      var v = m[2].split(',').map(parseFloat);
      var ang = Math.atan2(v[1], v[0]) * 180 / Math.PI;
      if (isFinite(ang) && Math.abs(Math.abs(ang) - 90) < 20) {
        HEAD_SIGN = ang > 0 ? -1 : 1;
      }
    }
  } catch (err) {
    rotateDetecting = false;
  }
}
detectRotateDirection();

// 지도가 화면에서 실제로 시계방향으로 회전한 각도 (진북이 화면 위에서 시계방향으로 몇 도 위치인지)
function mapCW() {
  return -HEAD_SIGN * ((map.getBearing ? map.getBearing() : 0) || 0);
}
// 진행 방향 h(진북 기준)가 화면 위로 오게 하는 setBearing 인자
function headToBearing(h) {
  return (((HEAD_SIGN * h) % 360) + 360) % 360;
}

// 지도 화면 위쪽이 가리키는 방위를 파이썬(상단 방위 바)으로 전송
var lastUpSend = 0, upTimer = null;
function reportUp() {
  var up = (((360 - mapCW()) % 360) + 360) % 360;
  try {
    fetch('http://127.0.0.1:' + PORT + '/up?d=' + up.toFixed(1)).catch(function() {});
  } catch (err) {}
}
function reportUpThrottled() {
  var now = Date.now();
  if (now - lastUpSend >= 100) {
    lastUpSend = now;
    reportUp();
  } else if (!upTimer) {
    upTimer = setTimeout(function() {
      upTimer = null;
      lastUpSend = Date.now();
      reportUp();
    }, 100 - (now - lastUpSend));
  }
}

map.on('rotate', function() {
  if (rotateDetecting) return;
  reportUpThrottled();
  var bearing = map.getBearing();
  var dialGroup = document.getElementById('dial-group');
  if (dialGroup) {
    dialGroup.setAttribute('transform', 'rotate(' + mapCW() + ', 18, 18)');
  }
  updateHeadingAngle();
  updateScreenCompass();
  // 자동 회전(기록 중 / 부채꼴 방향 표시 중)에는 손가락으로 회전할 때만 중앙 나침반 표시
  if (isFingerRotating() || (!autoSession && !headingMode && Date.now() >= quietUntil)) {
    showScreenCompassTemporarily();
  }
});
reportUp();

var centerFetchTimer = null;
map.on('moveend', function() {
  if (centerFetchTimer) clearTimeout(centerFetchTimer);
  centerFetchTimer = setTimeout(function() {
    var c = map.getCenter();
    try {
      fetch('http://127.0.0.1:' + PORT + '/center_move?lat=' + c.lat.toFixed(6) + '&lon=' + c.lng.toFixed(6)).catch(function(){});
    } catch(err){}
  }, 400);
});

function switchLayer(key, name, btn, e) {
  if (e) { e.preventDefault(); e.stopPropagation(); }
  if (!layers[key]) return;
  if (currentLayer) map.removeLayer(currentLayer);
  currentLayer = layers[key];
  currentLayer.addTo(map);
  
  var btns = document.getElementsByClassName('layer-btn');
  for (var i = 0; i < btns.length; i++) {
    btns[i].classList.remove('active');
  }
  btn.classList.add('active');
  toggleLayerBox();
  document.getElementById('layer-info-badge').innerText = '🗺️ ' + name;
}

var me = L.circleMarker([0,0], {radius:8, color:'#ffffff', weight:3, fillColor:'#ff3b30', fillOpacity:1});
var routeLine = L.polyline([], {color:'#ff9f0a', weight:5, opacity:0.8}).addTo(map);
var gpxLine = L.polyline([], {color:'#0a84ff', weight:5, opacity:0.8}).addTo(map);
var extraLayer = L.layerGroup().addTo(map);
var first = true;

var _meSetLatLng = me.setLatLng.bind(me);
me.setLatLng = function(ll) {
  _meSetLatLng(ll);
  if (hMarker) hMarker.setLatLng(ll);
  return me;
};

var animTargetLat = 0, animTargetLon = 0;
var animCurrentLat = 0, animCurrentLon = 0;
var isAnimating = false;

function updateMap(lat, lon, pts, rec) {
  isRecording = !!rec;
  lastLat = lat;
  lastLon = lon;
  animTargetLat = lat;
  animTargetLon = lon;

  if (first) {
    animCurrentLat = lat;
    animCurrentLon = lon;
    map.setView([lat, lon], 16);
    me.setLatLng([lat, lon]);
    if (!map.hasLayer(me)) me.addTo(map);
    me.bringToFront();
    first = false;
  } else if (!isAnimating) {
    startMarkerAnimation();
  }

  if (pts && pts.length > 0) {
    routeLine.setLatLngs(pts);
  }

  if (headingMode) {
    if (isRecording && hMarker) removeCone();
    else if (!isRecording && !hMarker) createCone();
    map.panTo([lat, lon], {animate: true, duration: 0.5});
  }
}

function startMarkerAnimation() {
  isAnimating = true;
  function frame() {
    var dLat = animTargetLat - animCurrentLat;
    var dLon = animTargetLon - animCurrentLon;
    
    if (Math.abs(dLat) < 0.000001 && Math.abs(dLon) < 0.000001) {
      animCurrentLat = animTargetLat;
      animCurrentLon = animTargetLon;
      me.setLatLng([animCurrentLat, animCurrentLon]);
      isAnimating = false;
      return;
    }
    
    animCurrentLat += dLat * 0.15;
    animCurrentLon += dLon * 0.15;
    
    me.setLatLng([animCurrentLat, animCurrentLon]);
    me.bringToFront();
    
    requestAnimationFrame(frame);
  }
  requestAnimationFrame(frame);
}

function recenterMap(lat, lon) {
  if (lat && lon) {
    map.setView([lat, lon], Math.max(map.getZoom(), 16));
  }
}

function setGpxRoute(pts, displayName) {
  gpxLine.setLatLngs(pts);
  setGpxData(pts);
  extraLayer.clearLayers();
  
  var badge = document.getElementById('gpx-name-badge');
  if (pts && pts.length > 0) {
    var elevBox = document.getElementById('gpx-elev');
    if (elevBox) elevBox.classList.add('show');
    if (displayName) {
      badge.innerText = displayName;
      badge.title = displayName;
      badge.classList.add('show');
    }
    L.circleMarker(pts[0], {radius:6, color:'#fff', weight:2, fillColor:'#30d158', fillOpacity:1}).addTo(extraLayer);
    L.circleMarker(pts[pts.length-1], {radius:6, color:'#fff', weight:2, fillColor:'#ff453a', fillOpacity:1}).addTo(extraLayer);
    map.fitBounds(gpxLine.getBounds(), {padding:[30, 30]});
  } else {
    badge.classList.remove('show');
    badge.innerText = '';
    var elevBox2 = document.getElementById('gpx-elev');
    if (elevBox2) elevBox2.classList.remove('show');
  }
}

// ---- 지도 중심(십자선)이 GPX선 근처일 때 고도 그래프에 위치 점 표시
var gpxPts = [], gpxCum = [], gpxTotal = 0;
var projZoom = null, projX = [], projY = [];
var elevProf = null, elevMin = 0, elevSpan = 0, elevTotal = 1;
var ELEV_NEAR_PX = 24;   // 화면 픽셀 기준 '인근' 범위

function havJs(la1, lo1, la2, lo2) {
  var R = 6371000, r = Math.PI / 180;
  var dp = (la2 - la1) * r, dl = (lo2 - lo1) * r;
  var h = Math.sin(dp / 2) * Math.sin(dp / 2) +
          Math.cos(la1 * r) * Math.cos(la2 * r) * Math.sin(dl / 2) * Math.sin(dl / 2);
  return 2 * R * Math.asin(Math.min(1, Math.sqrt(h)));
}

function setGpxData(pts) {
  gpxPts = pts || [];
  gpxCum = [0];
  for (var i = 1; i < gpxPts.length; i++) {
    gpxCum.push(gpxCum[i - 1] + havJs(gpxPts[i - 1][0], gpxPts[i - 1][1], gpxPts[i][0], gpxPts[i][1]));
  }
  gpxTotal = gpxPts.length ? gpxCum[gpxCum.length - 1] : 0;
  projZoom = null;
  if (!gpxPts.length) elevProf = null;
  updateElevCursor();
}

function ensureProj() {
  var z = map.getZoom();
  if (projZoom === z && projX.length === gpxPts.length) return z;
  projX = []; projY = [];
  for (var i = 0; i < gpxPts.length; i++) {
    var p = map.project([gpxPts[i][0], gpxPts[i][1]], z);
    projX.push(p.x); projY.push(p.y);
  }
  projZoom = z;
  return z;
}

function elevAt(d) {
  var n = elevProf.length;
  if (d <= elevProf[0][0]) return elevProf[0][1];
  if (d >= elevProf[n - 1][0]) return elevProf[n - 1][1];
  var lo = 0, hi = n - 1;
  while (hi - lo > 1) {
    var mid = (lo + hi) >> 1;
    if (elevProf[mid][0] <= d) lo = mid; else hi = mid;
  }
  var d0 = elevProf[lo][0], d1 = elevProf[hi][0];
  var t = d1 > d0 ? (d - d0) / (d1 - d0) : 0;
  return elevProf[lo][1] + t * (elevProf[hi][1] - elevProf[lo][1]);
}

function updateElevCursor() {
  var cur = document.getElementById('elev-cursor');
  if (!cur) return;
  var box = document.getElementById('gpx-elev');
  if (gpxPts.length < 2 || !elevProf || elevProf.length < 2 || !(gpxTotal > 0) ||
      !box || !box.classList.contains('show')) {
    cur.style.display = 'none';
    return;
  }
  var z = ensureProj();
  var c = map.project(map.getCenter(), z);
  var TH = ELEV_NEAR_PX, best = Infinity, bi = -1, bu = 0;
  for (var i = 0; i < gpxPts.length - 1; i++) {
    var ax = projX[i], ay = projY[i], bx = projX[i + 1], by = projY[i + 1];
    if (Math.max(ax, bx) < c.x - TH || Math.min(ax, bx) > c.x + TH ||
        Math.max(ay, by) < c.y - TH || Math.min(ay, by) > c.y + TH) continue;
    var dx = bx - ax, dy = by - ay, len2 = dx * dx + dy * dy;
    var u = len2 > 0 ? ((c.x - ax) * dx + (c.y - ay) * dy) / len2 : 0;
    u = Math.max(0, Math.min(1, u));
    var qx = ax + u * dx - c.x, qy = ay + u * dy - c.y;
    var d2 = qx * qx + qy * qy;
    if (d2 < best) { best = d2; bi = i; bu = u; }
  }
  if (bi < 0 || best > TH * TH) {   // 완전히 벗어나면 숨김
    cur.style.display = 'none';
    return;
  }
  var dist = gpxCum[bi] + bu * (gpxCum[bi + 1] - gpxCum[bi]);
  var frac = Math.max(0, Math.min(1, dist / gpxTotal));
  var e = elevAt(frac * elevTotal);
  var H = 30, padT = 3, padB = 2;
  var y = elevSpan < 1 ? H / 2 : (H - padB) - (e - elevMin) / elevSpan * (H - padT - padB);
  var dot = document.getElementById('elev-dot');
  dot.style.left = (frac * 100).toFixed(2) + '%';
  dot.style.top = (y / H * 100).toFixed(2) + '%';
  cur.style.display = 'block';
}

var lastElevUpd = 0, elevUpdTimer = null;
function updateElevCursorThrottled() {
  var now = Date.now();
  if (now - lastElevUpd >= 60) {
    lastElevUpd = now;
    updateElevCursor();
  } else if (!elevUpdTimer) {
    elevUpdTimer = setTimeout(function() {
      elevUpdTimer = null;
      lastElevUpd = Date.now();
      updateElevCursor();
    }, 60 - (now - lastElevUpd));
  }
}
map.on('move zoomend moveend', updateElevCursorThrottled);

// GPX 고도 프로파일 (prof: [[누적거리m, 고도m], ...])
function setElevationProfile(prof) {
  var box = document.getElementById('elev-svg');
  if (!box) return;
  if (!prof || prof.length < 2) {
    elevProf = null;
    box.innerHTML = '<span class="elev-none">고도 정보 없음</span>';
    updateElevCursor();
    return;
  }
  var minE = Infinity, maxE = -Infinity;
  var total = prof[prof.length - 1][0] || 1;
  for (var i = 0; i < prof.length; i++) {
    if (prof[i][1] < minE) minE = prof[i][1];
    if (prof[i][1] > maxE) maxE = prof[i][1];
  }
  var span = maxE - minE;
  var W = 100, H = 30, padT = 3, padB = 2;
  var d = '';
  for (var j = 0; j < prof.length; j++) {
    var x = prof[j][0] / total * W;
    var y = span < 1 ? H / 2 : (H - padB) - (prof[j][1] - minE) / span * (H - padT - padB);
    d += (j ? 'L' : 'M') + x.toFixed(2) + ',' + y.toFixed(2);
  }
  var area = d + 'L' + W + ',' + H + 'L0,' + H + 'Z';
  box.innerHTML = '<svg viewBox="0 0 100 30" preserveAspectRatio="none" width="100%" height="100%">'
    + '<defs><linearGradient id="elevg" x1="0" y1="0" x2="0" y2="1">'
    + '<stop offset="0" stop-color="#e8643c" stop-opacity="0.55"/>'
    + '<stop offset="1" stop-color="#e8643c" stop-opacity="0.04"/></linearGradient></defs>'
    + '<path d="' + area + '" fill="url(#elevg)"/>'
    + '<path d="' + d + '" fill="none" stroke="#e8643c" stroke-width="2" stroke-linejoin="round" stroke-linecap="round" vector-effect="non-scaling-stroke"/>'
    + '</svg>';
  elevProf = prof;
  elevMin = minE;
  elevSpan = span;
  elevTotal = total;
  updateElevCursor();
}

var lastBadgeTouch = 0;
function onGpxBadgeClick(e) {
  if (e) { e.preventDefault(); e.stopPropagation(); }
  var now = Date.now();
  if (now - lastBadgeTouch < 300) return;
  lastBadgeTouch = now;
  quietUntil = now + 600;

  var latLngs = gpxLine.getLatLngs();
  if (latLngs.length > 0) {
    if (headingMode) {
      setHeadingMode(false);
      map.setBearing(0);
      updateScreenCompass();
    }
    map.fitBounds(gpxLine.getBounds(), {padding: [30, 30]});
  }
}

var WX_CLOUD = 'M8,16 a4,4 0 0 1 0,-8 a5.5,5.5 0 0 1 10.5,-1.5 a4.5,4.5 0 0 1 1,9.5 Z';
var WX_MOON = 'M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z';

function wxCloud(fill, tf) {
  return '<path transform="' + tf + '" d="' + WX_CLOUD + '" fill="' + fill + '"/>';
}

function wxSun(cx, cy, r) {
  return '<circle cx="' + cx + '" cy="' + cy + '" r="' + (r + 2.8) + '" fill="#fbbc04" fill-opacity="0.22"/>'
       + '<circle cx="' + cx + '" cy="' + cy + '" r="' + r + '" fill="#fbbc04"/>';
}

function wxIconSvg(code, isDay) {
  var cat;
  if (code === 0 || code === 1) cat = 'clear';
  else if (code === 2) cat = 'partly';
  else if (code === 45 || code === 48) cat = 'fog';
  else if ((code >= 51 && code <= 67) || (code >= 80 && code <= 82)) cat = 'rain';
  else if ((code >= 71 && code <= 77) || code === 85 || code === 86) cat = 'snow';
  else if (code >= 95) cat = 'thunder';
  else cat = 'cloud';

  var up = 'translate(2.5,-1) scale(0.95)';
  var s = '';
  if (cat === 'clear') {
    s = isDay ? wxSun(14, 14, 9.5)
              : '<path transform="translate(4,3.5) scale(0.85)" d="' + WX_MOON + '" fill="#f2f2f7"/>';
  } else if (cat === 'partly') {
    s = isDay ? wxSun(10, 10, 5.5)
              : '<path transform="translate(1,1) scale(0.6)" d="' + WX_MOON + '" fill="#f2f2f7"/>';
    s += wxCloud('#d1d1d6', 'translate(5.5,5.5) scale(0.9)');
  } else if (cat === 'cloud') {
    s = wxCloud('#d1d1d6', 'translate(1,3.5) scale(0.95)');
  } else if (cat === 'rain') {
    s = wxCloud('#c7c7cc', up);
    var xs = [10, 14, 18];
    for (var i = 0; i < 3; i++) {
      s += '<line x1="' + xs[i] + '" y1="16.5" x2="' + (xs[i] - 1.5) + '" y2="22" stroke="#5ac8fa" stroke-width="2" stroke-linecap="round"/>';
    }
  } else if (cat === 'snow') {
    s = wxCloud('#c7c7cc', up);
    var sx = [9.5, 14, 18.5];
    for (var j = 0; j < 3; j++) {
      s += '<circle cx="' + sx[j] + '" cy="' + (j === 1 ? 20.5 : 18.5) + '" r="1.6" fill="#ffffff"/>';
    }
  } else if (cat === 'thunder') {
    s = wxCloud('#8e8e93', up);
    s += '<polygon points="15,13.5 11.3,19 14,19 12.4,23 17.5,16.5 14.8,16.5" fill="#ffd60a"/>';
  } else if (cat === 'fog') {
    s = wxCloud('#c7c7cc', up);
    s += '<line x1="6" y1="17.5" x2="22" y2="17.5" stroke="#8e8e93" stroke-width="1.8" stroke-linecap="round"/>';
    s += '<line x1="8" y1="21" x2="20" y2="21" stroke="#8e8e93" stroke-width="1.8" stroke-linecap="round"/>';
  }
  return '<svg width="28" height="28" viewBox="0 0 28 28">' + s + '</svg>';
}

function getDustInfo(pm10) {
  if (pm10 === null || pm10 === undefined || isNaN(pm10)) {
    return { text: '미세', barColor: '#4b89f3', textColor: '#a1a1a6' };
  }
  if (pm10 <= 30) {
    return { text: '좋음', barColor: '#4b89f3', textColor: '#a1a1a6' };
  } else if (pm10 <= 80) {
    return { text: '보통', barColor: '#30d158', textColor: '#a1a1a6' };
  } else if (pm10 <= 150) {
    return { text: '나쁨', barColor: '#ff9f0a', textColor: '#ff9f0a' };
  } else {
    return { text: '매우나쁨', barColor: '#ff453a', textColor: '#ff453a' };
  }
}

function applyWeather(t, code, isDay, pm10) {
  document.getElementById('wx-icon').innerHTML = wxIconSvg(code, isDay);
  document.getElementById('wx-temp').innerText = Math.round(t) + '\u00b0';
  
  var dust = getDustInfo(pm10);
  document.getElementById('wx-bar').style.background = dust.barColor;
  var dustEl = document.getElementById('wx-dust');
  dustEl.innerText = dust.text;
  dustEl.style.color = dust.textColor;
  
  document.getElementById('weather-box').style.display = 'flex';
}

var wxCenterMode = false, lastWxTouch = 0;

function applyGpsWeather(t, code, isDay, pm10) {
  if (wxCenterMode) return;
  applyWeather(t, code, isDay, pm10);
}

function gpsWeatherFail() {
  if (wxCenterMode) return;
  var box = document.getElementById('weather-box');
  if (box.style.display !== 'flex') {
    document.getElementById('wx-icon').innerHTML = '';
    document.getElementById('wx-temp').innerText = '--';
    document.getElementById('wx-dust').innerText = '미세';
    box.style.display = 'flex';
  }
}

function fetchWeatherAt(lat, lon) {
  document.getElementById('wx-temp').innerText = '...';
  var xhr = new XMLHttpRequest();
  xhr.open('GET', 'http://127.0.0.1:' + PORT + '/wx?lat=' + lat.toFixed(4) + '&lon=' + lon.toFixed(4) + '&_=' + Date.now());
  xhr.timeout = 15000;
  xhr.onload = function() {
    try {
      var d = JSON.parse(xhr.responseText);
      if (d.ok) { applyWeather(d.t, d.code, d.is_day === 1, d.pm10); return; }
    } catch (err) {}
    document.getElementById('wx-temp').innerText = '--';
  };
  xhr.onerror = xhr.ontimeout = function() {
    document.getElementById('wx-temp').innerText = '--';
  };
  xhr.send();
}

function onWeatherClick(e) {
  if (e) { e.preventDefault(); e.stopPropagation(); }
  var now = Date.now();
  if (now - lastWxTouch < 300) return;
  lastWxTouch = now;
  var c = map.getCenter();
  wxCenterMode = true;
  document.getElementById('weather-box').classList.add('pinned');
  fetchWeatherAt(c.lat, c.lng);
}

var DIFF_COLORS = ['#30d158', '#b5e853', '#ffd60a', '#ff9f0a', '#ff453a'];
var lastDiffTouch = 0;

function setDifficulty(level, label, distKm, gain, hours, hasEle) {
  var col = DIFF_COLORS[level - 1] || '#8e8e93';
  document.getElementById('diff-btn').style.color = col;
  document.getElementById('diff-lv').innerText = 'Lv' + level;
  var stars = '';
  for (var i = 0; i < 5; i++) { stars += (i < level) ? '★' : '☆'; }
  var html = '<div style="font-weight:800;font-size:14px;color:' + col + ';">' + stars + ' ' + label + '</div>'
           + '<div>거리 ' + distKm.toFixed(1) + ' km</div>'
           + (hasEle ? '<div>상승 +' + gain + ' m</div>' : '<div style="color:#8e8e93;">고도 정보 없음</div>')
           + '<div>예상 ' + hours + '</div>';
  var panel = document.getElementById('diff-panel');
  panel.innerHTML = html;
  panel.classList.remove('show');
  document.getElementById('diff-wrap').classList.add('show');
}

var diffTimer = null;

function toggleDiffPanel(e) {
  if (e) { e.preventDefault(); e.stopPropagation(); }
  var now = Date.now();
  if (now - lastDiffTouch < 300) return;
  lastDiffTouch = now;

  var panel = document.getElementById('diff-panel');
  panel.classList.toggle('show');
  if (diffTimer) clearTimeout(diffTimer);
  if (panel.classList.contains('show')) {
    diffTimer = setTimeout(function() { panel.classList.remove('show'); }, 4000);
  }
}

function hideDifficulty() {
  document.getElementById('diff-panel').classList.remove('show');
  document.getElementById('diff-wrap').classList.remove('show');
}

function clearGpxRoute() {
  gpxLine.setLatLngs([]);
  setGpxData([]);
  extraLayer.clearLayers();
  hideDifficulty();
  var elevBox = document.getElementById('gpx-elev');
  if (elevBox) {
    elevBox.classList.remove('show');
    var sv = document.getElementById('elev-svg');
    if (sv) sv.innerHTML = '';
  }
  var badge = document.getElementById('gpx-name-badge');
  badge.classList.remove('show');
  badge.innerText = '';
}
</script></html>"""

# ---------------------------------------------------------------- 로컬 타일 캐시 프록시 서버
def fetch_weather(lat, lon):
    url = ('https://api.open-meteo.com/v1/forecast?latitude=%.4f&longitude=%.4f'
           '&current=temperature_2m,weather_code,is_day&timezone=auto' % (lat, lon))
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (iPhone)'})
    with urllib.request.urlopen(req, timeout=8) as resp:
        data = json.loads(resp.read().decode('utf-8'))
    cur = data['current']
    
    pm10 = None
    try:
        aq_url = ('https://air-quality-api.open-meteo.com/v1/air-quality?latitude=%.4f&longitude=%.4f'
                  '&current=pm10' % (lat, lon))
        aq_req = urllib.request.Request(aq_url, headers={'User-Agent': 'Mozilla/5.0 (iPhone)'})
        with urllib.request.urlopen(aq_req, timeout=5) as aq_resp:
            aq_data = json.loads(aq_resp.read().decode('utf-8'))
            pm10 = aq_data.get('current', {}).get('pm10')
    except Exception:
        pass
        
    return float(cur['temperature_2m']), int(cur['weather_code']), int(cur.get('is_day', 1)) == 1, pm10

def fetch_elevation(lat, lon):
    try:
        url = 'https://api.open-meteo.com/v1/elevation?latitude=%.4f&longitude=%.4f' % (lat, lon)
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (iPhone)'})
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            eles = data.get('elevation')
            if eles and len(eles) > 0:
                return float(eles[0])
    except Exception:
        pass
    return None

def get_tile_remote_url(layer_id, z, x, y):
    if layer_id == 'opentopo':
        return 'https://tile.opentopomap.org/%s/%s/%s.png' % (z, x, y)
    return None

class MapHandler(http.server.BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def _send(self, body, ctype):
        try:
            data = body.encode('utf-8') if isinstance(body, str) else body
            self.send_response(200)
            self.send_header('Content-Type', ctype)
            self.send_header('Content-Length', str(len(data)))
            self.send_header('Cache-Control', 'max-age=86400')
            self.end_headers()
            self.wfile.write(data)
        except Exception:
            pass

    def do_GET(self):
        try:
            u = urllib.parse.urlparse(self.path)
            if u.path == '/':
                vworld_btns = ''
                if VWORLD_KEY:
                    vworld_btns = (
                        '<button class="layer-btn" id="btn-vworld_base" ontouchend="switchLayer(\'vworld_base\', \'국토부 일반\', this, event)" onclick="switchLayer(\'vworld_base\', \'국토부 일반\', this, event)"><span>국토부 (일반)</span><span class="badge">온라인</span></button>'
                        '<button class="layer-btn" id="btn-vworld_sat" ontouchend="switchLayer(\'vworld_sat\', \'국토부 위성\', this, event)" onclick="switchLayer(\'vworld_sat\', \'국토부 위성\', this, event)"><span>국토부 (위성)</span><span class="badge">온라인</span></button>'
                    )
                html = MAP_HTML.replace('__PORT__', str(SERVER_PORT))
                html = html.replace('__VWORLD_KEY__', VWORLD_KEY)
                html = html.replace('__VWORLD_BUTTONS__', vworld_btns)
                self._send(html, 'text/html; charset=utf-8')
            elif u.path.startswith('/proxy/'):
                parts = u.path.split('/')
                if len(parts) >= 6:
                    layer_id = parts[2]
                    z, x, y_ext = parts[3], parts[4], parts[5]
                    y = y_ext.split('?')[0]
                    
                    cache_dir = os.path.join(SAVE_DIR, 'tile_cache', layer_id, z, x)
                    cache_path = os.path.join(cache_dir, y)
                    
                    if os.path.exists(cache_path):
                        try:
                            with open(cache_path, 'rb') as f:
                                ctype = 'image/jpeg' if ('jpeg' in y or 'jpg' in y) else 'image/png'
                                self._send(f.read(), ctype)
                                return
                        except Exception:
                            pass
                    
                    url = get_tile_remote_url(layer_id, z, x, y)
                    if url:
                        tile_data = None
                        ctype = 'image/png'
                        for attempt in range(2):
                            try:
                                req = urllib.request.Request(
                                    url, 
                                    headers={'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) Trekker/4.20'}
                                )
                                with urllib.request.urlopen(req, timeout=5) as response:
                                    tile_data = response.read()
                                    ctype = response.headers.get('Content-Type', 'image/png')
                                    break
                            except Exception:
                                time.sleep(0.3)
                        
                        if tile_data:
                            try:
                                os.makedirs(cache_dir, exist_ok=True)
                                with open(cache_path, 'wb') as cf:
                                    cf.write(tile_data)
                            except Exception:
                                pass
                            self._send(tile_data, ctype)
                            return
                            
                    self.send_error(404)
            elif u.path == '/wx':
                q = urllib.parse.parse_qs(u.query)
                try:
                    wlat = float(q.get('lat', ['0'])[0])
                    wlon = float(q.get('lon', ['0'])[0])
                    t, code, is_day, pm10 = fetch_weather(wlat, wlon)
                    body = json.dumps({
                        'ok': True, 
                        't': t, 
                        'code': code, 
                        'is_day': 1 if is_day else 0,
                        'pm10': pm10
                    })
                except Exception:
                    body = json.dumps({'ok': False})
                self._send(body, 'application/json')
            elif u.path == '/center_move':
                q = urllib.parse.parse_qs(u.query)
                try:
                    clat = float(q.get('lat', ['0'])[0])
                    clon = float(q.get('lon', ['0'])[0])
                    ele = fetch_elevation(clat, clon)
                    if ele is not None and app_instance:
                        app_instance.center_elevation = ele
                    body = json.dumps({'ok': True})
                except Exception:
                    body = json.dumps({'ok': False})
                self._send(body, 'application/json')
            elif u.path == '/up':
                # 지도 화면 위쪽이 가리키는 방위(진북 기준 0~360) -> 상단 방위 바 갱신
                q = urllib.parse.parse_qs(u.query)
                try:
                    up_d = float(q.get('d', ['0'])[0])
                    if app_instance is not None:
                        run_on_main(lambda: app_instance.compass_bar.set_dir(up_d))
                except Exception:
                    pass
                self._send('ok', 'text/plain')
            elif u.path == '/hmode':
                q = urllib.parse.parse_qs(u.query)
                HEADING_STATE['on'] = (q.get('on', ['0'])[0] == '1')
                self._send('ok', 'text/plain')
            else:
                self.send_error(404)
        except Exception:
            pass

def hav(lat1, lon1, lat2, lon2):
    R = 6371000.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = p2 - p1
    dl = math.radians(lon2 - lon1)
    h = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * R * math.asin(math.sqrt(h))

def bearing_deg(lat1, lon1, lat2, lon2):
    """(lat1,lon1) -> (lat2,lon2) 진북 기준 방위각 (0~360)"""
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dl = math.radians(lon2 - lon1)
    y = math.sin(dl) * math.cos(p2)
    x = math.cos(p1) * math.sin(p2) - math.sin(p1) * math.cos(p2) * math.cos(dl)
    return math.degrees(math.atan2(y, x)) % 360.0

def fmt_time(sec):
    sec = int(sec)
    return '%02d:%02d:%02d' % (sec // 3600, sec % 3600 // 60, sec % 60)

def get_device_heading():
    if motion is None:
        return None
    try:
        g = motion.get_gravity()
        m = motion.get_magnetic_field()
    except Exception:
        return None
    if not g or not m or len(g) < 3 or len(m) < 3:
        return None

    gx, gy, gz = g[0], g[1], g[2]
    mx, my, mz = m[0], m[1], m[2]
    gn = math.sqrt(gx * gx + gy * gy + gz * gz)
    if gn < 1e-6 or (mx * mx + my * my + mz * mz) < 1e-6:
        return None

    dx, dy, dz = gx / gn, gy / gn, gz / gn
    ex = dy * mz - dz * my
    ey = dz * mx - dx * mz
    ez = dx * my - dy * mx
    en = math.sqrt(ex * ex + ey * ey + ez * ez)
    if en < 1e-6:
        return None
    ex, ey, ez = ex / en, ey / en, ez / en
    nx = ey * dz - ez * dy
    ny = ez * dx - ex * dz
    nz = ex * dy - ey * dx

    if abs(dz) > 0.75:
        v_e, v_n = ey, ny
    else:
        v_e, v_n = -ez, -nz
    h = math.degrees(math.atan2(v_e, v_n))
    return (h + MAG_DECLINATION) % 360.0

def write_gpx(points, path, name, distance, gain, elapsed):
    start_dt = datetime.datetime.fromtimestamp(points[0]['t']).strftime('%Y-%m-%dT%H:%M:%SZ')
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<gpx version="1.1" creator="Tracker" xmlns="http://www.topografix.com/GPX/1/1">',
             '  <metadata>',
             '    <name>%s</name>' % name,
             '    <time>%s</time>' % start_dt,
             '    <desc>Distance: %.2f km, Gain: %d m, Duration: %s</desc>' % (distance / 1000, gain, fmt_time(elapsed)),
             '  </metadata>',
             '  <trk>',
             '    <name>%s</name>' % name,
             '    <time>%s</time>' % start_dt,
             '    <trkseg>']
    for p in points:
        t = datetime.datetime.utcfromtimestamp(p['t']).strftime('%Y-%m-%dT%H:%M:%SZ')
        lines.append('      <trkpt lat="%.7f" lon="%.7f"><ele>%.1f</ele><time>%s</time></trkpt>'
                     % (p['lat'], p['lon'], p['alt'], t))
    lines.extend(['    </trkseg>', '  </trk>', '</gpx>'])
    
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    dlog("GPX 파일 저장됨: %s" % path)

def read_gpx_points(path):
    try:
        root = ET.parse(path).getroot()
        pts, eles = [], []
        for e in root.iter():
            tag = e.tag.rsplit('}', 1)[-1]
            if tag in ('trkpt', 'rtept'):
                lat = e.get('lat')
                lon = e.get('lon')
                if lat and lon:
                    ele = None
                    for c in e:
                        if c.tag.rsplit('}', 1)[-1] == 'ele':
                            try:
                                ele = float(c.text)
                            except Exception:
                                ele = None
                            break
                    pts.append([float(lat), float(lon)])
                    eles.append(ele)
        dlog("GPX 파일 로드 성공: %s (%d개 포인트)" % (path, len(pts)))
        return pts, eles
    except Exception as e:
        dlog("GPX 파일 읽기 오류: %s" % e)
        return [], []

def calc_route_stats(pts, eles):
    dist = 0.0
    for i in range(1, len(pts)):
        dist += hav(pts[i - 1][0], pts[i - 1][1], pts[i][0], pts[i][1])

    valid = [z for z in eles if z is not None]
    has_ele = len(valid) >= max(2, len(eles) * 0.5)
    gain = loss = 0.0
    max_alt = min_alt = None
    if has_ele:
        ref = None
        for z in valid:
            if ref is None:
                ref = z
            elif abs(z - ref) >= ALT_THRESHOLD:
                if z > ref:
                    gain += z - ref
                else:
                    loss += ref - z
                ref = z
        max_alt, min_alt = max(valid), min(valid)
    return {'dist': dist, 'gain': gain, 'loss': loss,
            'max_alt': max_alt, 'min_alt': min_alt, 'has_ele': has_ele}

def build_elev_profile(pts, eles, n=120):
    """GPX 거리-고도 프로파일 [[누적거리m, 고도m], ...] (최대 n개). 고도 정보가 부족하면 빈 리스트."""
    N = len(pts)
    valid_idx = [i for i, z in enumerate(eles) if z is not None]
    if N < 2 or len(valid_idx) < max(2, N * 0.5):
        return []

    cum = [0.0]
    for i in range(1, N):
        cum.append(cum[-1] + hav(pts[i - 1][0], pts[i - 1][1], pts[i][0], pts[i][1]))

    ys = list(eles)
    first, last = valid_idx[0], valid_idx[-1]
    for i in range(first):
        ys[i] = ys[first]
    for i in range(last + 1, N):
        ys[i] = ys[last]
    for a, b in zip(valid_idx, valid_idx[1:]):
        for i in range(a + 1, b):
            t = (i - a) / float(b - a)
            ys[i] = ys[a] + (ys[b] - ys[a]) * t

    if N > n:
        idx = [int(round(k * (N - 1) / float(n - 1))) for k in range(n)]
    else:
        idx = list(range(N))
    xs = [cum[i] for i in idx]
    zs = [ys[i] for i in idx]

    sm = []
    for k in range(len(zs)):
        lo, hi = max(0, k - 1), min(len(zs), k + 2)
        sm.append(sum(zs[lo:hi]) / (hi - lo))
    return [[round(x), round(z, 1)] for x, z in zip(xs, sm)]

def rate_difficulty(dist_m, gain_m):
    effort = dist_m / 1000.0 + gain_m / 100.0
    if effort < 6:
        lv, label = 1, '쉬움'
    elif effort < 12:
        lv, label = 2, '보통'
    elif effort < 18:
        lv, label = 3, '약간 어려움'
    elif effort < 26:
        lv, label = 4, '어려움'
    else:
        lv, label = 5, '매우 어려움'
    stars = '★' * lv + '☆' * (5 - lv)
    hours = effort / 4.5
    return stars, label, effort, hours

def fmt_hours(hours):
    total_min = int(round(hours * 60 / 5.0) * 5)
    h, m = total_min // 60, total_min % 60
    if h and m:
        return '%d시간 %d분' % (h, m)
    if h:
        return '%d시간' % h
    return '%d분' % m


class Tracker:
    def __init__(self):
        self.reset_track()
        self.gpx_route = []

    def reset_track(self):
        self.points = []
        self.state = 'idle'
        self.distance = 0.0
        self.gain = 0.0
        self.ref_alt = None
        self.elapsed = 0.0
        self.seg_start = None
        self.speed = 0.0
        self.start_ts = None
        # GPS 노이즈 제거용 상태
        self.kf_lat = None
        self.kf_lon = None
        self.kf_var = 0.0
        self.kf_ts = 0.0
        self.kf_vn = 0.0   # 추정 속도 (북쪽 m/s)
        self.kf_ve = 0.0   # 추정 속도 (동쪽 m/s)
        self.jump_cnt = 0
        self.jump_last = None
        self.last_meas = None

    def start(self):
        self.reset_track()
        self.start_ts = time.time()
        self.seg_start = self.start_ts
        self.state = 'recording'
        dlog("트래킹 시작됨")

    def pause(self):
        if self.seg_start:
            self.elapsed += time.time() - self.seg_start
        self.seg_start = None
        self.state = 'paused'
        dlog("트래킹 일시정지")

    def resume(self):
        self.seg_start = time.time()
        self.state = 'recording'
        dlog("트래킹 재개")

    def stop(self):
        if self.state == 'recording' and self.seg_start:
            self.elapsed += time.time() - self.seg_start
        self.seg_start = None
        self.state = 'idle'
        dlog("트래킹 종료")

    def total_elapsed(self):
        e = self.elapsed
        if self.state == 'recording' and self.seg_start:
            e += time.time() - self.seg_start
        return e

    # ---- GPS 노이즈 제거
    #  1) 정확도 필터  2) 단시간 장거리 이동은 예측 곡선 쪽으로 보정  3) 칼만 필터(속도 예측 포함)
    #  4) 정확도 비례 최소 이동거리  5) 기록된 점 곡선화(앞뒤 점 평균)
    def _kf_reset(self, lat, lon, acc, now):
        self.kf_lat, self.kf_lon = lat, lon
        self.kf_var = acc * acc
        self.kf_ts = now
        self.kf_vn = self.kf_ve = 0.0
        self.jump_cnt = 0
        self.jump_last = None

    def _kf_update(self, lat, lon, acc, now):
        """측정 좌표를 필터에 반영한다. 반영된 (보정) 위치는 kf_lat/kf_lon."""
        if self.kf_lat is None:
            self._kf_reset(lat, lon, acc, now)
            return True

        dt = max(now - self.kf_ts, 0.0)
        old_lat, old_lon = self.kf_lat, self.kf_lon
        m_lat = 111320.0
        m_lon = 111320.0 * math.cos(math.radians(old_lat))

        # 단시간 장거리 이동(예: 1초에 10m 이상) 여부
        d_prev = hav(old_lat, old_lon, lat, lon)
        spike = d_prev > FAST_SPEED_MPS * max(dt, 1.0) + acc * 0.5
        if spike:
            if self.jump_last is not None and hav(self.jump_last[0], self.jump_last[1], lat, lon) <= JUMP_LINK_M:
                self.jump_cnt += 1
            else:
                self.jump_cnt = 1
            self.jump_last = (lat, lon)
            if self.jump_cnt >= JUMP_CONFIRM:
                # 연속해서 같은 곳이면 진짜 이동(터널 통과, 차량 등)으로 보고 필터 재시작
                dlog("GPS 큰 이동 확정 (%.0fm), 필터 재시작" % d_prev)
                self._kf_reset(lat, lon, acc, now)
                return True
        else:
            self.jump_cnt = 0
            self.jump_last = None

        # 예측: 직전 속도로 이동 -> 경로가 휘어도 곡선을 따라감
        pdt = min(dt, 3.0)
        self.kf_lat += self.kf_vn * pdt / m_lat
        self.kf_lon += self.kf_ve * pdt / m_lon
        self.kf_var += dt * KF_PROCESS_NOISE * KF_PROCESS_NOISE

        # 보정: 정확도가 나쁠수록 측정값 반영 비중 감소, 튐이면 예측 곡선 쪽을 거의 그대로 유지
        k = self.kf_var / (self.kf_var + acc * acc)
        if spike:
            k = min(k, SPIKE_GAIN)
        self.kf_lat += k * (lat - self.kf_lat)
        self.kf_lon += k * (lon - self.kf_lon)
        self.kf_var = (1.0 - k) * self.kf_var
        self.kf_ts = now

        # 속도 추정 갱신 (튐 구간은 속도에 반영하지 않음)
        if not spike and dt >= 0.5:
            vn = (self.kf_lat - old_lat) * m_lat / dt
            ve = (self.kf_lon - old_lon) * m_lon / dt
            self.kf_vn = 0.8 * self.kf_vn + 0.2 * vn
            self.kf_ve = 0.8 * self.kf_ve + 0.2 * ve
            sp = math.hypot(self.kf_vn, self.kf_ve)
            if sp > 4.0:
                self.kf_vn *= 4.0 / sp
                self.kf_ve *= 4.0 / sp
        return True

    def filtered_pos(self, lat, lon):
        """기록 중이면 노이즈가 제거된 위치, 아니면 원본 위치."""
        if self.state == 'recording' and self.kf_lat is not None and time.time() - self.kf_ts < 5.0:
            return self.kf_lat, self.kf_lon
        return lat, lon

    def _smooth_prev(self):
        """방금 추가된 점 직전의 점을 앞뒤 점의 중간 쪽으로 당겨 곡선화 (뾰족한 튐 제거)."""
        pts = self.points
        if len(pts) < 3:
            return
        a, m, b = pts[-3], pts[-2], pts[-1]
        seg1 = hav(a['lat'], a['lon'], m['lat'], m['lon'])
        seg2 = hav(m['lat'], m['lon'], b['lat'], b['lon'])
        sp1 = seg1 / max(m['t'] - a['t'], 1.0)
        sp2 = seg2 / max(b['t'] - m['t'], 1.0)
        w = CURVE_SMOOTH_FAST if max(sp1, sp2) > FAST_SPEED_MPS else CURVE_SMOOTH
        tlat = (a['lat'] + b['lat']) / 2.0
        tlon = (a['lon'] + b['lon']) / 2.0
        m['lat'] += w * (tlat - m['lat'])
        m['lon'] += w * (tlon - m['lon'])
        new1 = hav(a['lat'], a['lon'], m['lat'], m['lon'])
        new2 = hav(m['lat'], m['lon'], b['lat'], b['lon'])
        self.distance += (new1 + new2) - (seg1 + seg2)

    def add_point(self, lat, lon, alt, acc=10.0, gps_speed=None):
        now = time.time()
        acc = max(float(acc), 3.0)

        # 새 GPS 갱신이 아닌 같은 값의 반복은 무시 (같은 측정을 여러 번 반영하는 것 방지)
        meas = (lat, lon, acc)
        if meas == self.last_meas:
            return False
        self.last_meas = meas

        # GPS 속도가 거의 0이면 정지 상태: 제자리 흔들림을 기록하지 않음
        if self.points and gps_speed is not None and 0 <= gps_speed < STILL_SPEED_MPS:
            return False

        if not self._kf_update(lat, lon, acc, now):
            return False
        flat, flon = self.kf_lat, self.kf_lon

        if self.points:
            q = self.points[-1]
            d = hav(q['lat'], q['lon'], flat, flon)
            # 정확도가 나쁠수록 더 많이 움직여야 이동으로 인정 (제자리 GPS 흔들림 제거)
            if d < max(MIN_STEP, min(acc * 0.6, 15.0)):
                return False
            self.distance += d
            dt = now - q['t']
            if dt > 0:
                self.speed = d / dt
        if self.ref_alt is None:
            self.ref_alt = alt
        elif abs(alt - self.ref_alt) >= ALT_THRESHOLD:
            if alt > self.ref_alt:
                self.gain += alt - self.ref_alt
            self.ref_alt = alt
        self.points.append({'lat': flat, 'lon': flon, 'alt': alt, 't': now})
        self._smooth_prev()
        return True

    def check_deviation(self, lat, lon, threshold=20.0):
        if not self.gpx_route:
            return False
        min_d = float('inf')
        for g_lat, g_lon in self.gpx_route:
            d = hav(lat, lon, g_lat, g_lon)
            if d < min_d:
                min_d = d
        return min_d > threshold


class CompassBar(ui.View):
    """지도 맨 위에 겹쳐 표시하는 투명 방위 바: 지도 화면 위쪽이 가리키는 방위를 중앙 기준으로 표시."""
    SPAN = 120.0   # 화면에 보이는 각도 범위 (중앙 기준 좌우 60도)
    NAMES = {0: 'N', 45: 'NE', 90: 'E', 135: 'SE', 180: 'S', 225: 'SW', 270: 'W', 315: 'NW'}

    def __init__(self):
        self.background_color = (0, 0, 0, 0)
        self.touch_enabled = False
        self.up_dir = 0.0

    def set_dir(self, d):
        self.up_dir = float(d) % 360.0
        self.set_needs_display()

    def draw(self):
        try:
            w, h = self.width, self.height
            if w <= 0 or h <= 0:
                return
            ppd = w / self.SPAN
            cx = w / 2.0
            half = self.SPAN / 2.0 + 6
            halo = (1, 1, 1, 0.9)

            for a in range(0, 360, 5):
                off = ((a - self.up_dir + 540.0) % 360.0) - 180.0
                if abs(off) > half:
                    continue
                x = cx + off * ppd
                if a % 45 == 0:
                    name = self.NAMES[a]
                    if name == 'N':
                        font, color = ('<System-Bold>', 16), (0.85, 0.1, 0.1, 1.0)
                    else:
                        font, color = ('<System-Bold>', 14), (0, 0, 0, 1.0)
                    tw, th = ui.measure_string(name, font=font)
                    y = (h - th) / 2.0
                    # 투명 배경에서도 잘 보이도록 흰 테두리 후 글자
                    for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1), (-1, 1), (1, -1)):
                        ui.draw_string(name, rect=(x - 20 + dx, y + dy, 40, th), font=font,
                                       color=halo, alignment=ui.ALIGN_CENTER)
                    ui.draw_string(name, rect=(x - 20, y, 40, th), font=font,
                                   color=color, alignment=ui.ALIGN_CENTER)
                else:
                    if abs(((a + 22.5) % 45.0) - 22.5) < 6:
                        continue   # 글자와 겹치는 눈금은 생략
                    major = (a % 15 == 0)
                    th = h * (0.42 if major else 0.28)
                    ty = (h - th) / 2.0
                    ui.set_color(halo)
                    ui.Path.rect(x - 1.5, ty - 1, 3, th + 2).fill()
                    ui.set_color((0, 0, 0, 1.0 if major else 0.8))
                    ui.Path.rect(x - 0.75, ty, 1.5, th).fill()

            # 중앙 표시 삼각형 (현재 위쪽 방향): 흰 테두리 + 검은색
            ui.set_color(halo)
            t1 = ui.Path()
            t1.move_to(cx - 7, 0)
            t1.line_to(cx + 7, 0)
            t1.line_to(cx, 9)
            t1.close()
            t1.fill()
            ui.set_color((0, 0, 0, 1.0))
            t2 = ui.Path()
            t2.move_to(cx - 5, 0)
            t2.line_to(cx + 5, 0)
            t2.line_to(cx, 6.5)
            t2.close()
            t2.fill()
        except Exception as e:
            dlog("방위 바 그리기 오류: %s" % e)


app_instance = None

class TrekApp(ui.View):
    def __init__(self):
        global app_instance
        app_instance = self

        enable_fault()
        self.is_online = True

        self.background_color = '#1c1c1e'
        self.T = Tracker()
        self.closed = False
        self.last_autosave = 0
        self.last_lat = None
        self.last_lon = None
        self.center_elevation = None
        self.last_deviation_alert = 0
        self.server = None

        self.heading_running = False
        self.has_h = False
        self.sm_sin = 0.0
        self.sm_cos = 0.0
        self.last_course = None
        self.last_course_ts = 0.0
        self.no_heading_warned = False
        self.track_heading = None       # 기록 경로 기반 진행 방향
        self.track_heading_ts = 0.0     # 마지막 갱신 시각

        self.wx_ts = 0
        self.wx_lat = None
        self.wx_lon = None
        self.wx_busy = False

        self.is_locked = False
        self.lock_tap_count = 0
        self.lock_tap_time = 0

        self.top_bar = ui.View(background_color='#1c1c1e')
        self.add_subview(self.top_bar)

        self.btn_close = ui.Button(title='✕', font=('<System>', 28), tint_color='#0a84ff')
        self.btn_close.action = lambda s: self.close()
        self.top_bar.add_subview(self.btn_close)

        self.title_label = ui.Label(text='', text_color='white',
                                    font=('<System-Bold>', 23), alignment=ui.ALIGN_LEFT)
        self.title_label.scales_font = True
        self.title_label.min_font_scale = 0.6
        self.top_bar.add_subview(self.title_label)

        self.menu_buttons = []
        self.btn_lock = None
        
        for title, action in (('저장', self.on_save_gpx), ('로드', self.on_gpx),
                              ('초기화', self.on_reset), ('잠금', self.on_toggle_lock)):
            b = ui.Button(title=title, font=('<System>', 19), tint_color='#0a84ff')
            b.action = action
            self.top_bar.add_subview(b)
            self.menu_buttons.append(b)
            if title == '잠금':
                self.btn_lock = b
        self.update_title()

        self.stat_boxes = {}
        for key, title in (('dist', '거리'), ('time', '시간'), ('speed', '속도'), ('gain_ele', '고도')):
            box = ui.View(background_color='#2c2c2e', corner_radius=10)
            t = ui.Label(text=title, text_color='#8e8e93', font=('<System>', 14), alignment=ui.ALIGN_CENTER)
            v = ui.Label(text='-', text_color='white', font=('<System-Bold>', 22), alignment=ui.ALIGN_CENTER)
            v.scales_font = True
            v.min_font_scale = 0.7
            box.add_subview(t)
            box.add_subview(v)
            self.stat_boxes[key] = (box, t, v)
            self.add_subview(box)

        self.web = ui.WebView()
        self.web.corner_radius = 10
        self.add_subview(self.web)

        # 지도 영역 맨 위에 겹쳐 표시하는 방위 바 (웹뷰보다 위에 와야 하므로 웹뷰 다음에 추가)
        self.compass_bar = CompassBar()
        self.add_subview(self.compass_bar)

        self.start_server()

        self.status = ui.Label(text='GPS 대기 중...', text_color='#8e8e93',
                               font=('<System>', 16), alignment=ui.ALIGN_CENTER)
        self.add_subview(self.status)

        self.btn_main = self._button('● 시작', '#30d158', self.on_main)
        self.btn_stop = self._button('■ 종료·저장', '#ff453a', self.on_stop)
        self.refresh_buttons()

        self.lock_view = ui.View(background_color=(0, 0, 0, 0.50))
        self.lock_box = ui.View(background_color=(0, 0, 0, 0.60), corner_radius=12)
        self.lock_label = ui.Label(text='🔒 화면이 잠겼습니다\n3번 빠르게 터치시 해제',
                                   text_color='white', font=('<System-Bold>', 16),
                                   alignment=ui.ALIGN_LEFT, number_of_lines=2)
        self.lock_box.add_subview(self.lock_label)
        self.lock_view.add_subview(self.lock_box)
        self.lock_view.hidden = True
        self.add_subview(self.lock_view)

        self.toast_token = 0
        self.toast = ui.View(background_color=(0, 0, 0, 0.82), corner_radius=14)
        self.toast_label = ui.Label(text='', text_color='white', font=('<System-Bold>', 20),
                                    alignment=ui.ALIGN_CENTER)
        self.toast.add_subview(self.toast_label)
        self.toast.hidden = True
        self.add_subview(self.toast)

        self.update_stats()
        location.start_updates()
        
        threading.Thread(target=self.check_network_loop, daemon=True).start()

    def update_title(self):
        net_str = '온라인' if self.is_online else '오프라인'
        self.title_label.text = '트레커[%s]' % net_str

    def on_toggle_lock(self, sender):
        self.is_locked = not self.is_locked
        self.lock_view.hidden = not self.is_locked

        if self.is_locked:
            for b in self.menu_buttons + [self.btn_close]:
                b.enabled = False
            self.remove_subview(self.lock_view)
            self.add_subview(self.lock_view)
            self.btn_lock.title = '해제'
            self.status.text = '화면이 잠겼습니다 (3번 빠르게 터치시 해제)'
        else:
            self.unlock_ui()
            self.status.text = '잠금이 해제되었습니다'

    def unlock_ui(self):
        for b in self.menu_buttons + [self.btn_close]:
            b.enabled = True
        self.btn_lock.title = '잠금'
        self.is_locked = False
        self.lock_view.hidden = True

    def touch_ended(self, touch):
        if not self.is_locked:
            return
        now = time.time()
        if now - self.lock_tap_time > 0.4:
            self.lock_tap_count = 1
        else:
            self.lock_tap_count += 1
            
        self.lock_tap_time = now
        if self.lock_tap_count >= 3:
            self.lock_tap_count = 0
            self.unlock_ui()
            self.status.text = '터치 잠금이 해제되었습니다'

    def check_network_loop(self):
        while not self.closed:
            status = True
            try:
                urllib.request.urlopen('https://clients3.google.com/generate_204', timeout=2)
            except Exception:
                status = False
            
            if self.is_online != status:
                self.is_online = status
                run_on_main(self.update_title)
            
            for _ in range(50):
                if self.closed:
                    break
                time.sleep(0.1)

    def start_server(self):
        global SERVER_PORT
        try:
            class ReusableHTTPServer(http.server.ThreadingHTTPServer):
                allow_reuse_address = True
                def server_bind(self):
                    self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                    http.server.ThreadingHTTPServer.server_bind(self)

            self.server = ReusableHTTPServer(('127.0.0.1', 0), MapHandler)
            SERVER_PORT = self.server.server_address[1]
            th = threading.Thread(target=self.server.serve_forever, daemon=True)
            th.start()
            self.web.load_url('http://127.0.0.1:%d/' % SERVER_PORT)
            dlog("HTTP 서버 안전 시작 포트: %d" % SERVER_PORT)
        except Exception as e:
            dlog("HTTP 서버 시작 실패: %s" % e)
            print("HTTP Server Error:", e)

    def stop_server(self):
        srv, self.server = self.server, None
        if srv:
            try:
                srv.shutdown()
                srv.server_close()
            except Exception:
                pass

    def _button(self, title, color, action):
        b = ui.Button(title=title, tint_color='white', background_color=color,
                      corner_radius=14, font=('<System-Bold>', 22))
        b.action = action
        self.add_subview(b)
        return b

    def layout(self):
        w, h = self.width, self.height
        if w == 0 or h == 0:
            return

        top = TOP_INSET
        bar_h = 40          # 제목줄 높이 (48 -> 40)
        self.top_bar.frame = (0, top, w, bar_h)
        self.btn_close.frame = (2, 0, 44, bar_h)

        def _mw(text, font):
            try:
                return float(ui.measure_string(text, font=font)[0])
            except Exception:
                return font[1] * len(text) * 0.95

        def _menu_widths(sz):
            f = ('<System>', sz)
            out = []
            for b in self.menu_buttons:
                if b is self.btn_lock:
                    out.append(max(_mw('잠금', f), _mw('해제', f)))
                else:
                    out.append(_mw(b.title, f))
            return out

        avail_total = (w - 6) - 48
        min_pad = 4.0
        size = 16
        for sz in (23, 22, 21, 20, 19, 18, 17, 16):
            t_need = _mw('트레커[오프라인]', ('<System-Bold>', sz)) + 10
            tws = _menu_widths(sz)
            if t_need + sum(tws) + 2 * min_pad * len(tws) <= avail_total:
                size = sz
                break

        t_need = _mw('트레커[오프라인]', ('<System-Bold>', size)) + 10
        tws = _menu_widths(size)
        self.title_label.font = ('<System-Bold>', size)
        for b in self.menu_buttons:
            b.font = ('<System>', size)

        pad = (avail_total - t_need - sum(tws)) / (2.0 * len(tws))
        pad = max(min_pad, min(10.0, pad))

        x = w - 6
        for b, tw in reversed(list(zip(self.menu_buttons, tws))):
            bw_menu = tw + 2 * pad
            x -= bw_menu
            b.frame = (x, 0, bw_menu, bar_h)
        self.title_label.frame = (48, 0, max(60, x - 48), bar_h)

        m, gap = 8, 6
        sw = (w - 2 * m - 3 * gap) / 4
        sh = 56             # 통계 박스 높이 (66 -> 56)
        vgap = 4            # 위아래 요소 사이 세로 간격 (8/6 -> 4)
        
        for i, key in enumerate(('dist', 'time', 'speed', 'gain_ele')):
            box, t, v = self.stat_boxes[key]
            box.frame = (m + i * (sw + gap), top + bar_h + vgap, sw, sh)
            t.frame = (0, 3, sw, 18)
            v.frame = (0, 21, sw, 30)

        y = top + bar_h + vgap + sh + vgap
        cb_h = 26
        btn_h = 52
        by = h - btn_h - m
        
        self.status.frame = (m, by - 28, w - 2 * m, 24)
        self.web.frame = (m, y, w - 2 * m, by - 32 - gap - y)
        self.compass_bar.frame = (m, y, w - 2 * m, cb_h)   # 지도 맨 위에 겹침
        
        bw = (w - 2 * m - gap) / 2
        self.btn_main.frame = (m, by, bw, btn_h)
        self.btn_stop.frame = (m + bw + gap, by, bw, btn_h)
        
        lock_w = 230
        web_bottom = by - 32 - gap
        self.lock_view.frame = (0, 0, w, h)
        self.lock_box.frame = (m + 8, web_bottom - btn_h - 8, lock_w, btn_h)
        self.lock_label.frame = (10, 4, lock_w - 20, btn_h - 8)

        tw, th = 220, 56
        self.toast.frame = (w / 2 - tw / 2, h / 2 - th / 2, tw, th)
        self.toast_label.frame = (0, 0, tw, th)

        try:
            self.web.evaluate_javascript('if(typeof map !== "undefined") { map.invalidateSize(); }')
        except Exception:
            pass

    def on_save_gpx(self, sender):
        if not self.T.points:
            self.status.text = '저장할 트래킹 기록이 없어요'
            return
        try:
            os.makedirs(SAVE_DIR, exist_ok=True)
            stamp = datetime.datetime.fromtimestamp(self.T.start_ts or time.time()).strftime('%Y%m%d_%H%M%S')
            path = os.path.join(SAVE_DIR, 'trek_%s.gpx' % stamp)
            write_gpx(self.T.points, path, 'Trek ' + stamp, self.T.distance, int(self.T.gain), self.T.total_elapsed())
            self.show_toast('✅ 저장되었습니다')
        except Exception as e:
            self.status.text = 'GPX 저장 실패'

    def on_gpx(self, sender):
        try:
            os.makedirs(SAVE_DIR, exist_ok=True)
            files = sorted([f for f in os.listdir(SAVE_DIR) if f.lower().endswith('.gpx') and not f.startswith('map_')], reverse=True)
            items = ['📂 외부 파일 선택...', '❌ 표시된 경로 해제'] + files
            
            sel = dialogs.list_dialog('GPX 경로 불러오기', items)
            if not sel:
                return
                
            path = None
            display_name = ''
            if sel == '📂 외부 파일 선택...':
                try:
                    path = dialogs.pick_document(types=['public.data'])
                    if path:
                        base_name = os.path.basename(path)
                        display_name = os.path.splitext(base_name)[0]
                except Exception:
                    self.status.text = '파일 선택 취소됨'
                    return
            elif sel == '❌ 표시된 경로 해제':
                self.T.gpx_route = []
                self.web.evaluate_javascript('clearGpxRoute();')
                self.status.text = 'GPX 경로 해제됨'
                return
            else:
                path = os.path.join(SAVE_DIR, sel)
                display_name = os.path.splitext(sel)[0]
                
            if path:
                pts, eles = read_gpx_points(path)
                if pts:
                    self.T.gpx_route = pts
                    prof = build_elev_profile(pts, eles)
                    js = 'setGpxRoute(%s, %s); setElevationProfile(%s);' % (
                        json.dumps(pts), json.dumps(display_name, ensure_ascii=False), json.dumps(prof))
                    self.web.evaluate_javascript(js)

                    st = calc_route_stats(pts, eles)
                    stars, label, effort, hours = rate_difficulty(st['dist'], st['gain'])
                    self.status.text = '경로 로드 · %.1fkm · 상승 %dm · %s %s' % (
                        st['dist'] / 1000, st['gain'], stars, label)

                    try:
                        js = 'setDifficulty(%d, %s, %.2f, %d, %s, %s);' % (
                            stars.count('★'),
                            json.dumps(label, ensure_ascii=False),
                            st['dist'] / 1000.0,
                            int(st['gain']),
                            json.dumps('약 ' + fmt_hours(hours), ensure_ascii=False),
                            'true' if st['has_ele'] else 'false')
                        self.web.evaluate_javascript(js)
                    except Exception as e:
                        dlog("난이도 표시 오류: %s" % e)
                else:
                    self.status.text = 'GPX 파일에서 좌표를 읽지 못했어요'
        except Exception as e:
            dlog("GPX 로드 메뉴 예외: %s" % e)

    def show_toast(self, text, sec=2.0):
        self.toast_token += 1
        token = self.toast_token
        self.toast_label.text = text
        try:
            self.remove_subview(self.toast)
            self.add_subview(self.toast)
        except Exception:
            pass
        self.toast.hidden = False
        ui.delay(lambda: self.hide_toast(token), sec)

    def hide_toast(self, token):
        if token == self.toast_token:
            self.toast.hidden = True

    def on_reset(self, sender):
        self.T.gpx_route = []
        try:
            self.web.evaluate_javascript('clearGpxRoute();')
        except Exception:
            pass
        self.status.text = 'GPX 경로가 초기화되었습니다'

    def on_main(self, sender):
        T = self.T
        if T.state == 'idle':
            T.start()
            self.track_heading = None
            self.last_autosave = time.time()
        elif T.state == 'recording':
            T.pause()
        else:
            T.resume()

        # 기록 시작/재개 시 진행 방향 up 자동 회전 켜기
        if T.state == 'recording':
            self.track_heading_ts = 0.0   # 즉시 다시 계산
            try:
                self.web.evaluate_javascript('autoHeading(true);')
            except Exception:
                pass

        try:
            console.set_idle_timer_disabled(T.state != 'idle')
        except Exception:
            pass
        self.refresh_buttons()

    def on_stop(self, sender):
        T = self.T
        T.stop()
        try:
            self.web.evaluate_javascript('autoHeading(false);')  # 정북 복귀
        except Exception:
            pass
        try:
            console.set_idle_timer_disabled(False)
        except Exception:
            pass
        self.refresh_buttons()
        
        if len(T.points) < 2:
            self.status.text = '기록된 좌표가 부족해 저장하지 않았어요'
            return
            
        stamp = datetime.datetime.fromtimestamp(T.start_ts).strftime('%Y%m%d_%H%M%S')
        path = os.path.join(SAVE_DIR, 'trek_%s.gpx' % stamp)
        try:
            write_gpx(T.points, path, 'Trek ' + stamp, T.distance, int(T.gain), T.total_elapsed())
            self.show_toast('✅ 저장되었습니다')
        except Exception as e:
            dlog("종료 저장 실패: %s" % e)
            self.status.text = '저장 실패'

    def refresh_buttons(self):
        st = self.T.state
        if st == 'recording':
            self.btn_main.title = '❚❚ 일시정지'
            self.btn_main.background_color = '#ff9f0a'
        elif st == 'paused':
            self.btn_main.title = '▶ 계속'
            self.btn_main.background_color = '#30d158'
        else:
            self.btn_main.title = '● 시작'
            self.btn_main.background_color = '#30d158'
        can_stop = st != 'idle'
        self.btn_stop.enabled = can_stop
        self.btn_stop.alpha = 1.0 if can_stop else 0.4

    def update_stats(self):
        T = self.T
        self.stat_boxes['dist'][2].text = '%.2fkm' % (T.distance / 1000)
        self.stat_boxes['time'][2].text = fmt_time(T.total_elapsed())
        self.stat_boxes['speed'][2].text = '%.1fkm/h' % (T.speed * 3.6) if T.state == 'recording' else '-'
        
        label_view, title_lbl, val_lbl = self.stat_boxes['gain_ele']
        if T.state == 'recording':
            title_lbl.text = '상승'
            val_lbl.text = '%dm' % int(T.gain)
        else:
            title_lbl.text = '고도'
            if self.center_elevation is not None:
                val_lbl.text = '%dm' % int(self.center_elevation)
            else:
                val_lbl.text = '-'

    def tick(self):
        if self.closed:
            return
        try:
            loc = location.get_location()
            if loc:
                lat = float(loc['latitude'])
                lon = float(loc['longitude'])
                self.on_location(loc)
                plat, plon = self.T.filtered_pos(lat, lon)

                if self.T.state == 'recording' and self.T.check_deviation(plat, plon, threshold=20.0):
                    self.status.text = '⚠️ 경고: 경로를 이탈했습니다!'
                    self.status.text_color = '#ff453a'
                    
                    now = time.time()
                    if now - self.last_deviation_alert > 5:
                        self.last_deviation_alert = now
                        try:
                            console.vibrate()
                        except Exception:
                            pass
                        try:
                            sound.play_effect('Coin_2', 1.0)
                        except Exception:
                            pass
                else:
                    self.status.text_color = '#8e8e93'

            self.update_stats()
            
            if self.T.state == 'recording' and time.time() - self.last_autosave > AUTOSAVE_SEC:
                if len(self.T.points) > 1:
                    stamp = datetime.datetime.fromtimestamp(self.T.start_ts).strftime('%Y%m%d_%H%M%S')
                    path = os.path.join(SAVE_DIR, 'trek_%s_autosave.gpx' % stamp)
                    write_gpx(self.T.points, path, 'Trek ' + stamp, self.T.distance, int(self.T.gain), self.T.total_elapsed())
                self.last_autosave = time.time()
        except Exception as e:
            dlog("tick 루프 오류: %s" % e)
        finally:
            if not self.closed:
                ui.delay(self.tick, 1)

    def maybe_fetch_weather(self, lat, lon):
        if self.wx_busy:
            return
        now = time.time()
        moved = 0.0
        if self.wx_lat is not None:
            moved = abs(lat - self.wx_lat) * 111.0 + abs(lon - self.wx_lon) * 88.0
        if self.wx_ts and now - self.wx_ts < 600 and moved < 5:
            return
        self.wx_busy = True
        self.wx_ts = now
        threading.Thread(target=self._weather_worker, args=(lat, lon), daemon=True).start()

    def _weather_worker(self, lat, lon):
        try:
            t, code, is_day, pm10 = fetch_weather(lat, lon)
            self.wx_lat, self.wx_lon = lat, lon
            dlog("날씨 수신: %.1f도, 코드 %d, 미세먼지 %s" % (t, code, str(pm10)))
            pm_js = 'null' if pm10 is None else ('%.1f' % pm10)
            js = 'applyGpsWeather(%.1f, %d, %s, %s);' % (t, code, 'true' if is_day else 'false', pm_js)
            run_on_main(lambda: self.web.evaluate_javascript(js))
        except Exception as e:
            dlog("날씨 조회 실패: %s" % e)
            self.wx_ts = time.time() - 540
            run_on_main(lambda: self.web.evaluate_javascript('gpsWeatherFail();'))
        finally:
            self.wx_busy = False

    def compute_track_heading(self):
        """현재(마지막 기록) 위치와 직선거리 10m 이상 떨어진 이전 기록 위치를 잇는 선의 방위각."""
        pts = self.T.points
        if len(pts) < 2:
            return None
        end = pts[-1]
        start = None
        for i in range(len(pts) - 2, -1, -1):
            if hav(pts[i]['lat'], pts[i]['lon'], end['lat'], end['lon']) >= TRACK_HEADING_DIST:
                start = pts[i]
                break
        if start is None:
            # 아직 10m를 못 갔으면 가장 처음 기록 위치 사용 (너무 가까우면 보류)
            start = pts[0]
            if hav(start['lat'], start['lon'], end['lat'], end['lon']) < 3.0:
                return None
        return bearing_deg(start['lat'], start['lon'], end['lat'], end['lon'])

    def heading_tick(self):
        if self.closed:
            return
        interval = 1.0
        try:
            on = HEADING_STATE['on']
            if on and not self.heading_running:
                if motion is not None:
                    try:
                        motion.start_updates()
                    except Exception as e:
                        dlog("motion 시작 오류: %s" % e)
                self.heading_running = True
                self.has_h = False
                self.no_heading_warned = False
            elif not on and self.heading_running:
                if motion is not None:
                    try:
                        motion.stop_updates()
                    except Exception:
                        pass
                self.heading_running = False

            if on:
                interval = 0.12
                h = None
                alpha = 0.3
                if self.T.state == 'recording':
                    now = time.time()
                    if now - self.track_heading_ts >= TRACK_HEADING_SEC:
                        th = self.compute_track_heading()
                        if th is not None:
                            self.track_heading = th
                            self.track_heading_ts = now
                    h = self.track_heading
                    if h is None:
                        h = self.last_course       # 경로가 쌓이기 전에는 GPS 진행 방향
                    alpha = 0.12
                    if h is None:
                        h = get_device_heading()   # 그것도 없으면 센서 방향
                        alpha = 0.3
                else:
                    h = get_device_heading()
                    if h is None and self.last_course is not None:
                        h = self.last_course
                if h is not None:
                    r = math.radians(h)
                    if not self.has_h:
                        self.sm_sin, self.sm_cos = math.sin(r), math.cos(r)
                        self.has_h = True
                    else:
                        self.sm_sin += alpha * (math.sin(r) - self.sm_sin)
                        self.sm_cos += alpha * (math.cos(r) - self.sm_cos)
                    sh = math.degrees(math.atan2(self.sm_sin, self.sm_cos)) % 360.0
                    self.web.evaluate_javascript('setHeading(%.1f);' % sh)
                elif not self.no_heading_warned:
                    self.no_heading_warned = True
                    self.status.text = '방향 센서를 읽을 수 없어요'
        except Exception as e:
            dlog("heading_tick 오류: %s" % e)
        finally:
            if not self.closed:
                ui.delay(self.heading_tick, interval)

    def on_location(self, loc):
        T = self.T
        acc = loc.get('horizontal_accuracy', -1)
        if acc < 0:
            self.status.text = 'GPS 대기 중...'
            return
            
        lat, lon = float(loc['latitude']), float(loc['longitude'])
        alt = float(loc.get('altitude', 0.0))
        self.last_lat, self.last_lon = lat, lon

        if T.state != 'recording' and self.center_elevation is None:
            self.center_elevation = alt

        course = loc.get('course', -1)
        speed = loc.get('speed', -1)
        if course is not None and course >= 0 and speed is not None and speed > 0.5:
            self.last_course = float(course)
            self.last_course_ts = time.time()

        if T.state == 'recording':
            max_acc = MAX_ACCURACY if T.points else START_MAX_ACCURACY
            if acc > max_acc:
                self.status.text = 'GPS 신호 향상 대기중 (±%dm)' % acc
            else:
                T.add_point(lat, lon, alt, acc, speed if (speed is not None and speed >= 0) else None)
                plat, plon = T.filtered_pos(lat, lon)
                if not T.check_deviation(plat, plon, threshold=20.0):
                    self.status.text = '기록 중 (±%dm)' % acc
        elif T.state == 'paused':
            self.status.text = '일시정지 상태 (±%dm)' % acc
        else:
            self.status.text = 'GPS 수신 양호 (±%dm)' % acc

        try:
            pts_js = json.dumps([[p['lat'], p['lon']] for p in T.points])
            mlat, mlon = T.filtered_pos(lat, lon)
            js = 'updateMap(%f, %f, %s, %s);' % (mlat, mlon, pts_js, 'true' if T.state == 'recording' else 'false')
            self.web.evaluate_javascript(js)
        except Exception:
            pass

        self.maybe_fetch_weather(lat, lon)

    def will_close(self):
        self.closed = True
        try:
            if self.T.state != 'idle' and len(self.T.points) > 1:
                stamp = datetime.datetime.fromtimestamp(self.T.start_ts).strftime('%Y%m%d_%H%M%S')
                path = os.path.join(SAVE_DIR, 'trek_%s_autosave.gpx' % stamp)
                write_gpx(self.T.points, path, 'Trek ' + stamp, self.T.distance, int(self.T.gain), self.T.total_elapsed())
        except Exception:
            pass
        try:
            console.set_idle_timer_disabled(False)
            location.stop_updates()
            if motion is not None:
                motion.stop_updates()
            self.stop_server()
        except Exception:
            pass


if __name__ == '__main__':
    app = TrekApp()
    ui.delay(app.tick, 0.5)
    ui.delay(app.heading_tick, 0.6)
    app.present('fullscreen', hide_title_bar=True)
