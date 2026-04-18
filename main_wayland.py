import cv2
import mediapipe as mp
import time
import os
import subprocess
from datetime import datetime
import numpy as np
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

model_path = 'hand_landmarker.task'

def take_screenshot():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"screenshot_{timestamp}.png"
    
    if os.path.exists('/app'):
        img_dir = "/app/capturas"
    else:
        img_dir = os.path.join(os.getcwd(), "capturas")
        
    if not os.path.exists(img_dir):
        try:
            os.makedirs(img_dir)
        except PermissionError:
            img_dir = "."
            print("Permission denied creating directory, saving to current folder.")

    path = os.path.join(img_dir, filename)

    # List of potential screenshot tools for Wayland/Linux
    tools = [
        ["gnome-screenshot", "-f", path],
        ["grim", path],
        ["spectacle", "-b", "-o", path],
        ["scrot", path]
    ]

    for tool in tools:
        try:
            subprocess.run(tool, check=True, capture_output=True)
            return path
        except (subprocess.CalledProcessError, FileNotFoundError):
            continue

    print("Error: No screenshot tool found.")
    return None

def main():
    print("Starting Gesture Vision (Wayland)...")
    
    permission_granted = False
    def on_mouse_click(event, x, y, flags, param):
        nonlocal permission_granted
        if event == cv2.EVENT_LBUTTONDOWN:
            if 200 <= x <= 400 and 200 <= y <= 250:
                permission_granted = True

    options = vision.HandLandmarkerOptions(
        base_options=python.BaseOptions(model_asset_path=model_path),
        num_hands=1,
        min_hand_detection_confidence=0.7,
        min_hand_presence_confidence=0.7,
        min_tracking_confidence=0.7
    )

    with vision.HandLandmarker.create_from_options(options) as landmarker:
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Error: Could not open camera /dev/video0")
            return

        cv2.namedWindow('Gesture Vision Wayland')
        cv2.setMouseCallback('Gesture Vision Wayland', on_mouse_click)
        
        print("Camera opened successfully. Press 'q' to quit.")
        gesture_start_time = None
        last_capture_time = 0
        cooldown_duration = 3
        detection_duration = 1
        
        while cap.isOpened():
            success, image = cap.read()
            if not success: break

            image = cv2.flip(image, 1)
            
            if not permission_granted:
                overlay = image.copy()
                cv2.rectangle(overlay, (150, 150), (450, 300), (0, 0, 0), -1)
                cv2.putText(overlay, "Permiso de Captura", (180, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
                cv2.rectangle(overlay, (200, 210), (400, 260), (0, 255, 0), -1)
                cv2.putText(overlay, "ACEPTAR", (250, 240), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
                cv2.addWeighted(overlay, 0.7, image, 0.3, 0, image)
                
                cv2.imshow('Gesture Vision Wayland', image)
                if cv2.waitKey(1) & 0xFF == ord('q'): break
                continue

            rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_image)
            results = landmarker.detect(mp_image)

            gesture_detected = False
            if results.hand_landmarks:
                for hand_landmarks in results.hand_landmarks:
                    for lm in hand_landmarks:
                        h, w, _ = image.shape
                        cv2.circle(image, (int(lm.x * w), int(lm.y * h)), 2, (0, 255, 0), -1)

                    index_open = hand_landmarks[8].y < hand_landmarks[6].y
                    middle_open = hand_landmarks[12].y < hand_landmarks[10].y
                    ring_closed = hand_landmarks[16].y > hand_landmarks[14].y
                    pinky_closed = hand_landmarks[20].y > hand_landmarks[18].y
                    
                    if index_open and middle_open and ring_closed and pinky_closed:
                        gesture_detected = True

            if gesture_detected:
                if gesture_start_time is None:
                    gesture_start_time = time.time()
                elif time.time() - gesture_start_time >= detection_duration:
                    if time.time() - last_capture_time >= cooldown_duration:
                        take_screenshot()
                        last_capture_time = time.time()
                        gesture_start_time = None
            else:
                gesture_start_time = None

            if time.time() - last_capture_time < cooldown_duration:
                cv2.putText(image, "Captura guardada!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            if gesture_detected and gesture_start_time:
                progress = min(1.0, (time.time() - gesture_start_time) / detection_duration)
                cv2.rectangle(image, (50, 80), (int(50 + 200 * progress), 100), (255, 0, 0), -1)

            cv2.imshow('Gesture Vision Wayland', image)
            if cv2.waitKey(1) & 0xFF == ord('q'): break

        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
