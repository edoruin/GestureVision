from pydantic import BaseModel
from typing import List, Optional
import json
import os

# Use user home directory for configuration
CONFIG_DIR = os.path.expanduser("~/gesturevision")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")

class Landmark(BaseModel):
    index: int
    x_offset: float = 0.0
    y_offset: float = 0.0

class Gesture(BaseModel):
    name: str
    gesture_type: str = "peace_sign"  # "peace_sign" | "fist" | "open_hand" | "three_fingers" | "pointing_up"
    required_hold_seconds: float = 1.0
    enabled: bool = True
    action: str = "screenshot"  # "screenshot" | "keyboard"
    shortcut: Optional[str] = None

class SwipeConfig(BaseModel):
    enabled: bool = True
    min_distance: float = 0.15
    max_time: float = 0.5

class AppConfig(BaseModel):
    gesture_hold_seconds: float
    cooldown_seconds: float
    gestures: List[Gesture]
    swipe_left_to_right: SwipeConfig = SwipeConfig()
    swipe_right_to_left: SwipeConfig = SwipeConfig()

DEFAULT_CONFIG = AppConfig(
    gesture_hold_seconds=1.0,
    cooldown_seconds=1.5,
    gestures=[
        Gesture(
            name="Paz (captura)",
            gesture_type="peace_sign",
            required_hold_seconds=1.0,
            enabled=True,
            action="screenshot"
        )
    ],
    swipe_left_to_right=SwipeConfig(enabled=True, min_distance=0.15, max_time=0.5),
    swipe_right_to_left=SwipeConfig(enabled=True, min_distance=0.15, max_time=0.5)
)

def load_config() -> AppConfig:
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                data = json.load(f)
                return AppConfig(**data)
        except Exception:
            return DEFAULT_CONFIG
    return DEFAULT_CONFIG

def save_config(config: AppConfig) -> None:
    os.makedirs(CONFIG_DIR, exist_ok=True)
    with open(CONFIG_FILE, "w") as f:
        json.dump(config.model_dump(), f, indent=2)