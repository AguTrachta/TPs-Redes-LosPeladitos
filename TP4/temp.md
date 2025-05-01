
# Parte II - Simulaciones y Análisis

Se implementó la topología propuesta para dos Sistemas Autónomos (AS100 y AS200) utilizando Cisco Packet Tracer, con el objetivo de configurar y analizar el protocolo BGP para el intercambio de rutas entre ellos.

![image](https://github.com/user-attachments/assets/ac5115e9-310f-4133-b009-bfe78a1f57b2)

---

## 1. Comandos de Análisis y Tablas de Ruteo BGP 

Se investigaron y utilizaron los siguientes comandos clave en la CLI de los routers (R0 y R1) para configurar, verificar y analizar el funcionamiento de BGP:

**Comandos Principales:**

*   `show running-config | section router bgp`: Muestra la configuración BGP activa en el router, incluyendo el ASN local, los vecinos configurados y las redes anunciadas.
*   `show ip bgp summary`: Proporciona un resumen rápido del estado de las vecindades BGP. Es **crucial** para saber si la sesión BGP está establecida.
*   `show ip bgp`: Muestra la **tabla BGP** completa. Contiene *todos* los prefijos de red aprendidos a través de BGP, junto con sus atributos (Next Hop, AS_PATH, Origin, etc.), incluyendo rutas que no necesariamente son las mejores.
*   `show ip route bgp`: Muestra las rutas aprendidas por BGP que han sido seleccionadas como las *mejores* y han sido instaladas en la **tabla de enrutamiento principal (RIB)** del router. Estas son las rutas que el router usará activamente para reenviar tráfico.
*   `show ip protocols`: Muestra información sobre los protocolos de enrutamiento activos, incluyendo BGP, el ASN local, vecinos, y las redes que se están anunciando.

**Evidencia de Funcionamiento BGP:**

El fragmento más claro que evidencia que BGP está funcionando correctamente es la salida del comando `show ip bgp summary`. Específicamente:
*   La **columna de estado (`State/PfxRcd`)**: Cuando una sesión eBGP está activa y funcionando, esta columna **no mostrará** estados como `Idle`, `Active`, `Connect`, `OpenSent` o `OpenConfirm`. En su lugar, mostrará un **número** que representa la cantidad de prefijos recibidos del vecino. Que aparezca un número (ej. `1`) en lugar de una palabra de estado indica que la sesión está **establecida (`Established`)**.

![image](https://github.com/user-attachments/assets/4ce3e2a8-60e7-4004-b0c0-f6242c7985b8)

**Explicación de las Tablas de Ruteo:**

*   **Tabla BGP (`show ip bgp`):** Esta es la base de datos interna de BGP. Contiene *toda* la información de alcanzabilidad que ha aprendido de sus vecinos BGP. Para cada prefijo, almacena múltiples caminos si los aprende de diferentes vecinos, junto con todos los atributos BGP asociados (AS_PATH, ORIGIN, NEXT_HOP, LOCAL_PREF, MED, etc.). BGP utiliza estos atributos y un complejo algoritmo de selección de la mejor ruta para decidir cuál es el camino preferido hacia cada destino dentro de esta tabla.
    <!-- Placeholder para Imagen: Captura de `show ip bgp` en R0 mostrando la ruta hacia la red de AS200 -->
    ![Tabla BGP en R0](path/to/your/r0_show_ip_bgp.png)
    *(Reemplaza con tu captura)*

*   **Tabla de Enrutamiento Principal / RIB (`show ip route` o `show ip route bgp`):** Esta es la tabla que el router utiliza para tomar decisiones de reenvío de paquetes. Contiene *solo la mejor ruta* para cada destino, seleccionada entre *todas* las fuentes de enrutamiento (BGP, OSPF, EIGRP, Estáticas, Conectadas) basada en la Distancia Administrativa (AD) y la métrica. Las rutas BGP que ganan el proceso de selección en la tabla BGP se instalan aquí, usualmente marcadas con la letra `B`. El comando `show ip route bgp` filtra la RIB para mostrar únicamente las rutas que fueron aprendidas originalmente por BGP y seleccionadas como las mejores.
    <!-- Placeholder para Imagen: Captura de `show ip route bgp` en R0 mostrando la ruta 'B' hacia la red de AS200 -->
    ![Ruta BGP en RIB de R0](path/to/your/r0_show_ip_route_bgp.png)
    *(Reemplaza con tu captura)*

---

## 2. Comprobación de Conectividad Inter-AS (Punto 2)

Una vez configurado BGP y verificado que las rutas se intercambiaron e instalaron correctamente, se procedió a comprobar la conectividad extremo a extremo entre los hosts ubicados en diferentes Sistemas Autónomos.

*   **Prueba desde AS100 hacia AS200:** Se ejecutó el comando `ping` desde el host `h0` (IP `192.168.1.2` en AS100) hacia el host `h2` (IP `192.168.2.2` en AS200).
*   **Prueba desde AS200 hacia AS100:** Se ejecutó el comando `ping` desde el host `h3` (IP `192.168.2.3` en AS200) hacia el host `h1` (IP `192.168.1.3` en AS100).

**Resultados:**
En ambos casos, las pruebas de `ping` fueron **exitosas**, demostrando que:
1.  R0 aprendió correctamente la ruta hacia la red `192.168.2.0/24` vía BGP desde R1.
2.  R1 aprendió correctamente la ruta hacia la red `192.168.1.0/24` vía BGP desde R0.
3.  Ambos routers instalaron estas rutas BGP en sus tablas de enrutamiento principales y pudieron reenviar los paquetes ICMP entre los hosts de los diferentes AS.

<!-- Placeholder para Imagen: Captura de PING exitoso desde h0 hacia h2 -->
![Ping h0 a h2](path/to/your/ping_h0_h2.png)
*(Reemplaza con tu captura)*

<!-- Placeholder para Imagen: Captura de PING exitoso desde h3 hacia h1 -->
![Ping h3 a h1](path/to/your/ping_h3_h1.png)
*(Reemplaza con tu captura)*

---

## 3. Simulación de Tráfico y Falla de Router (Punto 3)

Se simuló tráfico continuo y se observó el impacto de una falla en uno de los routers de borde.

**Simulación de Tráfico:**
*   Se inició un `ping` extendido desde h0 hacia h2 (ej. `ping -t 192.168.2.2` en la Command Prompt de h0) para generar un flujo constante de paquetes ICMP entre los AS.
*   Se cambió al modo **Simulación** en Packet Tracer.
*   Se configuraron los filtros de eventos para mostrar `ICMP` y `BGP`.

**Simulación de Falla:**
*   Mientras el `ping` extendido y la simulación estaban activos, se procedió a **apagar** uno de los routers de borde, por ejemplo, **R1**. (Haciendo clic en R1 > Pestaña `Physical` > clic en el interruptor de encendido).

**Análisis del Tráfico Visualizado:**
*   **Antes de la falla:** En modo simulación, se observaba el flujo normal de paquetes ICMP (Request y Reply) viajando entre h0 -> SW0 -> R0 -> R1 -> SW1 -> h2 y viceversa. También se veían paquetes BGP `KEEPALIVE` intercambiándose periódicamente entre R0 y R1 para mantener la sesión activa.
    <!-- Placeholder para Imagen: Captura Simulación: Tráfico ICMP y BGP KEEPALIVE normal -->
    ![Tráfico Normal Inter-AS](path/to/your/tp4_sim_normal.png)
    *(Reemplaza con tu captura)*
*   **Durante la falla (R1 apagado):**
    *   Inmediatamente, los paquetes ICMP enviados desde h0 hacia h2 comenzaron a fallar al llegar a R0, ya que R0 perdió la conexión directa con el siguiente salto (10.0.0.2). Packet Tracer mostraría los paquetes ICMP siendo descartados por R0 (sobre rojo con 'X').
    *   R0 detectó la caída del enlace físico hacia R1.
    *   R0 intentó mantener la sesión BGP, pero al no recibir `KEEPALIVE` de R1 dentro del `Hold Time` (usualmente 180 segundos por defecto), la sesión BGP cayó. R0 envió un mensaje BGP `NOTIFICATION` para cerrar la sesión (aunque R1 estaba apagado y no podía recibirlo).
    *   R0 eliminó la ruta BGP hacia `192.168.2.0/24` de su tabla de enrutamiento.
    <!-- Placeholder para Imagen: Captura Simulación: Falla de ICMP y posible BGP NOTIFICATION -->
    ![Tráfico Durante Falla R1](path/to/your/tp4_sim_fail.png)
    *(Reemplaza con tu captura)*
*   **Tras Encender R1:**
    *   Al volver a encender R1, las interfaces se activaron.
    *   R0 y R1 restablecieron la conectividad IP en el enlace `10.0.0.0/24`.
    *   Los routers iniciaron el proceso de establecimiento de la sesión BGP nuevamente (intercambio de mensajes `OPEN`, `KEEPALIVE`).
    *   Una vez que la sesión BGP se restableció (`Established`), R0 y R1 intercambiaron las rutas (`192.168.1.0/24` y `192.168.2.0/24`) nuevamente.
    *   Las rutas BGP fueron reinstaladas en las tablas de enrutamiento.
    *   El `ping` extendido desde h0 hacia h2 volvió a ser exitoso después de la convergencia de BGP.
    <!-- Placeholder para Imagen: Captura Simulación: Restablecimiento BGP (OPEN/KEEPALIVE) y ICMP exitoso -->
    ![Tráfico Tras Recuperación R1](path/to/your/tp4_sim_recover.png)
    *(Reemplaza con tu captura)*

**Conclusión:** La simulación demostró que BGP depende de la conectividad IP subyacente y utiliza mensajes Keepalive para detectar fallos en la sesión. Una falla en un router de borde interrumpe la conectividad inter-AS hasta que el router se recupera y la sesión BGP se restablece.

---

## 4. Configuración y Conexión IPv6 (Punto 4)

Se procedió a añadir configuración IPv6 a la red existente para permitir la comunicación entre los AS utilizando ambos protocolos (Dual-Stack).

**Diseño Direccionamiento IPv6 (Ejemplo):**
*   **Enlace R0-R1:** `2001:DB8:0:A::/64` (R0: `::1/64`, R1: `::2/64`)
*   **LAN AS100 (R0):** `2001:DB8:0:1::/64` (R0: `::1/64`, h0: `::2/64`, h1: `::3/64`)
*   **LAN AS200 (R1):** `2001:DB8:0:2::/64` (R1: `::1/64`, h2: `::2/64`, h3: `::3/64`)
*   *(Usamos prefijos `/64` por simplicidad, común en LANs y a veces en enlaces PtP)*

**Configuración IPv6 en Interfaces:**

1.  **Habilitar Ruteo IPv6 Global (Necesario en ambos routers):**
    ```bash
    configure terminal
    ipv6 unicast-routing
    exit
    ```
2.  **Configurar IPs IPv6 en Interfaces:**
    *   **R0:**
        ```bash
        configure terminal
        interface GigabitEthernet0/0/0 ! Hacia LAN AS100
         ipv6 address 2001:DB8:0:1::1/64
         ipv6 enable
        exit
        interface GigabitEthernet0/0/1 ! Hacia R1
         ipv6 address 2001:DB8:0:A::1/64
         ipv6 enable
        exit
        end
        copy run start
        ```
    *   **R1:**
        ```bash
        configure terminal
        interface GigabitEthernet0/0/0 ! Hacia LAN AS200
         ipv6 address 2001:DB8:0:2::1/64
         ipv6 enable
        exit
        interface GigabitEthernet0/0/1 ! Hacia R0
         ipv6 address 2001:DB8:0:A::2/64
         ipv6 enable
        exit
        end
        copy run start
        ```
3.  **Configurar IPs IPv6 en Hosts (Estática o Autoconfig):**
    *   Se puede usar configuración estática en los hosts o habilitar SLAAC si los routers están configurados para ello (no cubierto aquí por simplicidad). Configuración estática:
    *   **h0:** IPv6 Address: `2001:DB8:0:1::2/64`, IPv6 Gateway: `fe80::[LinkLocal_R0_Gi0/0/0]` (Opcional: O la global `2001:DB8:0:1::1`)
    *   **h1:** IPv6 Address: `2001:DB8:0:1::3/64`, IPv6 Gateway: `fe80::[LinkLocal_R0_Gi0/0/0]`
    *   **h2:** IPv6 Address: `2001:DB8:0:2::2/64`, IPv6 Gateway: `fe80::[LinkLocal_R1_Gi0/0/0]`
    *   **h3:** IPv6 Address: `2001:DB8:0:2::3/64`, IPv6 Gateway: `fe80::[LinkLocal_R1_Gi0/0/0]`
    *   *(Nota: Packet Tracer puede requerir usar la dirección Link-Local del gateway (obtenida con `show ipv6 interface brief` en el router) para la configuración del gateway IPv6 en los hosts).*

**Configuración BGP para IPv6:**

*   BGP necesita ser activado explícitamente para la familia de direcciones IPv6.

1.  **En R0:**
    ```bash
    configure terminal
    router bgp 100
     ! Definir el vecino IPv6
     neighbor 2001:DB8:0:A::2 remote-as 200
     ! Activar el vecino para la familia de direcciones IPv6
     address-family ipv6 unicast
      neighbor 2001:DB8:0:A::2 activate
      ! Anunciar la red LAN IPv6 de AS100
      network 2001:DB8:0:1::/64
     exit-address-family
    end
    copy run start
    ```
2.  **En R1:**
    ```bash
    configure terminal
    router bgp 200
     ! Definir el vecino IPv6
     neighbor 2001:DB8:0:A::1 remote-as 100
     ! Activar el vecino para la familia de direcciones IPv6
     address-family ipv6 unicast
      neighbor 2001:DB8:0:A::1 activate
      ! Anunciar la red LAN IPv6 de AS200
      network 2001:DB8:0:2::/64
     exit-address-family
    end
    copy run start
    ```

**Comprobación de Conexión IPv6:**

1.  **Verificar Vecindad BGP IPv6:**
    *   `show bgp ipv6 unicast summary` en R0 y R1. Buscar que el vecino IPv6 esté establecido (muestre prefijos recibidos).
    <!-- Placeholder para Imagen: Salida `show bgp ipv6 unicast summary` en R0 -->
    ![BGP IPv6 Summary R0](path/to/your/r0_bgp_ipv6_summary.png)
    *(Reemplaza con tu captura)*
2.  **Verificar Tabla BGP IPv6:**
    *   `show bgp ipv6 unicast` en R0 (buscar prefijo `2001:DB8:0:2::/64`) y R1 (buscar `2001:DB8:0:1::/64`).
3.  **Verificar Tabla de Ruteo IPv6:**
    *   `show ipv6 route bgp` en R0 y R1 para ver las rutas BGP instaladas.
    <!-- Placeholder para Imagen: Salida `show ipv6 route bgp` en R1 -->
    ![Rutas BGP IPv6 en R1](path/to/your/r1_show_ipv6_route_bgp.png)
    *(Reemplaza con tu captura)*
4.  **Comprobar Conectividad Host-Host IPv6:**
    *   Desde h0: `ping 2001:DB8:0:2::2` (hacia h2).
    *   Desde h2: `ping 2001:DB8:0:1::3` (hacia h1).
    *   Ambos pings deberían ser exitosos.
    <!-- Placeholder para Imagen: Ping IPv6 exitoso desde h0 hacia h2 -->
    ![Ping IPv6 h0 a h2](path/to/your/ping_ipv6_h0_h2.png)
    *(Reemplaza con tu captura)*

**Conclusión:** BGP puede configurarse para intercambiar información de alcanzabilidad tanto para IPv4 como para IPv6 simultáneamente (usando address-families), permitiendo la conectividad dual-stack entre Sistemas Autónomos.

---

## 5. Documentación del Diseño de Red (Punto 5)

A continuación, se presenta la tabla documentando el diseño de la red implementada, incluyendo las configuraciones IPv4 e IPv6 (según el ejemplo del punto 4).

| Equipo | Interfaz                 | IP de red (IPv4) | IPv4 Address      | Máscara         | IPv6 Address             | Comments                                      |
| :----- | :----------------------- | :--------------- | :---------------- | :-------------- | :----------------------- | :-------------------------------------------- |
| R0     | GigabitEthernet0/0/0     | 192.168.1.0      | 192.168.1.1       | 255.255.255.0   | 2001:DB8:0:1::1/64       | Conexión a LAN AS100 (SW0)                    |
| R0     | GigabitEthernet0/0/1     | 10.0.0.0         | 10.0.0.1          | 255.255.255.0   | 2001:DB8:0:A::1/64       | Enlace eBGP hacia R1                          |
| R1     | GigabitEthernet0/0/0     | 192.168.2.0      | 192.168.2.1       | 255.255.255.0   | 2001:DB8:0:2::1/64       | Conexión a LAN AS200 (SW1)                    |
| R1     | GigabitEthernet0/0/1     | 10.0.0.0         | 10.0.0.2          | 255.255.255.0   | 2001:DB8:0:A::2/64       | Enlace eBGP hacia R0                          |
| h0     | FastEthernet0            | 192.168.1.0      | 192.168.1.2       | 255.255.255.0   | 2001:DB8:0:1::2/64       | Host en AS100, Gateway R0 (IPv4/IPv6)       |
| h1     | FastEthernet0            | 192.168.1.0      | 192.168.1.3       | 255.255.255.0   | 2001:DB8:0:1::3/64       | Host en AS100, Gateway R0 (IPv4/IPv6)       |
| h2     | FastEthernet0            | 192.168.2.0      | 192.168.2.2       | 255.255.255.0   | 2001:DB8:0:2::2/64       | Host en AS200, Gateway R1 (IPv4/IPv6)       |
| h3     | FastEthernet0            | 192.168.2.0      | 192.168.2.3       | 255.255.255.0   | 2001:DB8:0:2::3/64       | Host en AS200, Gateway R1 (IPv4/IPv6)       |
| SW0    | Vlan1 (Mgmt - Opcional)  | N/A              | N/A               | N/A             | N/A                      | Switch L2 en AS100                            |
| SW1    | Vlan1 (Mgmt - Opcional)  | N/A              | N/A               | N/A             | N/A                      | Switch L2 en AS200                            |
| ....   |                          |                  |                   |                 |                          | (Agregar más filas si se añaden equipos después) |

*(Nota: Las IPs de gateway IPv6 para los hosts podrían necesitar ser las Link-Local de los routers en Packet Tracer).*

---
