import argparse
import subprocess
import sys
import os
import platform
from gesturevision.api.main import main as start_api

def install_system_deps():
    system = platform.system()
    if system != "Linux":
        print(f"Sistema no soportado: {system}")
        return

    print("Instalando dependencias del sistema...")

    packages = ["xdotool", "ydotool", "gnome-screenshot", "scrot"]

    for pkg in packages:
        try:
            subprocess.run(["sudo", "apt", "install", "-y", pkg], check=True)
            print(f"  ✓ {pkg} instalado")
        except subprocess.CalledProcessError:
            print(f"  ✗ Error instalando {pkg}")

def run_foreground():
    print("Iniciando GestureVision en primer plano...")
    try:
        start_api()
    except KeyboardInterrupt:
        print("\nDeteniendo el servidor...")

def run_background():
    print("Iniciando GestureVision en segundo plano...")
    
    # Log file path
    log_dir = os.path.expanduser("~/gesturevision")
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, "api.log")
    
    # We use uvicorn as a module to start the app in a detached process
    # This ensures it runs independently of the current shell
    try:
        with open(log_file, "a") as f:
            subprocess.Popen(
                [sys.executable, "-m", "uvicorn", "gesturevision.api.main:app", "--host", "0.0.0.0", "--port", "8080"],
                stdout=f,
                stderr=f,
                start_new_session=True
            )
        print(f"Sistema iniciado en segundo plano.")
        print(f"Logs disponibles en: {log_file}")
        print("Usa 'gesturevision-stop' para detenerlo.")
    except Exception as e:
        print(f"Error al iniciar en segundo plano: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="GestureVision Control CLI")
    parser.add_argument(
        "--background", "-b", 
        action="store_true", 
        help="Ejecutar el servidor en segundo plano (detached mode)"
    )
    parser.add_argument(
        "--install-deps",
        action="store_true",
        help="Instalar dependencias del sistema (xdotool, ydotool, etc)"
    )

    args = parser.parse_args()

    if args.install_deps:
        install_system_deps()
    elif args.background:
        run_background()
    else:
        run_foreground()

if __name__ == "__main__":
    main()