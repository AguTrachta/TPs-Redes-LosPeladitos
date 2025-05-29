#!/usr/bin/env python3
import socket
from datetime import datetime
from cryptography.fernet import Fernet

# 1) Carga la misma clave
with open("secret.key", "rb") as f:
    key = f.read()
fcrypto = Fernet(key)

HOST = '0.0.0.0'
PORT = 8081

def log_event(fn, dir, msg):
    ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    with open(fn, 'a') as g:
        g.write(f"[{ts}] {dir}: {msg}\n")

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((HOST, PORT))
    print(f"Servidor UDP escuchando en {HOST}:{PORT}")
    while True:
        data, addr = s.recvfrom(4096)
        # 2) Descifrar
        try:
            plain = fcrypto.decrypt(data)
        except Exception as e:
            print("ERROR descifrando:", e)
            continue
        print(f"{addr} → {plain.decode()}")
        log_event("udp_server_log.txt", "Recibido", plain.decode())

if __name__=="__main__":
    main()
