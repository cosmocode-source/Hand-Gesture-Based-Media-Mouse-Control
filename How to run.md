▶️ How to Run
1️⃣ Start the Server (on your laptop)
cd server
py -3.12 -m uvicorn main:app --host 0.0.0.0 --port 8000

2️⃣ Expose the Server
Option A: Same Wi-Fi (Recommended)
http://<your-laptop-ip>:8000

Option B: Different Network
ngrok http 8000
Copy the HTTPS ngrok link.

3️⃣ Open the Link on the Other Device
Paste the link in a browser
Allow camera permission
Start using gestures
That’s it.

✋ Gesture Controls
🔵 MEDIA MODE (Default)
Gesture	Action
✋ Palm	Play / Pause (toggle, once per gesture)
☝️ One finger	Next track
✌️ Two fingers	Volume down
🤟 Three fingers	Volume up
✋✋✋✋ Four fingers + swipe	Switch tabs
✊ Fist (hold)	Switch to Mouse mode

🖱️ MOUSE MODE
Gesture	Action
☝️ One finger	Move mouse
✌️ Two fingers (hold)	Left click
🤟 Three fingers + up/down	Scroll
✊ Fist (hold)	Switch to Media mode

⏱️ Latency Notes
WebSockets are used for low latency.
Best performance when both devices are on the same Wi-Fi.
ngrok adds some delay but is still usable.
Mouse and scroll gestures are motion-based and feel natural.

🧯 Safety Notes
PyAutoGUI FAILSAFE is disabled for smooth control.
To regain control:
Close the browser tab
Stop the server (Ctrl + C)
Gestures only work while the browser tab is open.

🐞 Troubleshooting

Camera not starting
Check browser camera permissions
Use HTTPS (required on mobile)
Mouse/scroll not smooth
Move hand slowly and steadily
Keep hand inside the camera frame
Reduce background clutter
High latency
Prefer local IP over ngrok
Ensure WebSocket connection is active

🚀 Future Improvements (Optional)

WebRTC for ultra-low latency
Gesture sensitivity calibration
Smoothing filters (EMA)
On-screen gesture indicators
Multi-user authentication

✅ Status

✔ Real-time
✔ Stable
✔ WebSocket-based
✔ Feature-complete

This is a proper distributed human–computer interaction system, not a demo.
Enjoy controlling your computer with your hands. 🖐️