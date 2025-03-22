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

## 2) Simulador vs emulador en redes

Un simulador es una herramienta que imita el comportamiento de una red sin ejecutar realmente los protocolos o sistemas operativos subyacentes. No utiliza hardware o software real, sino que crea una representación abstracta de los dispositivos y su interacción. Un caso puede ser Cisco Packet Tracer, que permite diseñar redes virtuales y observar cómo se comportan los paquetes, pero sin ejecutar un sistema operativo real de los routers o switches.

Un emulador replica el comportamiento de un dispositivo real. Ejecuta el mismo código de firmware o sistema operativo que un dispositivo físico, lo que lo hace más preciso y realista para ciertas pruebas. Un caso puede ser GNS3, que permite emular routers Cisco reales y probar configuraciones avanzadas de red, permitiendo además ver cómo los mismos se comportan.

## 3) Ping IPv4

Para poder realizar el ping exitosamente, debemos configurar el gateway que utilizará cada host.

## 4) Ping IPv6

Lo mismo que hemos realizado para IPv4, debemos configurar el gateway pero con su correspondiente dirección IPv6.

## 5) Tráfico ICMP desde h1 a h2

Se ha generado el siguiente tráfico luego de limpiar la lista ARP y realizar un ping de h1 a h2:

En la imagen se observa primero la solicitud ARP que realiza h1 y luego el primer ping, desde que sale hasta que vuelve. Para este caso, el router 1 ya conocía la dirección de h2, pero h1 no, por lo que la solicitud de ARP llega hasta el router 1 solamente.

### a) En una red IPv4 la comunicación entre dispositivos requiere la traducción de direcciones lógicas (IP, para identificar dispositivos en una red global) a direcciones físicas (MAC, utilizada en la capa de enlace de datos para la comunicación dentro de una red local). Con ARP se obtiene una dirección IP para una dirección MAC correspondiente.

Se observa que el primer evento de ARP es la generación de la solicitud para obtener la ip de su objetivo:

### b) Si analizamos la siguiente imagen, se puede observar el paquete ICMP que ha enviado h1 al router, y se observa que la dirección de origen es 192.168.1.10 (h1) y la de destino es 192.168.2.10 (h2).

Ahora, si buscamos el camino de vuelta del ping, se observa que el origen y el destino se invierten.

### c) Cuando un host quiere comunicarse con otro que está en otra red, el tráfico debe pasar por el router, que actúa como intermediario. Lo que ocurrió en esta simulación fue que, primero h1 detecta que h2 está en otra subred y envía el paquete a su puerta de enlace predeterminada. El router recibe el paquete y revisa su tabla de enrutamiento para determinar la interfaz de salida, el switch recibe el paquete por su interfaz y lo reenvía a h2, basándose en su dirección MAC. El router, al conocer las subredes que conecta, puede hacer llegar el mensaje desde ambos hosts. Esto se puede ver utilizando “show ip route” en el router.

### d) El switch es un dispositivo de Capa de enlace de datos, que conecta múltiples dispositivos dentro de la misma red, y su función es reenviar tramas basándose en direcciones MAC, sin interpretar las direcciones IP. Como este trabaja en una red en la capa 2 del modelo OSI y se basa en las direcciones MAC, no utiliza las direcciones IP para enviar las tramas. El switch solamente aprende las direcciones MAC que se conectan.

### e) ARP de h1, almacena la dirección del router:

### f) ARP de h3, almacena la dirección del router y de h2 que está dentro de la misma red:

### g) El router muestra los dispositivos a los que ha conectado y por cuál interfaz lo ha hecho, así que tiene registro tanto de h1 por su interfaz como h2 y h3 que comparten la otra interfaz:

### h) Las direcciones broadcast son direcciones especiales que permiten enviar un mensaje a todos los dispositivos dentro de una red. ARP la utiliza para conocer los dispositivos en ella. La dirección puede ser 192.168.1.255, un mensaje enviado a esa dirección será recibido por todos los dispositivos en esa red.

### i) Las direcciones de multicast permiten enviar paquetes a un grupo específico de dispositivos, en lugar de a toda la red completa como es el caso de la dirección de broadcast. Se suelen utilizar para aplicaciones como streaming, enrutamiento dinámico y VoIP.

## 6) Tráfico ICMPv6 desde h1 a h3

Se ha realizado un ping desde h1 hasta h3 a través de IPv6:

El procedimiento fue bastante similar a cuando se hizo la prueba con IPv4.

### a) Luego del ping, ocurrieron algunas transmisiones de paquetes NDP:

El router está enviando mensajes RA (Router Advertisement) para que los hosts sepan que pueden usarlo como gateway. Estos anuncios permiten que los hosts se configuren automáticamente en IPv6 sin necesidad de DHCP.

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

