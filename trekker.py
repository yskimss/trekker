# trekker.py - Pythonista 3용 트래킹 + 고도/상승 동적 전환 + GPX 배지 클릭 이동 + 기록 시 진행방향 자동회전 + 나침반/십자선 2초 표시 + 거리 척도 + GPX 고도 프로파일 + 기록 중 5초 간격 진행방향 회전 + 회전 방향 보정 + GPS 노이즈 제거/곡선 보정 + 상단 방위 바 + 상단 UI 높이 축소 + 고도 그래프 위치 점 + 방위 바 갱신 안정화 + 십자선 이동 시 표시/굵게 + 기본 지도 Topo(온라인) + 고도 상세 패널 + 기록 중 30초 생존 신호음 + HTTP 서버 오류 방어 + 지도 캐시 개선/오프라인 미리받기 + 클립보드 삭제 & 2초 숨김 & 툴팁 1.5배 띄우기 + 날씨 조회 안정화/날씨 로그 + 방위 바 양끝 흐림 + 풍향/풍속 표시 및 상세 정보창 + 날씨 1분 갱신 + 잠금 중 기록/진행방향만 수행 + 지도 터치 십자선/잠금 중 절전 + 종료 시 지도 회전/원형 나침반 없음 + 기록 중 경량 모드(진행 방향 외 갱신 지연) + 빠른 회전 시 다운 방지 + 잠금 중 부채꼴 방향 UI 숨김 + GPX 따라가기 시뮬레이션(배속) + 상단 메뉴 '저장' 제거 + 시뮬레이션 중 거리·시간 표시 + 초기화 시 시뮬레이션 거리·시간 초기화 + 시뮬/기록 동시 실행 방지 + 토스트 잘림 수정, 시뮬 나침반=진행방향 위로 + 시뮬 나침반 해제 시 지도 방향 유지 + 시뮬 중 나침반 배율 유지 + 시뮬 중 상단 고도70:GPX명30 비율 + 풍향 화살표 풍속별 색상 + 좌표 아래 주소 표시 + 시뮬/나침반 회전 다운 방지 + 시뮬 속도 표시, 초기화 시 기록 경로 삭제 + 시뮬 종료 시 종료 위치 유지 + Esri 위성 지도에서 원형 나침반 흰색 + 터치 시에만 주소 5초 표시 + 시뮬 중 로드/초기화 비활성화 + 시뮬 속도 '-' 표시 + 시뮬 시작/종료 메세지 삭제 + 시뮬 중 고도 상세창 그래프에 시뮬 위치 점 표시 + 고도/날씨 상세창 반투명 + 상세창 농도 상향 + 시뮬 시작/종료 알림음 + 기록 경로 선 자홍색+흰 테두리 + 고도 상세창에 작은 고도 위치 점 표시 + 시뮬 역방향/위치 점프 + 십자선 위치부터 시뮬 시작 메뉴 + 시뮬 메뉴 구분선 + 잠금 중 위치 반영 5초 간격 + 종료·저장 결과를 상태 줄에 3초 표시 + 알림(토스트) 제거, 모든 메시지를 상태 줄에 3초 표시 + 시뮬 중 고도 상세창은 시뮬 위치만 표시 + 지도 서버 재접속·타일 자동 재요청 + 시뮬 중 화면 슬립 방지 + 지도 서버 재시작 안정화(NameError 수정) + 설정 파일(trek_config.json)을 trekker.py와 같은 폴더에서 읽음 + VWorld 키 읽기 보강·오류 표시 + 지도 선택 메뉴를 오른쪽 아이콘과 겹치지 않게 이동, 설정 파일 없음 안내 삭제 + 국토부 위성 원형 나침반 흰색, 지도 선택 목록 잘림 수정 + VWorld 없을 때 지도 선택 목록 정렬 원복 + 지도 이동·회전 시 지도 선택 창 닫기 + 에러 외 로그 기록 안 함 + 시뮬·기록 중 고도 상세 간략 보기(이름 자리에 현재 고도·남은 거리, 경사·다음 정상 강조, 높이 2/3, 지도 선택 앞으로) + Apache 2.0 라이선스·법적 제한 안내 추가 + 파일 상단에 VWorld 키 설정 방법 안내 + 종료·저장 시 다운 대응 + 비정상 종료(ui.delay 람다) 수정 + 날씨 상세창을 항상 최상위로 (v4.87)
# SPDX-License-Identifier: Apache-2.0
#
# Copyright 2026 Yoseopkim
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# [법적 제한 안내 / Legal notice]
# 1. 보증 없음: 이 소프트웨어는 "있는 그대로(AS IS)" 제공되며, 정확성·안정성·특정 목적 적합성을 보증하지 않습니다.
#    저작권자는 사용으로 인한 사고·부상·데이터 손실·기타 손해에 대해 책임지지 않습니다.
# 2. 안전: GPS 위치·고도·지도·날씨 정보에는 오차가 있을 수 있습니다. 등산·길찾기·안전 판단의 유일한 근거로
#    사용하지 말고, 지도·나침반·현지 안내 등 다른 수단을 함께 사용하세요.
# 3. 외부 서비스: 지도 타일·주소·날씨 데이터(OpenStreetMap, OpenTopoMap, Esri, CyclOSM, VWorld(국토교통부),
#    Open-Meteo 등)는 각 제공처의 이용약관·저작권·출처 표시 의무를 따르며 이 라이선스에 포함되지 않습니다.
#    API 키(예: VWorld)는 사용자가 직접 발급·관리하며 타인에게 공개하지 마세요.
# 4. 개인정보: 날씨·주소 조회 시 현재 위치 좌표가 외부 서비스로 전송될 수 있습니다.
#    기록한 경로(GPX)는 기기에 저장되며, 공유·공개 여부와 그 책임은 사용자에게 있습니다.
#
# [VWorld(국토부) 지도 키 설정 방법]
# 1. vworld.kr 에서 오픈API 인증키를 발급받습니다.
# 2. 이 파일(trekker.py)과 같은 폴더에 trek_config.json 파일을 만들고 아래처럼 키를 넣습니다.
#        {"vworld_key": "발급받은-인증키"}
# 3. 앱을 다시 실행하면 지도 선택에 "국토부 (일반)", "국토부 (위성)"이 나타납니다. (키는 시작할 때만 읽습니다)
import ui, location, math, os, time, datetime, json, urllib.request, threading, sys, socket
import io, zlib, struct, shutil
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
try:
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
except Exception:
    SCRIPT_DIR = os.path.expanduser('~/Documents')
CONFIG_PATH = os.path.join(SCRIPT_DIR, 'trek_config.json')          # trekker.py와 같은 폴더의 설정 파일
OLD_CONFIG_PATH = os.path.join(SAVE_DIR, 'trek_config.json')        # 이전 위치(Documents/treks) - 새 위치에 없을 때만 읽음
LOG_PATH = os.path.join(SAVE_DIR, 'trek_debug.txt')

try:
    os.makedirs(SAVE_DIR, exist_ok=True)
except Exception:
    pass

MAX_ACCURACY = 30       # m, 이보다 부정확한 좌표는 기록 안 함
MIN_STEP = 5            # m, 이보다 적게 움직이면 기록 안 함
ALT_THRESHOLD = 3       # m, 고도 노이즈 필터
AUTOSAVE_SEC = 60
# ---- 기록 중 생존 신호 / 진단 설정
LIVE_BEEP_SEC = 30      # s, 기록 중 '앱이 살아있음' 신호음 간격
LIVE_SOUND = 'Ding_3'   # 부드러운 종소리 (기본 음 + 완전5도 위 음, 두 번 울림)
LIVE_VOLUME = 0.4       # 0~1
HEARTBEAT_SEC = 30      # s, 진단용 생존 기록(로그) 간격
KEEP_RUNNING_BG = True  # 기록 중 백그라운드에서 앱이 멈추지 않도록 유지 시도
RUN_MARK = os.path.join(SAVE_DIR, 'trek_running.txt')   # 정상 종료되지 않았는지 확인하는 표식 파일
# ---- 날씨 조회 / 날씨 로그 설정
WX_LOG_PATH = os.path.join(SAVE_DIR, 'trek_weather_log.txt')     # 날씨 전용 로그 (조회 시도·실패 원인·화면 적용 결과)
WX_LOG_MAX_KB = 1000       # KB, 넘으면 .1 파일로 넘기고 새로 기록 (1분 갱신이라 기록이 많아 늘림)
WX_CACHE_PATH = os.path.join(SAVE_DIR, 'trek_weather_cache.json')  # 마지막으로 받은 날씨 (오프라인/실패 시 표시용)
WX_REFRESH_SEC = 60        # s, 날씨 자동 갱신 간격 (1분). 아이콘을 누르면 즉시 갱신
WX_REFRESH_MOVE_KM = 5     # km, 이 거리 이상 이동해도 갱신
WX_TRIES = 3               # 한 번 조회할 때 재시도 횟수
WX_TIMEOUT = 10            # s, 1회 요청 제한 시간
WX_BUDGET = 40             # s, 한 번의 조회에 쓰는 총 시간 한도
WX_RETRY_BACKOFF = (30, 60, 120, 300)   # s, 조회가 연속 실패할 때 다음 시도까지 대기 시간
WX_WATCHDOG_SEC = 90       # s, 조회가 이 시간 넘게 끝나지 않으면 멈춘 것으로 보고 새로 시도
WX_STALE_SEC = 300         # s, 이보다 오래된(갱신이 계속 실패한) 날씨는 흐리게 표시
LOCK_HEADING_SEC = 10       # s, 잠금 중 진행 방향 계산 간격
LOCK_MAP_SEC = 5            # s, 잠금 중 지도 갱신(내 위치·경로·회전) 간격
LOCK_PAUSE_DEVIATION = False  # 잠금 중에는 경로 이탈 경고(진동/소리)도 일시 정지 (False면 잠금 중에도 경고)
WX_CACHE_MAX_AGE = 10800   # s, 저장된 날씨를 쓸 수 있는 최대 경과 시간(3시간)
# ---- 지도 타일 캐시 / 오프라인 설정
TILE_CACHE_DIR = os.path.join(SAVE_DIR, 'tile_cache')
TILE_CACHE_MAX_MB = 5000   # MB, 넘으면 오래 안 쓴 타일부터 자동 삭제
TILE_NET_TIMEOUT = 20       # s, 타일 1개 내려받기 제한 시간
NET_FAIL_COOLDOWN = 20     # s, 네트워크 실패 후 이 시간 동안은 네트워크 시도를 생략(즉시 저장본/대체 타일 표시)
OVERZOOM_LEVELS = 4        # 저장된 타일이 없을 때 이 단계까지 낮은 줌 타일을 확대해 대체
PREFETCH_MIN_ZOOM = 12     # 오프라인 미리받기 줌 범위
PREFETCH_MAX_ZOOM = 16
PREFETCH_MAX_TILES = 2500  # 한 번에 받을 최대 타일 수
PREFETCH_DELAY = 0.12      # s, 타일 사이 대기 (공개 서버 보호)
# ---- 기록 중 경량 모드 (진행 방향 회전 외의 작업은 늦추거나 멈춰 앱이 멈추는 현상을 줄임)
REC_MAP_SEC = 5            # s, 기록 중 지도(내 위치·기록 경로) 갱신 간격 (기존: 1초마다 전체 경로 전송)
REC_DEVIATION_SEC = 5      # s, 기록 중 경로 이탈 검사 간격 (기존: 1초에 2번씩 GPX 전체 점 계산)
REC_WX_REFRESH_SEC = 600   # s, 기록 중 날씨 자동 갱신 간격 (아이콘을 누르면 즉시 갱신)
REC_HEADING_TICK = 0.3     # s, 기록 중 진행 방향 처리 간격 (기존 0.12초)
REC_HEADING_MIN_DELTA = 0.5  # 도, 기록 중 이보다 적게 변하면 지도 회전 명령을 생략
REC_HEADING_RESEND_SEC = 5   # s, 변화가 없어도 이 간격마다 한 번은 방향을 다시 맞춤
# ---- GPX 따라가기 시뮬레이션
SIM_BASE_KMH = 4.0                      # km/h, 1배속일 때 걷는 속도
SIM_SPEEDS = (1, 2, 5, 10, 20, 50, 100)  # 선택할 수 있는 배속
SIM_LOOKAHEAD_M = 25.0                  # m, 시뮬레이션 진행 방향 계산 시 앞쪽으로 내다보는 거리
SIM_MENU_SEP = '\u2500' * 14             # 시뮬레이션 메뉴 구분선 (선택해도 아무 동작 안 함)
SIM_DEFAULT_SPEED = 5                   # 처음 선택되어 있는 배속
TRACK_HEADING_SEC = 5   # s, 기록 중 진행 방향(지도 회전 기준)을 갱신하는 간격
TRACK_HEADING_DIST = 10 # m, 현재 위치와 이만큼 이전 위치를 이은 선으로 방향 계산
# ---- GPS 노이즈 제거 설정
START_MAX_ACCURACY = 20 # m, 기록 첫 점은 이보다 정확할 때만 채택 (MAX_ACCURACY는 이후 점에 적용)
FAST_SPEED_MPS = 10.0   # m/s, 1초에 10m 이상 같은 '단시간 장거리 이동'은 GPS 튐으로 보고 곡선 보정
SPIKE_GAIN = 0.1        # 튐으로 보인 좌표를 반영하는 비율 (작을수록 예측 곡선을 더 따라감)
JUMP_CONFIRM = 3        # 튐으로 보였던 좌표가 연속 N회 비슷한 곳이면 실제 이동으로 인정
JUMP_LINK_M = 30        # m, 위 연속 판정 시 직전 후보 좌표와의 최대 거리
KF_PROCESS_NOISE = 3.0  # m/s, 칼만 필터 프로세스 노이즈 (클수록 반응 빠름, 작을수록 부드러움)
CURVE_SMOOTH = 0.5      # 0~1, 기록된 점을 앞뒤 점의 중간 쪽으로 당기는 정도 (곡선화 강도)
CURVE_SMOOTH_FAST = 0.85  # 단시간 장거리 구간에 쓰는 곡선화 강도
STILL_SPEED_MPS = 0.25  # m/s, GPS 속도가 이보다 낮으면 정지로 보고 좌표를 갱신하지 않음
SERVER_PORT = 0
TOP_INSET = 44          # 상태바(노치) 높이

# ---------------------------------------------------------------- 설정 파일 로드
CONFIG_INFO = {'path': None, 'error': None}      # 설정 파일을 어디서 읽었는지 / 왜 못 읽었는지 (지도 선택창 안내에 사용)

def load_config():
    cands = [CONFIG_PATH, OLD_CONFIG_PATH,
             os.path.join(os.getcwd(), 'trek_config.json'),
             os.path.join(os.path.expanduser('~/Documents'), 'trek_config.json')]
    seen = set()
    for path in cands:
        if path in seen or not os.path.exists(path):
            continue
        seen.add(path)
        try:
            with open(path, 'r', encoding='utf-8-sig') as f:     # utf-8-sig: 메모장 등이 붙이는 BOM도 허용
                data = json.load(f)
            if isinstance(data, dict):
                CONFIG_INFO['path'] = path
                CONFIG_INFO['error'] = None
                return data
            CONFIG_INFO['error'] = '%s: { } 형태의 JSON이 아님' % os.path.basename(path)
        except Exception as e:
            CONFIG_INFO['error'] = '%s: %s' % (os.path.basename(path), e)
    return {}

def find_vworld_key(cfg):
    """설정에서 VWorld 키를 찾는다 (항목 이름의 대소문자·하이픈 차이, 키 앞뒤 공백·따옴표·줄바꿈 허용)."""
    names = ('vworld_key', 'vworldkey', 'vworld', 'vworld_api_key', 'vworld_apikey')
    for k, v in cfg.items():
        if str(k).strip().lower().replace('-', '_') in names:
            txt = ''.join(str(v).split())
            return txt.strip('"\'\u201c\u201d\u2018\u2019')
    return ''

CONFIG = load_config()
VWORLD_KEY = find_vworld_key(CONFIG)

try:
    MAG_DECLINATION = float(CONFIG.get('declination', -8.0))
except Exception:
    MAG_DECLINATION = -8.0

HEADING_STATE = {'on': False}

# ---------------------------------------------------------------- 로거 설정
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

def ilog(msg):
    """정보성 기록은 남기지 않는다 (에러만 기록). 다시 기록하려면 여기서 dlog(msg)를 호출하면 된다."""
    pass

def wlog(msg):
    """날씨 전용 로그: trek_weather_log.txt (WX_LOG_MAX_KB를 넘으면 .1로 넘기고 새로 시작)"""
    try:
        os.makedirs(SAVE_DIR, exist_ok=True)
        try:
            if os.path.getsize(WX_LOG_PATH) > WX_LOG_MAX_KB * 1024:
                os.replace(WX_LOG_PATH, WX_LOG_PATH + '.1')
        except OSError:
            pass
        with open(WX_LOG_PATH, 'a', encoding='utf-8') as f:
            f.write('%s [날씨] %s\n' % (datetime.datetime.now().strftime('%m-%d %H:%M:%S'), msg))
    except Exception as e:
        print("Weather log error:", e)

def wx_cache_save(w):
    try:
        with open(WX_CACHE_PATH, 'w', encoding='utf-8') as f:
            json.dump(w, f)
    except Exception as e:
        wlog('날씨 저장 실패: %s' % e)

def wx_cache_load():
    """마지막으로 받은 날씨 (WX_CACHE_MAX_AGE 이내일 때만)"""
    try:
        with open(WX_CACHE_PATH, 'r', encoding='utf-8') as f:
            d = json.load(f)
        if time.time() - float(d['ts']) > WX_CACHE_MAX_AGE:
            return None
        return d
    except Exception:
        return None

def wx_extra(w, src):
    """화면(JS)에 함께 넘기는 부가 정보: 바람, 체감온도, 습도, 시간별 예보 등. 값이 없으면 None."""
    keys = ('t', 'code', 'is_day', 'wind', 'wdir', 'gust', 'feels', 'hum', 'precip', 'pressure',
            'cloud', 'pm10', 'pm25', 'hourly', 'lat', 'lon', 'ts')
    d = {k: w.get(k) for k in keys}
    d['src'] = src
    return d

_WX_DIAG_TS = [0.0]

def wx_diagnose():
    """날씨 조회가 실패했을 때 원인을 구분하기 위한 점검(DNS -> TCP -> HTTPS). 2분에 한 번만 실행."""
    now = time.time()
    if now - _WX_DIAG_TS[0] < 120:
        return
    _WX_DIAG_TS[0] = now
    host = 'api.open-meteo.com'
    try:
        t0 = time.time()
        infos = socket.getaddrinfo(host, 443, type=socket.SOCK_STREAM)
        addrs = sorted(set(i[4][0] for i in infos))
        ilog('진단 DNS 성공 %.2f초 %s' % (time.time() - t0, ','.join(addrs[:3])))
    except Exception as e:
        wlog('진단 DNS 실패 (%s: %s) -> 도메인 주소를 못 찾음: 데이터/와이파이/DNS/VPN 확인' % (type(e).__name__, e))
        return
    try:
        t0 = time.time()
        sk = socket.create_connection((host, 443), timeout=5)
        sk.close()
        ilog('진단 TCP 443 연결 성공 %.2f초' % (time.time() - t0))
    except Exception as e:
        wlog('진단 TCP 443 연결 실패 (%s: %s) -> 서버/네트워크 차단 가능성' % (type(e).__name__, e))
        return
    try:
        t0 = time.time()
        with urllib.request.urlopen('https://clients3.google.com/generate_204', timeout=5) as r:
            ilog('진단 일반 인터넷(HTTPS) 정상 HTTP %s %.2f초 -> Open-Meteo 쪽 문제 또는 일시 오류' % (r.status, time.time() - t0))
    except Exception as e:
        wlog('진단 일반 인터넷(HTTPS) 실패 (%s: %s)' % (type(e).__name__, e))

ilog("=== 트레커 앱 시작됨 (v4.36) == (+) 클립보드 삭제 & 2초 숨김 & 툴팁 1.5배 띄우기 + 날씨 조회 안정화/날씨 로그 + 방위 바 양끝 흐림 + 풍향/풍속 표시 및 상세 정보창 + 날씨 1분 갱신 + 잠금 중 기록/진행방향만 수행 + 지도 터치 십자선/잠금 중 절전")

def write_run_mark(info):
    try:
        with open(RUN_MARK, 'w', encoding='utf-8') as f:
            f.write(info)
    except Exception:
        pass

def clear_run_mark():
    try:
        if os.path.exists(RUN_MARK):
            os.remove(RUN_MARK)
    except Exception:
        pass

def check_previous_crash():
    try:
        if os.path.exists(RUN_MARK):
            with open(RUN_MARK, 'r', encoding='utf-8') as f:
                last = f.read().strip()
            dlog("!! 이전 실행이 정상 종료되지 않았습니다 (다운/강제 종료 추정). 마지막 생존 기록: %s" % last)
    except Exception:
        pass

check_previous_crash()
write_run_mark('시작 %s' % datetime.datetime.now().strftime('%m-%d %H:%M:%S'))

_FAULT_FILE = None

def enable_fault():
    """치명적 오류(비정상 종료) 때 파이썬 호출 기록을 trek_debug.txt에 남긴다. 파일은 계속 열어 두어야 한다."""
    global _FAULT_FILE
    try:
        import faulthandler
        _FAULT_FILE = open(LOG_PATH, 'a', encoding='utf-8')
        faulthandler.enable(file=_FAULT_FILE, all_threads=True)
    except Exception:
        pass

_APP_CLOSED = {'v': False}      # 화면이 닫힌 뒤에는 메인 스레드 예약 실행을 만들지 않기 위한 표시

def run_on_main(fn):
    if _APP_CLOSED['v']:
        return
    try:
        ui.delay(fn, 0)
    except Exception:
        try:
            fn()
        except Exception:
            pass

