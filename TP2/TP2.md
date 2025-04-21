# **Universidad Nacional de Córdoba**
## **Facultad de Ciencias Exactas, Físicas y Naturales**

## **Trabajo Práctico N°2:** Topologías Multi-path y Evaluación de Performance en Redes

**Integrantes del Grupo:**
*   Agustin Trachta
*   Mateo Rodriguez
*   Agustin Pallardo
*   Tomas Cisneros

**Profesor:** SANTIAGO MARTIN HENN

---

# 1. Introducción

El presente Trabajo Práctico N°2 tiene como objetivo principal el estudio y la implementación de conceptos fundamentales de redes, incluyendo el diseño de topologías multi-path, la configuración de enrutamiento estático, y la evaluación del rendimiento de la red bajo diferentes condiciones. Siguiendo los lineamientos del práctico, se busca aplicar estos conceptos tanto en un entorno simulado como, originalmente, en un entorno físico.

Debido a la modalidad actual, la totalidad de la implementación y las pruebas se realizaron utilizando el software de simulación **Cisco Packet Tracer**. Esto permitió modelar la topología propuesta, configurar los dispositivos de red (routers, switches, hosts) y simular el tráfico para evaluar la performance.

Los objetivos específicos abordados en este informe son:
*   Diseñar e implementar una topología de red con múltiples caminos entre segmentos.
*   Configurar direccionamiento IP fijo en hosts y dispositivos de red.
*   Implementar enrutamiento estático para permitir la comunicación entre distintas subredes.
*   Verificar la conectividad básica utilizando ICMP (`ping`).
*   Investigar y describir la herramienta `iperf3` y sus parámetros principales para la medición de performance.
*   Simular pruebas de transferencia de datos (TCP/UDP) utilizando las herramientas de Packet Tracer (como el Generador de Tráfico) para emular el comportamiento de `iperf3`.
*   Analizar los resultados de las pruebas de performance, considerando métricas como ancho de banda simulado, protocolos y posibles pérdidas de paquetes observadas en la simulación.
*   Realizar capturas y análisis de tráfico simulado mediante el modo Simulación de Packet Tracer.

Este informe detallará el diseño de la red, las configuraciones aplicadas, la metodología de prueba utilizada en Packet Tracer, los resultados obtenidos y un análisis de los mismos, concluyendo con las observaciones finales sobre la experiencia.

---

# 2. Diseño de la Red

## 2.1. Topología de Red

Se implementó una topología de red en Cisco Packet Tracer que consta de tres routers (simulando el núcleo de la red con múltiples caminos), tres switches (uno por cada red local o LAN) y tres computadoras personales (PCs), cada una representando un host dentro de su respectiva LAN (Grupo 1, Grupo 2, Grupo N en el esquema original, aquí PC0, PC1, PC2).

Los routers se interconectan entre sí mediante enlaces seriales, formando un triángulo, lo que proporciona redundancia de caminos (aunque con enrutamiento estático, la ruta será fija). Cada router conecta también a una LAN a través de un switch mediante una interfaz Ethernet/FastEthernet.

Los dispositivos utilizados en la simulación son:
*   **Routers:** 3 x Cisco 2901
*   **Switches:** 3 x Cisco 2960-24TT
*   **PCs:** 3 x PC-PT

A continuación, se muestra la topología implementada en Packet Tracer:

