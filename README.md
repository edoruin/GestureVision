<p align="center">
  <img src="logowithname.png" width="250" alt="Gesture Vision Logo">
</p>

<p align="center">
  <a href="#"><img src="https://img.shields.io/badge/build-passing-brightgreen" alt="Build"></a>
  <a href="#"><img src="https://img.shields.io/badge/Python-3.12-blue" alt="Tech"></a>
  <a href="#"><img src="https://img.shields.io/badge/license-MIT-lightgrey" alt="License"></a>
</p>

| Branch | Version | Status |
| :--- | :--- | :--- |
| `master` | `0.3.0` | ![passing](https://img.shields.io/badge/build-passing-brightgreen) |

| Platform | Python | System Dependencies |
| :--- | :--- | :--- |
| Linux (X11/Wayland) | `3.12+` | `libgl1`, `libglib2.0-0`, `notify-send`, `xdotool`, `ydotool` |
| macOS (ARM64) | `N/A` | `N/A` |
| Windows (x86_64) | `N/A` | `N/A` |

* **Docs:** [Link to documentation]

## Introduction

Gesture Vision is a gesture control system, developed in Python to automate desktop actions through real-time gesture recognition.

The system works through a computer vision pipeline where MediaPipe processes the camera stream to detect hand landmarks, coordinated by an asynchronous FastAPI backend. This provides precise event control with minimal impact on system resources.

## Architecture

![Architecture](architecture.png)

## Main Features

* **High Precision Tracking:** MediaPipe Hand Landmarker implementation for low-latency hand landmark detection.
* **Robust Trigger Control:** Validation system based on gesture hold time and cooldown periods to eliminate false positives.
* **Swipe Gestures:** Workspace switching with horizontal hand movements - left/right.
* **Screenshot Capture:** Detection of the "peace" gesture (index and middle fingers up) to take screenshots.
* **Invisible Mode (Background):** Fully background operation without preview windows, optimizing GPU/CPU usage.
* **Keyboard Shortcuts:** Associate gestures with system shortcuts like ctrl+shift+q to execute any action.
* **X11 and Wayland Support:** Automatically detects whether to use xdotool (X11) or ydotool (Wayland).
* **Native Notifications:** Integration with desktop notification system to instantly confirm actions.
* **Native Deployment:** Simplified installation via `pip` with dedicated CLI commands for service management.
* **Web Panel:** Graphical interface to configure gestures, shortcuts, and timing.

## Quick Start

### 1. Installation
```bash
# Install from PyPI
pip install gesturevision
```

### 2. Run
```bash
# First time: automatically install system dependencies
gesturevision-start --install-deps

# Start the system
gesturevision-start
```

### 4. Control Panel
Access the web panel: **http://localhost:8080**

There you can:
- Start/stop the system
- Configure gesture and cooldown timing
- Add gestures and associate keyboard shortcuts

## Available Gesture Types

| Gesture | Description |
| :--- | :--- |
| ✌️ **Peace** | Index and middle fingers up |
| ✊ **Fist** | Closed hand |
| ✋ **Open Hand** | 5 fingers extended |
| 👍 **Three Fingers** | Index, middle, and ring fingers up |
| ☝️ **Point** | Only index finger up |

## Supported Keyboard Shortcuts

You can use any of the predefined shortcuts or write your own:

- Screenshot: `Print`
- Close window: `alt+F4`
- Minimize all: `super+d`
- Lock screen: `super+l`
- Switch window: `alt+Tab`
- New tab: `ctrl+t`
- Close tab: `ctrl+w`
- Copy/Paste: `ctrl+c` / `ctrl+v`
- And many more...

## Project Structure

- `src/gesturevision/main_vision.py`: Gesture detection and capture engine.
- `src/gesturevision/api/`: FastAPI backend for control and configuration.
- `src/gesturevision/static/`: Control panel user interface.
- `pyproject.toml`: Package dependencies and entry points definition.
- `gesturevision/assets/hand_landmarker.task`: Pre-trained AI model.

## Configuration

Settings are stored in: `~/gesturevision/config.json`

Structure:
```json
{
  "gesture_hold_seconds": 1.0,
  "cooldown_seconds": 1.5,
  "gestures": [
    {
      "name": "Peace (screenshot)",
      "gesture_type": "peace_sign",
      "required_hold_seconds": 1.0,
      "enabled": true,
      "action": "screenshot",
      "shortcut": null
    }
  ]
}
```

## Docker (Optional)

```bash
docker-compose up --build
```

Access the panel at: **http://localhost:8080**
