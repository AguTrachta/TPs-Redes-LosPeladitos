# **Universidad Nacional de Córdoba**
# **Facultad de Ciencias Exactas, Físicas y Naturales**

## **Trabajo Práctico N°5:** Aaa

**Integrantes del Grupo:**
*   Agustin Trachta
*   Agustin Pallardo
*   Mateo Rodriguez
*   Tomas Cisneros
  
**Profesor/a:** SANTIAGO MARTIN HENN

---

# 1 - Scripts para enviar y recibir secuencias de paquetes por TCP

## 1.1 - Tráfico TCP entre dos computadoras

Para esta primera etapa, se han creado estos códigos que enviarán una secuencia incremental cada un segundo, así luego se podrán verificar los datos y el orden en Wireshark. Un servidor será el encargado de recibir los mensajes y procesarlos, mientras esa misma PC será la que recibe los datos por Wireshark. El cliente se conecta al servidor, y una vez establecida la conexión, comienza a transmitir datos.

Código servidor (recibe los datos):

```python
import socket

HOST = '0.0.0.0'  # Escuchar en todas las interfaces
PORT = 8080       # Puerto TCP a usar

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Servidor esperando conexión en {HOST}:{PORT}...")
        conn, addr = s.accept()
        with conn:
            print(f"Conectado con {addr}")
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                print(f"Recibido: {data.decode()}")

if __name__ == "__main__":
    main()
```

Código cliente (transmite los datos):

```python
import socket
import time

GRUPO = "LosPeladitos"  # Nombre del grupo
NUM_PAQUETES = 100      # Número de paquetes a enviar
INTERVALO_SEGUNDOS = 1  # Intervalo entre envíos en segundos

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

```

Mientras se ejecutan ambos scripts, en Wireshark se van registrando los paquetes. Para facilitar la lectura se colocó el filtro "**(eth.dst==b4:6b:fc:9b:a2:26) || (eth.src==b4:6b:fc:9b:a2:26)**" que indica que solamente muestre paquetes que se envían o se reciben a esa dirección MAC. Analizando las capturas, se pueden observar los paquetes transmitidos por el cliente y los ACK de respuesta del servidor.



---

## 1.2 - Tráfico TCP con log de transmisión y recepción

aaa

---

## 1.3 - Métricas de la transmisión TCP

aaa

---

# 2 - Scripts para enviar y recibir secuencias de paquetes por TCP

## 2.1 - Tráfico UDP entre dos computadoras

aaa

---

## 2.2 - Tráfico UDP con log de transmisión y recepción

aaa

---

## 2.3 - Métricas de la transmisión UDP

aaa