![image](https://github.com/user-attachments/assets/172be6ce-96ed-4231-9cc6-4ba9e22c4747)

## 2.2. Plan de Direccionamiento IP

Se definió y configuró el siguiente plan de direccionamiento IP fijo para todos los dispositivos de la red:

**Redes LAN:**

| Segmento        | Red / Prefijo       | Dispositivo | Interfaz      | Dirección IP     | Máscara         | Gateway (para PCs) |
| :-------------- | :------------------ | :---------- | :------------ | :--------------- | :-------------- | :----------------- |
| **LAN R1 (PC0)** | `192.168.10.0/24`   | Router1     | GigabitEth0/0 | `192.168.10.1`   | `255.255.255.0` | -                  |
|                 |                     | PC0         | FastEthernet0 | `192.168.10.10`  | `255.255.255.0` | `192.168.10.1`     |
| **LAN R2 (PC1)** | `192.168.20.0/24`   | Router2     | GigabitEth0/0 | `192.168.20.1`   | `255.255.255.0` | -                  |
|                 |                     | PC1         | FastEthernet0 | `192.168.20.10`  | `255.255.255.0` | `192.168.20.1`     |
| **LAN R3 (PC2)** | `192.168.30.0/24`   | Router3     | GigabitEth0/0 | `192.168.30.1`   | `255.255.255.0` | -                  |
|                 |                     | PC2         | FastEthernet0 | `192.168.30.10`  | `255.255.255.0` | `192.168.30.1`     |

**Enlaces Seriales Inter-Router (WAN):**

| Segmento          | Red / Prefijo   | Dispositivo | Interfaz      | Dirección IP | Máscara           |
| :---------------- | :-------------- | :---------- | :------------ | :----------- | :---------------- |
| **Enlace R1 - R2** | `10.0.12.0/30`  | Router1     | Serial0/0/0   | `10.0.12.1`  | `255.255.255.252` |
|                   |                 | Router2     | Serial0/0/0   | `10.0.12.2`  | `255.255.255.252` |
| **Enlace R2 - R3** | `10.0.23.0/30`  | Router2     | Serial0/0/1   | `10.0.23.1`  | `255.255.255.252` |
|                   |                 | Router3     | Serial0/0/1   | `10.0.23.2`  | `255.255.255.252` |
| **Enlace R3 - R1** | `10.0.13.0/30`  | Router3     | Serial0/0/0   | `10.0.13.1`  | `255.255.255.252` |
|                   |                 | Router1     | Serial0/0/1   | `10.0.13.2`  | `255.255.255.252` |

*(Nota: Asegúrate que las interfaces usadas en la tabla coincidan con las usadas en tu simulación Packet Tracer: Gi0/0, Se0/0/0, etc.)*

---

# 3. Configuración y Verificación Inicial (Punto 1 del TP)

## 3.1. Configuración de Dispositivos

Se procedió a configurar las direcciones IP y máscaras de subred en todas las interfaces activas de los routers y PCs, de acuerdo al plan de direccionamiento detallado en la sección 2.2. En los PCs, también se configuró la puerta de enlace predeterminada (Default Gateway) apuntando a la dirección IP de la interfaz LAN del router correspondiente.

![image](https://github.com/user-attachments/assets/385f3302-a65a-42e7-af76-db3732d976ca)

### Configuración de Enrutamiento Estático

Para permitir la comunicación entre las diferentes subredes (LANs 192.168.10.0/24, 192.168.20.0/24, 192.168.30.0/24 y las redes de los enlaces seriales), se configuraron rutas estáticas en cada uno de los routers. Se definieron rutas para alcanzar cada red remota especificando la dirección IP del siguiente salto.

**Rutas Estáticas Configuradas:**

*   **En Router1 (R1):**
    ```
    ip route 192.168.20.0 255.255.255.0 10.0.12.2  ! Hacia LAN R2 vía R2
    ip route 192.168.30.0 255.255.255.0 10.0.13.1  ! Hacia LAN R3 vía R3
    ```
*   **En Router2 (R2):**
    ```
    ip route 192.168.10.0 255.255.255.0 10.0.12.1  ! Hacia LAN R1 vía R1
    ip route 192.168.30.0 255.255.255.0 10.0.23.2  ! Hacia LAN R3 vía R3
    ```
*   **En Router3 (R3):**
    ```
    ip route 192.168.10.0 255.255.255.0 10.0.13.2  ! Hacia LAN R1 vía R1
    ip route 192.168.20.0 255.255.255.0 10.0.23.1  ! Hacia LAN R2 vía R2
    ```

Router 1:

![image](https://github.com/user-attachments/assets/b4dd014c-1597-4928-81f3-1d8b4fdfb01c)

Router 2:

![image](https://github.com/user-attachments/assets/aeb8a2be-7cc0-498b-9dc2-d33384097cf8)

Router 3:

![image](https://github.com/user-attachments/assets/2bd94c48-4824-4f4b-9889-212fd5339426)


## 3.2. Pruebas de Conectividad (ICMP)

Una vez configuradas las IPs y las rutas estáticas, se procedió a verificar la conectividad end-to-end utilizando el comando `ping` (protocolo ICMP) desde las consolas de los PCs.

Se realizaron las siguientes pruebas:
1.  **Ping de cada PC a su gateway:** Para verificar la conectividad dentro de la propia LAN.
2.  **Ping entre PCs de diferentes LANs:** Para verificar el correcto funcionamiento del enrutamiento estático a través de los routers.

**Resultados de las Pruebas `ping`:**

*   **PC0 a Gateway R1 (192.168.10.1):** [Éxito / Fallo]
    <!-- Placeholder para Imagen: Captura de pantalla del ping de PC0 a 192.168.10.1 -->
    ![image](https://github.com/user-attachments/assets/df86db8f-6f27-4ab4-a35d-d715a3870cd9)

*   **PC1 a Gateway R2 (192.168.20.1):** [Éxito / Fallo]
    <!-- Placeholder para Imagen: Captura de pantalla del ping de PC1 a 192.168.20.1 -->
    ![image](https://github.com/user-attachments/assets/09f2f6f9-97cd-4174-aff5-a3b5fd851530)

*   **PC2 a Gateway R3 (192.168.30.1):** [Éxito / Fallo]
    <!-- Placeholder para Imagen: Captura de pantalla del ping de PC2 a 192.168.30.1 -->
    ![image](https://github.com/user-attachments/assets/eac0c2d4-cb75-48a5-93da-89b78bf0e425)

*   **PC0 (192.168.10.10) a PC1 (192.168.20.10):** [Éxito / Fallo]
    <!-- Placeholder para Imagen: Captura de pantalla del ping de PC0 a PC1 -->
    ![image](https://github.com/user-attachments/assets/acea2a69-c7fa-4c7a-a192-8302d0a90ed1)

*   **PC0 (192.168.10.10) a PC2 (192.168.30.10):** [Éxito / Fallo]
    <!-- Placeholder para Imagen: Captura de pantalla del ping de PC0 a PC2 -->
    ![image](https://github.com/user-attachments/assets/b9b638ca-e019-40b4-a1a7-538ae69d0ab8)

*   **PC1 (192.168.20.10) a PC2 (192.168.30.10):** [Éxito / Fallo]
    <!-- Placeholder para Imagen: Captura de pantalla del ping de PC1 a PC2 -->
    ![image](https://github.com/user-attachments/assets/d68e275d-5a83-4a5d-8f72-ff486779f0bc)


**Análisis:** La primera vez que hacemos ping a otra PC el primer paquete demora y se pierde, después, la latencia disminuye, es decir envían y responden rapidamente.

---

# 4. Herramienta de Evaluación: iperf3 (Punto 2 del TP)

## 4.1. Descripción de iperf3

`iperf3` es una herramienta de código abierto ampliamente utilizada para realizar mediciones activas del máximo ancho de banda alcanzable en redes IP. Funciona bajo un modelo cliente-servidor, donde un extremo actúa como servidor esperando conexiones y el otro como cliente iniciando la transferencia de datos para la medición. Permite medir el rendimiento tanto para el protocolo TCP como para UDP.

Además del ancho de banda, `iperf3` puede reportar otras métricas importantes como la pérdida de paquetes y el jitter (variación del retardo entre paquetes), especialmente relevante en pruebas UDP. Es una herramienta muy flexible, configurable mediante diversos parámetros en la línea de comandos.

**Nota sobre Packet Tracer:** Cisco Packet Tracer **no incluye** una implementación funcional de `iperf3`. Para cumplir con los objetivos del TP relacionados con la evaluación de performance (Puntos 3, 4 y 5), se utilizarán las herramientas incorporadas en Packet Tracer, específicamente el **Generador de Tráfico (Traffic Generator)** disponible en los PCs simulados y el **Modo Simulación** para visualizar el flujo y posible pérdida de paquetes. Los parámetros de estas herramientas se configurarán para emular, en la medida de lo posible, las funcionalidades clave de `iperf3`.

## 4.2. Comandos y Parámetros Principales de iperf3

A continuación, se resumen algunos de los comandos y opciones más comunes de `iperf3` (conceptualmente, ya que no se ejecutan directamente en PT):

*   **Modo Servidor:**
    *   `iperf3 -s` : Inicia `iperf3` en modo servidor, escuchando en el puerto por defecto (5201 TCP/UDP).
    *   `iperf3 -s -p <puerto>`: Especifica un puerto diferente para escuchar.

*   **Modo Cliente:**
    *   `iperf3 -c <ip_servidor>`: Inicia `iperf3` en modo cliente, conectándose a la IP del servidor especificada. Realiza una prueba TCP por defecto.
    *   `iperf3 -c <ip_servidor> -p <puerto>`: Se conecta al servidor en un puerto específico.

*   **Parámetros Comunes (Cliente):**
    *   `-u`: Usar protocolo **UDP** en lugar de TCP.
    *   `-b <tasa>`: **Ancho de banda** objetivo para UDP (ej. `10M` para 10 Mbps, `1G` para 1 Gbps). Sin esta opción, UDP por defecto envía a 1 Mbps. Para TCP, intenta usar todo el ancho de banda disponible.
    *   `-t <segundos>`: **Duración** de la prueba en segundos (por defecto 10 segundos).
    *   `-n <bytes>`: **Número de bytes** a transmitir (alternativa a `-t`).
    *   `-k <bloques>`: **Número de bloques** a transmitir (alternativa a `-t` y `-n`).
    *   `-l <tamaño>`: **Tamaño del buffer** de lectura/escritura (TCP) o **tamaño del paquete** a enviar (UDP). Ej: `1400B`. Por defecto suele ser 128KB para TCP y ~1460B para UDP.
    *   `-i <segundos>`: **Intervalo** entre reportes periódicos de ancho de banda/pérdida/jitter (por defecto 1 segundo).
    *   `-R`: Realizar la prueba en **dirección inversa** (servidor envía, cliente recibe).
    *   `-P <n>`: Número de **flujos paralelos** a ejecutar.

Estos parámetros permiten simular diferentes tipos de tráfico y evaluar cómo la red responde bajo diversas cargas y configuraciones. En las siguientes secciones, se describirá cómo se intentó replicar parte de esta funcionalidad con las herramientas de Packet Tracer.

---

# 5. Pruebas de Performance y Captura de Tráfico (Punto 3 del TP)

## 5.1. Metodología de Pruebas en Packet Tracer

Dado que `iperf3` no está disponible, las pruebas de performance se simularon utilizando el **Generador de Tráfico (Traffic Generator)** accesible desde la pestaña `Desktop` de los PCs en Packet Tracer. Para la captura y análisis de tráfico (simulando Wireshark), se utilizó el **Modo Simulación** de Packet Tracer, configurando filtros para observar los protocolos y direcciones IP de interés (ej. TCP, UDP, ICMP, IPs de origen/destino específicas).

El Generador de Tráfico permite crear paquetes personalizados (Tipo: PDU - Protocol Data Unit) especificando:
*   Aplicación/Protocolo (Ej. simulando FTP para TCP, o Video/Voz para UDP).
*   IP de Origen y Destino.
*   Puerto de Origen y Destino.
*   Parámetros de Tráfico: Tamaño del paquete (Size), Tasa de envío (Rate - en paquetes por segundo o pps), Tipo de disparo (One Shot o Periodic).

Se configuró un PC como "servidor" (simplemente el destino del tráfico generado) y otro como "cliente" (el origen del tráfico generado).

![image](https://github.com/user-attachments/assets/bb453c23-690a-4c87-b8a3-8bca2faee073)
![image](https://github.com/user-attachments/assets/92195b0c-f39a-41b1-ae6e-a247904c55dc)

Envio y respuesta de ICMP de PC0 a PC2

## 5.2. Escenario A: Pruebas Intra-Grupo (Dentro de la misma LAN)

**Descripción:** Para simular una prueba entre dos hosts dentro de la misma LAN, y dado que la topología inicial solo tiene un PC por LAN, se añadió temporalmente un segundo PC (`PC0_temp`) a la LAN de R1. Se le asignó la dirección IP `192.168.10.11`, máscara `255.255.255.0` y gateway `192.168.10.1`. La prueba se realizó entre `PC0` (192.168.10.10) y `PC0_temp` (192.168.10.11).

**Prueba A.1: TCP Intra-LAN (PC0 -> PC0_temp)**

*   **Configuración de la Prueba Simulada:**
    *   Protocolo: TCP (simulado con aplicación 'FTP' en Traffic Generator)
    *   Cliente (Origen): PC0 (192.168.10.10)
    *   Servidor (Destino): PC0_temp (192.168.10.11)
    *   Tamaño de Paquete Simulado: 1024 Bytes
    *   Tasa/Duración Simulada: One Shot (un solo paquete)
*   **Resultados:**
    *   **Salida del Traffic Generator:** El generador indicó que el paquete PDU fue enviado. (Ej: "PDU 1 from PC0 to Server0 Sent.").
        <!-- Placeholder para Imagen: Captura Traffic Generator Intra-LAN TCP -->
        ![image](https://github.com/user-attachments/assets/5cc217e0-04b5-4556-b379-46980cce5ec9)

    *   **Captura de Tráfico (Modo Simulación):** Se observó que el tráfico TCP (mostrando típicamente paquetes SYN, SYN-ACK, ACK para el handshake si PT lo detalla, o directamente el segmento de datos) fluyó correctamente desde PC0, atravesó Switch0 y llegó a PC0_temp. Es crucial notar que **el paquete no fue encaminado hacia Router1**, permaneciendo dentro de la LAN. No se observó pérdida de paquetes indicada por Packet Tracer.
        <!-- Placeholder para Imagen: Captura Simulación Intra-LAN TCP -->
        ![image](https://github.com/user-attachments/assets/1aadb9b1-549d-4fab-a383-13bb386ce949)

    *   **Métricas Observadas:** Packet Tracer Traffic Generator no proporciona métricas directas de ancho de banda o latencia. Se verificó la correcta entrega del paquete y la ruta exclusivamente local.


## 5.3. Escenario B: Pruebas Inter-Grupo (Entre distintas LANs)

**Descripción:** Se realizaron pruebas simuladas entre PCs ubicados en diferentes LANs para evaluar el rendimiento a través de la red enrutada. Se probaron las comunicaciones entre los tres grupos/LANs principales.

**Prueba B.1: PC0 (Cliente) -> PC1 (Servidor)**

*   **Configuración (TCP):**
    *   Protocolo: TCP (simulado con 'FTP')
    *   Cliente: PC0 (192.168.10.10)
    *   Servidor: PC1 (192.168.20.10)
    *   Tamaño Paquete: 1024 Bytes
    *   Tasa/Duración: One Shot
*   **Resultados (TCP):**
    <!-- Placeholder para Imagen: Captura TG PC0->PC1 TCP -->
    ![image](https://github.com/user-attachments/assets/e316a733-8da3-4fdd-9783-48db4c91db36)

    <!-- Placeholder para Imagen: Captura Simulación PC0->PC1 TCP (mostrando la ruta R1->R2) -->
    ![image](https://github.com/user-attachments/assets/23475fb8-0588-4bb8-8255-d17d2bc26413)
    
    *   Análisis Simulación (TCP): El paquete TCP fue enviado desde PC0. La simulación mostró que siguió la ruta: `PC0 -> Switch0 -> Router1 -> Router2 -> Switch1 -> PC1`. Esto valida la ruta estática configurada en R1 (`ip route 192.168.20.0 255.255.255.0 10.0.12.2`). No se observaron pérdidas.
    *   Métricas: Entrega verificada, ruta confirmada.
  
![image](https://github.com/user-attachments/assets/669ac29b-3875-45a0-8dae-820bccc26693)

*   **Configuración (UDP):**
    *   Protocolo: UDP (simulado con 'TFTP')
    *   Cliente: PC0 (192.168.10.10)
    *   Servidor: PC2 (192.168.30.10)
    *   Tamaño Paquete: 512 Bytes
    *   Tasa/Duración: One Shot
*   **Resultados (UDP):**
    <!-- Placeholder para Imagen: Captura TG PC0->PC2 UDP -->
    ![image](https://github.com/user-attachments/assets/cdd92562-ad2e-4af4-8086-45bec044d1df)

    <!-- Placeholder para Imagen: Captura Simulación PC0->PC2 UDP -->
    ![image](https://github.com/user-attachments/assets/97eb278b-1134-4ef6-9f54-1f711d7b28d1)

    *   Análisis Simulación (UDP): La ruta seguida fue idéntica a la de TCP (`PC0 -> SW0 -> R1 -> R3 -> SW2 -> PC2`). No se observó handshake. Sin pérdidas.
    *   Métricas: Entrega verificada, ruta confirmada.
  
---

# 6. Análisis de Resultados (Punto 4 del TP)

En base a las pruebas realizadas en la sección 5, se analizan los siguientes aspectos:

*   **¿Cuál es el ancho de banda promedio de la prueba?**
    *   Packet Tracer no proporciona una métrica directa de "ancho de banda promedio" como `iperf3`. Se puede inferir cualitativamente observando si el tráfico fluyó sin problemas aparentes o si hubo congestión/pérdida en el Modo Simulación, por ejemplo la situación observada donde el primer paquete enviado de PC0 a PC1 o PC2 (viceversa también) tenia latencia alta e inlcusive fallaba.

*   **¿Cuánto duró la prueba?**
    *   La duración fue determinada por la configuración del Generador de Tráfico, cada movimiento de paquete duraba aproximadamente 1.3 segundos para 1024, para 512 demoraba aproximadamente 1 segundo.

*   **¿Cuál es el tamaño promedio de paquetes?**
    *   El tamaño fue el configurado en el Generador de Tráfico (1024 y 512)
*   **¿Observas alguna diferencia entre UDP y TCP?**
    *   TCP es **orientado a conexión**, lo que implica un proceso de establecimiento (**handshake 3-way**).
    *   Garantiza la **entrega ordenada y sin pérdidas** de los datos.
    *   En **Packet Tracer** se observa que:
        - Cada paquete enviado genera una **respuesta (ACK)**.
        - El tráfico aparece como **bidireccional**.
        - Si hay problemas en la entrega, el protocolo **reintenta**.
          
    * UDP es **no orientado a conexión**, más **liviano y rápido**.
    * No hay **confirmación de entrega ni control de errores**.
    * En **Packet Tracer** se observa que:
        - Los paquetes simplemente se **envían sin espera de respuesta**.
        - No hay mecanismos de **retransmisión** si el destino no responde.
        - El tráfico es **unidireccional** desde la fuente al destino.


*   **¿Observamos relación entre alguno de los parámetros de la prueba y la pérdida de paquetes?**
    *   Packet Tracer puede indicar paquetes perdidos (dropped) en el Modo Simulación (a menudo con una X roja). [Indica si observaste pérdidas].
    *   ¿Se relacionaron con alguna configuración específica? Por ejemplo:
        *   ¿Enviar tráfico UDP a una tasa muy alta (`-b` en iperf3, Rate en PT) causó pérdidas en enlaces más lentos (seriales)?
        *   ¿Usar tamaños de paquete muy grandes afectó?
    *   [Comenta tus hallazgos. Puede que en PT con configuraciones básicas no se vean pérdidas a menos que la red esté mal configurada o los enlaces sean muy lentos].

*   **Influencia del Enrutamiento Estático:**
    *   Las rutas observadas en el Modo Simulación [Confirma si coincidieron con las rutas estáticas configuradas]. Con enrutamiento estático, la ruta para un destino dado es siempre la misma, definida manualmente. No hay adaptación a cambios en la red o congestión (a diferencia del enrutamiento dinámico).

---

# 7. Prueba Cliente-Servidor Centralizado (Adaptación Punto 5 del TP)

Para simular el escenario propuesto en el punto 5 del TP (un cliente de un grupo hacia un servidor "propuesto en clase"), se designó uno de los PCs como servidor central y se realizaron pruebas desde los otros PCs hacia él.

**Escenario Simulado:**
*   **Servidor Designado:** [Ej. PC2 (192.168.30.10)]
*   **Clientes:** [Ej. PC0 (192.168.10.10) y PC1 (192.168.20.10)]

**Prueba 1: Cliente PC0 -> Servidor PC2**
*   **Configuración:** [Similar a 5.3, indica Protocolo, Tamaño, Tasa/Duración]
*   **Resultados:**
    <!-- Placeholder para Imagen: TG Cliente PC0 -> Servidor PC2 -->
    ![TG Cliente PC0 -> Servidor PC2](path/to/your/tg_client0_server2.png)
    <!-- Placeholder para Imagen: Simulación Cliente PC0 -> Servidor PC2 -->
    ![Simulación Cliente PC0 -> Servidor PC2](path/to/your/sim_client0_server2.png)
    *   Análisis: [Ruta seguida, pérdidas, métricas PT].

**Prueba 2: Cliente PC1 -> Servidor PC2**
*   **Configuración:** [Similar a 5.3, indica Protocolo, Tamaño, Tasa/Duración]
*   **Resultados:**
    <!-- Placeholder para Imagen: TG Cliente PC1 -> Servidor PC2 -->
    ![TG Cliente PC1 -> Servidor PC2](path/to/your/tg_client1_server2.png)
    <!-- Placeholder para Imagen: Simulación Cliente PC1 -> Servidor PC2 -->
    ![Simulación Cliente PC1 -> Servidor PC2](path/to/your/sim_client1_server2.png)
    *   Análisis: [Ruta seguida, pérdidas, métricas PT].

**Comparación y Conclusiones Específicas:**
*   **Comparación con Punto 5.3:** ¿Fueron los resultados (ruta, éxito/fallo, observaciones cualitativas de performance) similares a las pruebas inter-grupo realizadas previamente (ej. PC0->PC2 y PC1->PC2)? [Comenta similitudes/diferencias].
*   **Análisis (Aspectos Punto 4):** Aplicando las preguntas del punto 4 a este escenario centralizado:
    *   Ancho de banda (cualitativo): [Comentario]
    *   Duración/Tamaño: [Comentario]
    *   Diferencias TCP/UDP (si se probaron ambos): [Comentario]
    *   Pérdidas: [Comentario]
*   **Conclusión del Escenario:** [Resume si la comunicación hacia el servidor centralizado funcionó como se esperaba bajo la configuración de enrutamiento estático].

---

# 8. Conclusiones Generales

Este trabajo práctico permitió aplicar conceptos teóricos de redes en un entorno simulado mediante Cisco Packet Tracer. Se logró diseñar e implementar exitosamente la topología multi-path propuesta, configurar el direccionamiento IP y establecer la conectividad completa entre todas las subredes utilizando enrutamiento estático.

Las pruebas de conectividad inicial con `ping` confirmaron la correcta configuración básica de la red. Si bien no fue posible utilizar `iperf3` directamente, se exploraron sus funcionalidades y se intentó emular pruebas de performance utilizando el Generador de Tráfico y el Modo Simulación de Packet Tracer. Estas herramientas, aunque limitadas en cuanto a la precisión de las métricas de rendimiento (como ancho de banda real), fueron útiles para:
*   Visualizar el flujo de paquetes TCP y UDP a través de la red.
*   Verificar las rutas tomadas según las configuraciones de enrutamiento estático.
*   Observar cualitativamente el comportamiento de los protocolos y detectar posibles puntos de falla o pérdida de paquetes simulados.

Se identificaron las diferencias conceptuales entre TCP y UDP y se observaron algunas de ellas en la simulación. Se analizó cómo los parámetros configurados (tamaño de paquete, tasa de envío simulada) podrían influir en el tráfico, aunque la detección de pérdidas fue [Indica si observaste pérdidas o no, y si PT facilitó su detección].

La principal limitación encontrada fue la incapacidad de Packet Tracer para ejecutar herramientas de medición de performance estándar como `iperf3`, lo que restringe la obtención de métricas cuantitativas precisas de ancho de banda, jitter y pérdida en escenarios realistas. Sin embargo, como herramienta didáctica para comprender el flujo de datos, el enrutamiento y la configuración de protocolos, Packet Tracer demostró ser valioso.

Como trabajo futuro, sería interesante implementar enrutamiento dinámico (como OSPF o EIGRP) sobre la misma topología y comparar el comportamiento de las rutas, la convergencia y, si fuera posible en un entorno real o con simuladores más avanzados (GNS3, EVE-NG), medir la performance y la resiliencia ante fallos de enlaces.

En resumen, se cumplieron los objetivos principales del TP adaptados al entorno de simulación, reforzando la comprensión de direccionamiento, enrutamiento estático y los principios básicos de la evaluación de performance en redes.

---

# 9. Bibliografía

*   [Si usaste algún libro, web, manual específico, cítalo aquí. Ej: Kurose, J. F., & Ross, K. W. (2017). Computer Networking: A Top-Down Approach.]
*   [Documentación de Cisco Packet Tracer (si aplica)]
*   [Página oficial de iperf3: https://iperf.fr/]

---

# 10. Anexos

*(Opcional: Incluye aquí configuraciones completas de los routers (`show running-config`), tablas de enrutamiento detalladas, o cualquier otra información extensa que no encaje bien en el cuerpo principal del informe)*

*   **Anexo A:** Configuración completa de Router1.
    ```
    Router# show running-config
    [Pega aquí la configuración]
    ```
*   **Anexo B:** Configuración completa de Router2.
    ```
    Router# show running-config
    [Pega aquí la configuración]
    ```
*   **Anexo C:** Configuración completa de Router3.
    ```
    Router# show running-config
    [Pega aquí la configuración]
    ```
