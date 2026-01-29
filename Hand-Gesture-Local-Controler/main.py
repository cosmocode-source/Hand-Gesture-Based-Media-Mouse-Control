import cv2
import mediapipe as mp
import pyautogui
import time
from collections import deque

# ================= OS ACTIONS =================

def play_pause(): pyautogui.press("playpause")
def skip(): pyautogui.press("nexttrack")
def mute(): pyautogui.press("volumemute")
def vol_up(): pyautogui.press("volumeup")
def vol_down(): pyautogui.press("volumedown")
def tab_next(): pyautogui.hotkey("ctrl", "tab")
def tab_prev(): pyautogui.hotkey("ctrl", "shift", "tab")

def left_click(): pyautogui.click()
def right_click(): pyautogui.rightClick()
def scroll(delta): pyautogui.scroll(delta)

# ================= CONFIG =================

MODE = "MEDIA"                     # MEDIA | MOUSE
ONE_SHOT_HOLD = 0.5
VOLUME_INTERVAL = 0.25
SCROLL_INTERVAL = 0.25
SWIPE_THRESHOLD = 0.18

MODE_SWITCH_COOLDOWN = 1.2
last_mode_switch_time = 0

screen_w, screen_h = pyautogui.size()

# Hand-to-screen calibration (IMPORTANT)
HAND_X_MIN, HAND_X_MAX = 0.2, 0.8
HAND_Y_MIN, HAND_Y_MAX = 0.2, 0.8

# ================= STATE =================

current_gesture = None
gesture_start = 0
gesture_fired = False

last_volume_time = 0
last_scroll_time = 0

x_positions = deque(maxlen=30)

# ================= HELPERS =================

def reset_gesture_state():
    global current_gesture, gesture_start, gesture_fired
    current_gesture = None
    gesture_start = 0
    gesture_fired = False
    x_positions.clear()

def new_gesture(name):
    global current_gesture, gesture_start, gesture_fired
    current_gesture = name
    gesture_start = time.time()
    gesture_fired = False
    x_positions.clear()

def held_long_enough():
    return time.time() - gesture_start >= ONE_SHOT_HOLD

def can_switch_mode():
    return time.time() - last_mode_switch_time > MODE_SWITCH_COOLDOWN

def map_range(val, in_min, in_max, out_min, out_max):
    val = max(min(val, in_max), in_min)
    return int((val - in_min) / (in_max - in_min) * (out_max - out_min) + out_min)

# ================= MEDIAPIPE =================

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
cap = cv2.VideoCapture(0)

with mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.6,
    min_tracking_confidence=0.6
) as hands:

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            continue

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb)

        gesture = "NONE"

        if result.multi_hand_landmarks:
            hand = result.multi_hand_landmarks[0]
            lm = hand.landmark

            thumb  = lm[4].x  < lm[3].x
            index  = lm[8].y  < lm[6].y
            middle = lm[12].y < lm[10].y
            ring   = lm[16].y < lm[14].y
            pinky  = lm[20].y < lm[18].y

            # ---------- Gesture classification ----------
            if not thumb and not index and not middle and not ring and not pinky:
                gesture = "FIST"
            elif thumb and index and middle and ring and pinky:
                gesture = "PALM"
            elif index and not middle and not ring and not pinky:
                gesture = "ONE"
            elif index and middle and not ring and not pinky:
                gesture = "TWO"
            elif index and middle and ring and not pinky:
                gesture = "THREE"
            elif index and middle and ring and pinky:
                gesture = "FOUR"
            elif thumb and not index and not middle and not ring and not pinky:
                gesture = "THUMB"

            mp_draw.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)

            if gesture != current_gesture:
                new_gesture(gesture)

            # ---------- MODE SWITCH ----------
            if gesture == "FIST" and held_long_enough() and not gesture_fired and can_switch_mode():
                MODE = "MOUSE" if MODE == "MEDIA" else "MEDIA"
                last_mode_switch_time = time.time()
                reset_gesture_state()
                time.sleep(0.3)
                continue

            # ================= MEDIA MODE =================
            if MODE == "MEDIA":

                if gesture == "PALM" and held_long_enough() and not gesture_fired:
                    play_pause()
                    gesture_fired = True

                elif gesture == "ONE" and held_long_enough() and not gesture_fired:
                    skip()
                    gesture_fired = True

                elif gesture == "THUMB" and held_long_enough() and not gesture_fired:
                    mute()
                    gesture_fired = True

                elif gesture == "TWO":
                    if time.time() - last_volume_time > VOLUME_INTERVAL:
                        vol_down()
                        last_volume_time = time.time()

                elif gesture == "THREE":
                    if time.time() - last_volume_time > VOLUME_INTERVAL:
                        vol_up()
                        last_volume_time = time.time()

                elif gesture == "FOUR":
                    cx = sum(p.x for p in lm) / len(lm)
                    x_positions.append(cx)
                    if len(x_positions) > 6:
                        dx = x_positions[-1] - x_positions[0]
                        if dx > SWIPE_THRESHOLD:
                            tab_next()
                            x_positions.clear()
                        elif dx < -SWIPE_THRESHOLD:
                            tab_prev()
                            x_positions.clear()

            # ================= MOUSE MODE =================
            else:
                mx = map_range(lm[8].x, HAND_X_MIN, HAND_X_MAX, 0, screen_w)
                my = map_range(lm[8].y, HAND_Y_MIN, HAND_Y_MAX, 0, screen_h)

                if gesture == "ONE":
                    pyautogui.moveTo(mx, my, duration=0.01)

                elif gesture == "TWO" and held_long_enough() and not gesture_fired:
                    left_click()
                    gesture_fired = True

                elif gesture == "THREE" and held_long_enough() and not gesture_fired:
                    right_click()
                    gesture_fired = True

                elif gesture == "PALM":
                    if time.time() - last_scroll_time > SCROLL_INTERVAL:
                        scroll(-40)
                        last_scroll_time = time.time()

        else:
            reset_gesture_state()

        cv2.putText(
            frame,
            f"MODE: {MODE} | GESTURE: {gesture}",
            (20, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.1,
            (0, 255, 0),
            3
        )

        cv2.imshow("Gesture Control", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

cap.release()
cv2.destroyAllWindows()