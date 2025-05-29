#!/usr/bin/env python3
import socket
from datetime import datetime

HOST = '0.0.0.0'   # Escucha en todas las interfaces
PORT = 8081        # Puerto UDP para recibir datagramas

def log_event(filename, direction, message):
    ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    with open(filename, 'a') as f:
        f.write(f"[{ts}] {direction}: {message}\n")

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind((HOST, PORT))
        print(f"Servidor UDP escuchando en {HOST}:{PORT}…")
        while True:
            data, addr = s.recvfrom(1024)
            if not data:
                continue
            msg = data.decode()
            print(f"{addr} → {msg}")
            log_event("udp_server_log.txt", "Recibido", msg)

if __name__ == "__main__":
    main()
