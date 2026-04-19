import cv2
import mediapipe as mp
import mss
import time
import os
from datetime import datetime
import numpy as np
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from gesturevision.api.config import load_config
import logging

LOG_FILE = os.path.expanduser("~/gesturevision/log.txt")

def log(msg):
    with open(LOG_FILE, "a") as f:
        f.write(f"{datetime.now().strftime('%H:%M:%S')} - {msg}\n")

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(CURRENT_DIR, "assets", "hand_landmarker.task")

log("=== Starting Gesture Vision ===")

def ensure_xdotool():
    import subprocess
    try:
        subprocess.run(["xdotool", "--version"], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("xdotool not found. Please install: sudo apt-get install xdotool")
        return False

class KeyboardSimulator:
    def __init__(self):
        self.tool = self._detect_tool()
        log(f"KeyboardSimulator: using {self.tool}")

    def _detect_tool(self) -> str:
        import subprocess
        import os
        if os.environ.get("WAYLAND_DISPLAY"):
            try:
                subprocess.run(["ydotool", "key", "0"], capture_output=True, check=True)
                return "ydotool"
            except (subprocess.CalledProcessError, FileNotFoundError):
                pass
        try:
            subprocess.run(["xdotool", "key", "0"], capture_output=True, check=True)
            return "xdotool"
        except (subprocess.CalledProcessError, FileNotFoundError):
            return "none"

    def press_key(self, shortcut: str) -> bool:
        import subprocess
        import os
        if self.tool == "none":
            log(f"No keyboard simulator available")
            return False

        try:
            env = os.environ.copy()
            if self.tool == "xdotool":
                if "DISPLAY" not in env:
                    env["DISPLAY"] = ":0"
                if "XAUTHORITY" in os.environ:
                    env["XAUTHORITY"] = os.environ["XAUTHORITY"]
                subprocess.run(["xhost", "+local:"], capture_output=True, env=env)

            result = subprocess.run(
                [self.tool, "key", shortcut],
                capture_output=True,
                env=env
            )
            log(f"Executed shortcut via {self.tool}: {shortcut}, stdout: {result.stdout}, stderr: {result.stderr}")
            return result.returncode == 0
        except Exception as e:
            log(f"Failed to execute shortcut: {e}")
            return False

_keyboard_sim = None

def execute_keyboard_shortcut(shortcut: str):
    global _keyboard_sim
    if _keyboard_sim is None:
        _keyboard_sim = KeyboardSimulator()

    if _keyboard_sim.press_key(shortcut):
        import subprocess
        subprocess.run(["notify-send", "GestureVision", f"Atajo ejecutado: {shortcut}"], capture_output=True)

def take_screenshot():
    import subprocess
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"screenshot_{timestamp}.png"
    
    img_dir = os.path.join(os.path.expanduser("~"), "gesturevision", "capturas")
    
    if not os.path.exists(img_dir):
        try:
            os.makedirs(img_dir)
        except PermissionError:
            img_dir = "."
            print("Permission denied creating directory, saving to current folder.")

    path = os.path.join(img_dir, filename)

    tools = [
        ["gnome-screenshot", "-f", path],
        ["scrot", path],
    ]
    for tool in tools:
        try:
            subprocess.run(tool, check=True, capture_output=True)
            print(f"Screenshot captured using {tool[0]}")
            subprocess.run(["notify-send", "GestureVision", "¡La captura ha sido tomada!"], capture_output=True)
            return path
        except (subprocess.CalledProcessError, FileNotFoundError):
            continue

    try:
        with mss.mss() as sct:
            monitor = sct.monitors[1]
            screenshot = sct.grab(monitor)
            mss.tools.to_png(screenshot.rgb, screenshot.size, output=path)
            print("Screenshot captured using mss")
            subprocess.run(["notify-send", "GestureVision", "¡La captura ha sido tomada!"], capture_output=True)
            return path
    except Exception as e:
        print(f"mss failed ({e})")
    
    print("All screenshot methods failed.")
    return None

def check_gesture(hand_landmarks) -> str:
    finger_checks = [
        (8, 6, "index"),
        (12, 10, "middle"),
        (16, 14, "ring"),
        (20, 18, "pinky")
    ]
    
    fingers = {}
    finger_positions = []
    for tip_idx, pip_idx, name in finger_checks:
        tip_y = hand_landmarks[tip_idx].y
        pip_y = hand_landmarks[pip_idx].y
        is_up = tip_y < pip_y
        fingers[name] = is_up
        finger_positions.append(f"{name}={is_up}({tip_y:.2f}<{pip_y:.2f})")
    
    # Only log occasionally
    import random
    if random.random() < 0.01:
        log(f"Fingers: {', '.join(finger_positions)}")
    
    gesture_patterns = {
        "peace_sign": {"index": True, "middle": True, "ring": False, "pinky": False},
        "fist": {"index": False, "middle": False, "ring": False, "pinky": False},
        "open_hand": {"index": True, "middle": True, "ring": True, "pinky": True},
        "three_fingers": {"index": True, "middle": True, "ring": True, "pinky": False},
        "pointing_up": {"index": True, "middle": False, "ring": False, "pinky": False},
    }
    
    for gesture_name, pattern in gesture_patterns.items():
        if fingers == pattern:
            return gesture_name
    
    return "unknown"

def main():
    log("Starting Gesture Vision (Background Mode)...")
    
    # Ensure X11 permissions
    import subprocess
    subprocess.run(["xhost", "+local:"], capture_output=True)
    
    ensure_xdotool()
    config = load_config()
    log(f"Config loaded. Gestures: {[g.name + '(' + g.gesture_type + ')' for g in config.gestures]}")
    
    options = vision.HandLandmarkerOptions(
        base_options=python.BaseOptions(model_asset_path=model_path),
        num_hands=1,
        min_hand_detection_confidence=0.5,
        min_hand_presence_confidence=0.5,
        min_tracking_confidence=0.5
    )

    with vision.HandLandmarker.create_from_options(options) as landmarker:
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Error: Could not open camera")
            return

        print("System active in background. Press Ctrl+C in the terminal to quit.")
        gesture_start_time = None
        last_action_time = 0
        last_detected = None
        
        while cap.isOpened():
            success, image = cap.read()
            if not success: break

            rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            rgb_image = cv2.flip(rgb_image, 1)
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_image)
            results = landmarker.detect(mp_image)

            current_gesture = None
            
            if results.hand_landmarks:
                for hand_landmarks in results.hand_landmarks:
                    detected = check_gesture(hand_landmarks)
                    if detected != "unknown":
                        current_gesture = detected
            
            if current_gesture:
                if current_gesture != "unknown":
                    log(f"Detected: {current_gesture}")
            
            if current_gesture:
                # Match by gesture_type
                matched_gesture = None
                for g in config.gestures:
                    if g.gesture_type == current_gesture and g.enabled:
                        matched_gesture = g
                        break
                
                if matched_gesture:
                    # Only reset timer when gesture CHANGES
                    if current_gesture and current_gesture != last_detected:
                        log(f"New: {current_gesture} (last={last_detected})")
                        gesture_start_time = time.time()
                        last_detected = current_gesture
                    elif current_gesture == last_detected and gesture_start_time:
                        # Same gesture - check hold time
                        hold_time = time.time() - gesture_start_time
                        cooldown_ok = time.time() - last_action_time >= config.cooldown_seconds
                        
                        if hold_time >= matched_gesture.required_hold_seconds and cooldown_ok:
                            log(f"Action triggered: {matched_gesture.action}")
                            if matched_gesture.action == "screenshot":
                                take_screenshot()
                            elif matched_gesture.action == "keyboard" and matched_gesture.shortcut:
                                log(f"Executing shortcut: {matched_gesture.shortcut}")
                                execute_keyboard_shortcut(matched_gesture.shortcut)
                            last_action_time = time.time()
                            gesture_start_time = None
                            last_detected = None
                else:
                    last_detected = None

        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()