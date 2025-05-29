#!/usr/bin/env python3
import socket, time
from datetime import datetime
from cryptography.fernet import Fernet

# 1) Carga la clave
with open("secret.key", "rb") as f:
    key = f.read()
fcrypto = Fernet(key)

GRUPO = "LosPeladitos"
NUM_PAQUETES = 100
INTERVALO = 1.0
HOST = '192.168.1.56'
PORT = 8081

def log_event(fn, dir, msg):
    ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    with open(fn, 'a') as g:
        g.write(f"[{ts}] {dir}: {msg}\n")

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    for i in range(1, NUM_PAQUETES+1):
        texto = f"{GRUPO}_PKT_{i}".encode()
        # 2) Cifrar
        cipher = fcrypto.encrypt(texto)
        s.sendto(cipher, (HOST, PORT))
        print(f"Enviado (hex): {cipher.hex()}")
        log_event("udp_client_log.txt", "Enviado", cipher.hex())
        time.sleep(INTERVALO)
    s.close()

if __name__=="__main__":
    main()
