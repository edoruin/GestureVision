from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Optional
import subprocess
import json
import os
import sys
import signal

from gesturevision.api.config import AppConfig, Gesture, Landmark, load_config, save_config, DEFAULT_CONFIG

app = FastAPI(title="GestureVision API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# State to keep track of the vision process
vision_process: Optional[subprocess.Popen] = None

class StatusResponse(BaseModel):
    running: bool
    pid: Optional[int] = None
    status: str

def get_vision_status() -> StatusResponse:
    global vision_process
    if vision_process and vision_process.poll() is None:
        return StatusResponse(running=True, pid=vision_process.pid, status="running")
    return StatusResponse(running=False, status="stopped")

@app.on_event("startup")
async def startup_event():
    # Write PID to file on startup
    pid_file = os.path.expanduser("~/gesturevision/api.pid")
    os.makedirs(os.path.dirname(pid_file), exist_ok=True)
    with open(pid_file, "w") as f:
        f.write(str(os.getpid()))

@app.get("/api/x11-status")
async def check_x11():
    try:
        # Now we check natively if X11 is accessible
        result = subprocess.run(
            ["xset", "q"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            return {"accessible": True, "message": "X11 server accessible"}
        return {"accessible": False, "message": "X11 server not accessible. Please run 'xhost +local:docker' or check your X server."}
    except Exception as e:
        return {"accessible": False, "message": f"Error checking X11: {str(e)}"}

@app.get("/", response_class=FileResponse)
async def root():
    # Dynamic path for static files in the package
    static_path = os.path.join(os.path.dirname(__file__), "..", "static", "index.html")
    return static_path

@app.get("/api/status", response_model=StatusResponse)
async def status():
    return get_vision_status()

@app.post("/api/start")
async def start():
    global vision_process
    status = get_vision_status()
    if status.running:
        return {"message": "Vision system already running", "running": True}
    
    try:
        subprocess.run(["xhost", "+local:docker"], capture_output=True)
        
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        vision_script = os.path.join(base_dir, "main_vision.py")
        
        vision_process = subprocess.Popen(
            [sys.executable, vision_script],
            stdout=open("/tmp/vision_stdout.log", "w"),
            stderr=subprocess.STDOUT,
            text=True
        )
        return {"message": "Vision system started", "running": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/stop")
async def stop():
    global vision_process
    status = get_vision_status()
    if not status.running:
        return {"message": "Vision system already stopped", "running": False}
    
    try:
        vision_process.terminate()
        vision_process.wait(timeout=10)
        vision_process = None
        return {"message": "Vision system stopped", "running": False}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/config", response_model=AppConfig)
async def get_config():
    return load_config()

@app.post("/api/config")
async def set_config(config: AppConfig):
    save_config(config)
    return {"message": "Configuration saved", "config": config}

@app.get("/api/gestures", response_model=List[Gesture])
async def get_gestures():
    cfg = load_config()
    return cfg.gestures

@app.post("/api/gestures")
async def add_gesture(gesture: Gesture):
    cfg = load_config()
    gesture_exists = any(g.name == gesture.name for g in cfg.gestures)
    if gesture_exists:
        cfg.gestures = [g if g.name != gesture.name else gesture for g in cfg.gestures]
    else:
        cfg.gestures.append(gesture)
    save_config(cfg)
    return {"message": "Gesture saved", "gesture": gesture}

@app.delete("/api/gestures/{gesture_name}")
async def delete_gesture(gesture_name: str):
    cfg = load_config()
    cfg.gestures = [g for g in cfg.gestures if g.name != gesture_name]
    save_config(cfg)
    return {"message": f"Gesture {gesture_name} deleted"}

def main():
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)

if __name__ == "__main__":
    main()