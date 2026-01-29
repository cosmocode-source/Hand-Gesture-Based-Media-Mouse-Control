# Hand Gesture–Based Media & Mouse Control
This repository explores controlling a computer using hand gestures instead of physical input devices.
The system uses real-time hand tracking to convert finger movements into media controls and mouse actions at the operating-system level.
The same idea is implemented in two different architectures, each placed in its own branch to clearly separate design decisions and execution models.

# Repository Structure (by branch)
Branch	Description
local-cam:	Fully local gesture control using the laptop’s webcam
remote-webcam:	Browser-based camera input controlling a remote machine
main:	Documentation and project overview

The main branch does not contain runnable code.
It exists to explain the system and guide users to the correct implementation branch.

# System Capabilities (Common to Both Versions)

Real-time hand detection and tracking
Gesture-based media control (play, pause, next, volume)
Gesture-based mouse control (move, click, scroll)
Mode switching using hand gestures
No external hardware required

# Branch Selection Guide

Want low latency, offline, maximum reliability → local-cam
Want remote control from another device → remote-webcam
