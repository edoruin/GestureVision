import os
import signal
import sys

def main():
    pid_file = os.path.expanduser("~/gesturevision/api.pid")
    
    if not os.path.exists(pid_file):
        print("El sistema no está en ejecución (no se encontró el archivo api.pid).")
        sys.exit(0)
        
    try:
        with open(pid_file, "r") as f:
            pid = int(f.read().strip())
            
        # Kill the process group or the process itself
        os.kill(pid, signal.SIGTERM)
        print(f"Deteniendo el sistema (PID {pid})...")
        
        # Remove pid file
        os.remove(pid_file)
        print("Sistema detenido correctamente.")
        
    except ProcessLookupError:
        print("El proceso ya no existe, limpiando archivo de PID.")
        os.remove(pid_file)
    except Exception as e:
        print(f"Error al detener el sistema: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()