# ---------------------------------------------------------------- 지도 및 레이어 선택 HTML
MAP_HTML = """<!DOCTYPE html><html><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.css">
<script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.js"></script>
<!-- 지도 회전 플러그인 (leaflet-rotate) CDN -->
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
  /* GPX 정보 영역: [고도 프로파일 40%][GPX명 60%] (지도 선택 버튼 왼쪽) */
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
  #gpx-elev { cursor: pointer; }
  #elev-svg { position: absolute; left: 6px; right: 6px; top: 4px; bottom: 4px; }
  #elev-svg svg { width: 100%; height: 100%; }
  /* 십자선(지도 중심)이 GPX선 근처일 때 고도 그래프 위 해당 위치를 가리키는 점 */
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
  /* 시뮬레이션 실행 중에는 [고도 프로파일 70%][GPX명 30%] (종료하면 원래 40%/60%로 복귀) */
  body.sim-on #gpx-elev { width: calc(70% - 4px); }
  body.sim-on #gpx-name-badge { width: calc(30% - 4px); }

  #layer-toggle-btn {
    background: rgba(30,30,30,0.95); color: white; border: 1px solid rgba(255,255,255,0.3);
    padding: 10px 14px; border-radius: 8px; font-size: 14px; font-weight: bold;
    cursor: pointer; box-shadow: 0 4px 12px rgba(0,0,0,0.5);
    -webkit-appearance: none; touch-action: manipulation; white-space: nowrap;
  }
  #layer-box {
    margin-top: 6px;
    background: rgba(30,30,30,0.95); padding: 8px; border-radius: 8px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.5); display: none; flex-direction: column; gap: 6px;
    max-height: calc(100vh - 200px); overflow-y: auto; -webkit-overflow-scrolling: touch;   /* 목록 끝(국토부 위성 등)이 잘리지 않게 화면 높이에 맞춤 */
    border: 1px solid rgba(255,255,255,0.15);
  }
  #layer-box.show { display: flex; }
  body.has-vworld #layer-box { margin-right: 56px; }   /* VWorld 지도가 있어 목록이 길 때만 오른쪽 아이콘 열과 겹치지 않게 안쪽으로 */
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

  /* 화면 중앙 투명 나침반 오버레이 (사이즈 4/5로 축소: 256px) */
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
  /* Esri(위성) 지도에서는 원형 나침반(링·눈금·방위 글자·각도 숫자)을 검은색 대신 흰색으로 */
  body.sat-map #screen-compass-ring [stroke="#000000"] { stroke: #ffffff; }
  body.sat-map #screen-compass-ring [fill="#000000"] { fill: #ffffff; }
  body.sat-map #screen-compass-ring circle[fill^="rgba(0,0,0"] { fill: rgba(255,255,255,0.12); }

  /* 화면 중앙 십자선 + 세련된 고가시성 좌표 툴팁 (기존 대비 1.5배 더 띄움: 57px) */
  #center-cross {
    position: absolute; top: 50%; left: 50%; width: 64px; height: 64px;
    transform: translate(-50%, -50%); pointer-events: none; z-index: 999;
    opacity: 0; transition: opacity 0.3s ease;
  }
  #center-cross.show { opacity: 1; }

  #coord-tooltip {
    position: absolute; top: calc(50% + 57px); left: 50%;
    transform: translateX(-50%); background: rgba(20, 20, 22, 0.92);
    border: 1px solid rgba(255, 255, 255, 0.3);
    padding: 5px 12px; border-radius: 12px;
    box-shadow: 0 6px 16px rgba(0, 0, 0, 0.65);
    color: #ffffff; font-size: 13px; font-weight: 800;
    letter-spacing: -0.2px; white-space: nowrap; pointer-events: none;
    backdrop-filter: blur(8px); -webkit-backdrop-filter: blur(8px);
    display: flex; flex-direction: column; align-items: center; gap: 2px;
    width: max-content; max-width: 90vw; box-sizing: border-box;
  }
  #ct-row { display: flex; align-items: center; gap: 5px; }
  #ct-addr {
    display: none; font-size: 12px; font-weight: 700; color: #d1d1d6; text-shadow: none;
    white-space: normal; text-align: center; line-height: 1.25; max-width: 100%;
  }
  #ct-addr.show { display: block; }
  #coord-tooltip .lat { color: #38bdf8; text-shadow: 0 0 8px rgba(56, 189, 248, 0.4); }
  #coord-tooltip .lon { color: #ffffff; text-shadow: 0 0 8px rgba(255, 255, 255, 0.4); }
  #coord-tooltip .sep { color: #a1a1aa; font-weight: 500; }

  /* 현재위치 버튼 옆 거리 척도 (투명 배경, 검은 글자) */
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

  /* 고도 상세 패널 (고도 UI를 누르면 열리고 ✕로 닫음) */
  #elev-detail {
    position: absolute; left: 8px; right: 8px; top: 34px; z-index: 100000;
    display: none; flex-direction: column; color: #ffffff;
    max-height: calc(100% - 52px); overflow: hidden;
    background: rgba(28,28,30,0.88); border: 1px solid rgba(255,255,255,0.18);
    border-radius: 12px; box-shadow: 0 8px 24px rgba(0,0,0,0.6);
  }
  #elev-detail.show { display: flex; }
  /* 시뮬레이션·경로 기록 중 간략 보기: 상단 버튼 줄 아래에서 시작, 높이는 (십자선 위까지 높이)의 2/3 */
  #elev-detail.compact { top: 76px; bottom: auto; height: calc((50% - 100px) * 0.667); max-height: none; }
  #elev-detail.compact #ed-splits-wrap, #elev-detail.compact #ed-stats { display: none; }
  #elev-detail.compact #ed-head { padding: 4px 6px 0 8px; }
  #elev-detail.compact #ed-title { display: flex; gap: 4px; overflow: visible; white-space: normal; }
  #elev-detail.compact #ed-title .ed-stat { flex: 1 1 0; min-width: 0; padding: 2px 2px; }
  #elev-detail.compact #ed-title .ed-stat .k { font-size: 9px; }
  #elev-detail.compact #ed-title .ed-stat .v { font-size: 14px; color: #ffffff; }
  #elev-detail.compact #ed-close { width: 26px; height: 26px; border-radius: 13px; font-size: 13px; }
  #elev-detail.compact #ed-readout { display: flex; align-items: baseline; gap: 10px; font-size: 14px; font-weight: 700;
    padding: 2px 10px 0; min-height: 24px; white-space: nowrap; overflow: hidden; }
  #elev-detail.compact #ed-readout .g { font-size: 19px; font-weight: 800; }
  #elev-detail.compact #ed-chart { flex: 1 1 0; min-height: 36px; height: auto; margin: 0 6px 3px; overflow: hidden; touch-action: auto; }
  body.ed-compact #layer-container { z-index: 100001; }    /* 간략 보기 중에도 지도 선택 창이 앞에 보이게 */
  #ed-head { display: flex; align-items: center; padding: 8px 8px 4px 12px; flex: 0 0 auto; }
  #ed-title { flex: 1; min-width: 0; font-size: 14px; font-weight: 800; color: #0a84ff;
    white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  #ed-close {
    width: 32px; height: 32px; margin-left: 8px; border: none; border-radius: 16px;
    background: #3a3a3c; color: #ffffff; font-size: 16px; font-weight: 800; padding: 0;
    -webkit-appearance: none; touch-action: manipulation; cursor: pointer;
  }
  #ed-stats { display: grid; grid-template-columns: repeat(3, 1fr); gap: 6px; padding: 4px 10px; flex: 0 0 auto; }
  .ed-stat { background: rgba(44,44,46,0.75); border-radius: 8px; padding: 5px 4px; text-align: center; }
  .ed-stat .k { font-size: 10px; color: #8e8e93; }
  .ed-stat .v { font-size: 14px; font-weight: 800; white-space: nowrap; }
  #ed-readout { flex: 0 0 auto; font-size: 12px; color: #d1d1d6; padding: 4px 12px 0; min-height: 18px; }
  #ed-chart { flex: 0 0 auto; height: 170px; margin: 2px 8px 6px; touch-action: none; }
  #ed-splits-wrap { flex: 1 1 auto; min-height: 0; overflow-y: auto; -webkit-overflow-scrolling: touch; padding: 0 8px 8px; }
  #ed-splits { width: 100%; border-collapse: collapse; font-size: 12px; }
  #ed-splits th { color: #8e8e93; font-weight: 600; text-align: right; padding: 4px;
    position: sticky; top: 0; background: rgba(28,28,30,0.88); }
  #ed-splits td { text-align: right; padding: 5px 4px; border-top: 1px solid rgba(255,255,255,0.08); }

  /* 풍향/풍속 표시 (날씨 위) */
  #wind-box {
    background: #0d0d0d; border: 1px solid rgba(255,255,255,0.18);
    width: 44px; padding: 7px 0 6px 0; border-radius: 22px;
    display: none; flex-direction: column; align-items: center; justify-content: center;
    box-shadow: 0 4px 12px rgba(0,0,0,0.65); color: #ffffff;
    cursor: pointer; touch-action: manipulation; -webkit-appearance: none;
  }
  #wind-arrow-wrap { width: 30px; height: 30px; display: flex; align-items: center; justify-content: center; }
  #wind-arrow { width: 28px; height: 28px; transition: transform 0.12s linear; }
  #wind-speed { font-size: 16px; font-weight: 900; line-height: 1; letter-spacing: -0.5px; margin-top: 3px; }

  /* 날씨 상세 정보창 (풍향/풍속 아이콘을 누르면 열리고 ✕로 닫음) */
  #wx-detail {
    position: absolute; left: 8px; right: 8px; top: 34px; z-index: 100003;
    display: none; flex-direction: column; color: #ffffff;
    max-height: calc(100% - 52px); overflow: hidden;
    background: rgba(28,28,30,0.88); border: 1px solid rgba(255,255,255,0.18);
    border-radius: 12px; box-shadow: 0 8px 24px rgba(0,0,0,0.6);
  }
  #wx-detail.show { display: flex; }
  #wd-head { display: flex; align-items: center; padding: 8px 8px 4px 12px; flex: 0 0 auto; }
  #wd-title { flex: 1; font-size: 15px; font-weight: 800; color: #0a84ff; }
  #wd-close {
    width: 32px; height: 32px; margin-left: 8px; border: none; border-radius: 16px;
    background: #3a3a3c; color: #ffffff; font-size: 16px; font-weight: 800; padding: 0;
    -webkit-appearance: none; touch-action: manipulation; cursor: pointer;
  }
  #wd-body { flex: 1 1 auto; min-height: 0; overflow-y: auto; -webkit-overflow-scrolling: touch; padding: 0 10px 10px; }
  .wd-sub { font-size: 11px; color: #8e8e93; padding: 2px 2px 4px; }
  .wd-rose { display: flex; justify-content: center; }
  .wd-hint { text-align: center; font-size: 12px; font-weight: 700; padding: 2px 0 6px; }
  .wd-legend { text-align: center; font-size: 10px; color: #8e8e93; padding-bottom: 6px; }
  .wd-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 6px; }
  .wd-stat { background: rgba(44,44,46,0.75); border-radius: 8px; padding: 5px 4px; text-align: center; }
  .wd-stat .k { font-size: 10px; color: #8e8e93; }
  .wd-stat .v { font-size: 14px; font-weight: 800; white-space: nowrap; }
  .wd-stat .s { font-size: 10px; color: #a1a1a6; }
  .wd-h { font-size: 12px; font-weight: 800; color: #d1d1d6; padding: 10px 2px 4px; }
  .wd-hours { width: 100%; border-collapse: collapse; font-size: 12px; }
  .wd-hours th { color: #8e8e93; font-weight: 600; text-align: center; padding: 3px; }
  .wd-hours td { text-align: center; padding: 4px 3px; border-top: 1px solid rgba(255,255,255,0.08); }
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
      <text x="128" y="55" font-size="28" font-weight="900" fill="#000000" text-anchor="middle">북</text>
      <text x="202" y="137" font-size="28" font-weight="900" fill="#000000" text-anchor="middle">동</text>
      <text x="128" y="221" font-size="28" font-weight="900" fill="#000000" text-anchor="middle">남</text>
      <text x="54" y="137" font-size="28" font-weight="900" fill="#000000" text-anchor="middle">서</text>
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
    <g stroke="#ffffff" stroke-width="4.6" opacity="0.7" stroke-linecap="round">
      <line x1="4" y1="32" x2="60" y2="32"/>
      <line x1="32" y1="4" x2="32" y2="60"/>
    </g>
    <g stroke="#000000" stroke-width="2.2" opacity="0.95" stroke-linecap="round">
      <line x1="4" y1="32" x2="60" y2="32"/>
      <line x1="32" y1="4" x2="32" y2="60"/>
    </g>
  </svg>
  <div id="coord-tooltip">
    <div id="ct-row"><span class="lat" id="ct-lat">--</span><span class="sep">·</span><span class="lon" id="ct-lon">--</span></div>
    <div id="ct-addr"></div>
  </div>
</div>

<div id="wx-detail">
  <div id="wd-head">
    <div id="wd-title">날씨 상세</div>
    <button id="wd-close" ontouchend="closeWxDetail(event)" onclick="closeWxDetail(event)">✕</button>
  </div>
  <div id="wd-body"></div>
</div>

<div id="elev-detail">
  <div id="ed-head">
    <div id="ed-title"></div>
    <button id="ed-close" ontouchend="closeElevDetail(event)" onclick="closeElevDetail(event)">✕</button>
  </div>
  <div id="ed-stats"></div>
  <div id="ed-readout"></div>
  <div id="ed-chart"></div>
  <div id="ed-splits-wrap"><table id="ed-splits"></table></div>
</div>

<div id="layer-container">
  <div id="top-right-group">
    <div id="gpx-info">
      <div id="gpx-elev" ontouchend="onElevClick(event)" onclick="onElevClick(event)" title="고도 상세">
        <div id="elev-svg"></div>
        <div id="elev-cursor"><div id="elev-dot"></div></div>
      </div>
      <div id="gpx-name-badge" ontouchend="onGpxBadgeClick(event)" onclick="onGpxBadgeClick(event)" title=""></div>
    </div>
    <button id="layer-toggle-btn" ontouchend="toggleLayerBox(event)" onclick="toggleLayerBox(event)">🗺️ 지도 선택</button>
  </div>
  <div id="layer-box">
    <button class="layer-btn active" id="btn-opentopo-online" ontouchend="switchLayer('opentopo_online', 'Topo (온라인)', this, event)" onclick="switchLayer('opentopo_online', 'Topo (온라인)', this, event)"><span>Topo (온라인)</span><span class="badge">온라인</span></button>
    <button class="layer-btn" id="btn-opentopo" ontouchend="switchLayer('opentopo', 'Topo (오프라인)', this, event)" onclick="switchLayer('opentopo', 'Topo (오프라인)', this, event)"><span>Topo (오프라인)</span><span class="badge" style="background:#30d158;">오프라인</span></button>
    <button class="layer-btn" id="btn-esri" ontouchend="switchLayer('esri', 'Esri (위성)', this, event)" onclick="switchLayer('esri', 'Esri (위성)', this, event)"><span>Esri (위성)</span><span class="badge">온라인</span></button>
    <button class="layer-btn" id="btn-cyclosm" ontouchend="switchLayer('cyclosm', 'CyclOSM (등산)', this, event)" onclick="switchLayer('cyclosm', 'CyclOSM (등산)', this, event)"><span>CyclOSM (등산)</span><span class="badge">온라인</span></button>
    __VWORLD_BUTTONS__
  </div>
</div>

<div id="bottom-right-controls">
  <div id="diff-wrap">
    <div id="diff-panel"></div>
    <button id="diff-btn" ontouchend="toggleDiffPanel(event)" onclick="toggleDiffPanel(event)" title="경로 난이도">
      <svg width="24" height="17" viewBox="0 0 24 17">
        <polygon points="1,16 9,2 14,10 17,6 23,16" fill="currentColor" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/>
      </svg>
      <span id="diff-lv">Lv1</span>
    </button>
  </div>
  <div id="wind-box" ontouchend="onWindClick(event)" onclick="onWindClick(event)" title="바람 (눌러서 상세 정보)">
    <div id="wind-arrow-wrap">
      <svg id="wind-arrow" viewBox="0 0 28 28">
        <polygon points="14,3 24,24 14,18 4,24" fill="#ff5a36" stroke="#ff5a36" stroke-width="1" stroke-linejoin="round"/>
      </svg>
    </div>
    <span id="wind-speed">-</span>
  </div>
  <div id="weather-box" ontouchend="onWeatherClick(event)" onclick="onWeatherClick(event)" title="지도 중심 날씨">
    <span id="wx-icon"></span>
    <span id="wx-temp">-</span>
    <span id="wx-bar"></span>
    <span id="wx-dust">미세</span>
  </div>

  <button id="compass-btn" ontouchend="onCompassClick(event)" onclick="onCompassClick(event)" title="정북으로 복귀">
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
  <button id="loc-btn" ontouchend="onLocBtnClick(event)" onclick="onLocBtnClick(event)" title="내 위치로 이동">
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
      <circle cx="12" cy="12" r="7" stroke="#ffffff" stroke-width="2"/>
      <line x1="12" y1="2" x2="12" y2="6" stroke="#ffffff" stroke-width="2" stroke-linecap="round"/>
      <line x1="12" y1="18" x2="12" y2="22" stroke="#ffffff" stroke-width="2" stroke-linecap="round"/>
      <line x1="2" y1="12" x2="6" y2="12" stroke="#ffffff" stroke-width="2" stroke-linecap="round"/>
      <line x1="18" y1="12" x2="22" y2="12" stroke="#ffffff" stroke-width="2" stroke-linecap="round"/>
    </svg>
  </button>
  </div>
  <div id="layer-info-badge">🗺️ Topo (온라인)</div>
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

var tileErrCount = 0, tileRetryDelay = 6000, tileRetryTimer = null, lastBearingAt = 0;
try { var _sb = map.setBearing; if (_sb) map.setBearing = function() { lastBearingAt = Date.now(); return _sb.apply(this, arguments); }; } catch (e) {}
function retryTiles() {                 // 현재 지도 타일을 모두 다시 요청 (저장된 타일은 즉시, 나머지는 서버에서 다시 받음)
  if (isRecording || simOn) return;      // 기록·시뮬레이션 중(지도 자동 회전 중)에는 부하가 커서 하지 않음
  if (Date.now() - lastBearingAt < 8000) { tileErrCount++; scheduleTileRetry(); return; }   // 지도를 막 회전했으면 잠시 뒤에
  try { if (currentLayer && map.hasLayer(currentLayer)) currentLayer.redraw(); } catch (e) {}
}
function scheduleTileRetry() {          // 타일 불러오기 오류가 나면 점점 간격을 늘리며 자동 재시도
  if (tileRetryTimer) return;
  tileRetryTimer = setTimeout(function() {
    tileRetryTimer = null;
    if (tileErrCount > 0) {
      tileErrCount = 0;
      retryTiles();
      tileRetryDelay = Math.min(tileRetryDelay * 2, 60000);
    }
  }, tileRetryDelay);
}
function tl(path, maxZoom) {
  var lyr = L.tileLayer(proxyBase + path, {maxZoom: maxZoom, keepBuffer: 4, updateWhenIdle: false});
  lyr.on('tileerror', function() { tileErrCount++; scheduleTileRetry(); });
  lyr.on('load', function() { if (tileErrCount === 0) tileRetryDelay = 6000; });
  return lyr;
}
var layers = {
  'opentopo': tl('opentopo/{z}/{x}/{y}.png?mode=cache', 17),
  'opentopo_online': tl('opentopo/{z}/{x}/{y}.png', 17),
  'esri': tl('esri/{z}/{x}/{y}.jpg', 19),
  'cyclosm': tl('cyclosm/{z}/{x}/{y}.png', 20)
};

if (vworldKey) {
  document.body.classList.add('has-vworld');
  layers['vworld_base'] = tl('vworld_base/{z}/{x}/{y}.png', 19);
  layers['vworld_sat'] = tl('vworld_sat/{z}/{x}/{y}.jpeg', 19);
}

var currentLayerKey = 'opentopo_online';
var currentLayer = layers['opentopo_online'];
currentLayer.addTo(map);

L.DomEvent.disableClickPropagation(document.getElementById('layer-container'));
L.DomEvent.disableScrollPropagation(document.getElementById('layer-container'));
L.DomEvent.disableClickPropagation(document.getElementById('bottom-right-controls'));

function toggleLayerBox(e) {
  if (e) { e.preventDefault(); e.stopPropagation(); }
  document.getElementById('layer-box').classList.toggle('show');
}
// 손가락으로 지도를 움직이거나(한 손가락 이동) 회전·확대(두 손가락)하면 열려 있는 지도 선택 창을 닫음
function closeLayerBox() {
  var b = document.getElementById('layer-box');
  if (b && b.classList.contains('show')) b.classList.remove('show');
}
map.on('dragstart', closeLayerBox);          // 사용자가 직접 끌 때만 발생 (시뮬레이션·자동 회전은 해당 없음)
document.getElementById('map').addEventListener('touchmove', function(e) {
  if (e.touches && e.touches.length >= 2 && !(e.target && e.target.closest && e.target.closest('#layer-container'))) closeLayerBox();
}, {passive: true});

var lastLat = 0, lastLon = 0;
var lastTouchTime = 0;

function onLocBtnClick(e) {
  if (e) { e.preventDefault(); e.stopPropagation(); }
  var now = Date.now();
  if (now - lastTouchTime < 300) return;
  lastTouchTime = now;
  if (simOn) simFollow = true;

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
  hideCrosshairNow();
  overlay.classList.add('show');
  if (compassHideTimer) clearTimeout(compassHideTimer);
  compassHideTimer = setTimeout(function() {
    overlay.classList.remove('show');
    updateElevCursor();
  }, 2000);
}

function setHeading(h) {
  headingRaw = h;
  if (headingMode && !isFingerRotating()) {
    if (map.setBearing) {
      var nb = headToBearing(h);
      var cur = map.getBearing ? map.getBearing() : 0;
      if (Math.abs(((nb - cur + 540) % 360) - 180) >= 0.3) map.setBearing(nb);   // 0.3도 미만 변화는 생략
    }
  }
  updateHeadingAngle();
  updateScreenCompass();
}

var coneHiddenByLock = false;
function setConeLocked(on) {
  coneHiddenByLock = !!on;
  if (on) removeCone();
  else if (headingMode && !isRecording) createCone();
}

function createCone() {
  if (hMarker || coneHiddenByLock || simOn) return;
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
      // 시뮬레이션 중에는 지도 배율을 바꾸지 않음 (평소에는 17 이상으로 확대)
      map.setView([lastLat, lastLon], simOn ? map.getZoom() : Math.max(map.getZoom(), 17), {animate: false});
    }
  } else {
    btn.classList.remove('active');
    removeCone();
  }
  try {
    fetch('http://127.0.0.1:' + PORT + '/hmode?on=' + (on ? 1 : 0) + '&_=' + Date.now()).catch(function() {});
  } catch (err) {}
}

function onCompassClick(e) {
  if (e) { e.preventDefault(); e.stopPropagation(); }
  var now = Date.now();
  if (now - lastCompassTouch < 300) return;
  lastCompassTouch = now;
  quietUntil = now + 600;
  if (simOn) simFollow = true;      // 시뮬레이션 중: 진행 표시를 화면 중앙에 계속 유지

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
    if (!simOn) {                   // 시뮬레이션 중에는 해제해도 북쪽 위로 되돌리지 않고 현재 지도 방향을 유지
      map.setBearing(0);
      updateScreenCompass();
    }
  }
}

var SCALE_STEPS = [1, 2, 5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000, 50000, 100000, 200000, 500000, 1000000];
function updateScale() {
  var line = document.getElementById('scale-line');
  var txt = document.getElementById('scale-text');
  if (!line || !txt) return;
  var lat = map.getCenter().lat;
  var mpp = 156543.03392 * Math.cos(lat * Math.PI / 180) / Math.pow(2, map.getZoom());
  if (!(mpp > 0)) return;
  var maxM = mpp * 100;
  var pick = SCALE_STEPS[0];
  for (var i = 0; i < SCALE_STEPS.length; i++) {
    if (SCALE_STEPS[i] <= maxM) pick = SCALE_STEPS[i];
  }
  line.style.width = Math.max(20, Math.round(pick / mpp)) + 'px';
  txt.innerText = pick >= 1000 ? (pick / 1000) + 'km' : pick + 'm';
}
map.on('zoom moveend zoomend', updateScale);
updateScale();

var autoSession = false;
var quietUntil = 0;
var fingerDown = false, fingerUntil = 0;

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

var crossHideTimer = null;
var crossTimed = false;
var tapAddrMode = false;     // 이동/회전 없이 화면을 짧게 터치했을 때만 true (주소 표시 + 5초 유지)
function hideCrosshairNow() {
  var el = document.getElementById('center-cross');
  if (el) el.classList.remove('show');
  crossTimed = false;
  if (crossHideTimer) { clearTimeout(crossHideTimer); crossHideTimer = null; }
  endTapMode();
}
function hideCompassNow() {
  var ov = document.getElementById('screen-compass-overlay');
  if (ov) ov.classList.remove('show');
  if (compassHideTimer) { clearTimeout(compassHideTimer); compassHideTimer = null; }
}
function showCrosshairTemporarily(ms) {
  var el = document.getElementById('center-cross');
  if (!el) return;
  hideCompassNow();
  crossTimed = true;
  el.classList.add('show');
  if (crossHideTimer) clearTimeout(crossHideTimer);
  var dur = ms || (tapAddrMode ? 5000 : 2000);     // 이동/회전 없는 터치만 5초, 그 외 2초
  crossHideTimer = setTimeout(function() {
    crossTimed = false;
    crossHideTimer = null;
    endTapMode();
    if (typeof updateElevCursor === 'function') updateElevCursor();
    else el.classList.remove('show');
  }, dur);
}

// 지도를 터치/클릭하면 십자선(+중심 좌표)을 2초간 표시. 이미 보이면 시간만 연장 (두 번째 터치로 사라지지 않음)
function showCrossOnTouch() {
  updateCenterCoordDisplay();
  showCrosshairTemporarily();
}
map.on('click', showCrossOnTouch);
(function() {
  var mapEl = document.getElementById('map');
  if (!mapEl) return;
  var tapStart = null, tapMulti = false;
  // 라이브러리의 click 이벤트가 오지 않는 경우(회전된 지도, 짧은 터치 등)에도 나오도록 직접 터치를 감지
  mapEl.addEventListener('touchstart', function(e) {
    if (e.touches && e.touches.length > 1) {        // 두 손가락(회전/확대): 주소 표시 안 함
      tapMulti = true; tapStart = null; endTapMode();
      return;
    }
    tapMulti = false;
    endTapMode();                                    // 새 터치 시작: 일단 일반(2초) 모드
    var t = e.touches && e.touches[0];
    tapStart = t ? {x: t.clientX, y: t.clientY, ts: Date.now()} : null;
    showCrossOnTouch();
  }, {passive: true});
  mapEl.addEventListener('touchmove', function(e) {
    if (!tapStart) return;
    var t = e.touches && e.touches[0];
    if (!t || Math.abs(t.clientX - tapStart.x) > 10 || Math.abs(t.clientY - tapStart.y) > 10) {
      tapStart = null;                               // 손가락이 움직임 = 이동: 주소 표시 안 함
      endTapMode();
      showCrosshairTemporarily();
    }
  }, {passive: true});
  mapEl.addEventListener('touchend', function(e) {
    var st = tapStart; tapStart = null;
    if (!st || tapMulti) return;
    if (e.touches && e.touches.length > 0) return;
    if (Date.now() - st.ts > 600) return;            // 오래 누르는 터치는 제외
    startTapMode();                                  // 이동/회전 없는 짧은 터치: 좌표 + 주소를 5초간
  }, {passive: true});
  mapEl.addEventListener('touchcancel', function() { tapStart = null; endTapMode(); }, {passive: true});
  mapEl.addEventListener('mousedown', function() { showCrossOnTouch(); });
})();

map.on('drag', function() {
  endTapMode();
  showCrosshairTemporarily();
  updateCenterCoordDisplay();
});
map.on('move', function() {
  updateCenterCoordDisplay();
});

// ---- 중심 좌표 아래 주소 표시: 좌표/십자선이 보일 때만, 3초에 한 번 이하로 조회 (잠금 중에는 쉼)
var addrLat = null, addrLng = null, addrTimer = null, addrBusy = false, addrLastTs = 0;
function endTapMode() {
  tapAddrMode = false;
  if (addrTimer) { clearTimeout(addrTimer); addrTimer = null; }
  var box = document.getElementById('ct-addr');
  if (box) box.classList.remove('show');
  addrLat = null;
}
function startTapMode() {
  tapAddrMode = true;
  showCrosshairTemporarily(5000);
  updateCenterCoordDisplay();
  if (addrTimer) { clearTimeout(addrTimer); addrTimer = null; }
  scheduleAddress(150);
}
function onCenterMovedForAddr(c) {
  var box = document.getElementById('ct-addr');
  if (!box) return;
  if (addrLat !== null && map.distance(c, L.latLng(addrLat, addrLng)) > 25) {
    box.classList.remove('show');            // 중심이 25m 넘게 움직이면 이전 주소는 숨김
    addrLat = null;
  }
  scheduleAddress(700);
}
function scheduleAddress(delay) {
  if (addrLat !== null || addrBusy || addrTimer) return;
  addrTimer = setTimeout(function() { addrTimer = null; fetchAddress(); }, delay);
}
function fetchAddress() {
  var cross = document.getElementById('center-cross');
  var box = document.getElementById('ct-addr');
  if (!cross || !box || !tapAddrMode || !cross.classList.contains('show') || coneHiddenByLock) return;
  if (addrLat !== null || addrBusy) return;
  var gap = Date.now() - addrLastTs;
  var minGap = simOn ? 10000 : (tapAddrMode ? 1000 : 3000);
  if (gap < minGap) { scheduleAddress(minGap - gap + 50); return; }
  var c = map.getCenter();
  addrBusy = true;
  addrLastTs = Date.now();
  fetch('http://127.0.0.1:' + PORT + '/addr?lat=' + c.lat.toFixed(6) + '&lon=' + c.lng.toFixed(6) + '&_=' + Date.now())
    .then(function(r) { return r.json(); })
    .then(function(d) {
      addrBusy = false;
      if (d && d.ok && d.addr) {
        if (map.distance(map.getCenter(), c) <= 25) {
          box.innerText = d.addr;
          box.classList.add('show');
          addrLat = c.lat; addrLng = c.lng;
        } else {
          scheduleAddress(300);              // 조회하는 사이 지도가 많이 움직였으면 다시 조회
        }
      }
    })
    .catch(function() { addrBusy = false; });
}

function updateCenterCoordDisplay() {
  var c = map.getCenter();
  onCenterMovedForAddr(c);
  var latEl = document.getElementById('ct-lat');
  var lonEl = document.getElementById('ct-lon');
  if (latEl && lonEl) {
    latEl.innerText = c.lat.toFixed(5) + '° N';
    lonEl.innerText = c.lng.toFixed(5) + '° E';
  }
}

function autoHeading(on, keepBearing) {
  autoSession = !!on;
  if (on) {
    if (!headingMode) setHeadingMode(true);
  } else {
    if (headingMode) setHeadingMode(false);
    if (!keepBearing) {            // 종료 버튼: 지도 회전 상태를 그대로 두고 원형 나침반도 띄우지 않음
      map.setBearing(0);
      updateScreenCompass();
    }
  }
}

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

function mapCW() {
  return -HEAD_SIGN * ((map.getBearing ? map.getBearing() : 0) || 0);
}
function headToBearing(h) {
  return (((HEAD_SIGN * h) % 360) + 360) % 360;
}

var lastUpSend = 0, upTimer = null;
function getUpDir() {
  return (((360 - mapCW()) % 360) + 360) % 360;
}
var upBusy = false;
function reportUp() {
  if (upBusy || (simOn && headingMode && !isFingerRotating())) return;           // 이전 요청이 끝나기 전에는 새 요청을 보내지 않음 (서버 스레드 폭주 방지)
  upBusy = true;
  var release = function() { upBusy = false; };
  var up = getUpDir();
  try {
    fetch('http://127.0.0.1:' + PORT + '/up?d=' + up.toFixed(1) + '&_=' + Date.now()).then(release, release);
  } catch (err) { release(); }
  setTimeout(release, 2000);
}
function reportUpThrottled() {
  var now = Date.now();
  var upGap = isFingerRotating() ? 300 : ((autoSession || simOn) ? 1000 : 100);
  if (now - lastUpSend >= upGap) {
    lastUpSend = now;
    reportUp();
  } else if (!upTimer) {
    upTimer = setTimeout(function() {
      upTimer = null;
      lastUpSend = Date.now();
      reportUp();
    }, upGap - (now - lastUpSend));
  }
}

var rotFrame = null;
function onRotateFrame() {
  rotFrame = null;
  updateWindArrow();
  updateWxRose();
  var dialGroup = document.getElementById('dial-group');
  if (dialGroup) {
    dialGroup.setAttribute('transform', 'rotate(' + mapCW() + ', 18, 18)');
  }
  updateHeadingAngle();
  updateScreenCompass();
  if (isFingerRotating() || (!autoSession && !headingMode && Date.now() >= quietUntil)) {
    showScreenCompassTemporarily();
  }
}
map.on('rotate', function() {
  if (rotateDetecting) return;
  reportUpThrottled();
  // 빠르게 돌릴 때 이벤트마다 화면을 갱신하지 않고, 화면 프레임당 한 번만 갱신 (과부하 방지)
  if (rotFrame === null) {
    rotFrame = (window.requestAnimationFrame || function(f) { return setTimeout(f, 16); })(onRotateFrame);
  }
});
reportUp();

var centerFetchTimer = null;
map.on('moveend', function() {
  if (centerFetchTimer) clearTimeout(centerFetchTimer);
  centerFetchTimer = setTimeout(function() {
    if (simOn) return;               // 시뮬레이션 중에는 중심 고도 조회 생략 (매초 네트워크 요청 방지)
    var c = map.getCenter();
    try {
      fetch('http://127.0.0.1:' + PORT + '/center_move?lat=' + c.lat.toFixed(6) + '&lon=' + c.lng.toFixed(6) + '&_=' + Date.now()).catch(function(){});
    } catch(err){}
  }, 400);
});

function switchLayer(key, name, btn, e) {
  if (e) { e.preventDefault(); e.stopPropagation(); }
  if (!layers[key]) return;
  if (currentLayer) map.removeLayer(currentLayer);
  currentLayer = layers[key];
  currentLayerKey = key;
  currentLayer.addTo(map);
  if (key === 'esri' || key === 'vworld_sat') document.body.classList.add('sat-map');      // Esri(위성): 원형 나침반 흰색
  else document.body.classList.remove('sat-map');
  
  var btns = document.getElementsByClassName('layer-btn');
  for (var i = 0; i < btns.length; i++) {
    btns[i].classList.remove('active');
  }
  btn.classList.add('active');
  toggleLayerBox();
  document.getElementById('layer-info-badge').innerText = '🗺️ ' + name;
}

var me = L.circleMarker([0,0], {radius:8, color:'#ffffff', weight:3, fillColor:'#ff3b30', fillOpacity:1});
var gpxLine = L.polyline([], {color:'#0a84ff', weight:5, opacity:0.8}).addTo(map);
// 기록 경로: Topo/위성 지도에서도 눈에 띄도록 진한 자홍색 선 + 흰색 테두리 (GPX 경로선 위에 그림)
var routeCase = L.polyline([], {color:'#ffffff', weight:10, opacity:0.95, lineCap:'round', lineJoin:'round'}).addTo(map);
var routeLine = L.polyline([], {color:'#ff00cc', weight:5, opacity:1, lineCap:'round', lineJoin:'round'}).addTo(map);
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

var simOn = false, simFollow = false;
var simFrac = null, edTouched = false, curFrac = null, recFrac = null;     // 시뮬레이션 진행 비율(0~1), 고도 상세 그래프를 손으로 짚었는지
function setSimMode(on, lat, lon) {
  simOn = !!on;
  simFollow = !!on;
  simFrac = on ? 0 : null;
  applyEdMode();
  updateEdCur();
  updateEdSim();
  if (on) document.body.classList.add('sim-on');
  else document.body.classList.remove('sim-on');
  // 시뮬레이션 종료: 나침반(진행 방향 자동 회전/따라가기)을 끄고, 종료한 위치와 지도 방향을 그대로 유지
  // (끄지 않으면 나침반 모드가 실제 현재 위치로 지도를 옮겨 버림)
  if (!on && headingMode) setHeadingMode(false);
  if (on && headingMode) removeCone();
  if (on && lat !== undefined && lon !== undefined) {
    map.setView([lat, lon], Math.max(map.getZoom(), 16), {animate: false});
  }
}
map.on('dragstart', function() { simFollow = false; });
function simJump(lat, lon) {
  simFollow = true;
  animCurrentLat = lat; animCurrentLon = lon;
  animTargetLat = lat; animTargetLon = lon;
  try { me.setLatLng([lat, lon]); } catch (e) {}
  map.setView([lat, lon], map.getZoom(), {animate: false});
}

function updateMap(lat, lon, pts, rec) {
  var wasRec = isRecording;
  isRecording = !!rec;
  if (wasRec !== isRecording) { recFrac = null; recLastS = null; recMiss = 0; applyEdMode(); }
  lastLat = lat;
  lastLon = lon;
  if (isRecording) updateRecProgress();
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
    routeCase.setLatLngs(pts);
    routeLine.setLatLngs(pts);
  }

  if (simFollow && !headingMode) {
    var simC = map.getCenter();
    if (simC.distanceTo(L.latLng(lat, lon)) > 3000) {
      map.setView([lat, lon], Math.max(map.getZoom(), 16), {animate: false});
    } else {
      map.panTo([lat, lon], {animate: true, duration: 0.5});
    }
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

var gpxPts = [], gpxCum = [], gpxTotal = 0;
var projZoom = null, projX = [], projY = [];
var elevProf = null, elevMin = 0, elevSpan = 0, elevTotal = 1;
var ELEV_NEAR_PX = 24;

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
  recLastS = null; recMiss = 0; recFrac = null;
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

function findNearOnRoute() {
  if (gpxPts.length < 2 || !(gpxTotal > 0)) return null;
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
  if (bi < 0 || best > TH * TH) return null;
  return {i: bi, u: bu};
}

function updateRouteCrosshair(hasRoute, near) {
  var el = document.getElementById('center-cross');
  if (!el) return;
  var ov = document.getElementById('screen-compass-overlay');
  var compassOn = !!(ov && ov.classList.contains('show'));
  var want = !compassOn && (crossTimed || !!near);
  if (want) el.classList.add('show'); else el.classList.remove('show');
}

function updateElevCursor() {
  var cur = document.getElementById('elev-cursor');
  if (!cur) return;
  var box = document.getElementById('gpx-elev');
  var hasRoute = gpxPts.length >= 2 && gpxTotal > 0;
  var near = hasRoute ? findNearOnRoute() : null;
  updateRouteCrosshair(hasRoute, near);
  if (!near || !elevProf || elevProf.length < 2 || !box || !box.classList.contains('show')) {
    cur.style.display = 'none';
    curFrac = null;
    updateEdCur();
    return;
  }
  var dist = gpxCum[near.i] + near.u * (gpxCum[near.i + 1] - gpxCum[near.i]);
  var frac = Math.max(0, Math.min(1, dist / gpxTotal));
  var e = elevAt(frac * elevTotal);
  var H = 30, padT = 3, padB = 2;
  var y = elevSpan < 1 ? H / 2 : (H - padB) - (e - elevMin) / elevSpan * (H - padT - padB);
  var dot = document.getElementById('elev-dot');
  dot.style.left = (frac * 100).toFixed(2) + '%';
  dot.style.top = (y / H * 100).toFixed(2) + '%';
  cur.style.display = 'block';
  curFrac = frac;
  updateEdCur();
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

function setElevationProfile(prof) {
  var box = document.getElementById('elev-svg');
  if (!box) return;
  if (!prof || prof.length < 2) {
    elevProf = null;
    box.innerHTML = '<span class="elev-none">고도 정보 없음</span>';
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

var elevDetail = null, edGeom = null, lastElevClick = 0;

function niceStep(range, target) {
  var raw = range / target;
  var mag = Math.pow(10, Math.floor(Math.log(raw) / Math.LN10));
  var n = raw / mag;
  var f = n < 1.5 ? 1 : (n < 3 ? 2 : (n < 7 ? 5 : 10));
  return f * mag;
}
function profAt(arr, d) {
  var n = arr.length;
  if (d <= arr[0][0]) return arr[0][1];
  if (d >= arr[n - 1][0]) return arr[n - 1][1];
  var lo = 0, hi = n - 1;
  while (hi - lo > 1) {
    var mid = (lo + hi) >> 1;
    if (arr[mid][0] <= d) lo = mid; else hi = mid;
  }
  var d0 = arr[lo][0], d1 = arr[hi][0];
  var t = d1 > d0 ? (d - d0) / (d1 - d0) : 0;
  return arr[lo][1] + t * (arr[hi][1] - arr[lo][1]);
}
function fmtInt(v) { return Math.round(v).toLocaleString('en-US'); }
function kmStr(m) { return String(+(m / 1000).toFixed(2)); }

function setElevationProfile(prof) {
  var box = document.getElementById('elev-svg');
  if (!box) return;
  if (!prof || prof.length < 2) {
    elevProf = null;
    box.innerHTML = '<span class="elev-none">고도 정보 없음</span>';
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

function setElevDetail(d) {
  elevDetail = d || null;
  closeElevDetail();
}

function onElevClick(e) {
  if (e) { e.preventDefault(); e.stopPropagation(); }
  var now = Date.now();
  if (now - lastElevClick < 300) return;
  lastElevClick = now;
  openElevDetail();
}

function openElevDetail() {
  if (!elevDetail) return;
  var p = document.getElementById('elev-detail');
  if (!p) return;
  p.classList.add('show');
  p.classList.toggle('compact', edIsCompact());
  if (isRecording) recFrac = computeRecFrac();
  syncEdBodyClass();
  edTouched = false;
  buildElevDetail();
  drawElevChart();
}

function closeElevDetail(e) {
  if (e) { e.preventDefault(); e.stopPropagation(); }
  var p = document.getElementById('elev-detail');
  if (p) p.classList.remove('show');
  syncEdBodyClass();
}

// ---- 시뮬레이션·경로 기록 중에는 진행에 필요한 정보만 담은 간략 보기 ----
function edIsCompact() { return simOn || isRecording; }
function edProgM() {                       // 현재 진행 위치(경로 시작에서의 거리 m), 없으면 null
  var d = elevDetail;
  if (!d || !d.prof || d.prof.length < 2) return null;
  var tot = d.dist || d.prof[d.prof.length - 1][0] || 1;
  if (simOn && simFrac !== null) return Math.max(0, Math.min(1, simFrac)) * tot;
  if (isRecording && recFrac !== null) return Math.max(0, Math.min(1, recFrac)) * tot;
  return null;
}
function syncEdBodyClass() {
  var p = document.getElementById('elev-detail');
  document.body.classList.toggle('ed-compact', !!(p && p.classList.contains('show') && p.classList.contains('compact')));
}
function applyEdMode() {
  var p = document.getElementById('elev-detail');
  if (!p) return;
  p.classList.toggle('compact', edIsCompact());
  if (isRecording && p.classList.contains('show')) recFrac = computeRecFrac();
  if (p.classList.contains('show') && elevDetail) { buildElevDetail(); drawElevChart(); }
  syncEdBodyClass();
}
function refreshEdCompact() {              // 진행 위치가 바뀔 때마다 간략 보기를 새로 그림
  var p = document.getElementById('elev-detail');
  if (!p || !p.classList.contains('show') || !p.classList.contains('compact') || !elevDetail) return false;
  buildElevDetail();
  drawElevChart();
  return true;
}
var recLastS = null, recMiss = 0;
function lowerBound(arr, v) { var lo = 0, hi = arr.length; while (lo < hi) { var mid = (lo + hi) >> 1; if (arr[mid] < v) lo = mid + 1; else hi = mid; } return lo; }
function computeRecFrac() {                // 경로 기록 중 현재 위치가 GPX 경로의 어디쯤인지(0~1), 200m 넘게 벗어나면 null
  if (gpxPts.length < 2 || !(gpxTotal > 0)) return null;
  var n = gpxPts.length, i0 = 0, i1 = n - 2;
  if (recLastS !== null && recMiss < 3) {  // 직전 위치 주변만 먼저 검사
    i0 = Math.max(0, lowerBound(gpxCum, recLastS - 1500) - 1);
    i1 = Math.min(n - 2, lowerBound(gpxCum, recLastS + 3000));
    if (i1 < i0) { i0 = 0; i1 = n - 2; }
  }
  var kx = Math.cos(lastLat * Math.PI / 180) * 111320, ky = 110540;
  var best = Infinity, bi = -1, bu = 0, bd2 = 0;
  for (var i = i0; i <= i1; i++) {
    var ax = (gpxPts[i][1] - lastLon) * kx, ay = (gpxPts[i][0] - lastLat) * ky;
    var bx = (gpxPts[i + 1][1] - lastLon) * kx, by = (gpxPts[i + 1][0] - lastLat) * ky;
    var dx = bx - ax, dy = by - ay, l2 = dx * dx + dy * dy;
    var u = l2 > 0 ? Math.max(0, Math.min(1, -(ax * dx + ay * dy) / l2)) : 0;
    var qx = ax + u * dx, qy = ay + u * dy, d2 = qx * qx + qy * qy, sc = d2;
    if (recLastS !== null) {                // 같은 길을 왕복하는 경로에서 진행 방향을 따라가도록 앞쪽을 약간 유리하게
      var dl = gpxCum[i] - recLastS, w = dl >= 0 ? 0.02 : 0.06;
      sc += (dl * w) * (dl * w);
    }
    if (sc < best) { best = sc; bi = i; bu = u; bd2 = d2; }
  }
  if (bi < 0 || Math.sqrt(bd2) > 200) { recMiss++; return null; }
  recMiss = 0;
  recLastS = gpxCum[bi] + bu * (gpxCum[bi + 1] - gpxCum[bi]);
  return recLastS / gpxTotal;
}
function updateRecProgress() {             // 간략 보기가 열려 있을 때만 계산 (평소에는 아무 일도 하지 않음)
  var p = document.getElementById('elev-detail');
  if (!p || !p.classList.contains('show') || !p.classList.contains('compact')) return;
  recFrac = computeRecFrac();
  refreshEdCompact();
}
function nextExtreme(prof, m) {            // 앞으로 처음 만나는 정상(고점) 또는 저점 (20m 이상 오르내림)
  var n = prof.length, TH = 20, i = 0;
  while (i < n && prof[i][0] <= m) i++;
  if (i >= n) return null;
  var e0 = profAt(prof, m), hi = e0, lo = e0, hiD = m, loD = m;
  for (; i < n; i++) {
    var e = prof[i][1], dd = prof[i][0];
    if (e > hi) { hi = e; hiD = dd; }
    if (e < lo) { lo = e; loD = dd; }
    if (hi - e0 >= TH && hi - e >= TH) return {peak: true, d: hiD, e: hi};
    if (e0 - lo >= TH && e - lo >= TH) return {peak: false, d: loD, e: lo};
  }
  if (hi - e0 >= TH) return {peak: true, d: hiD, e: hi};
  if (e0 - lo >= TH) return {peak: false, d: loD, e: lo};
  return null;
}
function buildEdCompact(d) {
  var m = edProgM(), prof = d.prof, tot = d.dist || prof[prof.length - 1][0] || 1;
  var cells, txt;
  if (m === null) {
    cells = [['현재 고도', '-'], ['남은 거리', '-'], ['남은 상승', '-'], ['남은 하강', '-']];
    txt = '<span>' + (isRecording ? '경로에서 벗어나 있어요 (진행 위치 없음)' : '진행 위치를 기다리는 중…') + '</span>';
  } else {
    var e = profAt(prof, m), rg = 0, rl = 0, sp = d.splits || [];
    for (var j = 0; j < sp.length; j++) {            // 남은 상승·하강: 구간별 값을 현재 위치 기준으로 합산
      var s0 = sp[j][0], s1 = sp[j][1];
      if (s1 <= m) continue;
      var f = s0 >= m ? 1 : (s1 - m) / Math.max(s1 - s0, 1);
      rg += sp[j][2] * f; rl += sp[j][3] * f;
    }
    cells = [['현재 고도', fmtInt(e) + ' m'], ['남은 거리', kmStr(Math.max(0, tot - m)) + ' km'],
             ['남은 상승', '+' + fmtInt(rg) + ' m'], ['남은 하강', '−' + fmtInt(rl) + ' m']];
    var a = m, b = Math.min(tot, m + 150);           // 앞 150m 구간의 경사
    var grade = b > a ? (profAt(prof, b) - profAt(prof, a)) / (b - a) * 100 : 0;
    var col = grade > 0 ? '#ff9f0a' : (grade < 0 ? '#5ac8fa' : '#d1d1d6');
    var ex = nextExtreme(prof, m);
    txt = '<span class="g" style="color:' + col + ';">' + (grade > 0 ? '+' : '') + grade.toFixed(1) + '%</span>';
    if (ex) {
      var df = Math.round(ex.e - e);
      txt += '<span>' + (ex.peak ? '⛰ 다음 정상 ' : '⬇ 다음 저점 ') + kmStr(ex.d - m) + 'km · ' + fmtInt(ex.e) + 'm ('
          + (df > 0 ? '+' : '−') + Math.abs(df) + 'm)</span>';
    } else {
      txt += '<span>🏁 도착까지 ' + kmStr(Math.max(0, tot - m)) + 'km</span>';
    }
  }
  var html = '';
  for (var i = 0; i < cells.length; i++) {           // GPX 이름 자리에 현재 고도·남은 거리 등을 표시
    html += '<div class="ed-stat"><div class="k">' + cells[i][0] + '</div><div class="v">' + cells[i][1] + '</div></div>';
  }
  document.getElementById('ed-title').innerHTML = html;
  document.getElementById('ed-readout').innerHTML = txt;
}

function buildElevDetail() {
  var d = elevDetail;
  if (edIsCompact()) { buildEdCompact(d); return; }
  document.getElementById('ed-title').innerText = d.name || 'GPX';
  var items = [
    ['거리', kmStr(d.dist) + ' km'],
    ['누적 상승', '+' + fmtInt(d.gain) + ' m'],
    ['누적 하강', '−' + fmtInt(d.loss) + ' m'],
    ['최고 고도', fmtInt(d.max) + ' m'],
    ['최저 고도', fmtInt(d.min) + ' m'],
    ['시작 → 도착', fmtInt(d.start) + ' → ' + fmtInt(d.end)]
  ];
  var html = '';
  for (var i = 0; i < items.length; i++) {
    html += '<div class="ed-stat"><div class="k">' + items[i][0] + '</div><div class="v">' + items[i][1] + '</div></div>';
  }
  document.getElementById('ed-stats').innerHTML = html;
  document.getElementById('ed-readout').innerText = '그래프를 터치하면 위치별 고도와 경사를 볼 수 있어요';

  var rows = '<tr><th style="text-align:left">구간(km)</th><th>상승</th><th>하강</th><th>경사</th><th>고도</th></tr>';
  var sp = d.splits || [];
  for (var j = 0; j < sp.length; j++) {
    var g = sp[j][4];
    var col = g > 0 ? '#ff9f0a' : (g < 0 ? '#5ac8fa' : '#d1d1d6');
    rows += '<tr><td style="text-align:left">' + kmStr(sp[j][0]) + '~' + kmStr(sp[j][1]) + '</td>'
          + '<td>+' + sp[j][2] + '</td><td>−' + sp[j][3] + '</td>'
          + '<td style="color:' + col + ';">' + (g > 0 ? '+' : '') + g.toFixed(1) + '%</td>'
          + '<td>' + fmtInt(sp[j][5]) + 'm</td></tr>';
  }
  document.getElementById('ed-splits').innerHTML = rows;
}

function drawElevChart() {
  var d = elevDetail, box = document.getElementById('ed-chart');
  if (!d || !box || !d.prof || d.prof.length < 2) return;
  var compact = edIsCompact();
  var W = box.clientWidth || 320, H = box.clientHeight || (compact ? 110 : 170);
  var ml = compact ? 34 : 42, mr = compact ? 6 : 8, mt = compact ? 6 : 10, mb = compact ? 16 : 20;
  var prof = d.prof, i;
  var total = d.dist || prof[prof.length - 1][0] || 1;
  // 표시 구간: 보통은 전체 경로, 간략 보기에서는 현재 위치 앞뒤 약 4km만 확대해서 표시
  var a0 = 0, b0 = total, pm = compact ? edProgM() : null;
  if (compact && pm !== null) {
    var L = Math.min(4000, total);
    a0 = pm - 600; b0 = a0 + L;
    if (a0 < 0) { a0 = 0; b0 = L; }
    if (b0 > total) { b0 = total; a0 = Math.max(0, total - L); }
  }
  var pts = [[a0, profAt(prof, a0)]];
  for (i = 0; i < prof.length; i++) {
    if (prof[i][0] > a0 && prof[i][0] < b0) pts.push(prof[i]);
  }
  pts.push([b0, profAt(prof, b0)]);
  var minE = Infinity, maxE = -Infinity;
  for (i = 0; i < pts.length; i++) {
    if (pts[i][1] < minE) minE = pts[i][1];
    if (pts[i][1] > maxE) maxE = pts[i][1];
  }
  var ystep = niceStep(Math.max(maxE - minE, 20), compact ? 3 : 4);
  var y0 = Math.floor(minE / ystep) * ystep, y1 = Math.ceil(maxE / ystep) * ystep;
  if (y1 - y0 < ystep) y1 = y0 + ystep;
  var pw = W - ml - mr, ph = H - mt - mb;
  var span = Math.max(b0 - a0, 1);
  var X = function(m) { return ml + (m - a0) / span * pw; };
  var Y = function(e) { return mt + (1 - (e - y0) / (y1 - y0)) * ph; };

  var s = '<svg width="' + W + '" height="' + H + '" viewBox="0 0 ' + W + ' ' + H + '" style="display:block">';
  s += '<defs><linearGradient id="edg" x1="0" y1="0" x2="0" y2="1">'
     + '<stop offset="0" stop-color="#e8643c" stop-opacity="0.55"/>'
     + '<stop offset="1" stop-color="#e8643c" stop-opacity="0.05"/></linearGradient></defs>';
  for (var v = y0; v <= y1 + ystep * 0.01; v += ystep) {
    var yy = Y(v);
    s += '<line x1="' + ml + '" y1="' + yy.toFixed(1) + '" x2="' + (W - mr) + '" y2="' + yy.toFixed(1)
       + '" stroke="rgba(255,255,255,0.14)" stroke-width="1"/>';
    s += '<text x="' + (ml - 5) + '" y="' + (yy + 3.5).toFixed(1)
       + '" font-size="' + (compact ? 9 : 10) + '" fill="#8e8e93" text-anchor="end">' + Math.round(v) + '</text>';
  }
  var xstep = niceStep(Math.max(span / 1000, 0.2), compact ? 3 : 4);
  for (var km = Math.ceil(a0 / 1000 / xstep - 1e-9) * xstep; km * 1000 <= b0 + 1; km += xstep) {
    var xx = X(km * 1000);
    s += '<line x1="' + xx.toFixed(1) + '" y1="' + mt + '" x2="' + xx.toFixed(1) + '" y2="' + (H - mb)
       + '" stroke="rgba(255,255,255,0.07)" stroke-width="1"/>';
    s += '<text x="' + xx.toFixed(1) + '" y="' + (H - 4)
       + '" font-size="' + (compact ? 9 : 10) + '" fill="#8e8e93" text-anchor="middle">' + String(+km.toFixed(2)) + 'km</text>';
  }
  var line = '';
  for (i = 0; i < pts.length; i++) {
    line += (i ? 'L' : 'M') + X(pts[i][0]).toFixed(1) + ',' + Y(pts[i][1]).toFixed(1);
  }
  var area = line + 'L' + X(b0).toFixed(1) + ',' + (H - mb) + 'L' + X(a0).toFixed(1) + ',' + (H - mb) + 'Z';
  s += '<path d="' + area + '" fill="url(#edg)"/>';
  s += '<path d="' + line + '" fill="none" stroke="#e8643c" stroke-width="2" stroke-linejoin="round" stroke-linecap="round"/>';
  s += '<line id="ed-pos-line" x1="0" y1="' + mt + '" x2="0" y2="' + (H - mb)
     + '" stroke="#0a84ff" stroke-width="1.5" visibility="hidden"/>';
  s += '<circle id="ed-pos-dot" cx="0" cy="0" r="6" fill="#0a84ff" stroke="#ffffff" stroke-width="2" visibility="hidden"/>';
  s += '<line id="ed-sim-line" x1="0" y1="' + mt + '" x2="0" y2="' + (H - mb)
     + '" stroke="#30d158" stroke-width="1.5" visibility="hidden"/>';
  s += '<circle id="ed-sim-dot" cx="0" cy="0" r="6" fill="#30d158" stroke="#ffffff" stroke-width="2" visibility="hidden"/>';
  s += '<line id="ed-cur-line" x1="0" y1="' + mt + '" x2="0" y2="' + (H - mb)
     + '" stroke="#ffffff" stroke-width="1" stroke-dasharray="3,3" visibility="hidden"/>';
  s += '<circle id="ed-cur-dot" cx="0" cy="0" r="5" fill="#ffffff" stroke="#0a84ff" stroke-width="2" visibility="hidden"/>';
  s += '</svg>';
  box.innerHTML = s;
  edGeom = {W: W, H: H, ml: ml, mr: mr, mt: mt, mb: mb, total: total, a: a0, b: b0, X: X, Y: Y};
  updateEdCur();
  updateEdSim();
}

function updateEdCur() {
  var ln = document.getElementById('ed-pos-line'), dt = document.getElementById('ed-pos-dot');
  var pn = document.getElementById('elev-detail');
  if (!ln || !dt || !pn || !pn.classList.contains('show')) return;
  var g = edGeom, d = elevDetail;
  // 시뮬레이션 진행 중에는 십자선 위치 대신 시뮬 진행 위치(초록)만 표시
  if (curFrac === null || edIsCompact() || !g || !d || !d.prof || d.prof.length < 2) {
    ln.setAttribute('visibility', 'hidden');
    dt.setAttribute('visibility', 'hidden');
    return;
  }
  var m = Math.max(0, Math.min(1, curFrac)) * g.total;
  var e = profAt(d.prof, m);
  var x = g.X(m).toFixed(1);
  ln.setAttribute('x1', x); ln.setAttribute('x2', x); ln.setAttribute('visibility', 'visible');
  dt.setAttribute('cx', x); dt.setAttribute('cy', g.Y(e).toFixed(1)); dt.setAttribute('visibility', 'visible');
  if (!edTouched && !(simOn && simFrac !== null)) {
    var win = Math.max(g.total / 150, 60);
    var a = Math.max(0, m - win / 2), b = Math.min(g.total, m + win / 2);
    var grade = b > a ? (profAt(d.prof, b) - profAt(d.prof, a)) / (b - a) * 100 : 0;
    var col = grade > 0 ? '#ff9f0a' : (grade < 0 ? '#5ac8fa' : '#d1d1d6');
    document.getElementById('ed-readout').innerHTML = '📍 <b>' + (m / 1000).toFixed(2) + ' km</b> · <b>'
      + Math.round(e) + ' m</b> · 경사 <b style="color:' + col + ';">' + (grade > 0 ? '+' : '') + grade.toFixed(1) + '%</b>';
  }
}

function updateEdSim() {
  var ln = document.getElementById('ed-sim-line'), dt = document.getElementById('ed-sim-dot');
  var pn = document.getElementById('elev-detail');
  if (!ln || !dt || !pn || !pn.classList.contains('show')) return;
  var g = edGeom, d = elevDetail;
  var m = edProgM();          // 시뮬레이션 또는 경로 기록 중 GPX 위 진행 위치(m)
  if (m === null || !g || !d || !d.prof || d.prof.length < 2 || m < g.a - 1 || m > g.b + 1) {
    ln.setAttribute('visibility', 'hidden');
    dt.setAttribute('visibility', 'hidden');
    return;
  }
  var e = profAt(d.prof, m);
  var x = g.X(m).toFixed(1);
  ln.setAttribute('x1', x); ln.setAttribute('x2', x); ln.setAttribute('visibility', 'visible');
  dt.setAttribute('cx', x); dt.setAttribute('cy', g.Y(e).toFixed(1)); dt.setAttribute('visibility', 'visible');
  if (!edTouched && !edIsCompact()) {
    var win = Math.max(g.total / 150, 60);
    var a = Math.max(0, m - win / 2), b = Math.min(g.total, m + win / 2);
    var grade = b > a ? (profAt(d.prof, b) - profAt(d.prof, a)) / (b - a) * 100 : 0;
    var col = grade > 0 ? '#ff9f0a' : (grade < 0 ? '#5ac8fa' : '#d1d1d6');
    document.getElementById('ed-readout').innerHTML = '🧪 <b>' + (m / 1000).toFixed(2) + ' km</b> · <b>'
      + Math.round(e) + ' m</b> · 경사 <b style="color:' + col + ';">' + (grade > 0 ? '+' : '') + grade.toFixed(1) + '%</b>';
  }
}
function setSimElevPos(f) {
  simFrac = f;
  if (!refreshEdCompact()) updateEdSim();
}

function edPoint(clientX) {
  var g = edGeom, d = elevDetail;
  if (!g || !d || edIsCompact()) return;
  edTouched = true;
  var box = document.getElementById('ed-chart');
  var r = box.getBoundingClientRect();
  var m = g.a + (clientX - r.left - g.ml) / (g.W - g.ml - g.mr) * (g.b - g.a);
  m = Math.max(0, Math.min(g.total, m));
  var e = profAt(d.prof, m);
  var win = Math.max(g.total / 150, 60);
  var a = Math.max(0, m - win / 2), b = Math.min(g.total, m + win / 2);
  var grade = b > a ? (profAt(d.prof, b) - profAt(d.prof, a)) / (b - a) * 100 : 0;
  var x = g.X(m).toFixed(1);
  var ln = document.getElementById('ed-cur-line'), dt = document.getElementById('ed-cur-dot');
  if (ln) { ln.setAttribute('x1', x); ln.setAttribute('x2', x); ln.setAttribute('visibility', 'visible'); }
  if (dt) {
    dt.setAttribute('cx', x); dt.setAttribute('cy', g.Y(e).toFixed(1)); dt.setAttribute('visibility', 'visible');
  }
  var col = grade > 0 ? '#ff9f0a' : (grade < 0 ? '#5ac8fa' : '#d1d1d6');
  document.getElementById('ed-readout').innerHTML = '📍 <b>' + (m / 1000).toFixed(2) + ' km</b> · <b>'
    + Math.round(e) + ' m</b> · 경사 <b style="color:' + col + ';">' + (grade > 0 ? '+' : '') + grade.toFixed(1) + '%</b>';
}

(function() {
  var box = document.getElementById('ed-chart');
  if (!box) return;
  function handle(e) {
    var t = (e.touches && e.touches[0]) || e;
    edPoint(t.clientX);
    if (e.cancelable) e.preventDefault();
    e.stopPropagation();
  }
  box.addEventListener('touchstart', handle, {passive: false});
  box.addEventListener('touchmove', handle, {passive: false});
  box.addEventListener('mousemove', handle);
  box.addEventListener('mousedown', handle);
})();

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
    return { text: '미세', barColor: '#4b89f3', textColor: '#a1a1a6' };
  }
  if (pm10 <= 30) {
    return { text: '좋음', barColor: '#4b89f3', textColor: '#a1a1a6' };
  } else if (pm10 <= 80) {
    return { text: '보통', barColor: '#30d158', textColor: '#a1a1a6' };
  } else if (pm10 <= 150) {
    return { text: '나쁨', barColor: '#ff9f0a', textColor: '#ff9f0a' };
  } else {
    return { text: '매우나쁨', barColor: '#ff453a', textColor: '#ff453a' };
  }
}

function applyWeather(t, code, isDay, pm10, stale, extra) {
  document.getElementById('wx-icon').innerHTML = wxIconSvg(code, isDay);
  document.getElementById('wx-temp').innerText = Math.round(t) + '°';
  
  var dust = getDustInfo(pm10);
  document.getElementById('wx-bar').style.background = dust.barColor;
  var dustEl = document.getElementById('wx-dust');
  dustEl.innerText = dust.text;
  dustEl.style.color = dust.textColor;
  
  var wbox = document.getElementById('weather-box');
  wbox.style.display = 'flex';
  wbox.style.opacity = stale ? '0.55' : '1';      // 오래된(마지막으로 받은) 날씨는 흐리게
  wbox.title = stale ? '마지막으로 받은 날씨 (갱신 중)' : '지도 중심 날씨';
  setWxExtra(extra, stale);
}

var wxCenterMode = false, lastWxTouch = 0;

// 파이썬이 결과를 확인할 수 있도록 'ok'/'skip' 을 돌려준다 (함수가 없으면 호출 자체가 실패)
function applyGpsWeather(t, code, isDay, pm10, stale, extra) {
  if (wxCenterMode) return 'skip';
  applyWeather(t, code, isDay, pm10, stale, extra);
  return 'ok';
}

function gpsWeatherFail() {
  if (wxCenterMode) return;
  var box = document.getElementById('weather-box');
  if (box.style.display !== 'flex') {
    document.getElementById('wx-icon').innerHTML = '';
    document.getElementById('wx-temp').innerText = '--';
    document.getElementById('wx-dust').innerText = '미세';
    box.style.display = 'flex';
  }
}

function fetchWeatherAt(lat, lon) {
  document.getElementById('wx-temp').innerText = '...';
  var xhr = new XMLHttpRequest();
  xhr.open('GET', 'http://127.0.0.1:' + PORT + '/wx?lat=' + lat.toFixed(4) + '&lon=' + lon.toFixed(4) + '&_=' + Date.now());
  xhr.timeout = 25000;
  xhr.onload = function() {
    try {
      var d = JSON.parse(xhr.responseText);
      if (d.ok) { applyWeather(d.t, d.code, d.is_day === 1, d.pm10, false, d.extra); return; }
      document.getElementById('weather-box').title = '날씨 조회 실패: ' + (d.err || '알 수 없음');
    } catch (err) {}
    document.getElementById('wx-temp').innerText = '--';
  };
  xhr.onerror = xhr.ontimeout = function() {
    document.getElementById('weather-box').title = '날씨 조회 실패: 앱 내부 서버 응답 없음';
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

// ---- 풍향/풍속 표시 (날씨와 같은 위치의 값) + 상세 정보창
var wxExtra = null, windAng = null, wxDetailOpen = false, lastWindClick = 0;

function windDirName(deg) {
  var names = ['북', '북북동', '북동', '동북동', '동', '동남동', '남동', '남남동',
               '남', '남남서', '남서', '서남서', '서', '서북서', '북서', '북북서'];
  return names[Math.round(deg / 22.5) % 16] + '풍';      // 바람이 불어오는 쪽 기준 (북서풍 = 북서쪽에서 불어옴)
}

function beaufort(ms) {
  var lim = [0.3, 1.6, 3.4, 5.5, 8.0, 10.8, 13.9, 17.2, 20.8, 24.5, 28.5, 32.7];
  var nm = ['고요', '실바람', '남실바람', '산들바람', '건들바람', '흔들바람', '된바람',
            '센바람', '큰바람', '큰센바람', '노대바람', '왕바람', '싹쓸바람'];
  for (var i = 0; i < lim.length; i++) { if (ms < lim[i]) return {lv: i, name: nm[i]}; }
  return {lv: 12, name: nm[12]};
}

function windColor(ms) {
  if (ms < 5) return '#ffffff';
  if (ms < 10.8) return '#ffd60a';
  if (ms < 13.9) return '#ff9f0a';
  return '#ff453a';
}

// 풍향 화살표 색: 풍속(m/s)을 보퍼트 풍력 계급으로 나눠 초록→노랑→주황→빨강→보라
function windArrowColor(ms) {
  if (!(ms >= 0)) return '#ff5a36';   // 풍속을 모를 때는 기본색
  if (ms < 3.4) return '#30d158';     // 0~2단계: 고요~남실바람 (거의 무풍)
  if (ms < 8.0) return '#ffd60a';     // 3~4단계: 산들·건들바람
  if (ms < 13.9) return '#ff9f0a';    // 5~6단계: 흔들·된바람 (강한 바람)
  if (ms < 20.8) return '#ff453a';    // 7~8단계: 센바람·큰바람 (강풍)
  return '#bf5af2';                   // 9단계 이상: 폭풍
}

function windHint(ms) {
  if (ms < 8) return {text: '산행 참고: 양호', col: '#30d158'};
  if (ms < 10.8) return {text: '산행 참고: 다소 강함 (능선 주의)', col: '#ffd60a'};
  if (ms < 13.9) return {text: '산행 참고: 강풍 주의 (노출 구간 위험)', col: '#ff9f0a'};
  return {text: '산행 참고: 매우 강함 (능선 이동 위험)', col: '#ff453a'};
}

function wxDesc(c) {
  if (c === 0) return '맑음';
  if (c === 1) return '대체로 맑음';
  if (c === 2) return '구름 조금';
  if (c === 3) return '흐림';
  if (c === 45 || c === 48) return '안개';
  if (c >= 51 && c <= 55) return '이슬비';
  if (c === 56 || c === 57) return '어는 이슬비';
  if (c === 61) return '약한 비';
  if (c === 63) return '비';
  if (c === 65) return '강한 비';
  if (c === 66 || c === 67) return '어는 비';
  if (c === 71) return '약한 눈';
  if (c === 73) return '눈';
  if (c === 75) return '폭설';
  if (c === 77) return '싸락눈';
  if (c >= 80 && c <= 82) return '소나기';
  if (c === 85 || c === 86) return '소낙눈';
  if (c === 95) return '뇌우';
  if (c >= 96) return '우박 동반 뇌우';
  return '';
}

function wxEmoji(c) {
  if (c === 0 || c === 1) return '☀️';
  if (c === 2) return '🌤️';
  if (c === 3) return '☁️';
  if (c === 45 || c === 48) return '🌫️';
  if (c >= 51 && c <= 57) return '🌦️';
  if ((c >= 61 && c <= 67) || (c >= 80 && c <= 82)) return '🌧️';
  if ((c >= 71 && c <= 77) || c === 85 || c === 86) return '🌨️';
  if (c >= 95) return '⛈️';
  return '·';
}

function hasWind(x) {
  return !!x && x.wind !== null && x.wind !== undefined && x.wdir !== null && x.wdir !== undefined;
}

// 화살표는 '바람이 불어가는 방향'. 지도가 회전해 있으면 그만큼 더해 화면 기준으로 표시한다.
function updateWindArrow() {
  var el = document.getElementById('wind-arrow');
  if (!el || !hasWind(wxExtra)) return;
  var target = ((wxExtra.wdir + 180) % 360) + mapCW();
  if (windAng === null) windAng = target;
  else windAng += (((target - windAng) % 360) + 540) % 360 - 180;     // 한 바퀴 도는 현상 방지
  el.style.transform = 'rotate(' + windAng.toFixed(1) + 'deg)';
}

function setWxExtra(extra, stale) {
  wxExtra = extra || null;
  var box = document.getElementById('wind-box');
  if (!box) return;
  if (!hasWind(wxExtra)) {
    box.style.display = 'none';
    if (wxDetailOpen) closeWxDetail();
    return;
  }
  var sp = document.getElementById('wind-speed');
  sp.innerText = Number(wxExtra.wind).toFixed(1);
  sp.style.color = windColor(wxExtra.wind);
  var wa = document.getElementById('wind-arrow');
  var wp = wa ? wa.querySelector('polygon') : null;
  if (wp) {
    var wc = windArrowColor(Number(wxExtra.wind));
    wp.setAttribute('fill', wc);
    wp.setAttribute('stroke', wc);
  }
  box.style.display = 'flex';
  box.style.opacity = stale ? '0.55' : '1';
  box.title = '바람 ' + windDirName(wxExtra.wdir) + ' ' + Number(wxExtra.wind).toFixed(1) + 'm/s (눌러서 상세 정보)';
  updateWindArrow();
  if (wxDetailOpen) renderWxDetail();
}

// 갱신 주기를 기다리지 않고 지금 바로 날씨를 다시 받는다
//  - 지도 중심 날씨를 보고 있으면 지도 중심 기준, 아니면 현재 위치 기준(파이썬에 요청)
function refreshWeatherNow() {
  if (wxCenterMode) {
    var c = map.getCenter();
    fetchWeatherAt(c.lat, c.lng);
  } else {
    try {
      fetch('http://127.0.0.1:' + PORT + '/wxnow?_=' + Date.now()).catch(function() {});
    } catch (err) {}
  }
}

function onWindClick(e) {
  if (e) { e.preventDefault(); e.stopPropagation(); }
  var now = Date.now();
  if (now - lastWindClick < 300) return;
  lastWindClick = now;
  refreshWeatherNow();              // 아이콘을 누르면 즉시 갱신
  if (!hasWind(wxExtra)) return;
  wxDetailOpen = true;
  document.getElementById('wx-detail').classList.add('show');
  renderWxDetail();
}

function closeWxDetail(e) {
  if (e) { e.preventDefault(); e.stopPropagation(); }
  wxDetailOpen = false;
  var p = document.getElementById('wx-detail');
  if (p) p.classList.remove('show');
}

function smallArrow(dir, R, ms) {
  var ang = ((dir + 180) % 360) + R;
  return '<svg class="hw-arrow" data-dir="' + dir + '" width="14" height="14" viewBox="0 0 28 28" '
       + 'style="vertical-align:middle;transform:rotate(' + ang.toFixed(1) + 'deg)">'
       + '<polygon points="14,3 24,24 14,18 4,24" fill="' + windArrowColor(Number(ms)) + '"/></svg>';
}

// 방위 원판: 지도가 회전한 만큼 N/E/S/W 위치를 돌리고, 위쪽 흰 삼각형은 '지도 위쪽'
function roseSvg(x, R) {
  var c = 75, i, rad;
  var s = '<svg width="150" height="150" viewBox="0 0 150 150">';
  s += '<circle cx="75" cy="75" r="58" fill="rgba(255,255,255,0.04)" stroke="rgba(255,255,255,0.28)" stroke-width="1.5"/>';
  for (i = 0; i < 360; i += 30) {
    rad = (i + R) * Math.PI / 180;
    s += '<line x1="' + (c + 58 * Math.sin(rad)).toFixed(1) + '" y1="' + (c - 58 * Math.cos(rad)).toFixed(1)
       + '" x2="' + (c + 52 * Math.sin(rad)).toFixed(1) + '" y2="' + (c - 52 * Math.cos(rad)).toFixed(1)
       + '" stroke="rgba(255,255,255,0.45)" stroke-width="1.5"/>';
  }
  var L = [[0, 'N'], [90, 'E'], [180, 'S'], [270, 'W']];
  for (i = 0; i < L.length; i++) {
    rad = (L[i][0] + R) * Math.PI / 180;
    s += '<text x="' + (c + 43 * Math.sin(rad)).toFixed(1) + '" y="' + (c - 43 * Math.cos(rad) + 4.5).toFixed(1)
       + '" font-size="13" font-weight="800" text-anchor="middle" fill="' + (L[i][1] === 'N' ? '#ff453a' : '#d1d1d6') + '">'
       + L[i][1] + '</text>';
  }
  s += '<polygon points="69,1 81,1 75,10" fill="#ffffff"/>';
  var ang = ((x.wdir + 180) % 360) + R;
  s += '<g transform="rotate(' + ang.toFixed(1) + ' 75 75)">'
     + '<polygon points="75,26 92,94 75,82 58,94" fill="' + windArrowColor(Number(x.wind)) + '" stroke="#ffffff" stroke-width="1" stroke-linejoin="round"/></g>';
  return s + '</svg>';
}

function updateWxRose() {
  if (!wxDetailOpen || !hasWind(wxExtra)) return;
  var el = document.getElementById('wd-rose');
  if (el) el.innerHTML = roseSvg(wxExtra, mapCW());
  var arrows = document.getElementsByClassName('hw-arrow');
  for (var i = 0; i < arrows.length; i++) {
    var d = parseFloat(arrows[i].getAttribute('data-dir'));
    arrows[i].style.transform = 'rotate(' + (((d + 180) % 360) + mapCW()).toFixed(1) + 'deg)';
  }
}

function wstat(k, v, sub) {
  return '<div class="wd-stat"><div class="k">' + k + '</div><div class="v">' + v + '</div>'
       + (sub ? '<div class="s">' + sub + '</div>' : '') + '</div>';
}

function nz(v) { return v !== null && v !== undefined; }

function renderWxDetail() {
  var x = wxExtra, body = document.getElementById('wd-body');
  if (!x || !body || !hasWind(x)) return;
  var R = mapCW();
  var age = x.ts ? Math.max(0, Math.round((Date.now() / 1000 - x.ts) / 60)) : null;
  var bf = beaufort(x.wind), hint = windHint(x.wind);
  var h = '<div class="wd-sub">' + (x.src || '') + (nz(x.lat) ? ' · ' + Number(x.lat).toFixed(3) + ', ' + Number(x.lon).toFixed(3) : '')
        + (age !== null ? ' · ' + age + '분 전' : '') + '</div>';
  h += '<div class="wd-rose" id="wd-rose">' + roseSvg(x, R) + '</div>';
  h += '<div class="wd-legend">화살표 = 바람이 불어가는 방향 · 흰 삼각형 = 지도 위쪽 (지도 회전 반영)</div>';
  h += '<div class="wd-hint" style="color:' + hint.col + ';">' + hint.text + '</div>';
  h += '<div class="wd-grid">';
  h += wstat('풍속', Number(x.wind).toFixed(1) + ' m/s', Math.round(x.wind * 3.6) + ' km/h');
  h += wstat('풍향', windDirName(x.wdir), Math.round(x.wdir) + '° 에서 불어옴');
  h += wstat('돌풍', nz(x.gust) ? Number(x.gust).toFixed(1) + ' m/s' : '-');
  h += wstat('풍속 단계', bf.name, 'Lv ' + bf.lv + ' / 12');
  h += wstat('기온', nz(x.t) ? Math.round(x.t) + '°' : '-', wxDesc(x.code));
  h += wstat('체감온도', nz(x.feels) ? Math.round(x.feels) + '°' : '-');
  h += wstat('습도', nz(x.hum) ? Math.round(x.hum) + '%' : '-');
  h += wstat('강수량', nz(x.precip) ? Number(x.precip).toFixed(1) + ' mm' : '-');
  h += wstat('기압', nz(x.pressure) ? Math.round(x.pressure) + ' hPa' : '-');
  h += wstat('구름', nz(x.cloud) ? Math.round(x.cloud) + '%' : '-');
  h += wstat('미세먼지', nz(x.pm10) ? Math.round(x.pm10) : '-', getDustInfo(x.pm10).text);
  h += wstat('초미세먼지', nz(x.pm25) ? Math.round(x.pm25) : '-');
  h += '</div>';
  var hr = x.hourly || [];
  if (hr.length) {
    h += '<div class="wd-h">시간별 예보 (바람 화살표는 지도 방향 기준)</div>';
    h += '<table class="wd-hours"><tr><th>시각</th><th></th><th>기온</th><th>강수</th><th>바람 m/s</th></tr>';
    for (var i = 0; i < hr.length; i++) {
      var r = hr[i];
      h += '<tr><td>' + r[0] + '시</td><td>' + wxEmoji(r[3]) + '</td>'
         + '<td>' + (nz(r[1]) ? Math.round(r[1]) + '°' : '-') + '</td>'
         + '<td>' + (nz(r[2]) ? r[2] + '%' : '-') + '</td>'
         + '<td>' + ((nz(r[4]) && nz(r[5])) ? smallArrow(r[5], R, r[4]) + ' ' + Number(r[4]).toFixed(1) : '-') + '</td></tr>';
    }
    h += '</table>';
  }
  body.innerHTML = h;
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
           + '<div>거리 ' + distKm.toFixed(1) + ' km</div>'
           + (hasEle ? '<div>상승 +' + gain + ' m</div>' : '<div style="color:#8e8e93;">고도 정보 없음</div>')
           + '<div>예상 ' + hours + '</div>';
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

function clearTrackLine() {
  routeCase.setLatLngs([]);
  routeLine.setLatLngs([]);          // 시작 버튼으로 기록한 경로선(주황)
}

function clearGpxRoute() {
  gpxLine.setLatLngs([]);
  setGpxData([]);
  setElevDetail(null);
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
</script>"""

