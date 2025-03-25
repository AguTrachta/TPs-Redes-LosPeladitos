# Trabajo Práctico N°1

**Redes de computadoras**  
**Facultad de Ciencias Exactas, Físicas y Naturales - UNC**  

**Grupo: Los Peladitos**  

**Integrantes**  

    Agustín Pallardó
    Agustín Trachta
    Mateo Rodríguez
    Tomás A. Cisneros


**Profesores**   

    Santiago M. Henn
    Facundo N. Oliva C.

**Marzo de 2025** 

---

### Información de contacto
 
-  _apallardo@mi.unc.edu.ar_  
-  _agutrachta@mi.unc.edu.ar_  
-  _mateo.rodriguez@mi.unc.edu.ar_  
-  _tomas.cisneros@mi.unc.edu.ar_  

---

# Resumen

Este informe documenta la configuración de una red IPv4/IPv6, el análisis de tráfico ICMP mediante simuladores y la configuración de un switch Cisco Catalyst 2950. Se comparan protocolos de resolución de direcciones, se captura tráfico con Wireshark y se realiza un análisis detallado de los intercambios ARP y NDP, así como el uso de port mirroring (SPAN) para diagnóstico de red.



# Parte 1: Configuración y Análisis de tráfico IPv4/IPv6

## 1) Marco teórico

### Interconexión de Redes

La interconexión de redes se refiere a la unión de múltiples redes de comunicación independientes para formar una red más grande. Este proceso permite que dispositivos en diferentes redes se comuniquen entre sí, superando limitaciones geográficas y tecnológicas. Para lograr una interconexión efectiva, se utilizan dispositivos como routers y gateways.

### Protocolos de Interconexión: IPv4 e IPv6

Los protocolos de Internet son fundamentales para el direccionamiento y la transmisión de datos en redes interconectadas.

- **IPv4 (Internet Protocol version 4)**: Es la más usada, utiliza direcciones de 32 bits, lo que permite aproximadamente 4.3 mil millones de direcciones únicas, pero tiene un problema. El crecimiento exponencial de dispositivos conectados ha llevado al agotamiento de direcciones IPv4 disponibles, por lo que surge IPv6.
  
- **IPv6 (Internet Protocol version 6)**: Fue desarrollado para superar las limitaciones de IPv4. Utiliza direcciones de 128 bits, ofreciendo un espacio de direcciones prácticamente ilimitado. Además del aumento en el espacio de direcciones, IPv6 introduce mejoras en la eficiencia del enrutamiento, la configuración automática y la seguridad.

### Protocolos de Resolución de Direcciones: ARP y NDP

Para que los dispositivos en una red se comuniquen, es necesario traducir las direcciones lógicas (IP) a direcciones físicas (MAC). Este proceso es manejado por diferentes protocolos en IPv4 e IPv6:

- **ARP (Address Resolution Protocol)**: Utilizado en redes IPv4, permite a un dispositivo descubrir la dirección MAC correspondiente a una dirección IP determinada. Funciona enviando una solicitud ARP a la red, preguntando "¿Quién tiene esta dirección IP?", y el dispositivo con esa IP responde con su dirección MAC.

- **NDP (Neighbor Discovery Protocol)**: En IPv6, ARP es reemplazado por NDP, que además de resolver direcciones, maneja la detección de vecinos, la detección de routers y la autoconfiguración de direcciones. Este utiliza ICMPv6 para transmitir mensajes como Solicitud de Vecino y Anuncio de Vecino, que funcionan de manera similar a las solicitudes y respuestas ARP, pero con mejoras de seguridad.

### Protocolo ICMP

El Protocolo de Mensajes de Control de Internet (ICMP) es utilizado para el diagnóstico y la gestión de redes:

- **ICMP en IPv4**: Proporciona mensajes de error y control, como "Destino inalcanzable" o "Tiempo excedido", por ejemplo cuando se realiza un ping a una dirección, verifica la conectividad entre dispositivos.

- **ICMPv6 en IPv6**: Además de las funcionalidades que trae ICMPv4, este incorpora características adicionales, como las utilizadas por NDP para la autoconfiguración y la gestión de vecinos.

