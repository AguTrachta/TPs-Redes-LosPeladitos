
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
  
![image](https://github.com/user-attachments/assets/410761f7-c0f8-43a6-adcc-ae39e887cffd)

*   **Tabla de Enrutamiento Principal / RIB (`show ip route` o `show ip route bgp`):** Esta es la tabla que el router utiliza para tomar decisiones de reenvío de paquetes. Contiene *solo la mejor ruta* para cada destino, seleccionada entre *todas* las fuentes de enrutamiento (BGP, OSPF, EIGRP, Estáticas, Conectadas) basada en la Distancia Administrativa (AD) y la métrica. Las rutas BGP que ganan el proceso de selección en la tabla BGP se instalan aquí, usualmente marcadas con la letra `B`. El comando `show ip route bgp` filtra la RIB para mostrar únicamente las rutas que fueron aprendidas originalmente por BGP y seleccionadas como las mejores.

![image](https://github.com/user-attachments/assets/b127a8bb-b8e7-474e-82ed-e8835b6e016f)

---

## 2. Comprobación de Conectividad Inter-AS 

Una vez configurado BGP y verificado que las rutas se intercambiaron e instalaron correctamente, se procedió a comprobar la conectividad extremo a extremo entre los hosts ubicados en diferentes Sistemas Autónomos.

*   **Prueba desde AS100 hacia AS200:** Se ejecutó el comando `ping` desde el host `h0` (IP `192.168.1.2` en AS100) hacia el host `h2` (IP `192.168.2.2` en AS200).
*   **Prueba desde AS200 hacia AS100:** Se ejecutó el comando `ping` desde el host `h3` (IP `192.168.2.3` en AS200) hacia el host `h1` (IP `192.168.1.3` en AS100).

**Resultados:**
En ambos casos, las pruebas de `ping` fueron **exitosas**, demostrando que:
1.  R0 aprendió correctamente la ruta hacia la red `192.168.2.0/24` vía BGP desde R1.
2.  R1 aprendió correctamente la ruta hacia la red `192.168.1.0/24` vía BGP desde R0.
3.  Ambos routers instalaron estas rutas BGP en sus tablas de enrutamiento principales y pudieron reenviar los paquetes ICMP entre los hosts de los diferentes AS.

![image](https://github.com/user-attachments/assets/a8d80563-e014-46ea-9e90-16e7b03947ca)

Ping de h0 a h2

![image](https://github.com/user-attachments/assets/e5a81b43-1e57-43e8-bc9f-3a388975b3fd)

Ping de h3 a h1


---

## 3. Simulación de Tráfico y Falla de Router

Se simuló tráfico continuo y se observó el impacto de una falla en uno de los routers de borde.

**Simulación de Tráfico:**
*   Se inició un `ping` extendido desde h0 hacia h2 (`ping -t 192.168.2.2` en la Command Prompt de h0) para generar un flujo constante de paquetes ICMP entre los AS.
*   Se cambió al modo **Simulación** en Packet Tracer.
*   Se configuraron los filtros de eventos para mostrar `ICMP` y `BGP`.

**Simulación de Falla:**
*   Mientras el `ping` extendido y la simulación estaban activos, se procedió a **apagar** uno de los routers de borde, por ejemplo, **R1**. (Haciendo clic en R1 > Pestaña `Physical` > clic en el interruptor de encendido).

**Análisis del Tráfico Visualizado:**
*   **Antes de la falla:** En modo simulación, se observaba el flujo normal de paquetes ICMP (Request y Reply) viajando entre h0 -> SW0 -> R0 -> R1 -> SW1 -> h2 y viceversa. También se veían paquetes BGP `KEEPALIVE` intercambiándose periódicamente entre R0 y R1 para mantener la sesión activa.

![image](https://github.com/user-attachments/assets/0b14ccc7-c0f8-480e-8b4b-d2a3c580a8f3)

*   **Durante la falla (R1 apagado):**
    *   Inmediatamente, los paquetes ICMP enviados desde h0 hacia h2 comenzaron a fallar al llegar a R0, ya que R0 perdió la conexión directa con el siguiente salto (10.0.0.2). Packet Tracer mostraría los paquetes ICMP siendo descartados por R0 (sobre rojo con 'X').
    *   R0 detectó la caída del enlace físico hacia R1.
    *   R0 intentó mantener la sesión BGP, pero al no recibir `KEEPALIVE` de R1 dentro del `Hold Time` (usualmente 180 segundos por defecto), la sesión BGP cayó. R0 envió un mensaje BGP `NOTIFICATION` para cerrar la sesión (aunque R1 estaba apagado y no podía recibirlo).
    *   R0 eliminó la ruta BGP hacia `192.168.2.0/24` de su tabla de enrutamiento.

 ![image](https://github.com/user-attachments/assets/eeb17f35-1f7c-407d-966a-c41eeae23b87)

*   **Tras Encender R1:**
    *   Al volver a encender R1, las interfaces se activaron.
    *   R0 y R1 restablecieron la conectividad IP en el enlace `10.0.0.0/24`.
    *   Los routers iniciaron el proceso de establecimiento de la sesión BGP nuevamente (intercambio de mensajes `OPEN`, `KEEPALIVE`).
    *   Una vez que la sesión BGP se restableció (`Established`), R0 y R1 intercambiaron las rutas (`192.168.1.0/24` y `192.168.2.0/24`) nuevamente.
    *   Las rutas BGP fueron reinstaladas en las tablas de enrutamiento.
    *   El `ping` extendido desde h0 hacia h2 volvió a ser exitoso después de la convergencia de BGP.

**Conclusión:** La simulación demostró que BGP depende de la conectividad IP subyacente y utiliza mensajes Keepalive para detectar fallos en la sesión. Una falla en un router de borde interrumpe la conectividad inter-AS hasta que el router se recupera y la sesión BGP se restablece.

---

---

## 4. Configuración y Conexión IPv6 

Se intentó añadir configuración IPv6 a la red para lograr conectividad dual-stack entre AS100 y AS200. Si bien la configuración básica de direcciones IPv6 en interfaces y hosts es posible, **se encontró una limitación importante en Cisco Packet Tracer respecto a la configuración de BGP para intercambiar rutas IPv6.**

**Limitación de BGP IPv6 en Packet Tracer:**
Al intentar configurar la vecindad BGP utilizando las direcciones IPv6 de los routers vecinos (comando `neighbor <ipv6-address> remote-as <asn>` dentro del proceso `router bgp <asn>`), Packet Tracer genera un error (`% Invalid input detected`). Esto indica que la implementación de BGP en la versión utilizada de Packet Tracer no soporta completamente la configuración de sesiones BGP sobre IPv6 de esta manera directa, o requiere un método diferente (como usar address-families que también puede ser limitado en PT).

**Por lo tanto, no fue posible establecer el intercambio dinámico de rutas IPv6 entre R0 y R1 usando BGP en esta simulación.**

**Configuración de Conectividad IPv6 Básica:**

A pesar de la limitación de BGP, se procedió a configurar las direcciones IPv6 en las interfaces de los routers y hosts para establecer la conectividad básica dentro de cada AS y en el enlace entre R0 y R1.

1.  **Habilitar Ruteo IPv6 Global:** Es fundamental ejecutar `ipv6 unicast-routing` en modo de configuración global en **ambos routers (R0 y R1)** para que puedan enrutar paquetes IPv6.
    ```bash
    configure terminal
    ipv6 unicast-routing
    exit
    ```
2.  **Asignar Direcciones IPv6 a Interfaces de Routers:** Se asignaron direcciones globales únicas (GUA) y se habilitó IPv6 en las interfaces relevantes. (Se usó el plan del intento anterior como ejemplo).
    *   **R0:**
        *   `interface GigabitEthernet0/0/0` (LAN): `ipv6 address 2001:DB8:0:1::1/64`, `ipv6 enable`
        *   `interface GigabitEthernet0/0/1` (WAN): `ipv6 address 2001:DB8:0:A::1/64`, `ipv6 enable`
    *   **R1:**
        *   `interface GigabitEthernet0/0/0` (LAN): `ipv6 address 2001:DB8:0:2::1/64`, `ipv6 enable`
        *   `interface GigabitEthernet0/0/1` (WAN): `ipv6 address 2001:DB8:0:A::2/64`, `ipv6 enable`
    *   Se verificó la asignación y la generación de direcciones Link-Local con `show ipv6 interface brief`.
    *   
![image](https://github.com/user-attachments/assets/1c09d528-a5ea-4163-a00c-1b9c1309fa78)

**Comprobación de Conectividad IPv6 (Limitada a enlaces directos y misma LAN):**

*   Desde R0: `ping 2001:DB8:0:A::2` (Ping a R1 en el enlace directo) 
*   Desde h0: `ping 2001:DB8:0:1::1` (Ping a su gateway R0)
*   Desde h0: `ping 2001:DB8:0:1::3` (Ping a h1 en la misma LAN)
*   Desde h0: `ping 2001:DB8:0:2::2` (Ping a h2 en AS200) -> **NO FUNCIONA**

**Conclusión Conceptual (Cómo Debería Funcionar BGP):**
En un entorno real o con un simulador más completo, BGP utilizaría **MP-BGP (Multi-Protocol BGP)** y **Address Families** para manejar IPv6. La configuración dentro de `router bgp <asn>` incluiría una sección `address-family ipv6 unicast` donde se activarían los vecinos IPv6 (`neighbor <ipv6> activate`) y se anunciarían las redes IPv6 (`network <ipv6-prefix>`). Esto permitiría el intercambio dinámico de rutas IPv6, eliminando la necesidad de rutas estáticas. Debido a las limitaciones de Packet Tracer, recurrimos a rutas estáticas para lograr la conectividad IPv6 inter-AS requerida para las pruebas.

---

## 5. Documentación del Diseño de Red 

A continuación, se presenta la tabla documentando el diseño de la red implementada, incluyendo las configuraciones IPv4 e IPv6.

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
| SW0    | Vlan1  | N/A              | N/A               | N/A             | N/A                      | Switch L2 en AS100                            |
| SW1    | Vlan1  | N/A              | N/A               | N/A             | N/A                      | Switch L2 en AS200                            |

---

## 6. Extensión del Sistema Autónomo AS100 

Se procedió a expandir la topología dentro del Sistema Autónomo 100 (AS100) para simular una red interna más compleja, añadiendo los siguientes componentes:
*   Un nuevo router interno (`R0_interno`).
*   Un nuevo switch (`SW_interno`) conectado a `R0_interno`.
*   Un nuevo host (`h4`) conectado a `SW_interno`.
*   Un enlace punto a punto entre el router de borde existente (`R0`) y el nuevo router interno (`R0_interno`).

Se asignó el direccionamiento IP correspondiente a los nuevos enlaces y la nueva LAN:
*   Enlace R0-R0_interno: `192.168.100.0/30`
*   LAN h4 (conectada a R0_interno): `192.168.101.0/24`

![image](https://github.com/user-attachments/assets/56ec3335-2770-4014-b539-66b79e3c35b2)

---

## 7. Configuración de Enrutamiento Interno en AS100 (OSPF)

Para permitir la comunicación dentro del AS100 expandido (específicamente, para que R0 conozca la nueva LAN de h4 y R0_interno conozca las otras redes internas y cómo salir del AS), se configuró un protocolo de enrutamiento interior (IGP). Se eligió **OSPF (Proceso ID 10)**.

*   OSPF se habilitó en las interfaces relevantes de **R0** y **R0_interno**.
*   Las redes anunciadas en OSPF Area 0 fueron:
    *   En R0: `192.168.1.0/24` (LAN original h0/h1) y `192.168.100.0/30` (Enlace a R0_interno).
    *   En R0_interno: `192.168.100.0/30` (Enlace a R0) y `192.168.101.0/24` (LAN h4).

Se verificó la correcta formación de la **vecindad OSPF** entre R0 y R0_interno usando `show ip ospf neighbor`.

![image](https://github.com/user-attachments/assets/61c06ce2-1db1-4244-8eb3-c8386a182eb9)


Se verificó el **aprendizaje de rutas OSPF** en las tablas de enrutamiento:
*   En R0 (`show ip route ospf`), se observó la ruta `O` hacia `192.168.101.0/24`.
*   En R0_interno (`show ip route ospf`), se observó la ruta `O` hacia `192.168.1.0/24`.

![image](https://github.com/user-attachments/assets/298b04af-8fa1-4bb8-b7cf-f84100b2abb0)

Finalmente, se comprobó la conectividad interna dentro de AS100 mediante `ping` entre `h4` y `h0`, el cual fue exitoso.

![image](https://github.com/user-attachments/assets/97dfb5b1-23e9-4576-aec3-19c7cd32382a)

---

## 8. Redistribución de OSPF en BGP 

El objetivo de este paso fue hacer que la red interna de AS100, específicamente la nueva LAN de h4 (`192.168.101.0/24`) aprendida por R0 a través de OSPF, fuera visible para el AS vecino (AS200). Esto requiere que el router de borde (R0) **redistribuya** las rutas OSPF dentro de su proceso BGP.

**Configuración de Redistribución:**
*   En el router de borde `R0`, dentro de la configuración `router bgp 100`, se añadió el comando `redistribute ospf 10`. Este comando instruye a BGP para que tome las rutas aprendidas por OSPF proceso 10 y las anuncie a sus vecinos BGP.

**Análisis de Configuración y Tablas:**

1.  **Configuración BGP:** Se verificó la configuración de R0 (`show running-config | section router bgp`) para confirmar la presencia del comando `redistribute ospf 10`. La configuración de R1 no requirió cambios.

![image](https://github.com/user-attachments/assets/f3e02f33-6d79-437d-9dd7-c5912e545358)


2.  **Tabla BGP de R0 (`show ip bgp`):** Se observó que, además de la red `192.168.1.0` (anunciada con `network`), R0 ahora también incluía la red `192.168.101.0` en su tabla BGP, marcada con un origen `?` (Incomplete), indicando que fue redistribuida.

![image](https://github.com/user-attachments/assets/fd043368-9d65-41c9-9d31-ee34b5accb59)


3.  **Tabla BGP de R1 (`show ip bgp`):** ¡Crucial! Se verificó que R1 (en AS200) **ahora aprendía la ruta hacia `192.168.101.0/24`** de su vecino R0 (10.0.0.1). La ruta mostraba un AS_PATH de `100` y origen `?`.

![image](https://github.com/user-attachments/assets/e83f73cb-0d33-4f62-baf7-5d09cb4ede83)


4.  **Tabla de Ruteo de R1 (`show ip route bgp`):** Se confirmó que R1 instaló la ruta hacia `192.168.101.0/24` en su RIB, marcada con `B`, indicando que era la mejor ruta aprendida por BGP para ese destino.

![image](https://github.com/user-attachments/assets/8d293c5d-2039-4059-af92-508eeda3d19e)


5.  **Ruta de Retorno (R0_interno):** Se aseguró que R0_interno tuviera una forma de devolver el tráfico hacia AS200. Se configuró una **ruta estática predeterminada** en R0_interno apuntando a R0 (`ip route 0.0.0.0 0.0.0.0 192.168.100.1`). Esto es necesario porque R0_interno no participa en BGP y necesita una ruta genérica para alcanzar redes externas (como la de AS200).

![image](https://github.com/user-attachments/assets/773ba4ff-1560-46bc-8219-47d0707aa7f4)

**Explicación:** La redistribución permite "traducir" rutas aprendidas por un protocolo (OSPF en este caso) para que puedan ser anunciadas por otro protocolo (BGP). R0 actúa como el traductor, tomando la información de ruta interna de OSPF y compartiéndola con el mundo exterior a través de BGP. Sin redistribución, AS200 nunca se enteraría de la existencia de la red `192.168.101.0/24`. La ruta de retorno en `R0_interno` es esencial para completar la comunicación bidireccional.

---

## 9. Comprobación de Conectividad con h4 

El paso final fue verificar que los hosts en AS200 pudieran comunicarse con el nuevo host `h4` en AS100, y viceversa, ahora que las rutas fueron correctamente redistribuidas y propagadas.

*   **Prueba AS200 -> h4:** Se ejecutó un `ping` desde `h2` (en AS200, IP `192.168.2.2`) hacia `h4` (en AS100, IP `192.168.101.10`). El ping fue **exitoso**.

![image](https://github.com/user-attachments/assets/d3b600df-e0d4-43cd-97d9-e29a8401052b)

*   **Verificación de Ruta (`traceroute`):**
    *   Desde `h2`: `tracert 192.168.101.10`. La traza mostró el camino esperado: `h2 -> SW1 -> R1 -> R0 -> R0_interno -> SW_interno -> h4` (mostrando las IPs de las interfaces de los routers).
    *   Desde `h4`: `tracert 192.168.2.2`. La traza mostró el camino inverso: `h4 -> SW_interno -> R0_interno -> R0 -> R1 -> SW1 -> h2`.

![image](https://github.com/user-attachments/assets/c05f8e7a-1978-42fb-9799-7510211930a7)

Tracert desde h2 a h4

![image](https://github.com/user-attachments/assets/d24393d3-d224-4370-bf59-a9c8a60ab416)

Tracert desde h4 a h2


---