WX_UA = 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) Trekker/4.36'

def _wx_get_json(url, label, tries, timeout, deadline):
    """JSON GET. 실패하면 재시도(지수 백오프). 시도마다 소요시간·HTTP 상태·오류를 날씨 로그에 남긴다."""
    last_err = ''
    for n in range(1, tries + 1):
        remain = deadline - time.time()
        if remain < 2:
            last_err = last_err or '시간 한도 초과'
            wlog('%s 중단: 남은 시간 부족 (%s)' % (label, last_err))
            break
        t0 = time.time()
        try:
            req = urllib.request.Request(url, headers={'User-Agent': WX_UA, 'Accept': 'application/json'})
            with urllib.request.urlopen(req, timeout=min(timeout, remain)) as resp:
                status = resp.status
                raw = resp.read()
            try:
                data = json.loads(raw.decode('utf-8'))
            except ValueError:
                snippet = raw[:80].decode('utf-8', 'replace').replace('\n', ' ')
                raise ValueError('JSON이 아닌 응답 (와이파이 로그인 페이지/차단?): %s' % snippet)
            ilog('%s 응답 성공 (%d/%d) HTTP %s %.2f초 %dB' % (label, n, tries, status, time.time() - t0, len(raw)))
            return data
        except urllib.error.HTTPError as e:
            body = ''
            try:
                body = e.read().decode('utf-8', 'replace')[:100].replace('\n', ' ')
            except Exception:
                pass
            last_err = 'HTTP %s %s' % (e.code, body)
            wlog('%s 실패 (%d/%d) %s %.2f초' % (label, n, tries, last_err, time.time() - t0))
            if e.code in (400, 404):
                break                                   # 요청 자체가 잘못됨: 재시도해도 소용없음
            if e.code == 429:                           # 요청 제한: 서버가 알려준 시간만큼 대기
                try:
                    time.sleep(min(float(e.headers.get('Retry-After', '5')), 10.0))
                except Exception:
                    time.sleep(5)
        except Exception as e:
            last_err = '%s: %s' % (type(e).__name__, e)
            wlog('%s 실패 (%d/%d) %s %.2f초' % (label, n, tries, last_err, time.time() - t0))
        if n < tries:
            time.sleep(0.8 * (2 ** (n - 1)))
    raise RuntimeError('%s: %s' % (label, last_err or '알 수 없는 오류'))

