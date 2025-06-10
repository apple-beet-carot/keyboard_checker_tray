import threading
import time
import sys, os
from keyboard import on_press, on_release
from pystray import Icon, MenuItem
from PIL import Image, ImageDraw

# ────────────────────────────────────────────────────────────────────────────
# 전역 변수 설정
# tray: pystray 아이콘 객체를 저장할 변수
# state: 키보드 상태(active 여부, 마지막 입력 시각) 저장
tray = None
state = {
    "active": False,          # 키보드 활성 상태
    "last_event": time.time() # 마지막 키 입력 시각
}

# ────────────────────────────────────────────────────────────────────────────
# 아이콘 생성 함수
# active=True 일 때는 원본 PNG만 표시
# active=False 일 때는 빨간 테두리(레드링) 오버레이
def make_icon(active: bool) -> Image.Image:
    # 1) 실행 파일 번들(–onefile) 모드일 때 리소스 폴더 경로
    if getattr(sys, 'frozen', False):
        base_dir = sys._MEIPASS
    else:
        base_dir = os.path.dirname(__file__)
    # 2) keyboard.png 파일 경로
    img_path = os.path.join(base_dir, "keyboard.png")
    # 3) PNG 로드 후 16×16 크기로 리사이즈
    img = Image.open(img_path).resize((16, 16), Image.LANCZOS)
    # 4) inactive 상태인 경우 빨간 테두리 그리기
    if not active:
        draw = ImageDraw.Draw(img)
        draw.ellipse((1, 1, 14, 14), outline="red", width=2)
    return img

# ────────────────────────────────────────────────────────────────────────────
# 키 입력 이벤트 콜백
# 키를 누르거나 뗄 때마다 상태를 활성으로 갱신하고 아이콘을 변경
def on_key_event(e):
    state["active"] = True
    state["last_event"] = time.time()
    if tray:
        tray.icon  = make_icon(True)
        tray.title = "Keyboard Active"  # 툴팁도 Active로 변경

# ────────────────────────────────────────────────────────────────────────────
# 백그라운드 상태 감시 함수
# 마지막 입력 후 10초가 지나면 inactive 처리하고 아이콘 갱신
def watcher(icon: Icon):
    while True:
        if time.time() - state["last_event"] > 10:
            if state["active"]:
                state["active"] = False
                icon.icon  = make_icon(False)
                icon.title = "Keyboard Inactive"  # 툴팁도 Inactive로 변경
        time.sleep(0.5)

# ────────────────────────────────────────────────────────────────────────────
# 메인 함수
# 트레이 아이콘 초기화, 이벤트 훅 등록, 감시 스레드 시작
def main():
    global tray
    # 1) 트레이 아이콘 객체 생성
    tray = Icon("kbd_state")
    tray.icon  = make_icon(False)            # 초기에는 Inactive 아이콘
    tray.title = "Keyboard Inactive"         # 초기 툴팁
    # 2) 우클릭 메뉴에 종료 항목 추가
    tray.menu  = (MenuItem("Exit", lambda _: tray.stop()),)
    # 3) 키보드 이벤트 훅 등록
    on_press(on_key_event)
    on_release(on_key_event)
    # 4) 상태 감시용 백그라운드 스레드 시작
    t = threading.Thread(target=watcher, args=(tray,), daemon=True)
    t.start()
    # 5) 트레이 아이콘 이벤트 루프 실행
    tray.run()

# ────────────────────────────────────────────────────────────────────────────
# 실행 진입점
if __name__ == "__main__":
    main()
