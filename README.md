# 🖐️ Gesture Vision

Gesture Vision es una herramienta de automatización basada en visión artificial que permite tomar capturas de pantalla del escritorio mediante el reconocimiento de gestos con la cámara web.

## 🚀 Características

- **Rastreo de Manos en Tiempo Real**: Utiliza MediaPipe para detectar puntos clave de la mano con alta precisión.
- **Gesto de Activación**: Detecta el "Signo de la Paz" (dedos índice y medio extendidos) para disparar la captura.
- **Sistema de Permisos**: Incluye una pantalla de consentimiento interactiva al inicio para asegurar que el usuario autorice la captura de pantalla.
- **Soporte Multi-entorno**: Incluye scripts específicos para sesiones de **X11** y **Wayland** en Linux.
- **Control de Spam**: Implementa un sistema de cooldown de 3 segundos y un tiempo de mantenimiento del gesto (1 segundo) para evitar capturas accidentales.
- **Contenerización**: Listo para ejecutar en Docker con acceso al hardware de video.
- **Almacenamiento Organizado**: Las capturas se guardan automáticamente en la carpeta `/capturas` en la raíz del proyecto.

## 🛠️ Instalación

### Requisitos previos
- Python 3.12+
- Cámara web funcional.

### Instalación local
1. Clona el repositorio o descarga los archivos.
2. Crea y activa un entorno virtual:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```
3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
4. Descarga el modelo de MediaPipe `hand_landmarker.task` (si no está presente).

## 💻 Uso

Para saber qué script ejecutar, verifica tu tipo de sesión:
```bash
echo $XDG_SESSION_TYPE
```

- **Si es `x11`**:
  ```bash
  python main_x11.py
  ```
- **Si es `wayland`**:
  ```bash
  python main_wayland.py
  ```

*Al iniciar, haz clic en el botón **"ACEPTAR"** en la pantalla para habilitar las capturas. Presiona la tecla `q` en la ventana de video para salir.*

## 🐳 Ejecución con Docker

Para ejecutar la aplicación en un contenedor aislado:

1. Permite el acceso al servidor X:
   ```bash
   xhost +local:docker
   ```
2. Inicia el contenedor:
   ```bash
   docker compose up --build
   ```

## 📂 Estructura del Proyecto
- `main_x11.py`: Versión optimizada para X11 usando `mss` y herramientas de respaldo.
- `main_wayland.py`: Versión compatible con Wayland usando herramientas del sistema.
- `requirements.txt`: Dependencias del proyecto.
- `Dockerfile` & `docker-compose.yml`: Configuración de despliegue en Docker.
- `hand_landmarker.task`: Modelo pre-entrenado de detección de manos.
- `LICENSE`: Licencia MIT.
