# Quick Start

## Installation

```bash
pip install gesturevision
```

## System Dependencies

Install required system packages:
```bash
sudo apt-get update && sudo apt-get install -y libgl1 libglib2.0-0 libnotify-bin xdotool ydotool gnome-screenshot scrot
```

Or use the built-in installer:
```bash
gesturevision-start --install-deps
```

## Run

```bash
gesturevision-start
```

## Control Panel

Access the web interface: **http://localhost:8080**

Use the panel to:
- Start/stop the system
- Configure gesture timing
- Add gestures with keyboard shortcuts

## Stop

```bash
gesturevision-stop
```