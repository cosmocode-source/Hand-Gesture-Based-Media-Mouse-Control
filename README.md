# Hand-Gesture-Based-Media-Mouse-Control
## Local Webcam Gesture Control

### Overview
This branch implements a fully local gesture control system.

The webcam, gesture detection, and OS control all run on the same machine.

No browser. No server. No network dependency.

This is the simplest and most stable architecture.

### How It Works
OpenCV captures frames from the laptop webcam

MediaPipe Hands extracts 21 hand landmarks

Finger positions are classified into gestures

Gestures are mapped directly to OS actions using pyautogui

### Features
🟢 Mode Switching

Gesture	Description	Action

✊ Fist (all fingers closed)	Hold for ~0.5s	Toggle mode: MEDIA ↔ MOUSE

This prevents accidental mode changes.

🎵 MEDIA MODE (Default)
Gesture	Finger Pattern	Action

✋ Open Palm	All fingers open	Play / Pause

☝️ One Finger	Index finger only	Next track

✌️ Two Fingers	Index + Middle	Volume Down

🤟 Three Fingers	Index + Middle + Ring	Volume Up

👍 Thumb Only	Thumb open	Mute / Unmute

🖐 Four Fingers	All except thumb	Swipe left/right → Browser tab switch

Notes:

Volume changes repeat at a fixed interval while gesture is held

Swipe gestures use horizontal hand movement history

🖱 MOUSE MODE
Gesture	Finger Pattern	Action

☝️ One Finger	Index finger only	Move mouse cursor

✌️ Two Fingers	Hold	Left Click

🤟 Three Fingers	Hold	Right Click

✋ Open Palm	Palm facing camera	Scroll down

### Requirements

Python 3.9+

Webcam

Supported OS (Windows / Linux / macOS)

Python dependencies:

opencv-python

mediapipe

pyautogui



### How to Run
pip install -r requirements.txt

python main.py

