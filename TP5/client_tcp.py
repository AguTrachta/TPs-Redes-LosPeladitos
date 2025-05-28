import socket
import time

GRUPO = "LosPeladitos" # Nombre del grupo
NUM_PAQUETES = 100     # Número de paquetes a enviar
INTERVALO_SEGUNDOS = 1 # Intervalo entre envíos en segundos

# Dirección del servidor
HOST = '192.168.100.57'
PORT = 8080

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        print(f"Conectado a {HOST}:{PORT}")
        for i in range(1, NUM_PAQUETES + 1):
            mensaje = f"{GRUPO}_PKT_{i}"
            s.sendall(mensaje.encode())
            print(f"Enviado: {mensaje}")
            time.sleep(INTERVALO_SEGUNDOS)

if __name__ == "__main__":
    main()
