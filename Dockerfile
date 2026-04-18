FROM python:3.12-slim

# Install system dependencies for OpenCV and MediaPipe
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    libgles2 \
    libegl1 \
    wget \
    scrot \
    gnome-screenshot \
    x11-xserver-utils \
    util-linux \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Download the model if it doesn't exist in the context
RUN if [ ! -f hand_landmarker.task ]; then \
    wget -O hand_landmarker.task https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task; \
    fi

# Set environment variable for the display
ENV DISPLAY=:0

CMD ["python", "main_x11.py"]
