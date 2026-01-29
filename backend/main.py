from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import pyautogui
import time
import os
from collections import deque

# ---------------- SAFETY ----------------
pyautogui.FAILSAFE = False

# ---------------- APP ----------------
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- PATHS ----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WEB_DIR = os.path.join(BASE_DIR, "..", "web")

app.mount("/static", StaticFiles(directory=WEB_DIR), name="static")

@app.get("/")
def serve_ui():
    return FileResponse(os.path.join(WEB_DIR, "index.html"))

# ---------------- STATE ----------------
MODE = "MEDIA"

current_gesture = None
gesture_start = 0
gesture_fired = False

ONE_SHOT_HOLD = 0.6
VOLUME_INTERVAL = 0.3
last_volume_time = 0

# Screen
screen_w, screen_h = pyautogui.size()

# Mouse movement
last_x = None
last_y = None

# Scroll
last_scroll_y = None
SCROLL_SENSITIVITY = 800

# Swipe (MEDIA mode, ONE finger)
x_history = deque(maxlen=12)
SWIPE_THRESHOLD = 0.15

# ---------------- HELPERS ----------------
def held_long_enough():
    return time.time() - gesture_start >= ONE_SHOT_HOLD

# ---------------- WEBSOCKET ----------------
@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    global MODE, current_gesture, gesture_start, gesture_fired
    global last_volume_time, last_x, last_y, last_scroll_y

    await ws.accept()

    while True:
        data = await ws.receive_json()

        g = data.get("gesture")
        x = data.get("x")
        y = data.get("y")

        # ---------- Gesture transition ----------
        if g != current_gesture:
            current_gesture = g
            gesture_start = time.time()
            gesture_fired = False
            x_history.clear()
            last_scroll_y = None

        # ---------- MODE SWITCH ----------
        if g == "FIST" and held_long_enough() and not gesture_fired:
            MODE = "MOUSE" if MODE == "MEDIA" else "MEDIA"
            gesture_fired = True
            last_x = last_y = None
            await ws.send_json({"mode": MODE})
            continue

        # ================= MEDIA MODE =================
        if MODE == "MEDIA":

            # ---- Play / Pause (toggle) ----
            if g == "PALM" and not gesture_fired:
                pyautogui.press("playpause")
                gesture_fired = True

            # ---- Next Track ----
            elif g == "ONE" and held_long_enough() and not gesture_fired:
                pyautogui.press("nexttrack")
                gesture_fired = True

            # ---- Volume Down ----
            elif g == "TWO" and time.time() - last_volume_time > VOLUME_INTERVAL:
                pyautogui.press("volumedown")
                last_volume_time = time.time()

            # ---- Volume Up ----
            elif g == "THREE" and time.time() - last_volume_time > VOLUME_INTERVAL:
                pyautogui.press("volumeup")
                last_volume_time = time.time()

            # ---- ONE-FINGER SWIPE (TAB CHANGE) ----
            if g == "ONE" and x is not None:
                x_history.append(x)

                if len(x_history) == x_history.maxlen:
                    dx = x_history[-1] - x_history[0]

                    if dx > SWIPE_THRESHOLD:
                        pyautogui.hotkey("ctrl", "tab")
                        x_history.clear()

                    elif dx < -SWIPE_THRESHOLD:
                        pyautogui.hotkey("ctrl", "shift", "tab")
                        x_history.clear()
            else:
                x_history.clear()

        # ================= MOUSE MODE =================
        else:
            # ---- CURSOR MOVE (ONE finger) ----
            if g == "ONE" and x is not None and y is not None:
                if last_x is not None:
                    # X is inverted due to camera mirroring
                    dx = (last_x - x) * screen_w
                    dy = (y - last_y) * screen_h
                    pyautogui.moveRel(dx, dy, duration=0)

                last_x = x
                last_y = y
                last_scroll_y = None

            # ---- LEFT CLICK ----
            elif g == "TWO" and held_long_enough() and not gesture_fired:
                pyautogui.click()
                gesture_fired = True

            # ---- SCROLL (THREE fingers, up/down) ----
            elif g == "THREE" and y is not None:
                if last_scroll_y is not None:
                    dy = y - last_scroll_y
                    pyautogui.scroll(int(-dy * SCROLL_SENSITIVITY))

                last_scroll_y = y

            else:
                last_scroll_y = None
