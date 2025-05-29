#!/usr/bin/env python3
import re
from datetime import datetime
import statistics

def parse_log(fichero, etiqueta):
    """
    Parsea un log y devuelve un dict {número_paquete: timestamp}.
    Reconoce formatos 'PKT_1' o 'PKT1'.
    """
    patron = re.compile(r"\[(.*?)\].*"+etiqueta+r".*?PKT_?(\d+)")
    datos = {}
    with open(fichero) as f:
        for linea in f:
            m = patron.search(linea)
            if m:
                ts = datetime.strptime(m.group(1), "%Y-%m-%d %H:%M:%S.%f")
                idx = int(m.group(2))
                datos[idx] = ts
    return datos

# parseamos ambos logs
cli = parse_log("udp_client_log.txt", "Enviado")
srv = parse_log("udp_server_log.txt", "Recibido")

# emparejamos y calculamos latencias
latencies = []
for i in sorted(cli):
    if i in srv:
        delta = (srv[i] - cli[i]).total_seconds() * 1000
        latencies.append(delta)

if not latencies:
    print("Error: no se encontraron paquetes. Revisa nombres/formato de logs.")
    exit(1)

# estadísticas
mean_lat = statistics.mean(latencies)
min_lat  = min(latencies)
max_lat  = max(latencies)
jitters = [abs(latencies[i] - latencies[i-1]) for i in range(1, len(latencies))]
mean_jit = statistics.mean(jitters)

print(f"Paquetes considerados: {len(latencies)}")
print(f"Latencia promedio:  {mean_lat:.2f} ms")
print(f"Latencia mínima:     {min_lat:.2f} ms")
print(f"Latencia máxima:     {max_lat:.2f} ms")
print(f"Jitter promedio:     {mean_jit:.2f} ms")
