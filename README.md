# 🎮 Hand Gesture Controlled Media & Mouse (WebSocket Version)

A real-time hand gesture control system that lets you control **media playback, mouse movement, scrolling, and tab switching** on your laptop using **hand gestures from another device’s camera**.

The system uses:
- **MediaPipe Hands** (browser-side hand tracking)
- **FastAPI + WebSockets** (low-latency communication)
- **PyAutoGUI** (OS-level control)

Only the **server laptop** controls the system.

The **other device** is just a camera + browser.

## 🧠 How It Works (High-Level)

<img width="379" height="264" alt="image" src="https://github.com/user-attachments/assets/54053781-d7aa-4e48-b43d-6c913ecfadbc" />


- The browser detects the hand and classifies gestures.
- Gestures + finger position are streamed via **WebSockets**.
- 
- The server interprets gestures and performs OS actions.
- 
- WebSockets are used to minimize latency.

<img width="481" height="298" alt="image" src="https://github.com/user-attachments/assets/63fba881-1988-40d3-8299-1906819fef90" />


## ⚙️ Requirements

### Server Laptop (Controlled Device)

- Python **3.10+**
- Windows / macOS / Linux
- Keyboard & mouse access

Install dependencies:

py -3.12 -m pip install fastapi uvicorn pyautogui

py -3.12 -m pip install uvicorn[standard]
