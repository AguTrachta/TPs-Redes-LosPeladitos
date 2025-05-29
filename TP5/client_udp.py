#!/usr/bin/env python3
import socket
import time
from datetime import datetime

GRUPO = "LosPeladitos"
NUM_PAQUETES = 100
INTERVALO_SEGUNDOS = 1.0

# Cambia esta IP por la de tu notebook (servidor)
HOST = '192.168.1.56'
PORT = 8081

def log_event(filename, direction, message):
    ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    with open(filename, 'a') as f:
        f.write(f"[{ts}] {direction}: {message}\n")

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        for i in range(1, NUM_PAQUETES + 1):
            msg = f"{GRUPO}_PKT_{i}"
            s.sendto(msg.encode(), (HOST, PORT))
            print(f"Enviado: {msg}")
            log_event("udp_client_log.txt", "Enviado", msg)
            time.sleep(INTERVALO_SEGUNDOS)

if __name__ == "__main__":
    main()
