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

Paquete del cliente:

![Captura desde 2025-05-27 21-52-04](https://github.com/user-attachments/assets/fe7d98f1-a399-419f-ac36-1d4252beecd2)

Respuesta del servidor:

![Captura desde 2025-05-27 21-57-38](https://github.com/user-attachments/assets/24f8c0d5-af62-44a5-afd5-554947dd7731)

Carga útil:

![Captura desde 2025-05-27 22-07-47](https://github.com/user-attachments/assets/95aba04b-585e-450d-8c74-42014b6aa616)


---

## 1.2 - Tráfico TCP con log de transmisión y recepción

Modificando el código, ahora registramos los datos de la comunicación en un log. Además, se disminuyó el tiempo de espera entre transmisiones a 1 ms.

Código servidor:

```python
import socket
from datetime import datetime

HOST = '0.0.0.0'  # Escuchar en todas las interfaces
PORT = 8080       # Puerto TCP a usar

def log_event(message):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    with open("tcp_server_log.txt", "a") as log:
        log.write(f"[{timestamp}] Recibido: {message}\n")

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
                mensaje = data.decode()
                print(f"Recibido: {mensaje}")
                log_event(mensaje)

if __name__ == "__main__":
    main()
```

Código cliente:

```python
import socket
import time
from datetime import datetime

GRUPO = "LosPeladitos" # Nombre del grupo
NUM_PAQUETES = 100     # Número de paquetes a enviar
INTERVALO_SEGUNDOS = 1 # Intervalo entre envíos en segundos

# Dirección del servidor
HOST = '192.168.100.57'
PORT = 8080

def log_event(message):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    with open("tcp_client_log.txt", "a") as log:
        log.write(f"[{timestamp}] Enviado: {message}\n")

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        print(f"Conectado a {HOST}:{PORT}")
        for i in range(1, NUM_PAQUETES + 1):
            mensaje = f"{GRUPO}_PKT_{i}"
            s.sendall(mensaje.encode())
            print(f"Enviado: {mensaje}")
            log_event(mensaje)
            #time.sleep(INTERVALO_SEGUNDOS)

if __name__ == "__main__":
    main()

```

---

## 1.3 - Métricas de la transmisión TCP

Los logs obtenidos contienen lo siguiente:

Log del servidor:

```
[2025-05-27 23:13:25.158333] Recibido: LosPeladitos_PKT_1
[2025-05-27 23:13:25.159603] Recibido: LosPeladitos_PKT_2
[2025-05-27 23:13:25.161288] Recibido: LosPeladitos_PKT_3
[2025-05-27 23:13:25.162574] Recibido: LosPeladitos_PKT_4
[2025-05-27 23:13:25.163690] Recibido: LosPeladitos_PKT_5
[2025-05-27 23:13:25.165069] Recibido: LosPeladitos_PKT_6
[2025-05-27 23:13:25.166531] Recibido: LosPeladitos_PKT_7
[2025-05-27 23:13:25.167442] Recibido: LosPeladitos_PKT_8
[2025-05-27 23:13:25.169085] Recibido: LosPeladitos_PKT_9
[2025-05-27 23:13:25.170409] Recibido: LosPeladitos_PKT_10
[2025-05-27 23:13:25.171763] Recibido: LosPeladitos_PKT_11
[2025-05-27 23:13:25.173196] Recibido: LosPeladitos_PKT_12
[2025-05-27 23:13:25.173890] Recibido: LosPeladitos_PKT_13
[2025-05-27 23:13:25.175404] Recibido: LosPeladitos_PKT_14
[2025-05-27 23:13:25.176909] Recibido: LosPeladitos_PKT_15
[2025-05-27 23:13:25.178387] Recibido: LosPeladitos_PKT_16
[2025-05-27 23:13:25.179954] Recibido: LosPeladitos_PKT_17
[2025-05-27 23:13:25.180899] Recibido: LosPeladitos_PKT_18
[2025-05-27 23:13:25.182827] Recibido: LosPeladitos_PKT_19
[2025-05-27 23:13:25.184773] Recibido: LosPeladitos_PKT_20LosPeladitos_PKT_21
[2025-05-27 23:13:25.186377] Recibido: LosPeladitos_PKT_22
[2025-05-27 23:13:25.187975] Recibido: LosPeladitos_PKT_23
[2025-05-27 23:13:25.189570] Recibido: LosPeladitos_PKT_24
[2025-05-27 23:13:25.190940] Recibido: LosPeladitos_PKT_25
[2025-05-27 23:13:25.192329] Recibido: LosPeladitos_PKT_26
[2025-05-27 23:13:25.193926] Recibido: LosPeladitos_PKT_27
[2025-05-27 23:13:25.194529] Recibido: LosPeladitos_PKT_28
[2025-05-27 23:13:25.196001] Recibido: LosPeladitos_PKT_29
[2025-05-27 23:13:25.197311] Recibido: LosPeladitos_PKT_30
[2025-05-27 23:13:25.198830] Recibido: LosPeladitos_PKT_31
[2025-05-27 23:13:25.199846] Recibido: LosPeladitos_PKT_32
[2025-05-27 23:13:25.201215] Recibido: LosPeladitos_PKT_33
[2025-05-27 23:13:25.202790] Recibido: LosPeladitos_PKT_34
[2025-05-27 23:13:25.204164] Recibido: LosPeladitos_PKT_35
[2025-05-27 23:13:25.205861] Recibido: LosPeladitos_PKT_36
[2025-05-27 23:13:25.206438] Recibido: LosPeladitos_PKT_37
[2025-05-27 23:13:25.207931] Recibido: LosPeladitos_PKT_38
[2025-05-27 23:13:25.209415] Recibido: LosPeladitos_PKT_39
[2025-05-27 23:13:25.210837] Recibido: LosPeladitos_PKT_40
[2025-05-27 23:13:25.212398] Recibido: LosPeladitos_PKT_41
[2025-05-27 23:13:25.214592] Recibido: LosPeladitos_PKT_42LosPeladitos_PKT_43
[2025-05-27 23:13:25.216321] Recibido: LosPeladitos_PKT_44
[2025-05-27 23:13:25.217611] Recibido: LosPeladitos_PKT_45
[2025-05-27 23:13:25.219215] Recibido: LosPeladitos_PKT_46
[2025-05-27 23:13:25.220734] Recibido: LosPeladitos_PKT_47
[2025-05-27 23:13:25.221513] Recibido: LosPeladitos_PKT_48
[2025-05-27 23:13:25.223090] Recibido: LosPeladitos_PKT_49
[2025-05-27 23:13:25.224551] Recibido: LosPeladitos_PKT_50
[2025-05-27 23:13:25.225348] Recibido: LosPeladitos_PKT_51
[2025-05-27 23:13:25.226873] Recibido: LosPeladitos_PKT_52
[2025-05-27 23:13:25.228344] Recibido: LosPeladitos_PKT_53
[2025-05-27 23:13:25.229759] Recibido: LosPeladitos_PKT_54
[2025-05-27 23:13:25.230663] Recibido: LosPeladitos_PKT_55
[2025-05-27 23:13:25.233043] Recibido: LosPeladitos_PKT_56LosPeladitos_PKT_57
[2025-05-27 23:13:25.234681] Recibido: LosPeladitos_PKT_58
[2025-05-27 23:13:25.236151] Recibido: LosPeladitos_PKT_59
[2025-05-27 23:13:25.237993] Recibido: LosPeladitos_PKT_60
[2025-05-27 23:13:25.238674] Recibido: LosPeladitos_PKT_61
[2025-05-27 23:13:25.239915] Recibido: LosPeladitos_PKT_62
[2025-05-27 23:13:25.241722] Recibido: LosPeladitos_PKT_63
[2025-05-27 23:13:25.242400] Recibido: LosPeladitos_PKT_64
[2025-05-27 23:13:25.244064] Recibido: LosPeladitos_PKT_65
[2025-05-27 23:13:25.245694] Recibido: LosPeladitos_PKT_66
[2025-05-27 23:13:25.246391] Recibido: LosPeladitos_PKT_67
[2025-05-27 23:13:25.247884] Recibido: LosPeladitos_PKT_68
[2025-05-27 23:13:25.249410] Recibido: LosPeladitos_PKT_69
[2025-05-27 23:13:25.250706] Recibido: LosPeladitos_PKT_70
[2025-05-27 23:13:25.252233] Recibido: LosPeladitos_PKT_71
[2025-05-27 23:13:25.253719] Recibido: LosPeladitos_PKT_72
[2025-05-27 23:13:25.255063] Recibido: LosPeladitos_PKT_73
[2025-05-27 23:13:25.255765] Recibido: LosPeladitos_PKT_74
[2025-05-27 23:13:25.257271] Recibido: LosPeladitos_PKT_75
[2025-05-27 23:13:25.258623] Recibido: LosPeladitos_PKT_76
[2025-05-27 23:13:25.259992] Recibido: LosPeladitos_PKT_77
[2025-05-27 23:13:25.260709] Recibido: LosPeladitos_PKT_78
[2025-05-27 23:13:25.262620] Recibido: LosPeladitos_PKT_79
[2025-05-27 23:13:25.263562] Recibido: LosPeladitos_PKT_80
[2025-05-27 23:13:25.264808] Recibido: LosPeladitos_PKT_81
[2025-05-27 23:13:25.266064] Recibido: LosPeladitos_PKT_82
[2025-05-27 23:13:25.267731] Recibido: LosPeladitos_PKT_83
[2025-05-27 23:13:25.268442] Recibido: LosPeladitos_PKT_84
[2025-05-27 23:13:25.269925] Recibido: LosPeladitos_PKT_85
[2025-05-27 23:13:25.271270] Recibido: LosPeladitos_PKT_86
[2025-05-27 23:13:25.272613] Recibido: LosPeladitos_PKT_87
[2025-05-27 23:13:25.274699] Recibido: LosPeladitos_PKT_88
[2025-05-27 23:13:25.275889] Recibido: LosPeladitos_PKT_89
[2025-05-27 23:13:25.276565] Recibido: LosPeladitos_PKT_90
[2025-05-27 23:13:25.278118] Recibido: LosPeladitos_PKT_91
[2025-05-27 23:13:25.278821] Recibido: LosPeladitos_PKT_92
[2025-05-27 23:13:25.280498] Recibido: LosPeladitos_PKT_93
[2025-05-27 23:13:25.281941] Recibido: LosPeladitos_PKT_94
[2025-05-27 23:13:25.283746] Recibido: LosPeladitos_PKT_95
[2025-05-27 23:13:25.286818] Recibido: LosPeladitos_PKT_96LosPeladitos_PKT_97
[2025-05-27 23:13:25.287430] Recibido: LosPeladitos_PKT_98
[2025-05-27 23:13:25.288803] Recibido: LosPeladitos_PKT_99
[2025-05-27 23:13:25.290179] Recibido: LosPeladitos_PKT_100
```

Log del cliente:

```
[2025-05-27 23:13:25.094974] Enviado: LosPeladitos_PKT_1
[2025-05-27 23:13:25.096352] Enviado: LosPeladitos_PKT_2
[2025-05-27 23:13:25.097654] Enviado: LosPeladitos_PKT_3
[2025-05-27 23:13:25.098991] Enviado: LosPeladitos_PKT_4
[2025-05-27 23:13:25.100252] Enviado: LosPeladitos_PKT_5
[2025-05-27 23:13:25.101582] Enviado: LosPeladitos_PKT_6
[2025-05-27 23:13:25.102835] Enviado: LosPeladitos_PKT_7
[2025-05-27 23:13:25.104171] Enviado: LosPeladitos_PKT_8
[2025-05-27 23:13:25.105508] Enviado: LosPeladitos_PKT_9
[2025-05-27 23:13:25.106859] Enviado: LosPeladitos_PKT_10
[2025-05-27 23:13:25.108194] Enviado: LosPeladitos_PKT_11
[2025-05-27 23:13:25.109567] Enviado: LosPeladitos_PKT_12
[2025-05-27 23:13:25.110860] Enviado: LosPeladitos_PKT_13
[2025-05-27 23:13:25.112134] Enviado: LosPeladitos_PKT_14
[2025-05-27 23:13:25.113590] Enviado: LosPeladitos_PKT_15
[2025-05-27 23:13:25.115094] Enviado: LosPeladitos_PKT_16
[2025-05-27 23:13:25.116299] Enviado: LosPeladitos_PKT_17
[2025-05-27 23:13:25.117604] Enviado: LosPeladitos_PKT_18
[2025-05-27 23:13:25.118806] Enviado: LosPeladitos_PKT_19
[2025-05-27 23:13:25.120154] Enviado: LosPeladitos_PKT_20
[2025-05-27 23:13:25.121540] Enviado: LosPeladitos_PKT_21
[2025-05-27 23:13:25.123129] Enviado: LosPeladitos_PKT_22
[2025-05-27 23:13:25.124633] Enviado: LosPeladitos_PKT_23
[2025-05-27 23:13:25.126084] Enviado: LosPeladitos_PKT_24
[2025-05-27 23:13:25.127499] Enviado: LosPeladitos_PKT_25
[2025-05-27 23:13:25.128953] Enviado: LosPeladitos_PKT_26
[2025-05-27 23:13:25.130113] Enviado: LosPeladitos_PKT_27
[2025-05-27 23:13:25.131449] Enviado: LosPeladitos_PKT_28
[2025-05-27 23:13:25.132637] Enviado: LosPeladitos_PKT_29
[2025-05-27 23:13:25.133990] Enviado: LosPeladitos_PKT_30
[2025-05-27 23:13:25.135198] Enviado: LosPeladitos_PKT_31
[2025-05-27 23:13:25.136472] Enviado: LosPeladitos_PKT_32
[2025-05-27 23:13:25.137985] Enviado: LosPeladitos_PKT_33
[2025-05-27 23:13:25.139470] Enviado: LosPeladitos_PKT_34
[2025-05-27 23:13:25.140895] Enviado: LosPeladitos_PKT_35
[2025-05-27 23:13:25.142124] Enviado: LosPeladitos_PKT_36
[2025-05-27 23:13:25.143377] Enviado: LosPeladitos_PKT_37
[2025-05-27 23:13:25.144606] Enviado: LosPeladitos_PKT_38
[2025-05-27 23:13:25.146057] Enviado: LosPeladitos_PKT_39
[2025-05-27 23:13:25.147469] Enviado: LosPeladitos_PKT_40
[2025-05-27 23:13:25.148888] Enviado: LosPeladitos_PKT_41
[2025-05-27 23:13:25.150130] Enviado: LosPeladitos_PKT_42
[2025-05-27 23:13:25.151415] Enviado: LosPeladitos_PKT_43
[2025-05-27 23:13:25.152671] Enviado: LosPeladitos_PKT_44
[2025-05-27 23:13:25.154006] Enviado: LosPeladitos_PKT_45
[2025-05-27 23:13:25.155474] Enviado: LosPeladitos_PKT_46
[2025-05-27 23:13:25.156971] Enviado: LosPeladitos_PKT_47
[2025-05-27 23:13:25.158195] Enviado: LosPeladitos_PKT_48
[2025-05-27 23:13:25.159553] Enviado: LosPeladitos_PKT_49
[2025-05-27 23:13:25.160893] Enviado: LosPeladitos_PKT_50
[2025-05-27 23:13:25.162104] Enviado: LosPeladitos_PKT_51
[2025-05-27 23:13:25.163398] Enviado: LosPeladitos_PKT_52
[2025-05-27 23:13:25.164741] Enviado: LosPeladitos_PKT_53
[2025-05-27 23:13:25.166081] Enviado: LosPeladitos_PKT_54
[2025-05-27 23:13:25.167233] Enviado: LosPeladitos_PKT_55
[2025-05-27 23:13:25.168389] Enviado: LosPeladitos_PKT_56
[2025-05-27 23:13:25.169652] Enviado: LosPeladitos_PKT_57
[2025-05-27 23:13:25.171063] Enviado: LosPeladitos_PKT_58
[2025-05-27 23:13:25.172419] Enviado: LosPeladitos_PKT_59
[2025-05-27 23:13:25.173820] Enviado: LosPeladitos_PKT_60
[2025-05-27 23:13:25.175103] Enviado: LosPeladitos_PKT_61
[2025-05-27 23:13:25.176520] Enviado: LosPeladitos_PKT_62
[2025-05-27 23:13:25.177930] Enviado: LosPeladitos_PKT_63
[2025-05-27 23:13:25.179145] Enviado: LosPeladitos_PKT_64
[2025-05-27 23:13:25.180527] Enviado: LosPeladitos_PKT_65
[2025-05-27 23:13:25.181910] Enviado: LosPeladitos_PKT_66
[2025-05-27 23:13:25.183164] Enviado: LosPeladitos_PKT_67
[2025-05-27 23:13:25.184541] Enviado: LosPeladitos_PKT_68
[2025-05-27 23:13:25.185788] Enviado: LosPeladitos_PKT_69
[2025-05-27 23:13:25.187053] Enviado: LosPeladitos_PKT_70
[2025-05-27 23:13:25.188511] Enviado: LosPeladitos_PKT_71
[2025-05-27 23:13:25.189979] Enviado: LosPeladitos_PKT_72
[2025-05-27 23:13:25.191358] Enviado: LosPeladitos_PKT_73
[2025-05-27 23:13:25.192690] Enviado: LosPeladitos_PKT_74
[2025-05-27 23:13:25.193885] Enviado: LosPeladitos_PKT_75
[2025-05-27 23:13:25.195105] Enviado: LosPeladitos_PKT_76
[2025-05-27 23:13:25.196433] Enviado: LosPeladitos_PKT_77
[2025-05-27 23:13:25.197688] Enviado: LosPeladitos_PKT_78
[2025-05-27 23:13:25.198918] Enviado: LosPeladitos_PKT_79
[2025-05-27 23:13:25.200102] Enviado: LosPeladitos_PKT_80
[2025-05-27 23:13:25.201275] Enviado: LosPeladitos_PKT_81
[2025-05-27 23:13:25.202492] Enviado: LosPeladitos_PKT_82
[2025-05-27 23:13:25.203760] Enviado: LosPeladitos_PKT_83
[2025-05-27 23:13:25.205041] Enviado: LosPeladitos_PKT_84
[2025-05-27 23:13:25.206351] Enviado: LosPeladitos_PKT_85
[2025-05-27 23:13:25.207689] Enviado: LosPeladitos_PKT_86
[2025-05-27 23:13:25.209066] Enviado: LosPeladitos_PKT_87
[2025-05-27 23:13:25.210478] Enviado: LosPeladitos_PKT_88
[2025-05-27 23:13:25.211858] Enviado: LosPeladitos_PKT_89
[2025-05-27 23:13:25.213084] Enviado: LosPeladitos_PKT_90
[2025-05-27 23:13:25.214442] Enviado: LosPeladitos_PKT_91
[2025-05-27 23:13:25.215723] Enviado: LosPeladitos_PKT_92
[2025-05-27 23:13:25.217137] Enviado: LosPeladitos_PKT_93
[2025-05-27 23:13:25.218399] Enviado: LosPeladitos_PKT_94
[2025-05-27 23:13:25.219708] Enviado: LosPeladitos_PKT_95
[2025-05-27 23:13:25.221044] Enviado: LosPeladitos_PKT_96
[2025-05-27 23:13:25.222450] Enviado: LosPeladitos_PKT_97
[2025-05-27 23:13:25.224056] Enviado: LosPeladitos_PKT_98
[2025-05-27 23:13:25.225305] Enviado: LosPeladitos_PKT_99
[2025-05-27 23:13:25.226702] Enviado: LosPeladitos_PKT_100
```

Partiendo de estos resultados, podemos calcular lo siguiente:

**Latencia promedio**	63.41 ms

**Latencia mínima**	63.25 ms

**Latencia máxima**	63.63 ms

**Jitter promedio**	0.25 ms

---

# 2 - Scripts para enviar y recibir secuencias de paquetes por TCP

## 2.1 - Tráfico UDP entre dos computadoras

aaa

---

## 2.2 - Tráfico UDP con log de transmisión y recepción

Código servidor:

```python
import socket
from datetime import datetime

HOST = '0.0.0.0'
PORT = 8081


def log_event(message):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    with open("udp_server_log.txt", "a") as log:
        log.write(f"[{timestamp}] Recibido: {message}\n")


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind((HOST, PORT))
        print(f"Servidor UDP escuchando en {HOST}:{PORT}...")
        while True:
            data, addr = s.recvfrom(1024)
            mensaje = data.decode()
            print(f"Recibido de {addr}: {mensaje}")
            log_event(mensaje)


if __name__ == "__main__":
    main()
```

Código cliente:

```python
import socket
import time
from datetime import datetime

GRUPO = "LosPeladitos"
NUM_PAQUETES = 100
INTERVALO_SEGUNDOS = 1

HOST = '192.168.100.57'  # IP del servidor UDP
PORT = 8081


def log_event(message):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    with open("udp_client_log.txt", "a") as log:
        log.write(f"[{timestamp}] Enviado: {message}\n")


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        for i in range(1, NUM_PAQUETES + 1):
            mensaje = f"{GRUPO}_PKT_{i}"
            s.sendto(mensaje.encode(), (HOST, PORT))
            print(f"Enviado: {mensaje}")
            log_event(mensaje)
            time.sleep(INTERVALO_SEGUNDOS)


if __name__ == "__main__":
    main()
```

---

## 2.3 - Métricas de la transmisión UDP

aaa