WX_CUR_FULL = ('temperature_2m,relative_humidity_2m,apparent_temperature,is_day,precipitation,weather_code,'
               'cloud_cover,pressure_msl,wind_speed_10m,wind_direction_10m,wind_gusts_10m')
WX_CUR_BASIC = 'temperature_2m,weather_code,is_day,wind_speed_10m,wind_direction_10m,wind_gusts_10m'
WX_HOURLY = 'temperature_2m,precipitation_probability,weather_code,wind_speed_10m,wind_direction_10m'

def _wx_hourly(data, n=12):
    """시간별 예보 -> [[시(문자열), 기온, 강수확률, 날씨코드, 풍속, 풍향], ...] (최대 n개)"""
    hr = data.get('hourly') or {}
    times = hr.get('time') or []
    out = []
    for i, tm in enumerate(times[:n]):
        def g(k, i=i):
            arr = hr.get(k) or []
            return arr[i] if i < len(arr) else None
        out.append([tm[11:13] if len(tm) >= 13 else '', g('temperature_2m'), g('precipitation_probability'),
                    g('weather_code'), g('wind_speed_10m'), g('wind_direction_10m')])
    return out

def fetch_weather(lat, lon, source='GPS', tries=WX_TRIES, timeout=WX_TIMEOUT, budget=WX_BUDGET):
    """날씨 딕셔너리(t, code, is_day, pm10, pm25, wind, wdir, gust, feels, hum, precip, pressure, cloud, hourly).
    실패하면 예외. 풍속 단위는 m/s. 모든 과정을 날씨 로그에 남긴다."""
    t_all = time.time()
    deadline = t_all + budget
    ilog('조회 시작 [%s] %.4f, %.4f' % (source, lat, lon))
    aq = {}

    def aq_worker():
        try:
            aq_url = ('https://air-quality-api.open-meteo.com/v1/air-quality?latitude=%.4f&longitude=%.4f'
                      '&current=pm10,pm2_5' % (lat, lon))
            d = _wx_get_json(aq_url, '미세먼지', 2, 6, deadline)
            cur_aq = d.get('current') or {}
            aq['pm10'] = cur_aq.get('pm10')
            aq['pm25'] = cur_aq.get('pm2_5')
        except Exception as e:
            aq['err'] = str(e)

    th = threading.Thread(target=aq_worker, daemon=True)
    th.start()
    try:
        base = ('https://api.open-meteo.com/v1/forecast?latitude=%.4f&longitude=%.4f'
                '&timezone=auto&wind_speed_unit=ms' % (lat, lon))
        cur, hourly = None, []
        # 1) 전체 정보(현재 + 시간별) -> 2) 간단 정보 -> 3) 예전 형식(current_weather) 순서로 시도
        plans = [
            ('날씨', base + '&current=' + WX_CUR_FULL + '&hourly=' + WX_HOURLY + '&forecast_hours=12', tries),
            ('날씨(간단)', base + '&current=' + WX_CUR_BASIC, 2),
        ]
        for label, url, tr in plans:
            try:
                data = _wx_get_json(url, label, tr, timeout, deadline)
                c = data.get('current') or {}
                if c.get('temperature_2m') is None:
                    raise ValueError('응답에 기온이 없음: %s' % str(data)[:120])
                cur = c
                hourly = _wx_hourly(data)
                break
            except Exception as e:
                wlog('%s 방식 실패 -> 다음 방식 시도: %s' % (label, e))
        if cur is None:
            data = _wx_get_json(base + '&current_weather=true', '날씨(대체)', 2, timeout, deadline)
            cw = data.get('current_weather') or {}
            if cw.get('temperature') is None:
                raise ValueError('대체 응답에도 기온이 없음: %s' % str(data)[:120])
            cur = {'temperature_2m': cw['temperature'], 'weather_code': cw.get('weathercode', 0),
                   'is_day': cw.get('is_day', 1), 'wind_speed_10m': cw.get('windspeed'),
                   'wind_direction_10m': cw.get('winddirection')}
        th.join(timeout=max(0.1, min(7.0, deadline - time.time())))
        pm10, pm25 = aq.get('pm10'), aq.get('pm25')
        if pm10 is None:
            wlog('미세먼지 값 없음 (%s) -> 화면에는 "미세"로 표시' % (aq.get('err') or '응답에 pm10 없음/지연'))
        res = {
            't': float(cur['temperature_2m']),
            'code': int(cur.get('weather_code') or 0),
            'is_day': int(cur.get('is_day', 1)) == 1,
            'pm10': pm10, 'pm25': pm25,
            'wind': cur.get('wind_speed_10m'), 'wdir': cur.get('wind_direction_10m'),
            'gust': cur.get('wind_gusts_10m'), 'feels': cur.get('apparent_temperature'),
            'hum': cur.get('relative_humidity_2m'), 'precip': cur.get('precipitation'),
            'pressure': cur.get('pressure_msl'), 'cloud': cur.get('cloud_cover'),
            'hourly': hourly,
        }
        ilog('결과 성공 [%s] 기온 %.1f도 코드 %d %s 바람 %s m/s %s° 미세먼지 %s / 시간별 %d개 / 총 %.2f초' % (
            source, res['t'], res['code'], '낮' if res['is_day'] else '밤', res['wind'], res['wdir'], pm10,
            len(hourly), time.time() - t_all))
        return res
    except Exception as e:
        wlog('결과 실패 [%s] %s / 총 %.2f초' % (source, e, time.time() - t_all))
        raise

