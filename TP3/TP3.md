# **Universidad Nacional de Córdoba**
# **Facultad de Ciencias Exactas, Físicas y Naturales**

## **Trabajo Práctico N°3:** Evaluación de performance en redes y ruteo interno dinámico Open Shortest Path First (OSPF)

**Integrantes del Grupo:**
*   Agustin Trachta
*   Agustin Pallardo
*   Mateo Rodriguez
*   Tomas Cisneros
  
**Profesor/a:** SANTIAGO MARTIN HENN

---

# 1. Introducción Teórica a OSPF (Punto 1)

Open Shortest Path First (OSPF) es un protocolo de enrutamiento interior (IGP) de tipo **estado de enlace (link-state)**, estandarizado por la IETF (RFC 2328 para OSPFv2). A diferencia de los protocolos de vector distancia (como RIP), los routers OSPF construyen una **imagen completa de la topología** de la red (o del área OSPF a la que pertenecen) intercambiando **Anuncios de Estado de Enlace (LSAs - Link State Advertisements)**.

Cada router origina LSAs describiendo sus propios enlaces (interfaces, vecinos alcanzables, costos asociados). Estos LSAs se **inundan (flooding)** sin modificar a todos los demás routers dentro de la misma área OSPF. Cada router almacena los LSAs recibidos en su **Base de Datos de Estado de Enlace (LSDB - Link State Database)**.

Con una LSDB idéntica en todos los routers del área, cada uno ejecuta de forma independiente el algoritmo **SPF (Shortest Path First)**, comúnmente el **algoritmo de Dijkstra**. Este algoritmo calcula el árbol de rutas más cortas desde sí mismo (la raíz del árbol) hacia todos los demás destinos dentro del área. El "costo" de una ruta es la suma de los costos configurados en las interfaces de salida a lo largo del camino. El costo por defecto suele basarse inversamente en el ancho de banda de la interfaz. Las rutas resultantes con menor costo se instalan en la **Tabla de Enrutamiento (RIB - Routing Information Base)**.

**Teoría de Grafos y OSPF:**
La topología de una red OSPF puede representarse como un **grafo dirigido y ponderado**:
*   **Nodos (Vértices):** Son los routers OSPF.
*   **Arcos (Edges):** Son los enlaces (conexiones) entre los routers.
*   **Pesos:** Son los costos OSPF asociados a cada enlace (interfaz de salida).

La LSDB contiene la información necesaria para construir este grafo. El algoritmo de Dijkstra opera sobre este grafo para encontrar el camino de menor peso (menor costo total) desde el router que ejecuta el algoritmo (nodo fuente) a todos los demás nodos (routers/redes destino).

**Clases de Redes OSPF:** OSPF clasifica las redes según el tipo de enlace L2 subyacente, lo que afecta cómo se establecen las adyacencias y se eligen los Designated Routers (DR) y Backup Designated Routers (BDR):
*   **Punto a Punto (Point-to-Point):** Típicamente enlaces seriales. No se elige DR/BDR. Los vecinos se descubren automáticamente.
*   **Broadcast Multi-Acceso (Broadcast):** Típicamente Ethernet. Se elige un DR y un BDR para reducir el número de adyacencias (los routers solo forman adyacencia completa con DR/BDR). Los vecinos se descubren con Hello.
*   **No Broadcast Multi-Acceso (NBMA):** Ej. Frame Relay, ATM. Similar a Broadcast pero no soporta multicast/broadcast L2. Se elige DR/BDR, pero los vecinos suelen necesitar configuración manual.
*   **Punto a Multipunto (Point-to-Multipoint):** Colección de enlaces punto a punto tratados como una unidad lógica. No se elige DR/BDR.
*   **Redes Virtuales (Virtual Links):** Usados para conectar áreas no contiguas al área backbone (Area 0).

---

# 2. Diseño de la Red

## 2.1. Topología Implementada

Se implementó la topología especificada en el TP3 utilizando Cisco Packet Tracer. La red consta de 5 routers (R1 a R5), 1 switch (S1) y 5 hosts (h1 a h5). Los routers están interconectados mediante enlaces seriales, y los hosts se conectan a sus respectivos puntos de acceso (S1 para h1, h2, h3; R4 para h4; R5 para h5). R1 incluye una interfaz Loopback para simulación posterior.

