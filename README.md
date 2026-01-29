# 🎮 Hand Gesture Controlled Media & Mouse (WebSocket Version)

A real-time hand gesture control system that lets you control **media playback, mouse movement, scrolling, and tab switching** on your laptop using **hand gestures from another device’s camera**.

The system uses:
- **MediaPipe Hands** (browser-side hand tracking)
- **FastAPI + WebSockets** (low-latency communication)
- **PyAutoGUI** (OS-level control)

Only the **server laptop** controls the system.  
The **other device** is just a camera + browser.

## 🧠 How It Works (High-Level)

Other Device (Browser + Camera)
|
| WebSocket (gesture + x,y)
v
Server Laptop (FastAPI + PyAutoGUI)
|
├── Media Control (play, volume, next)
├── Mouse Control (move, click, scroll)
└── Tab Switching (swipe)


- The browser detects the hand and classifies gestures.
- Gestures + finger position are streamed via **WebSockets**.
- The server interprets gestures and performs OS actions.
- WebSockets are used to minimize latency.

## 📁 Project Structure

Hand Gesture Detection Site/
│
├── server/
│ └── main.py # FastAPI + WebSocket server
│
└── web/
├── index.html # UI + camera
└── app.js # MediaPipe + WebSocket clien

## ⚙️ Requirements

### Server Laptop (Controlled Device)
- Python **3.10+**
- Windows / macOS / Linux
- Keyboard & mouse access

Install dependencies:

py -3.12 -m pip install fastapi uvicorn pyautogui
py -3.12 -m pip install uvicorn[standard]