def fetch_elevation(lat, lon):
    if app_instance is not None and getattr(app_instance, 'sim_active', False):
        return None                     # 시뮬레이션 중에는 GPX 고도를 쓰므로 인터넷 조회 생략
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

ADDR_CACHE = {}
ADDR_LOCK = threading.Lock()
ADDR_SEM = threading.BoundedSemaphore(2)
ADDR_STATE = {'last': 0.0}

def _nominatim_ko(data):
    """Nominatim 응답을 '시도 시군구 동 도로 번지' 순서의 한국어 주소로 조립"""
    a = data.get('address') or {}
    parts = []
    for k in ('state', 'province', 'city', 'county', 'borough', 'city_district', 'suburb',
              'quarter', 'village', 'town', 'neighbourhood', 'road', 'house_number'):
        v = str(a.get(k) or '').strip()
        if v and v not in parts:
            parts.append(v)
    if parts:
        return ' '.join(parts)
    return str(data.get('display_name') or '').strip()

def fetch_address(lat, lon):
    """좌표 -> 주소. VWorld 키가 있으면 국토부 주소(도로명 우선, 없으면 지번), 없거나 실패하면 OpenStreetMap."""
    key = (round(lat, 4), round(lon, 4))            # 약 11m 단위로 캐시
    if key in ADDR_CACHE:
        return ADDR_CACHE[key]
    addr = None
    ua = 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) Trekker/4.52'
    try:
        if VWORLD_KEY:
            url = ('https://api.vworld.kr/req/address?service=address&request=getAddress&version=2.0'
                   '&crs=epsg:4326&point=%.6f,%.6f&type=BOTH&zipcode=false&simple=false&format=json&key=%s'
                   % (lon, lat, VWORLD_KEY))
            req = urllib.request.Request(url, headers={'User-Agent': ua})
            with urllib.request.urlopen(req, timeout=5) as resp:
                data = json.loads(resp.read().decode('utf-8'))
            r = data.get('response') or {}
            if r.get('status') == 'OK':
                items = r.get('result') or []
                road = next((i.get('text') for i in items if i.get('type') == 'road' and i.get('text')), None)
                parcel = next((i.get('text') for i in items if i.get('type') == 'parcel' and i.get('text')), None)
                addr = road or parcel
        if not addr:
            with ADDR_LOCK:                          # OpenStreetMap 은 초당 1회 이하로만 요청
                wait = 1.1 - (time.time() - ADDR_STATE['last'])
                if wait > 0:
                    time.sleep(wait)
                ADDR_STATE['last'] = time.time()
            url = ('https://nominatim.openstreetmap.org/reverse?format=jsonv2&zoom=18&addressdetails=1'
                   '&accept-language=ko&lat=%.6f&lon=%.6f' % (lat, lon))
            req = urllib.request.Request(url, headers={'User-Agent': ua, 'Accept': 'application/json'})
            with urllib.request.urlopen(req, timeout=5) as resp:
                addr = _nominatim_ko(json.loads(resp.read().decode('utf-8')))
    except Exception:
        addr = None
    if addr:
        if len(ADDR_CACHE) > 300:
            ADDR_CACHE.clear()
        ADDR_CACHE[key] = addr
    return addr or None

TILE_LAYERS = {'opentopo': 'png', 'esri': 'jpg', 'cyclosm': 'png', 'vworld_base': 'png', 'vworld_sat': 'jpeg'}
PREFETCH_LAYER_MAXZ = {'opentopo': 17, 'esri': 19, 'cyclosm': 20, 'vworld_base': 19, 'vworld_sat': 19}
TILE_AVG_KB = {'opentopo': 25, 'esri': 30, 'cyclosm': 20, 'vworld_base': 20, 'vworld_sat': 35}
LAYER_NAMES = {'opentopo': 'Topo', 'esri': 'Esri 위성', 'cyclosm': 'CyclOSM',
               'vworld_base': '국토부 일반', 'vworld_sat': '국토부 위성'}
NET_STATE = {'fail_until': 0.0}
TILE_STATS = {'miss': 0}    # 네트워크 일시 실패로 빈/대체 타일을 보낸 횟수 (복구되면 지도 타일을 다시 요청)
NET_SEM = threading.Semaphore(6)
TILE_REQ_SEM = threading.BoundedSemaphore(12)   # 동시에 처리하는 타일 요청 수 (빠른 회전 때 요청 폭주 방지)

def _make_png(r, g, b, a=255):
    def chunk(t, d):
        return struct.pack('>I', len(d)) + t + d + struct.pack('>I', zlib.crc32(t + d) & 0xffffffff)
    raw = b'\x00' + bytes([r, g, b, a])
    return (b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', struct.pack('>IIBBBBB', 1, 1, 8, 6, 0, 0, 0))
            + chunk(b'IDAT', zlib.compress(raw)) + chunk(b'IEND', b''))

BLANK_TILE = _make_png(217, 217, 217)

def canon_layer(layer_id):
    return 'opentopo' if layer_id == 'opentopo_online' else layer_id

def tile_cache_path(layer_id, z, x, y):
    ext = TILE_LAYERS.get(layer_id, 'png')
    return os.path.join(TILE_CACHE_DIR, layer_id, str(z), str(x), '%s.%s' % (y, ext))

def tile_ctype(layer_id):
    return 'image/jpeg' if TILE_LAYERS.get(layer_id, 'png') in ('jpg', 'jpeg') else 'image/png'

def vworld_hint_html():
    if CONFIG_INFO['error']:
        why = '설정 파일을 읽지 못함 - ' + CONFIG_INFO['error']
    elif not CONFIG_INFO['path']:
        return ''                       # 설정 파일이 없는 것은 정상(VWorld를 안 쓰는 경우)이므로 안내하지 않음
    else:
        why = '%s 에 vworld_key 항목이 없거나 비어 있음' % os.path.basename(CONFIG_INFO['path'])
    why = why.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    return '<div style="padding:6px 12px;font-size:11px;color:#8e8e93;">국토부 지도(VWorld) 키를 못 읽었어요: ' + why + '</div>'

def tile_remote_url(layer_id, z, x, y):
    if layer_id == 'opentopo':
        return 'https://tile.opentopomap.org/%s/%s/%s.png' % (z, x, y)
    if layer_id == 'esri':
        return 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/%s/%s/%s' % (z, y, x)
    if layer_id == 'cyclosm':
        return 'https://%s.tile-cyclosm.openstreetmap.fr/cyclosm/%s/%s/%s.png' % ('abc'[(x + y) % 3], z, x, y)
    if layer_id == 'vworld_base' and VWORLD_KEY:
        return 'https://api.vworld.kr/req/wmts/1.0.0/%s/Base/%s/%s/%s.png' % (VWORLD_KEY, z, y, x)
    if layer_id == 'vworld_sat' and VWORLD_KEY:
        return 'https://api.vworld.kr/req/wmts/1.0.0/%s/Satellite/%s/%s/%s.jpeg' % (VWORLD_KEY, z, y, x)
    return None

def is_valid_tile(data):
    if not data or len(data) < 64:
        return False
    if data[:8] == b'\x89PNG\r\n\x1a\n':
        return data[-12:-8] == b'\x00\x00\x00\x00' and data[-8:-4] == b'IEND'
    if data[:2] == b'\xff\xd8':
        return data[-2:] == b'\xff\xd9'
    return False

def tile_is_cached(layer_id, z, x, y):
    try:
        return os.path.getsize(tile_cache_path(layer_id, z, x, y)) >= 64
    except OSError:
        return False

def read_cached_tile(path):
    try:
        with open(path, 'rb') as f:
            data = f.read()
    except OSError:
        return None
    if not is_valid_tile(data):
        try:
            os.remove(path)
        except OSError:
            pass
        return None
    try:
        if time.time() - os.path.getmtime(path) > 3600:
            os.utime(path, None)
    except OSError:
        pass
    return data

def write_cached_tile(path, data):
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        tmp = '%s.tmp%d' % (path, threading.get_ident())
        with open(tmp, 'wb') as f:
            f.write(data)
        os.replace(tmp, path)
        return True
    except Exception as e:
        dlog("타일 저장 실패: %s" % e)
        return False

VWORLD_DIAG = {'msg': '', 'new': False, 'last': 0.0}

def vworld_diag(layer_id, text):
    """VWorld 타일 오류를 로그에 남기고 화면 상태 줄에 알린다 (60초에 한 번)."""
    if not str(layer_id).startswith('vworld'):
        return
    now = time.time()
    if now - VWORLD_DIAG['last'] < 60.0:
        return
    VWORLD_DIAG['last'] = now
    dlog("VWorld 타일 오류(%s): %s" % (layer_id, text))
    VWORLD_DIAG['msg'] = ('국토부 지도 오류: ' + text)[:46]
    VWORLD_DIAG['new'] = True

def fetch_tile_net(layer_id, z, x, y):
    """타일을 내려받는다. 반환: 이미지 데이터 / None(일시 실패 - 나중에 다시 시도) / False(서버에 타일이 없음 - 재시도 불필요)"""
    url = tile_remote_url(layer_id, z, x, y)
    if not url:
        return False
    if time.time() < NET_STATE['fail_until']:
        return None
    for _attempt in range(2):
        try:
            with NET_SEM:
                req = urllib.request.Request(
                    url, headers={'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) Trekker/4.36'})
                with urllib.request.urlopen(req, timeout=TILE_NET_TIMEOUT) as resp:
                    data = resp.read()
            if is_valid_tile(data):
                return data
            if str(layer_id).startswith('vworld'):
                vworld_diag(layer_id, '응답 이상 %r' % (data[:60],))
                if data[:1] in (b'<', b'{'):    # 오류 안내문(XML/JSON)이면 다시 시도해도 같음
                    return False
            return None
        except urllib.error.HTTPError as e:
            if e.code in (400, 401, 403, 404):
                if e.code != 404:
                    vworld_diag(layer_id, 'HTTP %d (키·사용 설정 확인)' % e.code)
                return False
            time.sleep(0.4)
        except Exception:
            if _attempt == 0:
                time.sleep(0.5)         # 재접속: 한동안 안 쓰다 돌아오면 첫 연결이 실패하는 경우가 있어 한 번 더 시도
                continue
            NET_STATE['fail_until'] = time.time() + NET_FAIL_COOLDOWN
            return None
    return None

def make_overzoom_tile(layer_id, z, x, y):
    try:
        from PIL import Image
    except Exception:
        return None
    try:
        resample = getattr(Image, 'BICUBIC', None) or Image.Resampling.BICUBIC
        for k in range(1, OVERZOOM_LEVELS + 1):
            pz = z - k
            if pz < 0:
                break
            px, py = x >> k, y >> k
            data = read_cached_tile(tile_cache_path(layer_id, pz, px, py))
            if not data:
                continue
            img = Image.open(io.BytesIO(data))
            img.load()
            if img.mode not in ('RGB', 'RGBA'):
                img = img.convert('RGB')
            size = img.size[0]
            sub = size >> k
            if sub < 1:
                break
            ox, oy = (x - (px << k)) * sub, (y - (py << k)) * sub
            out = img.crop((ox, oy, ox + sub, oy + sub)).resize((size, size), resample)
            buf = io.BytesIO()
            if TILE_LAYERS.get(layer_id, 'png') in ('jpg', 'jpeg'):
                out.convert('RGB').save(buf, 'JPEG', quality=85)
            else:
                out.save(buf, 'PNG')
            return buf.getvalue()
    except Exception as e:
        dlog("대체 타일 생성 실패: %s" % e)
    return None

def get_tile(layer_id, z, x, y, allow_net=True):
    layer_id = canon_layer(layer_id)
    ctype = tile_ctype(layer_id)
    path = tile_cache_path(layer_id, z, x, y)
    data = read_cached_tile(path)
    if data:
        return data, ctype, True
    if allow_net:
        data = fetch_tile_net(layer_id, z, x, y)
        if data:
            write_cached_tile(path, data)
            return data, ctype, True
        if data is None:
            TILE_STATS['miss'] += 1     # 일시 실패: 연결이 복구되면 지도 타일을 다시 요청하도록 기록
    approx = make_overzoom_tile(layer_id, z, x, y)
    if approx:
        return approx, ctype, False
    return BLANK_TILE, 'image/png', False

def scan_tile_cache():
    files = []
    now = time.time()
    for root, _dirs, names in os.walk(TILE_CACHE_DIR):
        for n in names:
            fp = os.path.join(root, n)
            try:
                st = os.stat(fp)
            except OSError:
                continue
            if '.tmp' in n:
                if now - st.st_mtime > 3600:
                    try:
                        os.remove(fp)
                    except OSError:
                        pass
                continue
            files.append((st.st_mtime, st.st_size, fp))
    return files

def tile_cache_stats():
    files = scan_tile_cache()
    return len(files), sum(f[1] for f in files)

def trim_tile_cache(max_mb=None):
    limit = (max_mb or TILE_CACHE_MAX_MB) * 1024 * 1024
    files = scan_tile_cache()
    total = sum(f[1] for f in files)
    removed = 0
    if total > limit:
        files.sort()
        for _mt, sz, fp in files:
            if total <= limit * 0.9:
                break
            try:
                os.remove(fp)
                total -= sz
                removed += 1
            except OSError:
                pass
    return total, len(files) - removed, removed

def lonlat_to_tile(lat, lon, z):
    n = 2 ** z
    lr = math.radians(max(min(lat, 85.0511), -85.0511))
    x = int((lon + 180.0) / 360.0 * n)
    y = int((1.0 - math.log(math.tan(lr) + 1.0 / math.cos(lr)) / math.pi) / 2.0 * n)
    return max(0, min(n - 1, x)), max(0, min(n - 1, y))

def tiles_for_route(pts, z, ring=1):
    n = 2 ** z
    tiles = set()

    def add(lat, lon):
        tx, ty = lonlat_to_tile(lat, lon, z)
        for dx in range(-ring, ring + 1):
            for dy in range(-ring, ring + 1):
                xx, yy = tx + dx, ty + dy
                if 0 <= xx < n and 0 <= yy < n:
                    tiles.add((z, xx, yy))

    prev = None
    for lat, lon in pts:
        if prev is None:
            add(lat, lon)
        else:
            d = hav(prev[0], prev[1], lat, lon)
            tile_m = 40075016.0 * max(math.cos(math.radians(lat)), 0.05) / n
            steps = max(1, int(d / (tile_m / 2.0)))
            for i in range(1, steps + 1):
                t = i / float(steps)
                add(prev[0] + (lat - prev[0]) * t, prev[1] + (lon - prev[1]) * t)
        prev = (lat, lon)
    return tiles

def _cap_by_zoom(by_zoom):
    zs = sorted(by_zoom)
    while len(zs) > 1 and sum(len(by_zoom[z]) for z in zs) > PREFETCH_MAX_TILES:
        zs.pop()
    if not zs or len(by_zoom[zs[0]]) > PREFETCH_MAX_TILES:
        return [], (0, 0)
    tiles = []
    for z in zs:
        tiles.extend(sorted(by_zoom[z]))
    return tiles, (zs[0], zs[-1])

def plan_route_tiles(pts, layer_id):
    maxz = min(PREFETCH_MAX_ZOOM, PREFETCH_LAYER_MAXZ.get(layer_id, 17))
    by_zoom = {}
    for z in range(PREFETCH_MIN_ZOOM, maxz + 1):
        by_zoom[z] = list(tiles_for_route(pts, z))
    return _cap_by_zoom(by_zoom)

def plan_view_tiles(south, west, north, east, zoom, layer_id):
    maxz = min(PREFETCH_MAX_ZOOM, PREFETCH_LAYER_MAXZ.get(layer_id, 17))
    dlat, dlon = (north - south) * 0.25, (east - west) * 0.25
    s_, n_ = max(-85.0, south - dlat), min(85.0, north + dlat)
    w_, e_ = max(-180.0, west - dlon), min(180.0, east + dlon)
    z0 = int(round(zoom))
    zhi = min(maxz, z0 + 2)
    zlo = max(10, min(z0 - 2, zhi))
    by_zoom = {}
    for z in range(zlo, zhi + 1):
        x0, y0 = lonlat_to_tile(n_, w_, z)
        x1, y1 = lonlat_to_tile(s_, e_, z)
        if (x1 - x0 + 1) * (y1 - y0 + 1) > PREFETCH_MAX_TILES * 4:
            by_zoom[z] = [None] * (PREFETCH_MAX_TILES + 1)
        else:
            by_zoom[z] = [(z, x, y) for x in range(x0, x1 + 1) for y in range(y0, y1 + 1)]
    tiles, zr = _cap_by_zoom(by_zoom)
    return [t for t in tiles if t is not None], zr