![image](https://github.com/user-attachments/assets/76ba48a8-ea3e-464b-9f59-2b296ce45af0)

**Dispositivos Utilizados (Ejemplo):**
*   Routers: Cisco 2911
*   Switch: Cisco 2960
*   Hosts: PC-PT
*   Módulos Router: HWIC-2T (Seriales), HWIC-4ESW (Switch Ethernet para R4/R5)

## 2.2. Plan de Direccionamiento IP (Punto 2)

Se diseñó el siguiente plan de direccionamiento IP, utilizando la subred `172.16.0.0/16` (Clase B) para las LANs y subredes `192.168.x.0/30` (Clase C) para los enlaces WAN seriales, según las interfaces especificadas y corregidas durante la implementación:

| Red/Segmento           | Red Base          | Máscara         | Rango Utilizable        | Dispositivo(Interfaz especificada) | IP Asignada     | Gateway (Hosts) |
| :--------------------- | :---------------- | :-------------- | :---------------------- | :---------------------------------- | :-------------- | :-------------- |
| **LAN h1,h2,h3 (S1)**  | `172.16.1.0`      | `255.255.255.0` | `172.16.1.1 - .254`   | R2 (GigabitEthernet0/0)           | `172.16.1.1`    | `172.16.1.1`    |
|                        |                   |                 |                         | h1 (FastEthernet0)                | `172.16.1.10`   | `172.16.1.1`    |
|                        |                   |                 |                         | h2 (FastEthernet0)                | `172.16.1.11`   | `172.16.1.1`    |
|                        |                   |                 |                         | h3 (FastEthernet0)                | `172.16.1.12`   | `172.16.1.1`    |
| **LAN h4 (R4)**        | `172.16.4.0`      | `255.255.255.0` | `172.16.4.1 - .254`   | R4 (Vlan1 - SVI)                  | `172.16.4.1`    | `172.16.4.1`    |
|                        |                   |                 |                         | h4 (FastEthernet0)                | `172.16.4.10`   | `172.16.4.1`    |
| **LAN h5 (R5)**        | `172.16.5.0`      | `255.255.255.0` | `172.16.5.1 - .254`   | R5 (Vlan1 - SVI)                  | `172.16.5.1`    | `172.16.5.1`    |
| **Enlace R1-R2**       | `192.168.12.0`    | `255.255.255.252` | `192.168.12.1 - .2`   | R1 (Serial0/2/0)                  | `192.168.12.1`  | N/A             |
|                        |                   |                 |                         | R2 (Serial0/3/0)                  | `192.168.12.2`  | N/A             |
| **Enlace R1-R3**       | `192.168.13.0`    | `255.255.255.252` | `192.168.13.1 - .2`   | R1 (Serial0/2/1)                  | `192.168.13.1`  | N/A             |
|                        |                   |                 |                         | R3 (Serial0/3/0)                  | `192.168.13.2`  | N/A             |
| **Enlace R2-R3**       | `192.168.23.0`    | `255.255.255.252` | `192.168.23.1 - .2`   | R2 (Serial0/3/1)                  | `192.168.23.1`  | N/A             |
|                        |                   |                 |                         | R3 (Serial0/3/1)                  | `192.168.23.2`  | N/A             |
| **Enlace R3-R4**       | `192.168.34.0`    | `255.255.255.252` | `192.168.34.1 - .2`   | R3 (Serial0/2/0)                  | `192.168.34.1`  | N/A             |
|                        |                   |                 |                         | R4 (Serial0/3/0)                  | `192.168.34.2`  | N/A             |
| **Enlace R3-R5**       | `192.168.35.0`    | `255.255.255.252` | `192.168.35.1 - .2`   | R3 (Serial0/2/1)                  | `192.168.35.1`  | N/A             |
|                        |                   |                 |                         | R5 (Serial0/3/0)                  | `192.168.35.2`  | N/A             |
| **Enlace R4-R5**       | `192.168.45.0`    | `255.255.255.252` | `192.168.45.1 - .2`   | R4 (Serial0/3/1)                  | `192.168.45.1`  | N/A             |
|                        |                   |                 |                         | R5 (Serial0/3/1)                  | `192.168.45.2`  | N/A             |
| **Loopback R1**        | `1.1.1.1`         | `255.255.255.255` | `1.1.1.1`               | R1 (Loopback0)                    | `1.1.1.1`       | N/A             |

---

# 3. Configuración Inicial y Verificación (Area 0) (Punto 3)

Se procedió con la configuración detallada de las interfaces y la activación inicial de OSPF en una única área (Area 0).

## 3.1. Configuración de Interfaces

Se configuraron las direcciones IP en todas las interfaces de routers y hosts según la tabla anterior. Se activaron las interfaces físicas con `no shutdown`. En las interfaces seriales designadas como DCE, se configuró `clock rate 64000`. Para las interfaces `Fa0/1/0` (R4) y `Fa0/2/0` (R5) pertenecientes a módulos de switch, se utilizó el método de SVI (Interfaz Virtual de Switch) en la VLAN 1, asignando el puerto físico a dicha VLAN y la dirección IP a la interfaz `Vlan1` correspondiente.

![image](https://github.com/user-attachments/assets/d8c553f1-7d71-4a99-a82c-a2fbf3e0daf3)

Interfaz de R4

![image](https://github.com/user-attachments/assets/a6705e11-fcc7-41d9-8093-83659d7d37a6)

Interfaz de R1

Se verificó la conectividad básica entre interfaces directamente conectadas mediante `ping`.

![image](https://github.com/user-attachments/assets/6322b170-720f-484f-8b5a-a72c25f29527)

Ping desde h1 a h4 y al loopback de R1

## 3.2. Configuración OSPF Básica (Area 0)

Se habilitó OSPF proceso 1 en todos los routers, asignando un `router-id` único a cada uno. Todas las redes directamente conectadas (incluyendo las redes de las SVIs y la Loopback) fueron anunciadas en `area 0` mediante el comando `network [direccion_red] [wildcard_mask] area 0`.

![image](https://github.com/user-attachments/assets/9325d25d-f46c-4a0f-8e6f-febe685d7106)

show run | section router ospf en R2

## 3.3. Verificación de Vecindad, Rutas y Conectividad

Tras permitir la convergencia de OSPF:
*   **Vecinos OSPF:** Se verificó el establecimiento de adyacencias con `show ip ospf neighbor`. Todos los vecinos esperados alcanzaron el estado `FULL`.
  
    ![image](https://github.com/user-attachments/assets/87c36093-06b4-4a79-9273-766448413209)

    Vecinos del router 3.

*   **Tabla de Enrutamiento:** Se examinó la tabla de rutas con `show ip route ospf`. Se observaron rutas OSPF (`O`) hacia todas las redes remotas de la topología.

    ![image](https://github.com/user-attachments/assets/a28504b0-73d4-4a3c-8da5-58819be77c2e)

*   **Conectividad End-to-End:** Se realizaron pruebas `ping` y `tracert` entre diferentes hosts (ej. h1 a h5, h4 a h2, h3 a Loopback R1), confirmando la conectividad completa a través de las rutas aprendidas por OSPF.

    ![image](https://github.com/user-attachments/assets/dd20af77-8299-4f59-bf54-7fd8fca4813d)
    
    `ping` de h3 a h4.
    
    ![image](https://github.com/user-attachments/assets/802d12aa-7018-41a0-8862-d3ea247525af)

    `ping` de h2 a Loopback R1.

---

# 4. Análisis de Mensajes OSPF (Punto 4)

OSPF utiliza varios tipos de paquetes para su funcionamiento, encapsulados directamente sobre IP (protocolo 89):

1.  **Hello:** Descubrimiento y mantenimiento de vecinos, elección de DR/BDR en redes multiacceso. Se envían periódicamente (10s por defecto en Broadcast/P2P, 30s en NBMA/P2MP). Contienen Router ID, Hello/Dead intervals, lista de vecinos conocidos, Area ID, Costo, DR/BDR (si aplica), flags de autenticación.
2.  **DBD (Database Description):** Resumen del contenido de la LSDB del remitente. Se intercambian durante la formación de adyacencia para sincronizar LSDBs.
3.  **LSR (Link State Request):** Solicitud de LSAs específicos que faltan o son más recientes en la LSDB local después de comparar DBDs.
4.  **LSU (Link State Update):** Contiene uno o más LSAs completos, enviados en respuesta a un LSR o cuando se origina/actualiza un LSA (flooding).
5.  **LSAck (Link State Acknowledgment):** Acuse de recibo explícito para paquetes DBD, LSR y LSU, asegurando la fiabilidad del intercambio de estado de enlace.

**Análisis en Packet Tracer:**
Se utilizó el modo Simulación de Packet Tracer, filtrando por el protocolo `OSPF`. Se observó el intercambio de paquetes `Hello` entre routers vecinos en los enlaces seriales y en el segmento Ethernet conectado a R2 (Gi0/0). Al iniciar la red o tras un cambio, se pudieron observar los paquetes `DBD`, `LSR`, `LSU` y `LSAck` (vistos como OSPF) durante el proceso de sincronización de LSDBs y formación de adyacencias.

![image](https://github.com/user-attachments/assets/9382e2bb-87ce-4398-83d8-b202598d6294)

![image](https://github.com/user-attachments/assets/d5341007-0bfb-4378-bd86-0968afa07ac2)


**Impacto:** Estos mensajes son fundamentales. Los Hello mantienen la vecindad (si se dejan de recibir Hellos por el Dead Interval, el vecino se considera caído). El intercambio DBD/LSR/LSU/LSAck asegura que todos los routers en un área tengan una LSDB idéntica, lo cual es prerrequisito para que el algoritmo SPF calcule rutas consistentes y se eviten bucles de enrutamiento. El flooding de LSUs propaga rápidamente la información sobre cambios en la topología (enlaces caídos/levantados, cambios de costo).

---

# 5. Base de Datos de Estado de Enlace (LSDB) (Punto 5b)

La LSDB contiene todos los LSAs recibidos que describen la topología del área. Se puede inspeccionar usando `show ip ospf database`.

## 5.1. Lectura de LSDB (Area 0 Inicial)

Se ejecutó `show ip ospf database` en varios routers (R2, R3 respectivamente en las imagenes) mientras todos estaban en Area 0.

![image](https://github.com/user-attachments/assets/a603ccef-84dc-44ea-afa6-8ec525c17f8b)

![image](https://github.com/user-attachments/assets/16d894d6-98fd-4927-a95c-8e6bae1247a3)


En la sección **Router Link States (Area 0)** se observaron LSAs tipo 1 originados por los routers con IDs 1.1.1.1 a 5.5.5.5. Cada entrada representa un resumen de los enlaces activos que cada router publica dentro del área.

- El Router 3.3.3.3 muestra 8 enlaces activos, lo que refleja su rol central en la topología.
- Los campos `Age`, `Seq#` y `Checksum` indican la antigüedad, versión y validez del LSA.
- La presencia de los cinco routers confirma que la LSDB está sincronizada y completa en el Área 0.

---

# 6. Configuración Multi-Área OSPF (Punto 6)

Se procedió a dividir la red OSPF en dos áreas según lo solicitado.

## 6.1. Diseño de Áreas

*   **Área 0 (Backbone):** Incluirá a **R3, R4, R5**. El Área 0 es especial y todas las demás áreas deben conectarse a ella (directa o virtualmente).
*   **Área 1:** Incluirá a **R1, R2**.
*   **Router de Borde de Área (ABR - Area Border Router):** **R3** se convierte en ABR, ya que tiene interfaces en Área 0 (hacia R4, R5) y en Área 1 (hacia R1, R2). Los ABRs son responsables de resumir e inyectar información de rutas entre áreas. R1 y R2 también serían ABRs si tuvieran interfaces en ambas áreas definidas.

**Revisión del Diseño:** Siguiendo estrictamente "R1 y R2 están en el área A [Area 1], el resto (R3, R4, R5) estarán en el área B [Area 0]":
*   **Area 1:** R1, R2. Redes: Loopback R1, LAN h1/h2/h3 (vía R2), **Enlace R1-R2**, **Enlace R1-R3**, **Enlace R2-R3**.
*   **Area 0:** R3, R4, R5. Redes: LAN h4, LAN h5, Enlace R3-R4, Enlace R3-R5, Enlace R4-R5.
*   **ABR:** **R3**. Las interfaces de R3 hacia R1 y R2 (Se0/3/0, Se0/3/1) se configurarán como parte del Area 1. Las interfaces de R3 hacia R4 y R5 (Se0/2/0, Se0/2/1) se configurarán como parte del Area 0.

## 6.2. Reconfiguración OSPF Multi-Área

Se modificaron los comandos `network` en los routers para asignar las redes a las áreas correctas.

*   **R1 (Todo en Area 1):**
    ```bash
    configure terminal
    router ospf 1
     no network 1.1.1.1 0.0.0.0 area 0
     no network 192.168.12.0 0.0.0.3 area 0
     no network 192.168.13.0 0.0.0.3 area 0 ! Remover de Area 0
     network 1.1.1.1 0.0.0.0 area 1
     network 192.168.12.0 0.0.0.3 area 1
     network 192.168.13.0 0.0.0.3 area 1 ! Añadir a Area 1
    end
    copy run start
    ```
*   **R2 (Todo en Area 1):**
    ```bash
    configure terminal
    router ospf 1
     no network 172.16.1.0 0.0.0.255 area 0
     no network 192.168.12.0 0.0.0.3 area 0
     no network 192.168.23.0 0.0.0.3 area 0 ! Remover de Area 0
     network 172.16.1.0 0.0.0.255 area 1
     network 192.168.12.0 0.0.0.3 area 1
     network 192.168.23.0 0.0.0.3 area 1 ! Añadir a Area 1
    end
    copy run start
    ```
*   **R3 (ABR - Interfaces en Area 1 y Area 0):**
    ```bash
    configure terminal
    router ospf 1
     ! Remover configuración antigua de Area 0 para enlaces a R1/R2
     no network 192.168.13.0 0.0.0.3 area 0
     no network 192.168.23.0 0.0.0.3 area 0
     ! Mantener enlaces a R4/R5 en Area 0
     network 192.168.34.0 0.0.0.3 area 0
     network 192.168.35.0 0.0.0.3 area 0
     ! Añadir enlaces a R1/R2 a Area 1
     network 192.168.13.0 0.0.0.3 area 1
     network 192.168.23.0 0.0.0.3 area 1
    end
    copy run start
    ```
*   **R4 (Todo en Area 0):** (Sin cambios en los comandos `network` OSPF ya que estaba todo en Area 0)
*   **R5 (Todo en Area 0):** (Sin cambios en los comandos `network` OSPF)

## 6.3. Verificación Multi-Área

![image](https://github.com/user-attachments/assets/a62530fc-1b81-47c0-82b7-6f887dbe15c5)

`show ip ospf interface` brief desde R3

*   **LSDB:** `show ip ospf database` en R3 (ABR) ahora muestra LSAs para ambas áreas. Además, R3 origina **Summary LSAs (Type 3)** para anunciar redes de un área a la otra. Los routers dentro de un área (ej. R1) verán LSAs Type 1 y 2 de su propia área y LSAs Type 3 originados por el ABR (R3) describiendo redes de la otra área.

![image](https://github.com/user-attachments/assets/ce365c5d-7c24-4c5b-8a05-2f86e5813e5a)

*   **Conectividad:** Se repitieron las pruebas `ping` y `tracert` entre hosts de diferentes áreas, confirmando que la conectividad total se mantiene.

![image](https://github.com/user-attachments/assets/75a7812a-ac2b-4c06-aa90-5a034fd27953)

Ping desde h1 a h4 con las nuevas areas
---

# 7. Verificación Detallada del Funcionamiento OSPF (Punto 7)

## 7.1. Información de Vecinos en R2

Se utilizó `show ip ospf neighbor detail` en R2 para obtener información extendida sobre sus vecinos (R1 y R3).

![image](https://github.com/user-attachments/assets/d5612bc3-1f77-4cb1-8fb7-7154ffe32044)

**Observaciones:** Se puede ver el Router ID del vecino, su prioridad (relevante para elección DR/BDR), estado de la adyacencia (`FULL`), dirección IP de la interfaz del vecino, interfaz local por la que se alcanza, timers (Hello/Dead), y opciones OSPF negociadas.

## 7.2. Información de Operaciones en R2

Se usaron comandos para inspeccionar el funcionamiento de OSPF en las interfaces de R2.

*   `show ip ospf interface GigabitEthernet0/0`: Muestra detalles de OSPF en la interfaz LAN. Incluye Area ID, Router ID, tipo de red (Broadcast), costo, estado (DR/BDR/DROTHER), timers, lista de vecinos en ese segmento.
*   `show ip ospf interface Serial0/3/0`: Muestra detalles en la interfaz hacia R1. Tipo de red (Point-to-Point), costo, timers, vecino.
*   `show ip ospf interface Serial0/3/1`: Muestra detalles en la interfaz hacia R3.

![image](https://github.com/user-attachments/assets/ef7f41f4-7f72-419c-ad73-fb2032994591)

![image](https://github.com/user-attachments/assets/ad3994f0-4944-4c2c-82bc-b7c1cc542510)

**Observaciones:** Estos comandos permiten verificar que OSPF esté activo en las interfaces correctas, con los parámetros esperados (área, costo, timers) y ver el rol del router en segmentos multiacceso (DR/BDR).

---

# 8. Modificación de Costos OSPF (Punto 8)

OSPF utiliza el costo como métrica principal. Por defecto, se calcula como `Costo = CostoReferencia / AnchoBandaInterfaz`. El CostoReferencia por defecto es 100 Mbps. Esto puede llevar a que FastEthernet (100 Mbps) y GigabitEthernet (1000 Mbps) tengan el mismo costo (1), lo cual no es ideal.

## 8.1. Modificación de Costo

**Opción 1: Ajustar Ancho de Banda de Referencia (Global)**
Se puede ajustar el ancho de banda de referencia globalmente para diferenciar mejor entre enlaces rápidos.
```bash
router ospf 1
 auto-cost reference-bandwidth 10000 ! (Ej. 10 Gbps en Mbps)
```
**Opción 2: Modificar Costo por Interfaz (Específico)**
Se eligió modificar manualmente el costo en un enlace específico para observar el impacto directo en el enrutamiento. 
* En R1:
```bash
configure terminal
interface Serial0/2/1
 ip ospf cost 100
end
copy run start
```

## 8.2. Verificación con Traceroute

*   **Antes de la Modificación:** Se ejecutó `tracert` desde h1 hacia h4. La ruta observada fue [Describe la ruta original, ej: PC -> R2 -> R3 -> R5 -> PC o similar, mostrando IPs de los routers].

*   **Después de la Modificación:** Se esperó la convergencia de OSPF (generalmente unos segundos) y se repitió `tracert` desde h1 hacia h4. Al aumentar significativamente el costo del enlace R2-R3, OSPF recalculó la ruta más corta. La nueva ruta observada fue [Describe la nueva ruta, ej: PC -> R2 -> R1 -> R3 -> R5 -> PC o PC -> R2 -> R1 -> R3 -> R4 -> R5 -> PC, mostrando IPs]. Esta nueva ruta evita el enlace R2-R3 directo debido a su alto costo.

    ![image](https://github.com/user-attachments/assets/2243755f-272d-458a-a3cc-9264bdd0c173)

El primer ping es antes de cambiar el costo de R1, el segundo es despues del cambio.

**Conclusión:** Modificar el costo OSPF es una herramienta clave para influir en la selección de rutas. Aumentar el costo de un enlace lo hace menos preferible, forzando a OSPF a buscar caminos alternativos con menor costo total acumulado, lo que se pudo verificar claramente con `traceroute`.

---

# 9. Redistribución de Ruta Predeterminada (Punto 9)

Se simuló una conexión a Internet en R1 y se configuró OSPF para distribuir una ruta predeterminada al resto de la red OSPF, permitiendo que los hosts internos puedan alcanzar destinos fuera del dominio OSPF.

## 9.1. Configuración Ruta Estática Predeterminada en R1

Se utilizó la interfaz Loopback0 (1.1.1.1) como un marcador simbólico del "exterior" o el punto de salida hacia un ISP hipotético. Se configuró una ruta estática predeterminada (`0.0.0.0/0`) en R1 apuntando a esta interfaz como siguiente salto.

*   **En R1:**
    ```bash
    configure terminal
    ! Ruta estática 0.0.0.0/0 apuntando a la interfaz Loopback0
    ! Esta ruta representa la salida hacia "Internet" en nuestra simulación
    ip route 0.0.0.0 0.0.0.0 Loopback0
    end
    copy running-config startup-config
    ```
    Se verificó la correcta instalación de esta ruta en la tabla de R1 con `show ip route static`.
      
![image](https://github.com/user-attachments/assets/7b2a0bd3-809e-4b32-af9b-c201eebea0ab)


## 9.2. Redistribución en OSPF

Se instruyó al proceso OSPF en R1 para que generara y anunciara información de ruta predeterminada a sus vecinos OSPF. Esto se logra con el comando `default-information originate`.

*   **En R1:**
    ```bash
    configure terminal
    router ospf 1
     ! Comando para inyectar la ruta default (si existe en la RIB) en OSPF
     default-information originate
    end
    copy run start
    ```

## 9.3. Verificación

Se verificó la tabla de enrutamiento en los otros routers para confirmar que recibieron la ruta predeterminada vía OSPF.


![image](https://github.com/user-attachments/assets/a79e31ac-0169-47bc-a072-26b3bf5dca74)

Salida `show ip route` en R4 mostrando ruta O*E2 

**Observaciones:** En las tablas de enrutamiento de R2, R3, R4 y R5, apareció una nueva entrada para la ruta predeterminada, identificada como `O*E2 0.0.0.0/0`.
*   `O`: Aprendida vía OSPF.
*   `*`: Es la ruta candidata a ser el Gateway of Last Resort (Puerta de Enlace de Último Recurso).
*   `E2`: Es una ruta Externa OSPF Tipo 2. Su métrica principal es el costo externo asignado por el ASBR (Autonomous System Boundary Router, R1 en este caso). Este costo no se incrementa al atravesar los routers internos del dominio OSPF. El costo por defecto para `default-information originate` es 1.
*   La ruta indica correctamente la dirección IP del siguiente salto para alcanzar R1 (a través de la ruta OSPF calculada hacia R1).

Con esta configuración, cualquier host (ej. h4) que intente contactar una IP no presente en la tabla de enrutamiento de su gateway (R4), utilizará esta ruta `O*E2` para enviar el tráfico hacia R1, que a su vez (en nuestra simulación) lo dirigiría a Loopback0.

---

# 10. Análisis de Falla de Interfaz en R2 (Punto 10)

Se analiza el impacto esperado y observable en la red OSPF si fallan diferentes interfaces del router R2. OSPF está diseñado para detectar estos fallos y converger a una nueva topología estable si existen caminos alternativos.

*   **Falla R2 - R1 (Interfaz `Serial0/3/0` en R2):**
    1.  **Detección:** R2 y R1 detectan la caída del enlace (estado `down`, `line protocol down`).
    2.  **Adyacencia:** R2 deja de recibir Hellos de R1 por `Se0/3/0` (y viceversa). Tras el `Dead Interval` (normalmente 4x Hello Interval, ~40s), la adyacencia OSPF entre ellos se rompe.
    3.  **Actualización LSA:** Ambos routers (R1 y R2) originan un **nuevo Router LSA (Type 1)**, indicando que el enlace entre ellos ya no existe o tiene un costo infinito.
    4.  **Inundación (Flooding):** Estos LSAs actualizados se inundan dentro del Área 1.
    5.  **Recálculo SPF:** Todos los routers en Area 1 (R1, R2, y R3 como ABR) reciben los LSAs, actualizan su LSDB y re-ejecutan el algoritmo SPF.
    6.  **Nueva Ruta:** R2 pierde su ruta directa hacia R1. Si necesita alcanzar la red Loopback `1.1.1.1` (o cualquier otra red solo alcanzable vía R1 desde R2), deberá enrutar el tráfico a través de su otro vecino OSPF, R3 (`R2 -> R3 -> R1`). R1 también redirigirá el tráfico destinado a la LAN de R2 (`172.16.1.0/24`) a través de R3 (`R1 -> R3 -> R2`).
    7.  **ABR:** R3 (ABR) podría actualizar los Summary LSAs (Type 3) si las métricas hacia redes en otras áreas cambian debido a la nueva ruta.
    8.  **Impacto:** Pérdida de la conexión directa R1-R2. El tráfico entre ellos y las redes detrás de ellos ahora debe pasar por R3. La convergencia es automática y relativamente rápida.

*   **Falla R2 - R3 (Interfaz `Serial0/3/1` en R2):**
    1.  **Detección y Adyacencia:** Similar al caso anterior, R2 y R3 detectan la caída y la adyacencia OSPF expira.
    2.  **Actualización LSA:** R2 (en Area 1) y R3 (en Area 1 y Area 0, como ABR) originan nuevos LSAs reflejando la pérdida del enlace R2-R3.
    3.  **Inundación:** Los LSAs se inundan en Area 1 (desde R2 y R3) y en Area 0 (desde R3).
    4.  **Recálculo SPF:** Todos los routers en ambas áreas (o los afectados) re-ejecutan SPF.
    5.  **Nueva Ruta:** R2 pierde su conexión directa con el ABR (R3). Para alcanzar cualquier red en Area 0 (LAN h4, LAN h5, etc.) o incluso al propio R3, R2 deberá usar su única ruta restante: a través de R1 (`R2 -> R1 -> R3 -> Area 0`). R3 también perderá la ruta directa a la LAN de R2 y deberá pasar por R1 (`R3 -> R1 -> R2`).
    6.  **Impacto:** Pérdida del enlace directo R2-R3. Todo el tráfico entre R2 (y su LAN) y el resto de la red (R3, R4, R5, Area 0) ahora debe obligatoriamente transitar por R1.

*   **Falla R2 - S1 (Interfaz `GigabitEthernet0/0` en R2):**
    1.  **Detección:** R2 detecta la caída de su interfaz LAN (`Gi0/0 down`, `line protocol down`).
    2.  **Actualización LSA:** R2 origina un nuevo Router LSA (Type 1) indicando que la red `172.16.1.0/24` (el enlace stub conectado a Gi0/0) ya no es alcanzable a través de él o tiene un costo infinito.
    3.  **Inundación:** Este LSA se inunda en Area 1.
    4.  **Recálculo SPF:** R1 y R3 (ABR) actualizan sus LSDBs y re-ejecutan SPF.
    5.  **Nueva Ruta:** R1 y R3 eliminan la ruta hacia `172.16.1.0/24` vía R2.
    6.  **ABR:** R3 (ABR) envía un Summary LSA actualizado (o retira el existente) hacia Area 0, informando que la red `172.16.1.0/24` ya no es alcanzable.
    7.  **Impacto:** Los hosts h1, h2, h3 quedan completamente **aislados** del resto de la red OSPF, ya que R2 era su único gateway. Ningún otro router tendrá una ruta válida hacia `172.16.1.0/24`. R2 también pierde conectividad con estos hosts. OSPF maneja la actualización de la topología, pero no puede restaurar la conectividad si no hay caminos redundantes hacia esa LAN específica.

![image](https://github.com/user-attachments/assets/556e1de5-0a7a-4ef6-8928-7b8f84706fd5)

Ejemplo de tracert desde h1 al Loopback R1. El primero es con todos los serial activados, el ultimo es con el serial 0/3/1 (es decir, el de R2 a R3 apagado (falla).

![image](https://github.com/user-attachments/assets/866c8d3b-f297-463a-8280-e00fb18dd5be)

Ejemplo de tracert desde h1 al Loopback R1 con falla de R2 a S1 (G0/0 en shutdown).

---

# 11. RIB vs FIB (Punto 11)

## 11.1. Explicación Teórica

*   **RIB (Routing Information Base):** Conocida comúnmente como la **Tabla de Enrutamiento**. Es una base de datos mantenida en el plano de control del router. Contiene la información de rutas aprendidas de todas las fuentes configuradas:
    *   Redes directamente conectadas (`C`, `L`).
    *   Rutas estáticas (`S`).
    *   Rutas aprendidas por protocolos de enrutamiento dinámico (OSPF `O`, EIGRP `D`, BGP `B`, RIP `R`, etc.).
    Para cada prefijo de red, la RIB puede contener múltiples rutas candidatas si son aprendidas por diferentes protocolos o con diferentes métricas. El router aplica un proceso de selección basado primero en la **Distancia Administrativa** (AD, un índice de confiabilidad de la fuente, menor es mejor) y luego en la **Métrica** específica del protocolo (menor es mejor) para elegir la **mejor ruta única** para cada destino. Solo la mejor ruta se considera activa y se utiliza para poblar la FIB. El comando principal para ver la RIB activa es `show ip route`.

*   **FIB (Forwarding Information Base):** Es una tabla optimizada para el **reenvío rápido de paquetes** y reside en el **plano de datos**. Se deriva directamente de las mejores rutas seleccionadas en la RIB. La FIB está estructurada para una búsqueda muy rápida (a menudo basada en hardware o estructuras de datos eficientes como árboles de prefijos) de la interfaz de salida y la información del siguiente salto para cualquier dirección IP de destino dada. En los routers Cisco modernos, la FIB es un componente clave de **CEF (Cisco Express Forwarding)**. CEF precalcula la información de reenvío, incluyendo la interfaz de salida y la dirección MAC del siguiente salto (a través de la tabla de adyacencia de CEF), para evitar consultas recursivas o la intervención del procesador principal para cada paquete. El comando principal para inspeccionar la FIB es `show ip cef`.

**Diferencia Clave:** La RIB es donde se *toman* las decisiones de enrutamiento (plano de control), mientras que la FIB es donde se *ejecutan* esas decisiones a alta velocidad (plano de datos). La FIB es una copia optimizada y lista para usar de las mejores rutas de la RIB.

## 11.2. Verificación en el Práctico

*   **Visualización de la RIB:** Se utilizó el comando `show ip route` en router 3 que tiene varias conexiones. Se observaron rutas conectadas (`C`), locales (`L`), OSPF intra-área (`O`).

![image](https://github.com/user-attachments/assets/fcf5cfcd-6622-43e6-a222-61b12d69aecb)


*   **Visualización de la FIB (CEF):** Se intentó usar `show ip cef` en los mismos routers.
![image](https://github.com/user-attachments/assets/4fb7d3c9-8d90-4dfa-ac2f-cd7942558a9c)

#### Elementos clave observados:

- **Ruta por defecto** (`0.0.0.0/0`): apunta a `192.168.13.1` por `Serial0/3/0`, usada si no hay coincidencia más específica.
- **Redes LAN activas**:
  - `172.16.1.0/24` → vía `192.168.23.1` (Serial0/3/1)
  - `172.16.4.0/24` y `172.16.5.0/24` → vía `192.168.35.2` (Serial0/2/1)
- **Redes directamente conectadas** aparecen como `attached`.
- **IPs propias** del router como `192.168.13.1/32` figuran como `receive`.
- **Multicast** (`224.0.0.0/4`) y otras direcciones especiales se descartan (`drop`).

---

# 12. Conclusiones Generales

Este trabajo práctico proporcionó una experiencia práctica invaluable en la configuración y análisis del protocolo de enrutamiento OSPF. A través de la implementación en Cisco Packet Tracer, se abordaron desde los conceptos fundamentales de estado de enlace y el algoritmo de Dijkstra hasta configuraciones avanzadas como multi-área y redistribución.

Se diseñó e implementó con éxito la topología de red propuesta, incluyendo la resolución de desafíos específicos como la configuración de interfaces en módulos de switch mediante SVIs. La configuración inicial de OSPF en una sola área permitió verificar la formación de adyacencias, la sincronización de LSDBs y el establecimiento de conectividad completa, validada mediante `ping` y `traceroute`.

La transición a una configuración multi-área demostró la capacidad de OSPF para escalar y organizar dominios de enrutamiento más grandes, introduciendo el rol crucial del ABR (R3) y la diferenciación entre rutas intra-área (`O`) e inter-área (`O IA`). 

La modificación deliberada de los costos OSPF y la posterior verificación con `traceroute` ilustraron de manera efectiva cómo influir en la selección de rutas y la ingeniería de tráfico básica. Asimismo, la configuración de la redistribución de una ruta predeterminada desde un ASBR simulado (R1) demostró cómo OSPF puede integrar información de rutas externas y proveer conectividad hacia fuera del dominio OSPF.

El análisis teórico y la observación (limitada por PT) de la respuesta de OSPF ante fallos de interfaz subrayaron su resiliencia y capacidad de convergencia automática, un pilar de las redes modernas. Finalmente, se clarificó la distinción fundamental entre la RIB (plano de control, decisión) y la FIB (plano de datos, reenvío), componentes esenciales en la arquitectura de un router.

Aunque la simulación tiene limitaciones (especialmente en la medición de performance real y la visibilidad completa de mecanismos como CEF), Packet Tracer fue una herramienta extremadamente útil para consolidar los conocimientos teóricos y desarrollar habilidades prácticas en la configuración y troubleshooting de OSPF. Los objetivos del trabajo práctico se consideran cumplidos.