### DHCP: Protocolo de Configuración Dinámica de Host

DHCP es un protocolo que permite la asignación automática de direcciones IP y otros parámetros de configuración a dispositivos en una red:

- **DHCP en IPv4**: Permite a los dispositivos obtener una dirección IP, máscara de subred, puerta de enlace y servidores DNS de forma automática, simplificando la gestión de redes grandes.

- **DHCPv6 en IPv6**: Ofrece una configuración más controlada y detallada, permitiendo la asignación de información adicional como servidores DNS y dominios de búsqueda. Además, IPv6 soporta la autoconfiguración sin estado (SLAAC), donde los dispositivos pueden autoconfigurarse sin necesidad de un servidor.

![image](https://github.com/user-attachments/assets/8d2920d1-af5a-40dc-9976-bcbfc78daff6)

## 2) Simulador vs emulador en redes

Un simulador es una herramienta que imita el comportamiento de una red sin ejecutar realmente los protocolos o sistemas operativos subyacentes. No utiliza hardware o software real, sino que crea una representación abstracta de los dispositivos y su interacción. Un caso puede ser Cisco Packet Tracer, que permite diseñar redes virtuales y observar cómo se comportan los paquetes, pero sin ejecutar un sistema operativo real de los routers o switches.

Un emulador replica el comportamiento de un dispositivo real. Ejecuta el mismo código de firmware o sistema operativo que un dispositivo físico, lo que lo hace más preciso y realista para ciertas pruebas. Un caso puede ser GNS3, que permite emular routers Cisco reales y probar configuraciones avanzadas de red, permitiendo además ver cómo los mismos se comportan.

## 3) Ping IPv4

Para poder realizar el ping exitosamente, debemos configurar el gateway que utilizará cada host.

![image](https://github.com/user-attachments/assets/9d02c378-63d1-46db-89b0-14aa4e8bee06)

![image](https://github.com/user-attachments/assets/76613cc7-992e-422e-9eb6-376c493ea51e)

![image](https://github.com/user-attachments/assets/e807fd68-b6ee-44d2-87e3-c99bbebe4701)

## 4) Ping IPv6

Lo mismo que hemos realizado para IPv4, debemos configurar el gateway pero con su correspondiente dirección IPv6.

![image](https://github.com/user-attachments/assets/3e3ade9a-4420-4d87-b6a7-78340d19773a)

![image](https://github.com/user-attachments/assets/4417d815-964b-4e1f-9139-069f2c4b155f)

![image](https://github.com/user-attachments/assets/450885dc-8949-4df0-bfbf-fb9438053ae0)

## 5) Tráfico ICMP desde h1 a h2

Se ha generado el siguiente tráfico luego de limpiar la lista ARP y realizar un ping de h1 a h2:

![image](https://github.com/user-attachments/assets/bf359eac-8ae0-4cb8-86d7-c99d206c94fa)

En la imagen se observa primero la solicitud ARP que realiza h1 y luego el primer ping, desde que sale hasta que vuelve. Para este caso, el router 1 ya conocía la dirección de h2, pero h1 no, por lo que la solicitud de ARP llega hasta el router 1 solamente.

### a) En una red IPv4 la comunicación entre dispositivos requiere la traducción de direcciones lógicas (IP, para identificar dispositivos en una red global) a direcciones físicas (MAC, utilizada en la capa de enlace de datos para la comunicación dentro de una red local). Con ARP se obtiene una dirección IP para una dirección MAC correspondiente.

Se observa que el primer evento de ARP es la generación de la solicitud para obtener la ip de su objetivo:

![image](https://github.com/user-attachments/assets/fc1b462b-b360-48cb-b2dc-7425b0600dee)

El siguiente evento, el router obtiene la solicitud ARP y la procesa:

![image](https://github.com/user-attachments/assets/a938ace8-79fb-44b3-b451-bfaadcdc975a)

Y el último evento es la recepción del host con la ip que solicitaba para luego poder hacer el ping:

![image](https://github.com/user-attachments/assets/6b24a456-2fb7-4d41-a0ff-052efac56ec5)

### b) Si analizamos la siguiente imagen, se puede observar el paquete ICMP que ha enviado h1 al router, y se observa que la dirección de origen es 192.168.1.10 (h1) y la de destino es 192.168.2.10 (h2).

![image](https://github.com/user-attachments/assets/f3c2f6ea-a5b5-457a-b6c3-4de3a860e89a)

Ahora, si buscamos el camino de vuelta del ping, se observa que el origen y el destino se invierten.

![image](https://github.com/user-attachments/assets/384fc103-70ba-4e87-bdc0-48e5c7495a9d)

### c) Cuando un host quiere comunicarse con otro que está en otra red, el tráfico debe pasar por el router, que actúa como intermediario. Lo que ocurrió en esta simulación fue que, primero h1 detecta que h2 está en otra subred y envía el paquete a su puerta de enlace predeterminada. El router recibe el paquete y revisa su tabla de enrutamiento para determinar la interfaz de salida, el switch recibe el paquete por su interfaz y lo reenvía a h2, basándose en su dirección MAC. El router, al conocer las subredes que conecta, puede hacer llegar el mensaje desde ambos hosts. Esto se puede ver utilizando “show ip route” en el router.

### d) El switch es un dispositivo de Capa de enlace de datos, que conecta múltiples dispositivos dentro de la misma red, y su función es reenviar tramas basándose en direcciones MAC, sin interpretar las direcciones IP. Como este trabaja en una red en la capa 2 del modelo OSI y se basa en las direcciones MAC, no utiliza las direcciones IP para enviar las tramas. El switch solamente aprende las direcciones MAC que se conectan.

### e) ARP de h1, almacena la dirección del router:

![image](https://github.com/user-attachments/assets/45c7fbde-4735-41f7-8531-c348ffaf0b62)

### f) ARP de h3, almacena la dirección del router y de h2 que está dentro de la misma red:

![image](https://github.com/user-attachments/assets/8a24ece8-5189-44c1-815a-ee3c668acd4a)

### g) El router muestra los dispositivos a los que ha conectado y por cuál interfaz lo ha hecho, así que tiene registro tanto de h1 por su interfaz como h2 y h3 que comparten la otra interfaz:

![image](https://github.com/user-attachments/assets/feccfaf1-9410-4c4c-b9a3-87e9626487a7)

### h) Las direcciones broadcast son direcciones especiales que permiten enviar un mensaje a todos los dispositivos dentro de una red. ARP la utiliza para conocer los dispositivos en ella. La dirección puede ser 192.168.1.255, un mensaje enviado a esa dirección será recibido por todos los dispositivos en esa red.

### i) Las direcciones de multicast permiten enviar paquetes a un grupo específico de dispositivos, en lugar de a toda la red completa como es el caso de la dirección de broadcast. Se suelen utilizar para aplicaciones como streaming, enrutamiento dinámico y VoIP.

## 6) Tráfico ICMPv6 desde h1 a h3

Se ha realizado un ping desde h1 hasta h3 a través de IPv6:

![image](https://github.com/user-attachments/assets/abec27b2-7b3b-4ca1-9be2-cf352d0f7596)

El procedimiento fue bastante similar a cuando se hizo la prueba con IPv4.

### a) Luego del ping, ocurrieron algunas transmisiones de paquetes NDP:

![image](https://github.com/user-attachments/assets/9ecc0671-d7a8-49a0-9aad-05341456e3f9)

El router está enviando mensajes RA (Router Advertisement) para que los hosts sepan que pueden usarlo como gateway. Estos anuncios permiten que los hosts se configuren automáticamente en IPv6 sin necesidad de DHCP.

![image](https://github.com/user-attachments/assets/90d78b4d-ba82-437c-b3af-2893bdf1f448)

En esta imágen se puede ver cuando se genera la solicitud de NDP en el router 1, y será transmitida al host 1

![image](https://github.com/user-attachments/assets/c24dc1f3-b0a7-4475-8c27-a68975cbace0)

En esta otra imagen, podemos ver como recibe el host 2 una solicitud NDP con su dirección asociada.

### b) En concreto, NDP reemplaza ARP, es más eficiente, utiliza multicast en lugar de broadcast como hace ARP, además de permitir la autoconfiguración, haciendo anuncios de router cada cierto tiempo a los dispositivos conectados.

### c) NDP (Neighbor Discovery Protocol) tiene 5 funciones principales en IPv6:
- **Descubrimiento de vecinos**: Encuentra direcciones MAC asociadas a direcciones IPv6.
- **Descubrimiento de routers**: Los hosts pueden encontrar routers disponibles en la red.
- **Detección de direcciones duplicadas (DAD)**: Antes de asignar una IP, verifica que no esté en uso.
- **Redirección de tráfico**: Un router puede indicar un camino mejor para llegar a un destino.
- **Mantener la conectividad**: Permite detectar si un vecino aún está activo.

### d) En IPv6 se elimina el uso de broadcast y lo reemplaza por multicast directamente. Se utilizan direcciones como FF02::1 para todos los dispositivos en la red, FF02::2 para todos los routers en la red y FF02::1:FFXX:XXXX (direcciones específicas) para el descubrimiento de vecinos. Esto logra que IPv6 sea más eficiente y reduzca tráfico innecesario que podría provocar el uso de broadcast.

### e) En IPv6 existen diferentes tipos de direcciones con propósitos específicos:
- **Link-Local**: Direcciones IPv6 presentes en una interfaz de red, utilizadas para la comunicación dentro de la misma red sin necesidad de un router.
- **Unique-Local**: Equivalentes a las direcciones privadas de IPv4, usadas en redes internas, no enrutables en Internet.
- **Global Unicast**: Las únicas direcciones IPv6 que pueden usarse en Internet, equivalentes a las direcciones públicas en IPv4.

# Parte 2: Manejo de Equipamiento Físico y Configuración del Switch Cisco Catalyst 2950

## 1. Introducción

Este apartado documenta el proceso realizado para la configuración, administración y monitoreo de un switch Cisco Catalyst 2950, abordando desde la conexión inicial hasta el análisis de tráfico de red. Se empleó una conexión serial a través del software Minicom en un sistema operativo Linux Mint, permitiendo establecer comunicación con el switch para su configuración y recuperación de credenciales.

Asimismo, se realizaron pruebas de conectividad y análisis de tráfico de red mediante Wireshark, observando el comportamiento de los protocolos ARP, ICMP y la asignación de direcciones mediante DHCP. También se configuró un puerto en modo mirroring (SPAN) para capturar y monitorear el tráfico entre dos dispositivos conectados al switch.

## 2. Objetivos

Los objetivos principales de este trabajo fueron:

- Familiarizarse con el equipamiento de red y comprender su anatomía, paneles e interfaces.
- Poner en funcionamiento un switch empresarial desde cero y acceder a su configuración.
- Recuperar credenciales de acceso mediante conexión por consola.
- Realizar pruebas de conectividad y análisis de tráfico en la red.
- Configurar el switch para realizar monitoreo de tráfico mediante port mirroring (SPAN).
- Observar el comportamiento de los protocolos ARP, ICMP y DHCP en un entorno controlado.

## 3. Materiales Utilizados

Para la realización de este trabajo práctico se emplearon los siguientes elementos:

- Switch Cisco Catalyst 2950
- Tres computadoras (PC1, PC2 y PC3)
- Cable consola RJ45 a Serial
- Adaptador USB-Serial
- Software Minicom (alternativa a PuTTY en Linux Mint)
- Software Wireshark para captura y análisis de tráfico de red

## 4. Características del Switch Cisco Catalyst 2950

El Cisco Catalyst 2950 es un switch de capa 2 diseñado para redes empresariales pequeñas y medianas. Según el datasheet oficial, sus principales características son:

- 24 puertos Fast Ethernet (10/100 Mbps)
- Conexión y administración mediante consola (RJ45), Telnet y SSH
- Soporte para VLANs
- Funcionalidad de Port Mirroring (SPAN) para monitoreo de tráfico
- No dispone de puertos Gigabit
- Enfocado en redes de tamaño mediano o pequeño

## 5. Procedimientos y Checklists

### a) Conexión del switch mediante Minicom

Para conectar una PC al switch a través del puerto consola, se siguieron los siguientes pasos:

1. **Conectar el cable**  
   - Conectar el cable RJ45-Serial desde el puerto consola del switch al adaptador USB-Serial en la PC.

2. **Identificar el puerto serie en Linux**  
   - Ejecutar el siguiente comando en la terminal para verificar el puerto asignado:
     ```bash
     dmesg | grep tty
     ```
   - El puerto asignado será `/dev/ttyUSB0`.

3. **Instalar y configurar Minicom**  
   - Ajustar los parámetros de comunicación:
     - **Serial Device**: `/dev/ttyUSB0`
     - **Velocidad de transmisión**: 9600 bps
     - **Data bits**: 8
     - **Paridad**: none
     - **Flow Control**: no
   - Guardar la configuración y conectarse.

![image](https://github.com/user-attachments/assets/c55c0579-6276-4836-9893-e119ae1e6e77)

### b) Recuperación y modificación de contraseñas del switch

Una vez dentro de la interfaz de administración del switch, se procedió a modificar las claves de acceso:

1. **Ingresar al modo privilegiado**:
   ```bash
   Switch> enable
   ```
2. **Acceder al modo configuración global**:
   ```bash
   Switch# configure terminal
   ```
3. **Modificar la contraseña al modo privilegiado**:
   ```bash
   Switch(config)# enable secret cisco
   ```
4. **Guardar los cambios de configuración**:
   ```bash
   Switch# copy running-config startup-config
   ```

### c) Configuración de red y prueba de conectividad

1. **Conectar físicamente las PCs a los puertos del switch**:
   - PC1 en Fa0/1
   - PC2 en Fa0/2

2. **Para administrar el switch remotamente mediante Telnet o SSH, se configuró la IP de la VLAN 1 con la dirección 192.168.1.2**:
   - Acceder al modo de configuración global
   - Configurar la dirección IP en la VLAN 1
   - Guardar la configuración

![image](https://github.com/user-attachments/assets/5e7bb1d7-9aec-48c8-97fe-d458e03f275b)

3. **Asignar direcciones IP estáticas en cada computadora**:
   - PC1: `192.168.1.10/24`
   - PC2: `192.168.1.20/24`

4. **Probar conectividad con ping**:
   ```bash
   ping 192.168.1.20
   ```
![image](https://github.com/user-attachments/assets/ea3eb511-ff9c-4ddc-98b1-05a9710e207e)

### d) Configuración de Port Mirroring (SPAN) y análisis de tráfico

Para monitorear el tráfico entre PC1 y PC2 desde PC3, se configuró el puerto Fa0/3 como puerto espejo (SPAN).

1. **Eliminar configuración SPAN previa (si existiera)**:
   ```bash
   Switch(config)# no monitor session 1
   ```
2. **Configurar el puerto en modo mirroring**:
   ```bash
   Switch(config)# monitor session 1 source interface Fa0/1
   Switch(config)# monitor session 1 source interface Fa0/2
   Switch(config)# monitor session 1 destination interface Fa0/3
   ```
3. **Verificar la configuración**:
   ```bash
   Switch# show monitor session 1
   ```
![image](https://github.com/user-attachments/assets/048e0eeb-c0c8-4e9b-bb92-6c28fd01cfc4)
![image](https://github.com/user-attachments/assets/27bcd041-86ac-4a10-9f22-0167c63c9b52)

4. **Capturar tráfico con Wireshark**:
   - En PC3 (conectada en Fa0/3), abrimos Wireshark y capturamos paquetes.

![file_2025-03-20_19 00 29](https://github.com/user-attachments/assets/3d0efbf4-d7b2-4537-aa0a-a5d1e3e6eed8)

## Análisis del Tráfico ICMP Capturado

### Análisis General de la Captura

1. **Tráfico ICMP (Ping)**: En la captura se observa que el tráfico capturado está relacionado con un proceso de ping (ICMP Echo Request y Echo Reply). Se está haciendo un "ping" entre dos dispositivos con las direcciones IP `192.168.1.10` (Cliente 1) y `192.168.1.15` (Cliente 2).

2. **ARP**: En las primeras líneas se observa un tráfico ARP, que es usado para resolver direcciones IP en direcciones MAC dentro de una red local. Aquí, los dispositivos están preguntando "¿Quién tiene esta dirección IP?", y respondiendo con sus respectivas direcciones MAC para que el tráfico pueda ser enviado correctamente a través de la red.

### Análisis Detallado de la Comunicación ARP:

- **Comunicaciones ARP observadas**:
  - Las solicitudes ARP son emitidas por los dispositivos para determinar la dirección MAC correspondiente a una dirección IP específica en la red local. En el tráfico ARP capturado, se ve que los dispositivos están realizando esta consulta.

  **Ejemplo**:  
  **Solicitud ARP de 192.168.1.10** (Cliente 1) buscando la dirección MAC de `192.168.1.15`. Este paquete se transmite en el broadcast de la red, ya que el origen no conoce la MAC del destino.
  
  Una vez que el dispositivo que tiene la IP correspondiente (`192.168.1.15`) responde, esta información se almacena en la tabla ARP del dispositivo solicitante, lo que permite futuras comunicaciones sin la necesidad de nuevas solicitudes ARP.

### Datagramas ICMP:

- **Ping Echo Request**:
  - Cliente 1 envía un paquete ICMP de tipo "Echo Request" a `192.168.1.15` (Cliente 2). Este mensaje es enviado con una secuencia que permite al receptor responder.
  
- **Ping Echo Reply**:
  - Cliente 2 responde con un "Echo Reply", que es la respuesta al paquete de "Echo Request". Este paquete lleva la dirección IP de origen como `192.168.1.15` y el destino como `192.168.1.10`.

### Direcciones IP en los Datagramas:

- **Direcciones IP**:
  - **Origen**: `192.168.1.10` (Cliente 1)
  - **Destino**: `192.168.1.15` (Cliente 2)
  
  Estas direcciones son las que se observan en los paquetes ICMP de tipo Echo Request y Echo Reply. Los paquetes ICMP contienen estas direcciones dentro del encabezado para garantizar que el tráfico llegue al destino correcto.

### Comportamiento del Enrutador:

- **El enrutador no es necesario en este escenario**: Ya que ambos dispositivos (Cliente 1 y Cliente 2) están dentro de la misma red (subred `192.168.1.0/24`), el tráfico no pasa por un enrutador. El intercambio de paquetes ICMP se maneja directamente entre los dispositivos a través de la red local.

### Función del Switch:

- **Switch**:
  - El switch se encarga de reenviar tramas basadas en direcciones MAC. El switch no necesita conocer las direcciones IP, ya que está operando en la capa de enlace de datos (Capa 2 del modelo OSI). Su función es simplemente asegurar que las tramas lleguen al puerto adecuado según la dirección MAC de destino.
  
  - Los switches no tienen direcciones IP asignadas en sus interfaces porque no realizan funciones de enrutamiento, solo manejan tráfico dentro de la misma red local.

## 6. Análisis y Resultados

### Prueba de conectividad

- El ping entre PC1 y PC2 fue exitoso. Las pruebas de conectividad realizadas entre PC1 y PC2 confirmaron el correcto establecimiento de la comunicación en la red. El envío y recepción exitosos de paquetes ICMP (Echo Request y Echo Reply) validaron la operatividad de los dispositivos y su configuración de red.

### Análisis de tráfico con Wireshark

- Se observaron correctamente paquetes ARP: Esto evidencia que la resolución de direcciones IP a direcciones MAC se llevó a cabo correctamente, permitiendo la comunicación entre los dispositivos.
- Se identificaron paquetes ICMP, usados en el ping, con respuestas tipo Echo Request y Echo Reply.
- Se verificó la funcionalidad del port mirroring (SPAN), capturando todo el tráfico entre PC1 y PC2 desde PC3, indica que la configuración de monitoreo fue adecuada, permitiendo la observación del tráfico sin afectar el rendimiento de la red.

![image](https://github.com/user-attachments/assets/6c7c5885-0f00-4069-91ce-19cfa608f8a0)

Escucha de PC2 sobre mensaje desde PC1	

En conclusión, la infraestructura de red se encuentra correctamente configurada, garantizando la comunicación entre los dispositivos y permitiendo su análisis en tiempo real. Estos resultados sugieren que la red es funcional y estable, proporcionando una base confiable para futuras pruebas o mejoras en la configuración.