class MapHandler(http.server.BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def _send(self, body, ctype, cache=True):
        try:
            data = body.encode('utf-8') if isinstance(body, str) else body
            self.send_response(200)
            self.send_header('Content-Type', ctype)
            self.send_header('Content-Length', str(len(data)))
            self.send_header('Cache-Control', 'max-age=86400' if cache else 'no-store')
            self.end_headers()
            self.wfile.write(data)
        except Exception:
            pass

    def do_GET(self):
        try:
            u = urllib.parse.urlparse(self.path)
            if u.path == '/':
                vworld_btns = '' if VWORLD_KEY else vworld_hint_html()
                if VWORLD_KEY:
                    vworld_btns = (
                        '<button class="layer-btn" id="btn-vworld_base" ontouchend="switchLayer(\'vworld_base\', \'국토부 일반\', this, event)" onclick="switchLayer(\'vworld_base\', \'국토부 일반\', this, event)"><span>국토부 (일반)</span><span class="badge">온라인</span></button>'
                        '<button class="layer-btn" id="btn-vworld_sat" ontouchend="switchLayer(\'vworld_sat\', \'국토부 위성\', this, event)" onclick="switchLayer(\'vworld_sat\', \'국토부 위성\', this, event)"><span>국토부 (위성)</span><span class="badge">온라인</span></button>'
                    )
                html = MAP_HTML.replace('__PORT__', str(SERVER_PORT))
                html = html.replace('__VWORLD_KEY__', VWORLD_KEY)
                html = html.replace('__VWORLD_BUTTONS__', vworld_btns)
                self._send(html, 'text/html; charset=utf-8', cache=False)
            elif u.path.startswith('/proxy/'):
                parts = u.path.split('/')
                served = False
                if len(parts) >= 6:
                    layer_id = canon_layer(parts[2])
                    z, x, y = parts[3], parts[4], parts[5].split('.')[0]
                    if layer_id in TILE_LAYERS and z.isdigit() and x.isdigit() and y.isdigit():
                        mode = urllib.parse.parse_qs(u.query).get('mode', ['net'])[0]
                        if TILE_REQ_SEM.acquire(timeout=10):
                            try:
                                data, ctype, cacheable = get_tile(layer_id, int(z), int(x), int(y), allow_net=(mode != 'cache'))
                            finally:
                                TILE_REQ_SEM.release()
                        else:
                            data, ctype, cacheable = BLANK_TILE, 'image/png', False
                        self._send(data, ctype, cache=cacheable)
                        served = True
                if not served:
                    self.send_error(404)
            elif u.path == '/wx':
                q = urllib.parse.parse_qs(u.query)
                try:
                    wlat = float(q.get('lat', ['0'])[0])
                    wlon = float(q.get('lon', ['0'])[0])
                    res = fetch_weather(wlat, wlon, '지도중심', tries=2, timeout=7, budget=18)
                    res['lat'], res['lon'], res['ts'] = wlat, wlon, time.time()
                    body = json.dumps({
                        'ok': True, 
                        't': res['t'], 
                        'code': res['code'], 
                        'is_day': 1 if res['is_day'] else 0,
                        'pm10': res['pm10'],
                        'extra': wx_extra(res, '지도 중심')
                    })
                except Exception as e:
                    threading.Thread(target=wx_diagnose, daemon=True).start()   # 실패 원인 점검(날씨 로그에 기록)
                    body = json.dumps({'ok': False, 'err': str(e)[:160]})
                self._send(body, 'application/json', cache=False)
            elif u.path == '/center_move':
                q = urllib.parse.parse_qs(u.query)
                try:
                    clat = float(q.get('lat', ['0'])[0])
                    clon = float(q.get('lon', ['0'])[0])
                    if app_instance is not None and getattr(app_instance, 'is_locked', False):
                        body = json.dumps({'ok': True, 'paused': True})      # 잠금 중에는 고도 조회 일시 정지
                    else:
                        ele = fetch_elevation(clat, clon)
                        if ele is not None and app_instance:
                            app_instance.center_elevation = ele
                        body = json.dumps({'ok': True})
                except Exception:
                    body = json.dumps({'ok': False})
                self._send(body, 'application/json', cache=False)
            elif u.path == '/addr':
                q = urllib.parse.parse_qs(u.query)
                try:
                    alat = float(q.get('lat', ['0'])[0])
                    alon = float(q.get('lon', ['0'])[0])
                    if app_instance is not None and getattr(app_instance, 'is_locked', False):
                        body = json.dumps({'ok': True, 'paused': True})          # 잠금 중에는 주소 조회 일시 정지
                    elif ADDR_SEM.acquire(blocking=False):
                        try:
                            a = fetch_address(alat, alon)
                        finally:
                            ADDR_SEM.release()
                        body = json.dumps({'ok': bool(a), 'addr': a or ''})
                    else:
                        body = json.dumps({'ok': False, 'busy': True})
                except Exception:
                    body = json.dumps({'ok': False})
                self._send(body, 'application/json', cache=False)
            elif u.path == '/wxnow':
                # 날씨/풍향 아이콘을 눌렀을 때: 갱신 주기를 기다리지 않고 바로 현재 위치 날씨를 다시 받음
                if app_instance is not None:
                    run_on_main(app_instance.force_weather_refresh)
                self._send('ok', 'text/plain', cache=False)
            elif u.path == '/up':
                q = urllib.parse.parse_qs(u.query)
                try:
                    up_d = float(q.get('d', ['0'])[0])
                    if app_instance is not None and not getattr(app_instance, 'is_locked', False):
                        app_instance.up_pending = up_d
                        if not getattr(app_instance, 'up_scheduled', False):
                            app_instance.up_scheduled = True
                            run_on_main(app_instance.apply_up_dir)
                except Exception:
                    pass
                self._send('ok', 'text/plain', cache=False)
            elif u.path == '/hmode':
                q = urllib.parse.parse_qs(u.query)
                HEADING_STATE['on'] = (q.get('on', ['0'])[0] == '1')
                self._send('ok', 'text/plain', cache=False)
            else:
                self.send_error(404)
        except Exception:
            pass

class SafeHTTPServer(http.server.ThreadingHTTPServer):
    allow_reuse_address = True
    daemon_threads = True

    def server_bind(self):
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        super().server_bind()

    @staticmethod
    def _unwrap(request):
        while isinstance(request, tuple):
            request = request[0] if request else None
        return request

    def get_request(self):
        request, client_address = super().get_request()
        return self._unwrap(request), client_address

    def finish_request(self, request, client_address):
        request = self._unwrap(request)
        if request is None:
            return
        super().finish_request(request, client_address)

    def shutdown_request(self, request):
        request = self._unwrap(request)
        if request is None:
            return
        try:
            super().shutdown_request(request)
        except Exception:
            pass

    def close_request(self, request):
        request = self._unwrap(request)
        if request is None:
            return
        try:
            super().close_request(request)
        except Exception:
            pass

    def handle_error(self, request, client_address):
        try:
            import traceback
            last = traceback.format_exc().strip().splitlines()[-1]
            dlog("HTTP 요청 처리 오류 %s: %s" % (client_address, last))
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
    ilog("GPX 파일 저장됨: %s" % path)

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
        ilog("GPX 파일 로드 성공: %s (%d개 포인트)" % (path, len(pts)))
        return pts, eles
    except Exception as e:
        dlog("GPX 파일 읽기 오류: %s" % e)
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

def _interp_elev(pts, eles):
    N = len(pts)
    valid_idx = [i for i, z in enumerate(eles) if z is not None]
    if N < 2 or len(valid_idx) < max(2, N * 0.5):
        return None

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
    return cum, ys

def _resample_smooth(cum, ys, n, win=1):
    N = len(cum)
    if N > n:
        idx = [int(round(k * (N - 1) / float(n - 1))) for k in range(n)]
    else:
        idx = list(range(N))
    xs = [cum[i] for i in idx]
    zs = [ys[i] for i in idx]
    sm = []
    for k in range(len(zs)):
        lo, hi = max(0, k - win), min(len(zs), k + win + 1)
        sm.append(sum(zs[lo:hi]) / (hi - lo))
    return xs, sm

def build_elev_profile(pts, eles, n=120):
    r = _interp_elev(pts, eles)
    if r is None:
        return []
    cum, ys = r
    xs, sm = _resample_smooth(cum, ys, n, 1)
    return [[round(x), round(z, 1)] for x, z in zip(xs, sm)]

def _lin_at(cum, ys, d):
    if d <= cum[0]:
        return ys[0]
    if d >= cum[-1]:
        return ys[-1]
    lo, hi = 0, len(cum) - 1
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if cum[mid] <= d:
            lo = mid
        else:
            hi = mid
    span = cum[hi] - cum[lo]
    t = (d - cum[lo]) / span if span > 0 else 0.0
    return ys[lo] + (ys[hi] - ys[lo]) * t

def _gain_loss(seq):
    gain = loss = 0.0
    ref = None
    for z in seq:
        if ref is None:
            ref = z
        elif abs(z - ref) >= ALT_THRESHOLD:
            if z > ref:
                gain += z - ref
            else:
                loss += ref - z
            ref = z
    return gain, loss

def build_elev_detail(pts, eles, name, st):
    r = _interp_elev(pts, eles)
    if r is None:
        return None
    cum, ys = r
    total = cum[-1]
    if total <= 0:
        return None

    xs, sm = _resample_smooth(cum, ys, 300, 2)

    if total >= 5000:
        step = 1000.0
    elif total >= 2000:
        step = 500.0
    else:
        step = 250.0
    bounds = [0.0]
    while bounds[-1] + step < total - 1e-6:
        bounds.append(bounds[-1] + step)
    bounds.append(total)
    if len(bounds) > 2 and (bounds[-1] - bounds[-2]) < step * 0.2:
        bounds.pop(-2)

    splits = []
    for a, b in zip(bounds, bounds[1:]):
        seq = [_lin_at(cum, ys, a)]
        seq += [ys[i] for i in range(len(cum)) if a < cum[i] < b]
        seq.append(_lin_at(cum, ys, b))
        g, l = _gain_loss(seq)
        grade = (seq[-1] - seq[0]) / (b - a) * 100.0
        splits.append([round(a), round(b), round(g), round(l), round(grade, 1), round(seq[-1])])

    mx = st.get('max_alt') if st.get('max_alt') is not None else max(ys)
    mn = st.get('min_alt') if st.get('min_alt') is not None else min(ys)
    return {
        'name': name,
        'dist': round(total),
        'gain': round(st['gain']),
        'loss': round(st['loss']),
        'max': round(mx),
        'min': round(mn),
        'start': round(ys[0]),
        'end': round(ys[-1]),
        'prof': [[round(x), round(z, 1)] for x, z in zip(xs, sm)],
        'splits': splits,
    }

def rate_difficulty(dist_m, gain_m):
    effort = dist_m / 1000.0 + gain_m / 100.0
    if effort < 6:
        lv, label = 1, '쉬움'
    elif effort < 12:
        lv, label = 2, '보통'
    elif effort < 18:
        lv, label = 3, '약간 어려움'
    elif effort < 26:
        lv, label = 4, '어려움'
    else:
        lv, label = 5, '매우 어려움'
    stars = '★' * lv + '☆' * (5 - lv)
    hours = effort / 4.5
    return stars, label, effort, hours

def fmt_hours(hours):
    total_min = int(round(hours * 60 / 5.0) * 5)
    h, m = total_min // 60, total_min % 60
    if h and m:
        return '%d시간 %d분' % (h, m)
    if h:
        return '%d시간' % h
    return '%d분' % m

class Tracker:
    def __init__(self):
        self.clock_offset = 0.0         # 시뮬레이션 배속으로 앞당겨진 시간(초). 평소에는 0
        self.reset_track()
        self.gpx_route = []

    def now(self):
        return time.time() + self.clock_offset

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
        self.kf_lat = None
        self.kf_lon = None
        self.kf_var = 0.0
        self.kf_ts = 0.0
        self.kf_vn = 0.0
        self.kf_ve = 0.0
        self.jump_cnt = 0
        self.jump_last = None
        self.last_meas = None

    def start(self):
        self.reset_track()
        self.start_ts = self.now()
        self.seg_start = self.start_ts
        self.state = 'recording'
        ilog("트래킹 시작됨")

    def pause(self):
        if self.seg_start:
            self.elapsed += self.now() - self.seg_start
        self.seg_start = None
        self.state = 'paused'
        ilog("트래킹 일시정지")

    def resume(self):
        self.seg_start = self.now()
        self.state = 'recording'
        ilog("트래킹 재개")

    def stop(self):
        if self.state == 'recording' and self.seg_start:
            self.elapsed += self.now() - self.seg_start
        self.seg_start = None
        self.state = 'idle'
        ilog("트래킹 종료")

    def total_elapsed(self):
        e = self.elapsed
        if self.state == 'recording' and self.seg_start:
            e += self.now() - self.seg_start
        return e

    def _kf_reset(self, lat, lon, acc, now):
        self.kf_lat, self.kf_lon = lat, lon
        self.kf_var = acc * acc
        self.kf_ts = now
        self.kf_vn = self.kf_ve = 0.0
        self.jump_cnt = 0
        self.jump_last = None

    def _kf_update(self, lat, lon, acc, now):
        if self.kf_lat is None:
            self._kf_reset(lat, lon, acc, now)
            return True

        dt = max(now - self.kf_ts, 0.0)
        old_lat, old_lon = self.kf_lat, self.kf_lon
        m_lat = 111320.0
        m_lon = 111320.0 * math.cos(math.radians(old_lat))

        d_prev = hav(old_lat, old_lon, lat, lon)
        spike = d_prev > FAST_SPEED_MPS * max(dt, 1.0) + acc * 0.5
        if spike:
            if self.jump_last is not None and hav(self.jump_last[0], self.jump_last[1], lat, lon) <= JUMP_LINK_M:
                self.jump_cnt += 1
            else:
                self.jump_cnt = 1
            self.jump_last = (lat, lon)
            if self.jump_cnt >= JUMP_CONFIRM:
                ilog("GPS 큰 이동 확정 (%.0fm), 필터 재시작" % d_prev)
                self._kf_reset(lat, lon, acc, now)
                return True
        else:
            self.jump_cnt = 0
            self.jump_last = None

        pdt = min(dt, 3.0)
        self.kf_lat += self.kf_vn * pdt / m_lat
        self.kf_lon += self.kf_ve * pdt / m_lon
        self.kf_var += dt * KF_PROCESS_NOISE * KF_PROCESS_NOISE

        k = self.kf_var / (self.kf_var + acc * acc)
        if spike:
            k = min(k, SPIKE_GAIN)
        self.kf_lat += k * (lat - self.kf_lat)
        self.kf_lon += k * (lon - self.kf_lon)
        self.kf_var = (1.0 - k) * self.kf_var
        self.kf_ts = now

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
        if self.state == 'recording' and self.kf_lat is not None and self.now() - self.kf_ts < 5.0:
            return self.kf_lat, self.kf_lon
        return lat, lon

    def _smooth_prev(self):
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
        now = self.now()
        acc = max(float(acc), 3.0)

        meas = (lat, lon, acc)
        if meas == self.last_meas:
            return False
        self.last_meas = meas

        if self.points and gps_speed is not None and 0 <= gps_speed < STILL_SPEED_MPS:
            return False

        if not self._kf_update(lat, lon, acc, now):
            return False
        flat, flon = self.kf_lat, self.kf_lon

        if self.points:
            q = self.points[-1]
            d = hav(q['lat'], q['lon'], flat, flon)
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
    SPAN = 120.0
    FADE = 0.30    # 양쪽 끝에서 폭의 이만큼(30%) 구간에 걸쳐 서서히 흐려짐 (0이면 흐림 없음)
    NAMES = {0: 'N', 45: 'NE', 90: 'E', 135: 'SE', 180: 'S', 225: 'SW', 270: 'W', 315: 'NW'}

    def __init__(self):
        self.background_color = (0, 0, 0, 0)
        self.touch_enabled = False
        self.up_dir = 0.0

    def set_dir(self, d):
        self.up_dir = float(d) % 360.0
        self.set_needs_display()

    def _fade(self, x, w):
        """좌우 끝으로 갈수록 0에 가까워지는 투명도 계수 (부드러운 그라데이션)"""
        if self.FADE <= 0:
            return 1.0
        f = min(x, w - x) / (w * self.FADE)
        if f >= 1.0:
            return 1.0
        if f <= 0.0:
            return 0.0
        return f * f * (3.0 - 2.0 * f)      # smoothstep

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
                fade = self._fade(x, w)
                if fade <= 0.02:
                    continue
                halo_f = (1, 1, 1, 0.9 * fade)
                if a % 45 == 0:
                    name = self.NAMES[a]
                    if name == 'N':
                        font, color = ('<System-Bold>', 16), (0.85, 0.1, 0.1, 1.0)
                    else:
                        font, color = ('<System-Bold>', 14), (0, 0, 0, 1.0)
                    color = (color[0], color[1], color[2], color[3] * fade)
                    tw, th = ui.measure_string(name, font=font)
                    y = (h - th) / 2.0
                    for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1), (-1, 1), (1, -1)):
                        ui.draw_string(name, rect=(x - 20 + dx, y + dy, 40, th), font=font,
                                       color=halo_f, alignment=ui.ALIGN_CENTER)
                    ui.draw_string(name, rect=(x - 20, y, 40, th), font=font,
                                   color=color, alignment=ui.ALIGN_CENTER)
                else:
                    if abs(((a + 22.5) % 45.0) - 22.5) < 6:
                        continue
                    major = (a % 15 == 0)
                    th = h * (0.42 if major else 0.28)
                    ty = (h - th) / 2.0
                    ui.set_color(halo_f)
                    ui.Path.rect(x - 1.5, ty - 1, 3, th + 2).fill()
                    ui.set_color((0, 0, 0, (1.0 if major else 0.8) * fade))
                    ui.Path.rect(x - 0.75, ty, 1.5, th).fill()

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
            dlog("방위 바 그리기 오류: %s" % e)

