# 🖐️ Gesture Vision (Docker Edition)

Gesture Vision es una herramienta de automatización basada en visión artificial que permite tomar capturas de pantalla del escritorio mediante el reconocimiento de gestos con la cámara web, ejecutándose enteramente dentro de un contenedor Docker para facilitar su despliegue.

## 🚀 Características

- **Rastreo de Manos en Tiempo Real**: Utiliza MediaPipe para detectar puntos clave de la mano con alta precisión.
- **Gesto de Activación**: Detecta el **"Signo de la Paz"** (dedos índice y medio extendidos, anular y meñique cerrados) para disparar la captura.
- **Sistema de Permisos**: Incluye una pantalla de consentimiento interactiva al inicio para asegurar que el usuario autorice la captura de pantalla.
- **Control de Spam**: Implementa un sistema de cooldown de 3 segundos y un tiempo de mantenimiento del gesto (1 segundo) para evitar capturas accidentales.
- **Aislamiento Total**: Despliegue simplificado mediante Docker, evitando conflictos de dependencias en el sistema host.
- **Almacenamiento Organizado**: Las capturas se guardan automáticamente en la carpeta `/capturas` en la raíz del proyecto.

## 🛠️ Requisitos Previos

- **Docker** y **Docker Compose** instalados.
- Una cámara web funcional conectada al sistema.

## 💻 Uso y Despliegue

Para ejecutar Gesture Vision, sigue estos pasos en tu terminal:

### 1. Permitir acceso al servidor gráfico
Para que el contenedor pueda mostrar la ventana de la cámara en tu pantalla, debes ejecutar:
```bash
xhost +local:docker
```

### 2. Iniciar la aplicación
Desde la raíz del proyecto, ejecuta el siguiente comando para construir e iniciar el contenedor:
```bash
docker compose up --build
```

### 3. Interactuar con el sistema
- **Permiso**: Al iniciar, verás una ventana con la cámara. Haz clic en el botón **"ACEPTAR"** para habilitar la función de capturas.
- **Gesto**: Realiza el signo de la paz frente a la cámara durante 1 segundo.
- **Salir**: Presiona la tecla `q` en la ventana de video para cerrar la aplicación.

## 📂 Estructura del Proyecto
- `main_x11.py`: Núcleo de la aplicación ejecutado dentro del contenedor.
- `requirements.txt`: Dependencias de Python.
- `Dockerfile`: Configuración de la imagen (Librerías GL, EGL y herramientas de captura).
- `docker-compose.yml`: Orquestación del contenedor (mapeo de cámara, pantalla y volúmenes).
- `hand_landmarker.task`: Modelo pre-entrenado de detección de manos.
- `LICENSE`: Licencia MIT.