MENU_PREFETCH_ROUTE = '⬇️ 경로 주변 지도 미리받기'
MENU_PREFETCH_VIEW = '⬇️ 현재 화면 주변 지도 미리받기'
MENU_PREFETCH_CANCEL = '⏹ 지도 미리받기 취소'
MENU_CACHE_INFO = '🧹 지도 캐시 정보/정리'
MENU_WX_LOG = '🌦 날씨 로그 보기'

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
        self.server_thread = None
        self.server_fail_n = 0
        _APP_CLOSED['v'] = False
        self.pushed_pts_len = -1          # 마지막으로 지도에 보낸 기록 점 개수 (바뀐 경우에만 전체 경로 전송)

        self.heading_running = False
        self.has_h = False
        self.sm_sin = 0.0
        self.sm_cos = 0.0
        self.last_course = None
        self.last_course_ts = 0.0
        self.no_heading_warned = False
        self.track_heading = None
        self.track_heading_ts = 0.0
        self.last_live_beep = 0.0
        self.last_heartbeat = 0.0
        self._bg_ctx = None
        self.prefetching = False
        self.prefetch_cancel = False
        self.prefetch_text = ''
        self.last_map_refresh = 0.0     # 마지막으로 지도(내 위치·경로)를 갱신한 시각
        self.sim_active = False         # GPX 따라가기 시뮬레이션 진행 중
        self.sim_paused = False
        self.js_busy = False            # 주기 작업(tick/heading_tick)이 JS 응답을 기다리는 중 (겹쳐 실행 방지)
        self.sim_heading = None         # 시뮬레이션 진행 방향(도) - 나침반 모드에서 화면 위쪽이 되는 방향
        self.sim_hold = False           # 시뮬레이션이 끝난 뒤에도 마지막 거리·시간을 계속 보여 줌
        self.sim_mult = SIM_DEFAULT_SPEED
        self.sim_route = None
        self.sim_s = 0.0                # 경로를 따라 이동한 거리(m)
        self.sim_ts = 0.0
        self.sim_trav = 0.0             # 시뮬레이션으로 실제 이동한 누적 거리(m) - 점프·시작 위치와 무관하게 표시용
        self.sim_dir = 1                # 시뮬레이션 진행 방향 (1=정방향, -1=역방향)
        self.gpx_eles = []              # 불러온 GPX의 고도 (시뮬레이션 고도용)
        self.dev_ts = 0.0               # 마지막 경로 이탈 검사 시각 (기록 중 간격 조절용)
        self.dev_result = False
        self.up_pending = 0.0           # 서버가 받은 최신 위쪽 방향 (방위 바 갱신 요청을 합치기 위함)
        self.up_scheduled = False
        self.last_sent_h = None         # 마지막으로 지도에 보낸 회전 각도
        self.last_sent_ts = 0.0
        self.lock_heading_ts = 0.0      # 잠금 중 마지막 진행 방향 계산 시각
        self.locked_heading = None      # 잠금 중 계산해 둔 진행 방향 (지도 갱신 때 적용)

        self.wx_ts = 0                  # 마지막으로 '성공'한 시각
        self.wx_lat = None
        self.wx_lon = None
        self.wx_busy = False
        self.wx_started = 0.0           # 진행 중인 조회의 시작 시각 (멈춤 감시용)
        self.wx_gen = 0                 # 조회 세대 번호 (멈췄다가 늦게 끝난 옛 조회가 상태를 망치지 않게)
        self.wx_fail_count = 0          # 연속 실패 횟수
        self.wx_next_try = 0.0          # 이 시각 전에는 다시 조회하지 않음 (실패 후 대기)
        self.wx_last = None             # 마지막 날씨 값 (화면에 적용할 데이터)
        self.wx_applied = False         # wx_last 가 화면(JS)에 적용됐는지
        self.wx_verify_ts = 0.0
        self.wx_wait_log = 0.0
        self.wx_apply_log_ts = 0.0
        self.app_start_ts = time.time()
        _c = wx_cache_load()            # 저장된 마지막 날씨가 있으면 우선 흐리게 보여 주고 새로 조회
        if _c:
            self.wx_last = _c
            ilog('저장된 날씨 불러옴 (%d분 전, %.1f도)' % ((time.time() - float(_c['ts'])) / 60, _c['t']))

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
        self.btn_load = None            # '로드' 버튼 (시뮬레이션 중 비활성화)
        self.btn_reset = None           # '초기화' 버튼 (시뮬레이션 중 비활성화)
        
        for title, action in (('로드', self.on_gpx),
                              ('초기화', self.on_reset), ('시뮬', self.on_sim), ('잠금', self.on_toggle_lock)):
            b = ui.Button(title=title, font=('<System>', 19), tint_color='#0a84ff')
            b.action = action
            self.top_bar.add_subview(b)
            self.menu_buttons.append(b)
            _an = getattr(action, '__name__', '')
            if _an == 'on_gpx':
                self.btn_load = b
            elif _an == 'on_reset':
                self.btn_reset = b
            if title == '잠금':
                self.btn_lock = b
        self.update_title()

        self.stat_boxes = {}
        for key, title in (('dist', '거리'), ('time', '시간'), ('speed', '속도'), ('gain_ele', '고도')):
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

        self.compass_bar = CompassBar()
        self.add_subview(self.compass_bar)

        self.start_server()

        self.status = ui.Label(text='GPS 대기 중...', text_color='#8e8e93',
                               font=('<System>', 16), alignment=ui.ALIGN_CENTER)
        self.add_subview(self.status)

        self.btn_main = self._button('● 시작', '#30d158', self.on_main)
        self.btn_stop = self._button('■ 종료·저장', '#ff453a', self.on_stop)
        self.refresh_buttons()

        self.lock_view = ui.View(background_color=(0, 0, 0, 0.50))
        self.lock_box = ui.View(background_color=(0, 0, 0, 0.60), corner_radius=12)
        self.lock_label = ui.Label(text='🔒 화면이 잠겼습니다\n3번 빠르게 터치시 해제',
                                   text_color='white', font=('<System-Bold>', 16),
                                   alignment=ui.ALIGN_LEFT, number_of_lines=2)
        self.lock_box.add_subview(self.lock_label)
        self.lock_view.add_subview(self.lock_box)
        self.lock_view.hidden = True
        self.add_subview(self.lock_view)

        self.status_hold_until = 0.0     # 상태 줄 메시지 고정 해제 시각 (그 전까지는 GPS 상태 갱신이 덮어쓰지 않음)
        self.status_hold_text = ''
        self.status_hold_color = '#8e8e93'
        self.tile_retry_at = 0.0          # 지도 타일 재요청 가능 시각
        self.tile_retry_n = 0

        self.update_stats()
        location.start_updates()
        
        threading.Thread(target=self.check_network_loop, daemon=True).start()
        threading.Thread(target=self._trim_cache_bg, daemon=True).start()

    def update_title(self):
        net_str = '온라인' if self.is_online else '오프라인'
        self.title_label.text = '트레커[%s]%s' % (net_str, self.prefetch_text)

    def on_toggle_lock(self, sender):
        self.is_locked = not self.is_locked
        self.lock_view.hidden = not self.is_locked
        self.set_cone_locked(self.is_locked)

        if self.is_locked:
            for b in self.menu_buttons + [self.btn_close]:
                b.enabled = False
            self.remove_subview(self.lock_view)
            self.add_subview(self.lock_view)
            self.btn_lock.title = '해제'
            self.status.text = '화면이 잠겼습니다 (3번 빠르게 터치시 해제)'
            ilog("잠금: 경로 기록 + 진행 방향 계산(%d초)·지도 갱신(%d초)만 수행, 방위 바·자동저장·날씨·고도 조회·네트워크 점검·이탈 경고 일시 정지" % (LOCK_HEADING_SEC, LOCK_MAP_SEC))
        else:
            self.unlock_ui()
            self.status.text = '잠금이 해제되었습니다'

    def unlock_ui(self):
        for b in self.menu_buttons + [self.btn_close]:
            b.enabled = True
        self.btn_lock.title = '잠금'
        self.is_locked = False
        self.lock_view.hidden = True
        self.set_cone_locked(False)
        self.refresh_buttons()          # 시뮬레이션 중이면 로드/초기화는 계속 비활성
        self.on_unlocked()

    def on_unlocked(self):
        """잠금 해제: 일시 정지했던 작업을 바로 따라잡는다 (날씨 즉시 갱신, 화면 점검, 중심 고도)."""
        ilog("잠금 해제: 일시 정지했던 작업 재개")
        try:
            self.wx_verify_ts = 0.0
            if self.wx_last:
                self.wx_applied = False
            self.force_weather_refresh()
            self.web.evaluate_javascript("map.fire('moveend')")      # 지도 중심 고도 다시 조회
            if self.last_lat is not None:
                self.push_map(self.last_lat, self.last_lon)          # 지도 즉시 갱신
            r = self.web.evaluate_javascript('getUpDir()')           # 방위 바 즉시 맞춤
            if r:
                d = float(r)
                if d == d:
                    self.compass_bar.set_dir(d)
        except Exception as e:
            dlog("잠금 해제 후 재개 오류: %s" % e)

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
            self.status.text = '터치 잠금이 해제되었습니다'

    def ensure_server(self):
        """로컬 지도 서버가 살아 있는지 확인하고, 죽었으면 같은 포트로 다시 시작한다 (페이지는 다시 불러오지 않음).
        서버 스레드가 끝났거나 연결 확인이 2번 연속 실패했을 때만 재시작한다 (일시적으로 바쁜 것을 죽은 것으로 오인 방지)."""
        if self.closed or not SERVER_PORT or self.server is None:
            return True
        th = self.server_thread
        dead = th is not None and not th.is_alive()
        if not dead:
            try:
                c = socket.create_connection(('127.0.0.1', SERVER_PORT), timeout=3.0)
                c.close()
                self.server_fail_n = 0
                return True
            except Exception:
                self.server_fail_n += 1
            if self.server_fail_n < 2:
                return False
        self.server_fail_n = 0
        ilog("지도 서버 응답 없음 -> 같은 포트로 재시작")
        try:
            old, self.server = self.server, None
            self._shutdown_http_server(old)         # 이전 서버 스레드까지 확실히 정지
            if self.closed:
                return False
            srv = SafeHTTPServer(('127.0.0.1', SERVER_PORT), MapHandler)
            self.server = srv
            th = threading.Thread(target=srv.serve_forever, daemon=True)
            th.start()
            self.server_thread = th
            ilog("지도 서버 재시작 완료 (포트 %d)" % SERVER_PORT)
            return True
        except Exception as e:
            dlog("지도 서버 재시작 실패: %s" % e)
            return False

    def map_recover(self, online):
        """일시 실패한 지도 타일이 있으면, 연결이 되는 동안 간격을 늘려가며 지도 타일을 다시 요청한다."""
        now = time.time()
        if TILE_STATS['miss'] <= 0:
            self.tile_retry_n = 0
            return
        if (not online) or self.is_locked or self.sim_active or self.T.state == 'recording' or now < self.tile_retry_at:
            return
        TILE_STATS['miss'] = 0
        self.tile_retry_n += 1
        self.tile_retry_at = now + min(60.0, 6.0 * (2 ** min(self.tile_retry_n, 4)))
        run_on_main(self.retry_map_tiles)

    def retry_map_tiles(self):
        if self.closed:
            return
        if self.js_busy:                # 다른 JS 작업 중이면 다음 점검 때 다시
            TILE_STATS['miss'] += 1
            self.tile_retry_at = 0.0
            return
        self.js_busy = True
        try:
            self.web.evaluate_javascript('retryTiles();')
            ilog("지도 타일 재요청 (%d차)" % self.tile_retry_n)
        except Exception as e:
            dlog("지도 타일 재요청 오류: %s" % e)
        finally:
            self.js_busy = False

    def check_network_loop(self):
        last_loop = time.time()
        lock_n = 0
        while not self.closed:
            now = time.time()
            if now - last_loop > 20.0:      # 루프가 오래 멈췄다 = 앱이 백그라운드에서 쉬다 돌아옴 -> 지도 재접속
                ilog("앱 복귀 감지 (%.0f초 정지) -> 지도 재접속 시도" % (now - last_loop))
                NET_STATE['fail_until'] = 0.0
                self.ensure_server()
                self.tile_retry_at = 0.0
            last_loop = now
            if self.is_locked:          # 잠금 중에는 인터넷 점검 일시 정지 (로컬 지도 서버만 가끔 확인)
                lock_n += 1
                if lock_n % 10 == 0:
                    self.ensure_server()
                time.sleep(1.0)
                continue
            lock_n = 0
            status = True
            try:
                urllib.request.urlopen('https://clients3.google.com/generate_204', timeout=2)
            except Exception:
                status = False
            
            if self.is_online != status:
                self.is_online = status
                if status:
                    NET_STATE['fail_until'] = 0.0
                run_on_main(self.update_title)
            if status:
                NET_STATE['fail_until'] = 0.0   # 인터넷이 되면 지도 서버 연결 대기 시간도 바로 해제
            else:
                NET_STATE['fail_until'] = time.time() + 15
            
            self.ensure_server()
            self.map_recover(status)
            if VWORLD_DIAG['new']:
                VWORLD_DIAG['new'] = False
                run_on_main(lambda m=VWORLD_DIAG['msg']: self.show_status_msg(m, 6.0))
            
            for _ in range(50):
                if self.closed:
                    break
                time.sleep(0.1)

    def start_server(self):
        global SERVER_PORT
        try:
            self.server = SafeHTTPServer(('127.0.0.1', 0), MapHandler)
            SERVER_PORT = self.server.server_address[1]
            th = threading.Thread(target=self.server.serve_forever, daemon=True)
            th.start()
            self.server_thread = th
            self.web.load_url('http://127.0.0.1:%d/' % SERVER_PORT)
            ilog("HTTP 서버 안전 시작 포트: %d" % SERVER_PORT)
        except Exception as e:
            dlog("HTTP 서버 시작 실패: %s" % e)
            print("HTTP Server Error:", e)

    @staticmethod
    def _shutdown_http_server(srv):
        """서버 루프를 멈추고 소켓을 닫는다 (shutdown이 오래 걸려도 2초 후엔 넘어감)."""
        if not srv:
            return
        t = threading.Thread(target=srv.shutdown, daemon=True)
        t.start()
        t.join(2.0)
        try:
            srv.server_close()
        except Exception:
            pass

    def stop_server(self):
        srv, self.server = self.server, None
        self._shutdown_http_server(srv)

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
        bar_h = 40
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
                    out.append(max(_mw('잠금', f), _mw('해제', f)))
                else:
                    out.append(_mw(b.title, f))
            return out

        avail_total = (w - 6) - 48
        min_pad = 4.0
        size = 16
        for sz in (23, 22, 21, 20, 19, 18, 17, 16):
            t_need = _mw('트레커[오프라인]', ('<System-Bold>', sz)) + 10
            tws = _menu_widths(sz)
            if t_need + sum(tws) + 2 * min_pad * len(tws) <= avail_total:
                size = sz
                break

        t_need = _mw('트레커[오프라인]', ('<System-Bold>', size)) + 10
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
        sh = 56
        vgap = 4
        
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
        self.compass_bar.frame = (m, y, w - 2 * m, cb_h)
        
        bw = (w - 2 * m - gap) / 2
        self.btn_main.frame = (m, by, bw, btn_h)
        self.btn_stop.frame = (m + bw + gap, by, bw, btn_h)
        
        lock_w = 230
        web_bottom = by - 32 - gap
        self.lock_view.frame = (0, 0, w, h)
        self.lock_box.frame = (m + 8, web_bottom - btn_h - 8, lock_w, btn_h)
        self.lock_label.frame = (10, 4, lock_w - 20, btn_h - 8)

        try:
            self.web.evaluate_javascript('if(typeof map !== "undefined") { map.invalidateSize(); }')
        except Exception:
            pass

    def on_save_gpx(self, sender):
        if not self.T.points:
            self.status.text = '저장할 트래킹 기록이 없어요'
            return
        try:
            os.makedirs(SAVE_DIR, exist_ok=True)
            stamp = datetime.datetime.fromtimestamp(self.T.start_ts or time.time()).strftime('%Y%m%d_%H%M%S')
            path = os.path.join(SAVE_DIR, 'trek_%s.gpx' % stamp)
            write_gpx(self.T.points, path, 'Trek ' + stamp, self.T.distance, int(self.T.gain), self.T.total_elapsed())
            self.show_status_msg('✅ 저장되었습니다')
        except Exception as e:
            self.status.text = 'GPX 저장 실패'

    def on_gpx(self, sender):
        if self.sim_active:
            self.show_status_msg('시뮬레이션 중에는 사용할 수 없어요')
            return
        try:
            os.makedirs(SAVE_DIR, exist_ok=True)
            files = sorted([f for f in os.listdir(SAVE_DIR) if f.lower().endswith('.gpx') and not f.startswith('map_')], reverse=True)
            if self.prefetching:
                map_items = [MENU_PREFETCH_CANCEL, MENU_CACHE_INFO, MENU_WX_LOG]
            else:
                map_items = [MENU_PREFETCH_ROUTE, MENU_PREFETCH_VIEW, MENU_CACHE_INFO, MENU_WX_LOG]
            items = ['📂 외부 파일 선택...', '❌ 표시된 경로 해제'] + map_items + files
            
            sel = dialogs.list_dialog('GPX 경로 불러오기', items)
            if not sel:
                return
            if sel in (MENU_PREFETCH_ROUTE, MENU_PREFETCH_VIEW, MENU_PREFETCH_CANCEL, MENU_CACHE_INFO, MENU_WX_LOG):
                self.on_map_menu(sel)
                return
                
            path = None
            display_name = ''
            if sel == '📂 외부 파일 선택...':
                try:
                    path = dialogs.pick_document(types=['public.data'])
                    if path:
                        base_name = os.path.basename(path)
                        display_name = os.path.splitext(base_name)[0]
                except Exception:
                    self.status.text = '파일 선택 취소됨'
                    return
            elif sel == '❌ 표시된 경로 해제':
                self.sim_end()
                self.gpx_eles = []
                self.T.gpx_route = []
                self.web.evaluate_javascript('clearGpxRoute();')
                self.status.text = 'GPX 경로 해제됨'
                return
            else:
                path = os.path.join(SAVE_DIR, sel)
                display_name = os.path.splitext(sel)[0]
                
            if path:
                pts, eles = read_gpx_points(path)
                if pts:
                    self.sim_end()
                    self.T.gpx_route = pts
                    self.gpx_eles = eles
                    st = calc_route_stats(pts, eles)
                    prof = build_elev_profile(pts, eles)
                    detail = build_elev_detail(pts, eles, display_name, st)
                    js = 'setGpxRoute(%s, %s); setElevationProfile(%s); setElevDetail(%s);' % (
                        json.dumps(pts), json.dumps(display_name, ensure_ascii=False), json.dumps(prof),
                        json.dumps(detail, ensure_ascii=False))
                    self.web.evaluate_javascript(js)

                    stars, label, effort, hours = rate_difficulty(st['dist'], st['gain'])
                    self.status.text = '경로 로드 · %.1fkm · 상승 %dm · %s %s' % (
                        st['dist'] / 1000, st['gain'], stars, label)

                    try:
                        js = 'setDifficulty(%d, %s, %.2f, %d, %s, %s);' % (
                            stars.count('★'),
                            json.dumps(label, ensure_ascii=False),
                            st['dist'] / 1000.0,
                            int(st['gain']),
                            json.dumps('약 ' + fmt_hours(hours), ensure_ascii=False),
                            'true' if st['has_ele'] else 'false')
                        self.web.evaluate_javascript(js)
                    except Exception as e:
                        dlog("난이도 표시 오류: %s" % e)
                else:
                    self.status.text = 'GPX 파일에서 좌표를 읽지 못했어요'
        except Exception as e:
            dlog("GPX 로드 메뉴 예외: %s" % e)

    def _trim_cache_bg(self):
        try:
            total, count, removed = trim_tile_cache()
            ilog("지도 캐시 %d개 %.0fMB (정리 %d개)" % (count, total / 1048576.0, removed))
        except Exception as e:
            dlog("지도 캐시 정리 오류: %s" % e)

    def _current_cache_layer(self):
        key = ''
        try:
            key = (self.web.evaluate_javascript('currentLayerKey') or '').strip()
        except Exception:
            pass
        key = canon_layer(key or 'opentopo_online')
        return key if key in TILE_LAYERS else 'opentopo'

    def _alert(self, title, msg, b1='확인', b2=None):
        try:
            if b2:
                return dialogs.alert(title, msg, b1, b2, hide_cancel_button=True)
            return dialogs.alert(title, msg, b1, hide_cancel_button=True)
        except KeyboardInterrupt:
            return 0
        except Exception as e:
            dlog("알림 표시 오류: %s" % e)
            return 0

    def _confirm(self, title, msg, ok='시작'):
        try:
            dialogs.alert(title, msg, ok)
            return True
        except KeyboardInterrupt:
            return False
        except Exception as e:
            dlog("확인창 오류: %s" % e)
            return False

    def on_map_menu(self, sel):
        if sel == MENU_PREFETCH_CANCEL:
            self.prefetch_cancel = True
            self.status.text = '지도 미리받기를 취소하는 중...'
        elif sel == MENU_PREFETCH_ROUTE:
            self.prefetch_route()
        elif sel == MENU_PREFETCH_VIEW:
            self.prefetch_view()
        elif sel == MENU_CACHE_INFO:
            self.cache_info()
        elif sel == MENU_WX_LOG:
            self.show_weather_log()

    def prefetch_route(self):
        pts = self.T.gpx_route
        if not pts:
            self._alert('지도 미리받기', '먼저 GPX 경로를 불러와 주세요.')
            return
        layer = self._current_cache_layer()
        tiles, zr = plan_route_tiles(pts, layer)
        self._confirm_and_prefetch(layer, tiles, zr, '경로 주변')

    def prefetch_view(self):
        layer = self._current_cache_layer()
        try:
            r = self.web.evaluate_javascript(
                'JSON.stringify([map.getBounds().getSouth(), map.getBounds().getWest(), '
                'map.getBounds().getNorth(), map.getBounds().getEast(), map.getZoom()])')
            s_, w_, n_, e_, z_ = json.loads(r)
        except Exception:
            self._alert('지도 미리받기', '현재 지도 범위를 읽지 못했어요.')
            return
        tiles, zr = plan_view_tiles(s_, w_, n_, e_, z_, layer)
        self._confirm_and_prefetch(layer, tiles, zr, '현재 화면 주변')

    def _confirm_and_prefetch(self, layer, tiles, zr, what):
        if not tiles:
            self._alert('지도 미리받기', '범위가 너무 넓어요. 지도를 더 확대하거나 더 짧은 경로로 시도해 주세요.')
            return
        todo = [t for t in tiles if not tile_is_cached(layer, *t)]
        if not todo:
            self._alert('지도 미리받기', '이 범위는 이미 모두 저장되어 있어요.')
            return
        if not self.is_online:
            self._alert('지도 미리받기', '인터넷에 연결되어 있지 않아요.')
            return
        mb = len(todo) * TILE_AVG_KB.get(layer, 30) / 1024.0
        msg = ('%s 지도(%s) 타일 %d개(약 %.0fMB)를 내려받아 오프라인용으로 저장합니다.\n줌 %d~%d\n\n'
               '공개 지도 서버를 쓰므로 한 번에 너무 넓은 지역은 피해 주세요.') % (
                   what, LAYER_NAMES.get(layer, layer), len(todo), mb, zr[0], zr[1])
        if not self._confirm('지도 미리받기', msg, '시작'):
            return
        self.prefetching = True
        self.prefetch_cancel = False
        NET_STATE['fail_until'] = 0.0
        threading.Thread(target=self._prefetch_worker, args=(layer, todo), daemon=True).start()

    def _prefetch_worker(self, layer, todo):
        total = len(todo)
        done = saved = failed = 0
        why = ''
        try:
            for (z, x, y) in todo:
                if self.prefetch_cancel:
                    why = '취소'
                    break
                while self.is_locked and not self.prefetch_cancel and not self.closed:
                    self.prefetch_text = ' ⏸'      # 잠금 중에는 미리받기 일시 정지
                    run_on_main(self.update_title)
                    time.sleep(1.0)
                data = fetch_tile_net(layer, z, x, y)
                if data and write_cached_tile(tile_cache_path(layer, z, x, y), data):
                    saved += 1
                else:
                    failed += 1
                    if time.time() < NET_STATE['fail_until']:
                        why = '연결 끊김'
                        break
                done += 1
                if done % 3 == 0 or done == total:
                    self.prefetch_text = ' ⬇%d%%' % int(done * 100 / total)
                    run_on_main(self.update_title)
                time.sleep(PREFETCH_DELAY)
        except Exception as e:
            why = '오류'
            dlog("미리받기 오류: %s" % e)
        finally:
            self.prefetching = False
            self.prefetch_text = ''
            (dlog if failed else ilog)("지도 미리받기 종료: 저장 %d / 실패 %d / 대상 %d %s" % (saved, failed, total, why))
            msg = ('⚠️ %s (%d개 저장)' % (why, saved)) if why else ('✅ 지도 %d개 저장' % saved)
            run_on_main(self.update_title)
            run_on_main(lambda: self.show_status_msg(msg, 3.0))

    def cache_info(self):
        count, size = tile_cache_stats()
        msg = '저장된 지도 타일 %d개 · %.1fMB\n(%dMB를 넘으면 오래 안 쓴 타일부터 자동 삭제)' % (
            count, size / 1048576.0, TILE_CACHE_MAX_MB)
        if self._alert('지도 캐시', msg, '확인', '전체 삭제') == 2:
            if self._confirm('지도 캐시 전체 삭제', '저장된 지도를 모두 지울까요?\n인터넷이 없으면 지도를 볼 수 없게 됩니다.', '삭제'):
                shutil.rmtree(TILE_CACHE_DIR, ignore_errors=True)
                self.show_status_msg('🧹 지도 캐시 삭제됨')

    def on_reset(self, sender):
        if self.sim_active:
            self.show_status_msg('시뮬레이션 중에는 사용할 수 없어요')
            return
        """초기화: 불러온 GPX 경로, 시뮬레이션, 그리고 시작 버튼으로 기록한 경로를 모두 지운다."""
        T = self.T
        if T.state != 'idle':               # 기록 중/일시정지 상태면 삭제 전에 한 번 확인
            try:
                console.alert('기록 초기화', '진행 중인 기록이 삭제돼요. 계속할까요?', '삭제')
            except KeyboardInterrupt:
                return
            except Exception:
                pass
            self.stop_keep_running()
            try:
                self.web.evaluate_javascript('autoHeading(false, true);')
            except Exception:
                pass
            try:
                console.set_idle_timer_disabled(False)
            except Exception:
                pass
        self.sim_end()
        self.sim_route = None
        self.gpx_eles = []
        T.gpx_route = []
        T.reset_track()                     # 기록한 좌표·거리·시간·상승고도·상태를 모두 비움
        T.clock_offset = 0.0
        self.track_heading = None
        self.refresh_buttons()
        try:
            self.web.evaluate_javascript('clearGpxRoute(); clearTrackLine();')
        except Exception:
            pass
        try:
            self.update_stats()             # 거리·시간·속도 표시도 바로 초기화
        except Exception:
            pass
        self.status.text = '경로와 기록이 초기화되었습니다'
    def on_main(self, sender):
        T = self.T
        if self.sim_active and T.state == 'idle':
            self.show_status_msg('시뮬레이션 중에는 기록할 수 없어요')
            return
        if T.state == 'idle':
            self.sim_hold = False
            if not self.sim_active:
                T.clock_offset = 0.0
            T.start()
            self.tile_retry_at = max(self.tile_retry_at, time.time() + 30.0)     # 시작 직후 지도 회전과 겹치지 않게 타일 재요청을 미룸
            self.track_heading = None
            self.last_autosave = time.time()
        elif T.state == 'recording':
            T.pause()
        else:
            T.resume()

        if T.state == 'recording':
            self.track_heading_ts = 0.0
            self.last_sent_h = None
            self.last_live_beep = time.time()
            self.start_keep_running()
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
        self.tile_retry_at = max(self.tile_retry_at, time.time() + 30.0)     # 정지 직후 지도 회전 복귀와 겹치지 않게 타일 재요청을 미룸
        self.stop_keep_running()
        try:
            self.web.evaluate_javascript('autoHeading(false, true);')
        except Exception:
            pass
        try:
            console.set_idle_timer_disabled(False)
        except Exception:
            pass
        self.refresh_buttons()
        
        if len(T.points) < 2:
            self.show_status_msg('기록된 좌표가 부족해 저장하지 않았어요', color='#ff9f0a')
            return
            
        stamp = datetime.datetime.fromtimestamp(T.start_ts).strftime('%Y%m%d_%H%M%S')
        path = os.path.join(SAVE_DIR, 'trek_%s.gpx' % stamp)
        try:
            write_gpx(T.points, path, 'Trek ' + stamp, T.distance, int(T.gain), T.total_elapsed())
            self.show_status_msg('✅ 저장되었습니다')
        except Exception as e:
            dlog("종료 저장 실패: %s" % e)
            self.show_status_msg('저장 실패', color='#ff9f0a')

    def refresh_buttons(self):
        st = self.T.state
        if st == 'recording':
            self.btn_main.title = '❚❚ 일시정지'
            self.btn_main.background_color = '#ff9f0a'
        elif st == 'paused':
            self.btn_main.title = '▶ 계속'
            self.btn_main.background_color = '#30d158'
        else:
            self.btn_main.title = '● 시작'
            self.btn_main.background_color = '#30d158'
        sim_lock = bool(self.sim_active and st == 'idle')   # 시뮬레이션 중에는 기록 시작 불가
        self.btn_main.enabled = not sim_lock
        self.btn_main.alpha = 0.4 if sim_lock else 1.0
        sim_busy = bool(self.sim_active)                    # 시뮬레이션 중에는 로드/초기화 사용 불가
        for _b in (getattr(self, 'btn_load', None), getattr(self, 'btn_reset', None)):
            if _b is not None:
                _b.enabled = (not sim_busy) and (not self.is_locked)
                _b.alpha = 0.4 if sim_busy else 1.0
        can_stop = st != 'idle'
        self.btn_stop.enabled = can_stop
        self.btn_stop.alpha = 1.0 if can_stop else 0.4

    def update_stats(self):
        T = self.T
        dist_m, elapsed = T.distance, T.total_elapsed()
        sim_view = bool((self.sim_active or self.sim_hold) and T.state == 'idle')
        if sim_view:
            # 시뮬레이션 중(기록 전)에는 가상으로 이동한 거리와 걸린 시간(배속 반영)을 표시
            dist_m, elapsed = self.sim_trav, self.sim_trav / (SIM_BASE_KMH / 3.6)
        self.stat_boxes['dist'][2].text = '%.2fkm' % (dist_m / 1000)
        self.stat_boxes['time'][2].text = fmt_time(elapsed)
        if sim_view:                        # 시뮬레이션 중에는 속도를 측정하지 않고 '-' 로 표시
            spd_txt = '-'
        else:
            spd_txt = '%.1fkm/h' % (T.speed * 3.6) if T.state == 'recording' else '-'
        self.stat_boxes['speed'][2].text = spd_txt
        
        label_view, title_lbl, val_lbl = self.stat_boxes['gain_ele']
        if T.state == 'recording':
            title_lbl.text = '상승'
            val_lbl.text = '%dm' % int(T.gain)
        else:
            title_lbl.text = '고도'
            if self.center_elevation is not None:
                val_lbl.text = '%dm' % int(self.center_elevation)
            else:
                val_lbl.text = '-'

    def tick(self):
        if self.closed:
            return
        if self.js_busy:                # 다른 주기 작업이 JS 응답을 기다리는 중이면 겹쳐 실행하지 않고 잠시 뒤 다시
            ui.delay(self.tick, 0.2)
            return
        self.js_busy = True
        try:
            loc = self.sim_location() if self.sim_active else location.get_location()
            if loc:
                lat = float(loc['latitude'])
                lon = float(loc['longitude'])
                self.on_location(loc)
                if self.sim_active:
                    self.center_elevation = float(loc.get('altitude', 0.0))
                plat, plon = self.T.filtered_pos(lat, lon)

                if (self.T.state == 'recording' and not (self.is_locked and LOCK_PAUSE_DEVIATION)
                        and self.deviation_now(plat, plon)):
                    self.status.text = '⚠️ 경고: 경로를 이탈했습니다!'
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
                elif time.time() >= self.status_hold_until:
                    self.status.text_color = '#8e8e93'

            if self.sim_active:
                self.sim_status()

            if self.is_locked:
                self.locked_map_refresh()       # 잠금 중: 방위 바 갱신 없음, 지도 갱신은 30초에 한 번
            elif not ((self.T.state == 'recording' or self.sim_active) and HEADING_STATE['on']):
                try:
                    r = self.web.evaluate_javascript('getUpDir()')
                    if r:
                        d = float(r)
                        if d == d:
                            self.compass_bar.set_dir(d)
                except Exception:
                    pass

            self.weather_maintenance()

            now_t = time.time()
            if self.T.state == 'recording' and now_t - self.last_live_beep >= LIVE_BEEP_SEC:
                self.last_live_beep = now_t
                self.play_live_signal()
            if now_t - self.last_heartbeat >= HEARTBEAT_SEC:
                self.last_heartbeat = now_t
                self.heartbeat()

            self.update_stats()
            
            if self.T.state == 'recording' and not self.is_locked and time.time() - self.last_autosave > AUTOSAVE_SEC:
                if len(self.T.points) > 1:
                    stamp = datetime.datetime.fromtimestamp(self.T.start_ts).strftime('%Y%m%d_%H%M%S')
                    path = os.path.join(SAVE_DIR, 'trek_%s_autosave.gpx' % stamp)
                    write_gpx(self.T.points, path, 'Trek ' + stamp, self.T.distance, int(self.T.gain), self.T.total_elapsed())
                self.last_autosave = time.time()
        except Exception as e:
            dlog("tick 루프 오류: %s" % e)
        finally:
            self.js_busy = False
            if not self.closed:
                ui.delay(self.tick, 1)

    # ---- 날씨 (조회 -> 저장 -> 화면 적용 확인 -> 실패 시 단계적 재시도, 전 과정 날씨 로그 기록)
    def maybe_fetch_weather(self, lat, lon, force=False):
        if self.sim_active and not force:
            return                      # 시뮬레이션 중에는 자동 날씨 조회 생략
        if self.is_locked:
            return                      # 잠금 중에는 날씨 조회 일시 정지
        now = time.time()
        if self.wx_busy:
            if now - self.wx_started < WX_WATCHDOG_SEC:
                return
            wlog('이전 조회가 %d초째 끝나지 않음(네트워크 멈춤 추정) -> 새로 시도' % (now - self.wx_started))
        if not force:
            if now < self.wx_next_try:
                return
            moved_km = 0.0
            if self.wx_lat is not None:
                moved_km = abs(lat - self.wx_lat) * 111.0 + abs(lon - self.wx_lon) * 88.0
            refresh_sec = REC_WX_REFRESH_SEC if self.T.state == 'recording' else WX_REFRESH_SEC
            if self.wx_ts and now - self.wx_ts < refresh_sec and moved_km < WX_REFRESH_MOVE_KM:
                return
        else:
            ilog('즉시 갱신 요청 (아이콘 클릭/잠금 해제)')
        self.wx_busy = True
        self.wx_started = now
        self.wx_gen += 1
        threading.Thread(target=self._weather_worker, args=(lat, lon, self.wx_gen), daemon=True).start()

    def force_weather_refresh(self):
        """아이콘을 눌렀을 때 등: 갱신 주기를 기다리지 않고 지금 바로 현재 위치 날씨를 다시 받는다."""
        if self.last_lat is None or self.is_locked:
            return
        self.maybe_fetch_weather(self.last_lat, self.last_lon, force=True)

    def _weather_worker(self, lat, lon, gen):
        try:
            res = fetch_weather(lat, lon, 'GPS')
            self.wx_lat, self.wx_lon = lat, lon
            self.wx_ts = time.time()
            self.wx_fail_count = 0
            self.wx_next_try = 0.0
            self.wx_last = dict(res, ts=self.wx_ts, lat=lat, lon=lon)
            self.wx_applied = False
            wx_cache_save(self.wx_last)
            ilog("날씨 수신: %.1f도, 코드 %d, 바람 %s m/s, 미세먼지 %s" % (res['t'], res['code'], res.get('wind'), str(res['pm10'])))
            run_on_main(self.apply_weather)
        except Exception as e:
            self.wx_fail_count += 1
            delay = WX_RETRY_BACKOFF[min(self.wx_fail_count - 1, len(WX_RETRY_BACKOFF) - 1)]
            self.wx_next_try = time.time() + delay
            wlog('조회 실패 (연속 %d회): %s -> %d초 뒤 재시도' % (self.wx_fail_count, e, delay))
            dlog("날씨 조회 실패: %s" % e)
            try:
                wx_diagnose()
            except Exception as e2:
                wlog('진단 중 오류: %s' % e2)
            if self.wx_last:
                ilog('저장된 날씨를 흐리게 표시합니다 (%d분 전 값)' % ((time.time() - float(self.wx_last['ts'])) / 60))
                self.wx_applied = False
                run_on_main(self.apply_weather)
            else:
                run_on_main(lambda: self.web.evaluate_javascript('gpsWeatherFail();'))
        finally:
            if gen == self.wx_gen:
                self.wx_busy = False

    def apply_weather(self):
        """마지막 날씨 값을 화면(JS)에 적용하고 결과를 확인한다. 페이지가 아직 준비되지 않았으면 tick 에서 다시 시도."""
        w = self.wx_last
        if not w:
            return
        stale = (time.time() - float(w['ts'])) > WX_STALE_SEC
        pm_js = 'null' if w.get('pm10') is None else ('%.1f' % w['pm10'])
        js = 'applyGpsWeather(%.1f, %d, %s, %s, %s, %s)' % (
            w['t'], w['code'], 'true' if w['is_day'] else 'false', pm_js, 'true' if stale else 'false',
            json.dumps(wx_extra(w, 'GPS 위치'), ensure_ascii=False))
        r = None
        try:
            r = self.web.evaluate_javascript(js)
        except Exception as e:
            r = 'ERR %s' % e
        if r in ('ok', 'skip'):
            if not self.wx_applied:
                ilog('화면 적용 %s (%.1f도, 코드 %d, 미세먼지 %s%s)' % (
                    '완료' if r == 'ok' else '생략(지도 중심 날씨 표시 중)', w['t'], w['code'], w.get('pm10'),
                    ', 오래된 값' if stale else ''))
            self.wx_applied = True
        else:
            self.wx_applied = False
            now = time.time()
            if now - self.wx_apply_log_ts >= 30:
                self.wx_apply_log_ts = now
                wlog('화면 적용 실패: JS 결과 %r (지도 페이지가 아직 로딩 중일 수 있음) -> 1초마다 재시도' % (r,))

    def verify_weather_shown(self):
        """화면의 날씨 칸이 비어 있으면(예: 페이지가 다시 로드됨) 다시 적용하도록 표시한다."""
        if not self.wx_last or not self.wx_applied:
            return
        try:
            txt = self.web.evaluate_javascript(
                "(typeof wxCenterMode !== 'undefined' && wxCenterMode) ? 'center' : "
                "document.getElementById('wx-temp').innerText")
        except Exception:
            return
        if txt is None or txt == 'center':
            return
        if txt.strip() in ('', '-', '--', '...'):
            wlog('화면의 날씨 칸이 비어 있음(%r) -> 다시 적용' % txt)
            self.wx_applied = False

    def weather_maintenance(self):
        """tick(1초)마다 호출: 미적용 날씨 재적용, 화면 점검, 날씨가 오래 없을 때 사유 기록."""
        if self.is_locked:
            return                      # 잠금 중에는 날씨 관련 작업 일시 정지
        now = time.time()
        if self.wx_last and not self.wx_applied:
            self.apply_weather()
        if self.T.state != 'recording' and now - self.wx_verify_ts >= 20:
            self.wx_verify_ts = now
            self.verify_weather_shown()
        if (self.wx_ts == 0 and not self.wx_busy and now - self.app_start_ts > 20
                and now - self.wx_wait_log >= 60):
            self.wx_wait_log = now
            if self.last_lat is None:
                ilog('날씨 대기: GPS 위치를 아직 받지 못함 (위치 권한/실내/신호 확인)')
            else:
                ilog('날씨 대기: 다음 조회까지 %d초' % max(0, self.wx_next_try - now))

    def show_weather_log(self):
        """날씨 로그(최근 기록)를 보여 준다. 파일: Documents/treks/trek_weather_log.txt"""
        lines = []
        for path in (WX_LOG_PATH + '.1', WX_LOG_PATH):
            try:
                with open(path, 'r', encoding='utf-8', errors='replace') as f:
                    lines.extend(f.read().splitlines())
            except OSError:
                pass
        if not lines:
            self._alert('날씨 로그', '아직 날씨 로그가 없어요.\n(GPS를 받으면 조회가 시작됩니다)')
            return
        recent = lines[-300:]
        ok = sum(1 for l in recent if '결과 성공' in l)
        ng = sum(1 for l in recent if '결과 실패' in l)
        last_ok = next((l[:14] for l in reversed(recent) if '결과 성공' in l), '없음')
        head = ('최근 조회: 성공 %d회 / 실패 %d회\n마지막 성공: %s\n파일: Documents/treks/trek_weather_log.txt\n'
                '(복사해서 보내면 원인 확인이 쉬워요)\n' + '-' * 28 + '\n') % (ok, ng, last_ok)
        text = head + '\n'.join(recent[-120:][::-1])      # 최신 기록이 위로
        try:
            dialogs.text_dialog('날씨 로그', text, font=('<System>', 11))
        except KeyboardInterrupt:
            pass
        except Exception as e:
            self._alert('날씨 로그', '로그를 표시하지 못했어요: %s' % e)

    def play_live_signal(self):
        try:
            sound.play_effect(LIVE_SOUND, LIVE_VOLUME, 1.0)
            ui.delay(self._live_second_note, 0.2)
        except Exception as e:
            dlog("신호음 재생 오류: %s" % e)

    def _live_second_note(self):
        try:
            sound.play_effect(LIVE_SOUND, LIVE_VOLUME, 1.5)
        except Exception:
            pass

    def heartbeat(self):
        T = self.T
        mem = -1.0
        try:
            import resource
            div = 1024.0 if sys.platform.startswith('linux') else 1048576.0
            mem = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / div
        except Exception:
            pass
        info = '%s 상태=%s 점=%d 거리=%.0fm 메모리~%.0fMB' % (
            datetime.datetime.now().strftime('%m-%d %H:%M:%S'), T.state, len(T.points), T.distance, mem)
        ilog('생존 ' + info)
        write_run_mark(info)

    def start_keep_running(self):
        if not KEEP_RUNNING_BG or background is None or self._bg_ctx is not None:
            return
        try:
            ctx = background.keep_running()
            ctx.__enter__()
            self._bg_ctx = ctx
            ilog("백그라운드 유지 시작")
        except Exception as e:
            dlog("백그라운드 유지 실패: %s" % e)

    def stop_keep_running(self):
        ctx, self._bg_ctx = self._bg_ctx, None
        if ctx is None:
            return
        try:
            ctx.__exit__(None, None, None)
            ilog("백그라운드 유지 종료")
        except Exception as e:
            dlog("백그라운드 유지 종료 오류: %s" % e)

    def compute_track_heading(self):
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
            start = pts[0]
            if hav(start['lat'], start['lon'], end['lat'], end['lon']) < 3.0:
                return None
        return bearing_deg(start['lat'], start['lon'], end['lat'], end['lon'])

    def set_cone_locked(self, locked):
        """잠금 중에는 지도의 부채꼴 방향 표시를 숨기고, 해제하면 다시 보여 준다."""
        try:
            self.web.evaluate_javascript('setConeLocked(%s);' % ('true' if locked else 'false'))
        except Exception:
            pass

    # ---- GPX 따라가기 시뮬레이션 (불러온 경로를 따라 가상 GPS 위치를 만들어 실제 GPS 대신 사용)
    def sim_build(self):
        route = self.T.gpx_route
        if not route or len(route) < 2:
            return None
        cum = [0.0]
        for i in range(1, len(route)):
            cum.append(cum[-1] + hav(route[i - 1][0], route[i - 1][1], route[i][0], route[i][1]))
        if cum[-1] < 5.0:
            return None
        eles = self.gpx_eles if len(self.gpx_eles) == len(route) else [None] * len(route)
        alts, last = [], None
        for z in eles:
            if z is not None:
                last = z
            alts.append(last)
        first = next((z for z in alts if z is not None), 0.0)
        alts = [first if z is None else z for z in alts]
        return {'cum': cum, 'alts': alts, 'total': cum[-1]}

    def sim_position(self, s):
        import bisect
        sm = self.sim_route
        cum, alts, route = sm['cum'], sm['alts'], self.T.gpx_route
        s = max(0.0, min(s, sm['total']))
        i = bisect.bisect_right(cum, s) - 1
        i = max(0, min(i, len(route) - 2))
        seg = cum[i + 1] - cum[i]
        u = (s - cum[i]) / seg if seg > 0 else 0.0
        a, b = route[i], route[i + 1]
        lat = a[0] + (b[0] - a[0]) * u
        lon = a[1] + (b[1] - a[1]) * u
        alt = alts[i] + (alts[i + 1] - alts[i]) * u
        course = bearing_deg(a[0], a[1], b[0], b[1])
        return lat, lon, alt, course

    def sim_location(self):
        """시뮬레이션 중 tick(1초)마다: 경로를 따라 이동한 가상 위치를 실제 GPS 위치처럼 돌려준다."""
        now = time.time()
        dt = min(max(now - self.sim_ts, 0.0), 3.0)      # 앱이 잠깐 멈춰도 한꺼번에 점프하지 않도록
        self.sim_ts = now
        sm = self.sim_route
        moving = not self.sim_paused
        if moving:
            self.sim_s += self.sim_dir * SIM_BASE_KMH / 3.6 * self.sim_mult * dt
            self.sim_trav += SIM_BASE_KMH / 3.6 * self.sim_mult * dt
            self.T.clock_offset += (self.sim_mult - 1) * dt   # 배속만큼 기록 시간도 빠르게 흐름
        if self.sim_dir > 0:
            finished = self.sim_s >= sm['total']
        else:
            finished = self.sim_s <= 0.0
        if finished:
            self.sim_s = sm['total'] if self.sim_dir > 0 else 0.0
        lat, lon, alt, course = self.sim_position(self.sim_s)
        lat2, lon2, _a2, _c2 = self.sim_position(self.sim_s + self.sim_dir * SIM_LOOKAHEAD_M)
        if self.sim_dir < 0:
            course = (course + 180.0) % 360.0
        if hav(lat, lon, lat2, lon2) > 1.0:
            self.sim_heading = bearing_deg(lat, lon, lat2, lon2)      # 앞쪽을 내다본 방향 (꺾이는 곳에서 덜 흔들림)
        else:
            self.sim_heading = course
        loc = {'latitude': lat, 'longitude': lon, 'altitude': alt, 'horizontal_accuracy': 5.0,
               'course': course, 'speed': (SIM_BASE_KMH / 3.6) if (moving and not finished) else 0.0}
        if finished:
            self.sim_end(done=True)
        return loc

    def sim_status(self):
        if time.time() < self.status_hold_until:
            return
        base = self.status.text
        if base.startswith('\U0001F9EA') and ' | ' in base:
            base = base.split(' | ', 1)[1]
        sm = self.sim_route
        pct = int(100.0 * self.sim_s / sm['total']) if sm and sm['total'] > 0 else 0
        state = '\u23F8' if self.sim_paused else '\u00D7%d' % self.sim_mult
        self.status.text = '\U0001F9EA %s %d%% | %s' % (state, pct, base)

    def sim_start(self, reverse=False, start_s=None):
        if self.T.state != 'idle':
            self.show_status_msg('기록 중에는 시뮬레이션을 할 수 없어요')
            return
        sm = self.sim_build()
        if not sm:
            self.status.text = '시뮬레이션할 GPX 경로가 없어요'
            return
        self.sim_route = sm
        self.sim_hold = False
        self.sim_dir = -1 if reverse else 1
        if start_s is not None:
            self.sim_s = max(1.0, min(sm['total'] - 1.0, float(start_s)))
        else:
            self.sim_s = sm['total'] if reverse else 0.0
        self.sim_trav = 0.0
        self.sim_ts = time.time()
        self.sim_paused = False
        self.sim_active = True
        try:
            console.set_idle_timer_disabled(True)       # 시뮬레이션 중에는 화면이 꺼지지(슬립) 않게
        except Exception:
            pass
        self.refresh_buttons()
        if self.T.state == 'idle':
            self.T.clock_offset = 0.0
        self.center_elevation = None
        lat, lon, _alt, _c = self.sim_position(self.sim_s)
        if reverse:
            _c = (_c + 180.0) % 360.0
        self.sim_heading = _c
        self.last_sent_h = None
        try:
            self.web.evaluate_javascript('setSimMode(true, %.6f, %.6f);' % (lat, lon))
        except Exception:
            pass
        ilog("시뮬레이션 시작: %d배속, 경로 %.2fkm" % (self.sim_mult, sm['total'] / 1000.0))
        self.play_live_signal()         # 시작 알림음 (기록 중 생존 신호음과 같은 소리)
        #self.show_status_msg('\U0001F9EA 시뮬레이션 %d배속' % self.sim_mult)

    def sim_end(self, done=False):
        was = self.sim_active
        self.sim_hold = bool(done and was)
        if not done:
            self.sim_trav = 0.0
            self.sim_s = 0.0            # 시뮬레이션 거리·시간 초기화 (완료로 끝났을 때만 마지막 값을 보여 줌)
        self.sim_active = False
        self.sim_paused = False
        try:
            console.set_idle_timer_disabled(self.T.state != 'idle')     # 시뮬 종료: 기록 중이 아니면 화면 슬립 허용
        except Exception:
            pass
        if self.T.state == 'idle':
            self.T.clock_offset = 0.0
        if not was:
            return
        try:
            self.refresh_buttons()
        except Exception:
            pass
        try:
            self.web.evaluate_javascript('setSimMode(false);')
        except Exception:
            pass
        ilog("시뮬레이션 종료 (%s)" % ('경로 끝까지 완료' if done else '중지'))
        self.play_live_signal()         # 종료 알림음 (시뮬레이션이 실제로 켜져 있다가 끝날 때만 여기까지 옴)
        #if done:
            #self.show_status_msg('\U0001F3C1 시뮬레이션 완료')

    def _sim_here_label(self):
        return '\U0001F4CD 십자선 위치부터 시작 (%d배속)' % self.sim_mult

    def _sim_here_rev_label(self):
        return '\U0001F4CD 십자선 위치부터 거꾸로 시작'

    def sim_nearest_s(self, sm, lat, lon, hint=None, rng=None):
        """경로에서 (lat, lon)에 가장 가까운 지점까지의 경로 누적 거리(m)와, 그 지점까지 떨어진 거리(m)."""
        route, cum = self.T.gpx_route, sm['cum']
        kx = math.cos(math.radians(lat)) * 111320.0
        ky = 110540.0
        best = None
        i_lo, i_hi = 0, len(route) - 2
        if rng is not None:                 # 경로 거리 범위(m) 안의 구간만 검사 (기록 중 반복 계산 부하 줄이기)
            import bisect
            i_lo = max(0, bisect.bisect_right(cum, rng[0]) - 1)
            i_hi = min(len(route) - 2, bisect.bisect_left(cum, rng[1]))
            if i_hi < i_lo:
                i_lo, i_hi = 0, len(route) - 2
        for i in range(i_lo, i_hi + 1):
            ax, ay = (route[i][1] - lon) * kx, (route[i][0] - lat) * ky
            bx, by = (route[i + 1][1] - lon) * kx, (route[i + 1][0] - lat) * ky
            dx, dy = bx - ax, by - ay
            l2 = dx * dx + dy * dy
            u = max(0.0, min(1.0, -(ax * dx + ay * dy) / l2)) if l2 > 0 else 0.0
            qx, qy = ax + u * dx, ay + u * dy
            d2 = qx * qx + qy * qy
            score = d2
            if hint is not None:            # 직전 진행 위치에서 멀수록 점수를 불리하게 (앞쪽 1km = 약 20m, 뒤쪽 1km = 약 60m 오차)
                dlt = cum[i] - hint         # 같은 길로 왕복하는 경로에서 되돌아가는 쪽으로 튀지 않고 진행 방향을 따라가게 함
                score += (dlt * (0.02 if dlt >= 0 else 0.06)) ** 2
            if best is None or score < best[0]:
                best = (score, i, u, d2)
        _sc, i, u, d2 = best
        return cum[i] + u * (cum[i + 1] - cum[i]), math.sqrt(d2)

    def sim_start_here(self, reverse=False):
        """지도 중앙(십자선) 위치에서 가장 가까운 경로 지점부터 시뮬레이션을 시작한다."""
        sm = self.sim_build()
        if not sm:
            self.status.text = '시뮬레이션할 GPX 경로가 없어요'
            return
        try:
            r = self.web.evaluate_javascript('(function(){var c = map.getCenter(); return c.lat + "," + c.lng;})()')
            clat, clon = [float(x) for x in str(r).split(',')]
        except Exception:
            self.show_status_msg('십자선 위치를 읽지 못했어요')
            return
        s, dist = self.sim_nearest_s(sm, clat, clon)
        if dist > 100.0:
            self.show_status_msg('경로에서 %dm 떨어짐 · 가까운 곳에서 시작' % int(dist))
        self.sim_start(reverse=reverse, start_s=s)

    def _sim_rev_label(self):
        return '\u23EA 끝에서 거꾸로 시작 (%d배속)' % self.sim_mult

    def _sim_dir_label(self):
        return '\U0001F504 방향 반대로 (현재: %s)' % ('역방향' if self.sim_dir < 0 else '정방향')

    def _sim_jump_label(self):
        return '\U0001F3AF 위치 점프'

    def sim_toggle_dir(self):
        """시뮬레이션 진행 방향을 반대로 바꾼다 (정방향 <-> 역방향)."""
        sm = self.sim_route
        if not sm:
            return
        if self.sim_dir > 0 and self.sim_s <= 1.0:
            self.show_status_msg('시작점에서는 반대로 갈 수 없어요')
            return
        if self.sim_dir < 0 and self.sim_s >= sm['total'] - 1.0:
            self.show_status_msg('끝점에서는 정방향이 안 돼요')
            return
        self.sim_dir = -self.sim_dir
        self.sim_ts = time.time()
        self.has_h = False              # 진행 방향이 180도 바뀌므로 방향 평활화를 새로 시작
        self.last_sent_h = None
        ilog("시뮬레이션 방향: %s" % ('역방향' if self.sim_dir < 0 else '정방향'))

    def sim_jump(self):
        """시뮬레이션 위치를 경로의 다른 지점으로 한 번에 옮긴다."""
        sm = self.sim_route
        if not sm:
            return
        total = sm['total']
        rel = [('-5km', -5000.0), ('-1km', -1000.0), ('-500m', -500.0),
               ('+500m', 500.0), ('+1km', 1000.0), ('+5km', 5000.0)]
        a_start = '\u23EE 시작점'
        a_mid = '50% 지점'
        a_end = '\u23ED 끝 100m 전'
        a_in = '\u270F 거리(km)·퍼센트(%) 직접 입력'
        items = [r[0] for r in rel] + [a_start, a_mid, a_end, a_in]
        sel = dialogs.list_dialog('위치 점프 (현재 %.2f / %.2fkm)' % (self.sim_s / 1000.0, total / 1000.0), items)
        if not sel:
            return
        target = None
        for lab, dm in rel:
            if sel == lab:
                target = self.sim_s + dm
        if sel == a_start:
            target = 0.0
        elif sel == a_mid:
            target = total * 0.5
        elif sel == a_end:
            target = total - 100.0
        elif sel == a_in:
            txt = dialogs.input_alert('위치 점프', '이동할 위치 입력\n예: 3.5 (km) 또는 40%', '', '이동')
            txt = (txt or '').strip().lower().replace(',', '.').replace('km', '').strip()
            try:
                if txt.endswith('%'):
                    target = float(txt[:-1]) / 100.0 * total
                else:
                    target = float(txt) * 1000.0
            except ValueError:
                self.show_status_msg('숫자를 입력해 주세요')
                return
        if target is None:
            return
        target = max(1.0, min(total - 1.0, target))
        self.sim_s = target
        self.sim_ts = time.time()
        lat, lon, _a, _c = self.sim_position(target)
        try:
            self.web.evaluate_javascript('simJump(%.6f, %.6f);' % (lat, lon))
        except Exception:
            pass
        ilog("시뮬레이션 점프: %.2fkm 지점" % (target / 1000.0))

    def sim_pick_speed(self):
        items = ['%d배속  (약 %.1fkm/h)' % (m, SIM_BASE_KMH * m) for m in SIM_SPEEDS]
        sel = dialogs.list_dialog('배속 선택', items)
        if not sel or sel not in items:
            return False
        self.sim_mult = SIM_SPEEDS[items.index(sel)]
        return True

    def on_sim(self, sender):
        try:
            if not self.sim_active:
                if self.T.state != 'idle':
                    self.show_status_msg('기록 중에는 시뮬레이션을 할 수 없어요')
                    return
                if not self.T.gpx_route or len(self.T.gpx_route) < 2:
                    self.status.text = '먼저 GPX 경로를 불러와 주세요 (로드)'
                    return
                a_start = '\u25B6 시작 (%d배속)' % self.sim_mult
                a_speed = '\u23E9 배속 선택 후 시작'
                sel = dialogs.list_dialog('GPX 따라가기 시뮬레이션', [self._sim_here_label(), self._sim_here_rev_label(), SIM_MENU_SEP, a_start, self._sim_rev_label(), a_speed])
                if sel == self._sim_here_label():
                    self.sim_start_here(False)
                elif sel == self._sim_here_rev_label():
                    self.sim_start_here(True)
                elif sel == SIM_MENU_SEP:
                    pass
                elif sel == a_start:
                    self.sim_start()
                elif sel == self._sim_rev_label():
                    self.sim_start(reverse=True)
                elif sel == a_speed:
                    if self.sim_pick_speed():
                        self.sim_start()
            else:
                a_pause = '\u25B6 계속' if self.sim_paused else '\u23F8 일시정지'
                a_speed = '\u23E9 배속 변경 (현재 %d배속)' % self.sim_mult
                a_restart = '\u23EE 처음부터 다시'
                a_end = '\u23F9 시뮬레이션 종료'
                sel = dialogs.list_dialog('GPX 따라가기 시뮬레이션', [a_pause, a_speed, self._sim_dir_label(), self._sim_jump_label(), a_restart, a_end])
                if sel == a_pause:
                    self.sim_paused = not self.sim_paused
                    self.sim_ts = time.time()
                elif sel == a_speed:
                    self.sim_pick_speed()
                    self.sim_ts = time.time()
                elif sel == self._sim_dir_label():
                    self.sim_toggle_dir()
                elif sel == self._sim_jump_label():
                    self.sim_jump()
                elif sel == a_restart:
                    self.sim_start(reverse=(self.sim_dir < 0))
                elif sel == a_end:
                    self.sim_end()
                    self.update_stats()
                    self.status.text = '시뮬레이션을 종료했어요'
        except KeyboardInterrupt:
            pass
        except Exception as e:
            dlog("시뮬레이션 메뉴 오류: %s" % e)

    def apply_up_dir(self):
        """/up 으로 들어온 최신 값만 방위 바에 반영 (빠른 회전 중 요청이 쌓이지 않도록)"""
        self.up_scheduled = False
        try:
            if not self.is_locked:
                self.compass_bar.set_dir(self.up_pending)
        except Exception:
            pass

    def deviation_now(self, plat, plon):
        """경로 이탈 여부. 기록 중에는 REC_DEVIATION_SEC 간격으로만 계산하고 그 사이에는 직전 결과를 재사용."""
        T = self.T
        if self.sim_active:
            return False                # 시뮬레이션은 경로를 그대로 따라가므로 이탈 검사 생략 (큰 GPX 에서 부하 큼)
        if T.state != 'recording':
            return T.check_deviation(plat, plon, threshold=20.0)
        now = time.time()
        if now - self.dev_ts >= REC_DEVIATION_SEC:
            self.dev_ts = now
            self.dev_result = T.check_deviation(plat, plon, threshold=20.0)
        return self.dev_result

    def push_map(self, lat, lon):
        """지도(내 위치 점·기록 경로)를 갱신한다."""
        T = self.T
        try:
            n_pts = len(T.points)
            if n_pts != self.pushed_pts_len:        # 기록 점이 늘었을 때만 전체 경로 전송 (같으면 빈 목록 = 지도 쪽은 그대로 둠)
                pts_js = json.dumps([[p['lat'], p['lon']] for p in T.points])
            else:
                pts_js = '[]'
            mlat, mlon = T.filtered_pos(lat, lon)
            js = 'updateMap(%f, %f, %s, %s);' % (mlat, mlon, pts_js, 'true' if T.state == 'recording' else 'false')
            sm = getattr(self, 'sim_route', None)
            if self.sim_active and sm and sm.get('total', 0) > 0:
                # 시뮬레이션 진행 위치를 같은 호출에 실어 보냄 (고도 상세창이 열려 있으면 그래프에 점 표시)
                js += 'setSimElevPos(%.5f);' % max(0.0, min(1.0, self.sim_s / sm['total']))
            self.web.evaluate_javascript(js)
            self.pushed_pts_len = n_pts
            self.last_map_refresh = time.time()
        except Exception:
            pass

    def locked_map_refresh(self):
        """잠금 중: 지도 갱신(내 위치·기록 경로·진행 방향 회전)을 LOCK_MAP_SEC(5초)에 한 번만 수행."""
        now = time.time()
        if now - self.last_map_refresh < LOCK_MAP_SEC or self.last_lat is None:
            return
        self.push_map(self.last_lat, self.last_lon)
        self.last_map_refresh = now
        if HEADING_STATE['on'] and self.locked_heading is not None:
            try:
                self.web.evaluate_javascript('setHeading(%.1f);' % self.locked_heading)
            except Exception:
                pass

    def locked_heading_update(self):
        """잠금 중: 진행 방향 계산을 LOCK_HEADING_SEC(10초)에 한 번만 수행 (지도에는 갱신 때 반영)."""
        now = time.time()
        if now - self.lock_heading_ts < LOCK_HEADING_SEC:
            return
        self.lock_heading_ts = now
        h = None
        if self.T.state == 'recording':
            th = self.compute_track_heading()
            if th is not None:
                self.track_heading = th
                self.track_heading_ts = now
            h = self.track_heading
            if h is None:
                h = self.last_course
            if h is None:
                h = get_device_heading()
        else:
            h = get_device_heading()
            if h is None and self.last_course is not None:
                h = self.last_course
        if h is not None:
            self.locked_heading = h
            r = math.radians(h)
            self.sm_sin, self.sm_cos = math.sin(r), math.cos(r)      # 잠금 해제 후 부드럽게 이어지도록 맞춰 둠
            self.has_h = True

    def heading_tick(self):
        if self.closed:
            return
        if self.js_busy:                # tick 이 JS 응답을 기다리는 중이면 겹치지 않게 잠시 뒤 다시
            ui.delay(self.heading_tick, 0.1)
            return
        self.js_busy = True
        interval = 1.0
        try:
            on = HEADING_STATE['on']
            if on and not self.heading_running:
                if motion is not None:
                    try:
                        motion.start_updates()
                    except Exception as e:
                        dlog("motion 시작 오류: %s" % e)
                self.heading_running = True
                self.has_h = False
                self.last_sent_h = None
                self.no_heading_warned = False
            elif not on and self.heading_running:
                if motion is not None:
                    try:
                        motion.stop_updates()
                    except Exception:
                        pass
                self.heading_running = False

            if on and self.is_locked:
                interval = 1.0
                self.locked_heading_update()        # 잠금 중: 10초마다 계산만 (방위 바·지도 회전은 하지 않음)
            elif on:
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
                        h = self.last_course
                    alpha = 0.27
                    interval = REC_HEADING_TICK
                    if h is None:
                        h = get_device_heading()
                        alpha = 0.3
                elif self.sim_active and self.sim_heading is not None:
                    interval = REC_HEADING_TICK             # 시뮬레이션도 기록 중처럼 가볍게 (초당 8회 -> 약 3회)
                    alpha = 0.27
                    h = self.sim_heading                    # 시뮬레이션 중: 폰 센서 대신 진행 방향을 위로
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
                    send = True
                    if (self.T.state == 'recording' or self.sim_active) and self.last_sent_h is not None:
                        now_s = time.time()
                        dd = abs((sh - self.last_sent_h + 540.0) % 360.0 - 180.0)
                        if dd < REC_HEADING_MIN_DELTA and now_s - self.last_sent_ts < REC_HEADING_RESEND_SEC:
                            send = False
                    if send:
                        self.last_sent_h = sh
                        self.last_sent_ts = time.time()
                        self.web.evaluate_javascript('setHeading(%.1f);' % sh)
                        self.compass_bar.set_dir(sh)
                elif not self.no_heading_warned:
                    self.no_heading_warned = True
                    self.status.text = '방향 센서를 읽을 수 없어요'
        except Exception as e:
            dlog("heading_tick 오류: %s" % e)
        finally:
            self.js_busy = False
            if not self.closed:
                ui.delay(self.heading_tick, interval)

    def show_status_msg(self, text, sec=3.0, color=None):
        """상태 줄(GPS 수신 상태 자리)에 메시지를 sec초 동안 표시한다. 그동안 GPS 상태 갱신이 덮어쓰지 않는다."""
        if color is None:               # 성공(✅·🧹)은 초록, 그 외 안내·경고는 주황
            color = '#30d158' if text[:1] in ('\u2705', '\U0001F9F9') else '#ff9f0a'
        self.status_hold_until = time.time() + sec      # 만료 시각만 기록 (타이머를 만들지 않음). 색·문구 복원은 1초마다 도는 tick이 처리
        self.status_hold_text = text
        self.status_hold_color = color
        self.status.text = text
        self.status.text_color = color

    def on_location(self, loc):
        hold = time.time() < self.status_hold_until
        try:
            self._on_location(loc)
        finally:
            if hold:                    # 메시지 표시 중에는 GPS 상태 문구·색으로 덮어쓰지 않음
                self.status.text = self.status_hold_text
                self.status.text_color = self.status_hold_color

    def _on_location(self, loc):
        T = self.T
        acc = loc.get('horizontal_accuracy', -1)
        if acc < 0:
            self.status.text = 'GPS 대기 중...'
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
                self.status.text = 'GPS 신호 향상 대기중 (±%dm)' % acc
            else:
                T.add_point(lat, lon, alt, acc, speed if (speed is not None and speed >= 0) else None)
                plat, plon = T.filtered_pos(lat, lon)
                if (self.is_locked and LOCK_PAUSE_DEVIATION) or not self.deviation_now(plat, plon):
                    self.status.text = '기록 중 (±%dm)' % acc
        elif T.state == 'paused':
            self.status.text = '일시정지 상태 (±%dm)' % acc
        else:
            self.status.text = 'GPS 수신 양호 (±%dm)' % acc

        if not self.is_locked:          # 잠금 중에는 지도 갱신을 30초에 한 번만 (tick 의 locked_map_refresh)
            if T.state != 'recording' or time.time() - self.last_map_refresh >= REC_MAP_SEC:
                self.push_map(lat, lon)

        self.maybe_fetch_weather(lat, lon)

    def will_close(self):
        self.closed = True
        _APP_CLOSED['v'] = True
        try:
            ui.cancel_delays()          # 예약돼 있던 tick·방향 갱신 등이 화면이 닫힌 뒤 실행되지 않게 취소
        except Exception:
            pass
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
        try:
            self.stop_keep_running()
            clear_run_mark()
        except Exception:
            pass

if __name__ == '__main__':
    app = TrekApp()
    ui.delay(app.tick, 0.5)
    ui.delay(app.heading_tick, 0.6)
    app.present('fullscreen', hide_title_bar=True)
