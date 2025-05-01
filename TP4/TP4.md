# **Universidad Nacional de Córdoba**
# **Facultad de Ciencias Exactas, Físicas y Naturales**

## **Trabajo Práctico N°4:** Ruteo externo dinámico (Border Gateway Protocol (BGP)) y sistemas autónomos (Autonomous Systems (AS))

**Integrantes del Grupo:**
*   Agustin Trachta
*   Agustin Pallardo
*   Mateo Rodriguez
*   Tomas Cisneros
  
**Profesor/a:** SANTIAGO MARTIN HENN

---

# Parte I - Integración de conceptos, actividades online e investigación

## 1 - Investigar y elaborar reportes de conceptos e información sobre AS

### 1.1 - Autonomous System (AS).

Un sistema autónomo (AS) es una gran red o un grupo de redes que tiene una política de enrutamiento específica y unificada hacia el exterior. Cada dispositivo que se conecta a internet está primero conectado a un AS. Por ejemplo, una empresa que brinda servicios de internet administra miles de routers distribuídos por toda una región, y todos estos routers pueden contener muchas redes, pero comparten una política común de cómo enrutar los datos hacia internet. En conjunto forman un único AS, que desde el exterior se lo ve como una "caja negra" que contiene una política común de enrutamiento.

---

### 1.2 - Autonomous System Number (ASN) y su conformación.

Un ASN (Autonomous System Number) es un número único que identifica a cada sistema autónomo (AS) en internet. Este número permite que distintos AS se comuniquen entre sí utilizando el protocolo BGP (Border Gateway Protocol).

Los ASN pueden ser públicos, cuando son asignados por organizaciones regionales y se usan para identificar AS que se conectan a internet y participan en el enrutamiento global. O pueden ser privados si se reservan para uso interno, si es que, por ejemplo, una empresa no necesita anunciar sus rutas al exterior.

Los ASN pueden ser tanto de 16 bits como de 32 bits (este último implementado con un fin similar a cuando se implementó IPv6, ampliar la capacidad de la disponibilidad). Si son de 16 bits, llegan a un límite de 65535, y si son de 32 bits, llegan hasta 4294967295.

---

### 1.3 Ejemplos de ASN de empresas, universidades u organizaciones.

Para buscar algunos ejemplos de ASN, se ha utilizado la siguiente web: https://bgpview.io/

La misma brinda un buscador con el que se pueden buscar ASN con ciertas palabras claves, por ejemplo, colocando la palabra "Córdoba", se encuentra que el `AS27790` corresponde a la Universidad Nacional de Córdoba. Buscando la palabra "Aluar", se encuentra con un prefijo, que este luego especifica que viene de la empresa Telefónica Argentina, la cual tiene asignado el `AS10834`. Y buscando "Google", encontramos varias ASN asignadas, la de Estados Unidos corresponde con el número `AS15169`.

---

### 1.4 - ASN de mi conexión actual, con su información relevante.

Para averiguar el ASN asociado a mi conexión actual a internet, utilicé la herramienta que brinda la página de https://ipinfo.io/what-is-my-ip que muestra información sobre la IP pública, el proveedor y el ASN correspondiente. Los resultados que mostró la página fueron:

 - ASN: AS7303 - Telecom Argentina S.A. 
 - Range: 181.164.0.0/15
 - Company: Telecom Argentina S.A.

Consultando información más detallada en https://bgpview.io/asn/7303, donde se muestra el soporte de protocolos y conectividad del AS, se obtuvo que IPv4 tiene 237 prefijos anunciados, 214 peers y 3 upstreams, en tanto IPv6 tiene 102 prefijos anunciados, 48 peers y 3 upstreams. Esto quiere decir que el AS está ampliamente interconectado con múltiples peers (conexiones horizontales con otros AS) y upstreams (proveedores de tránsito), tanto en IPv4 como en IPv6.

---

## 2 - Investigar y elaborar reportes de conceptos e información sobre BGP

### 2.1 - Border Gateway Protocol (BGP).

El Border Gateway Protocol (BGP) es el **protocolo de enrutamiento** que se utiliza para **intercambiar información de rutas entre AS en internet**. Es considerado un protocolo de enrutamiento externo y es fundamental para que internet funcione como una red global.

A diferencia de otros protocolos de enrutamiento internos (como OSPF o RIP, utilizados dentro de una red o empresa), BGP permite que redes independientes compartan rutas y se comuniquen entre sí. Utiliza un modelo basado en políticas, lo que permite a los operadores de red decidir qué rutas aceptar o anunciar.

Por ejemplo, si dos empresas con distintos ASN necesitan intercambiar tráfico, a través de BGP, ambos AS comunican cuáles redes pueden alcanzar y deciden qué rutas seguir para enviar datos entre sus sistemas.

---

### 2.2 - Funcionamiento del BGP.

BGP opera estableciendo relaciones entre routers vecinos (conocidas como peers o neighbors) para intercambiar información de enrutamiento. A través de un proceso de negociación y actualización, los routers anuncian qué rutas conocen y cuáles están disponibles, permitiendo construir la tabla global de rutas de Internet.

Las etapas funcionales se pueden resumir en:

 - **Adquisición de vecino**: Dos routers BGP configuran una relación peer. Esto implica una conexión TCP entre ellos.
 - **Detección de vecino alcanzable**: Se envían periódicamente mensajes "KEEPALIVE" para verificar que el vecino sigue activo.
 - **Detección de red alcanzable**: Cada router anuncia las rutas que puede alcanzar a su vecino mediante mensajes "UPDATE".

Lo tipos de mensaje que maneja BGP se pueden resumir en:

 - **OPEN**: Inicia la conexión BGP. Se negocian parámetros como ASN, ID del router y versión.
 - **KEEPALIVE**: Mantiene la conexión viva. Se envían regularmente para confirmar disponibilidad.
 - **UPDATE**: Informa nuevas rutas alcanzables o retiros de rutas anteriores.
 - **NOTIFICATION**: Se envía cuando ocurre un error. También cierra la sesión BGP si es necesario.

Un paquete BGP contendrá un formato básico como el siguiente:
```
| Marker (16 bytes) | Length (2 bytes) | Type (1 byte) | Data (variable) |
```
Donde los parámetros son:

 - **Marker**: Valor fijo para autenticación.
 - **Length**: Tamaño total del mensaje.
 - **Type**: Indica si es OPEN, UPDATE, etc.
 - **Data**: Contenido del mensaje, depende del tipo.

Por ejemplo, un router A se quiere conectar al router B. Primero se intercambian mensajes OPEN para establecer la sesión. Luego, A envía un UPDATE informando que puede llegar a la red 192.168.10.0/24. B lo agrega a su tabla y puede reenviar esta información a otros vecinos BGP si así lo desea.

--- 

### 2.3 - Diferencias entre BGP externo (eBGP) y BGP interno (iBGP).

El BGP puede operar en dos modos principales: **eBGP** (External BGP) e **iBGP** (Internal BGP), dependiendo de si la conexión es entre sistemas autónomos distintos o dentro de un mismo sistema autónomo.

El eBGP se utiliza para el **intercambio de rutas entre diferentes sistemas autónomos**. Es el mecanismo que permite que redes independientes, como los proveedores de internet o grandes organizaciones, puedan intercambiar información de enrutamiento. Cuando un router envía rutas por eBGP, agrega su propio número de ASN al camino (AS_PATH), lo que ayuda a evitar bucles y permite tomar decisiones de enrutamiento en base a la cantidad de saltos entre AS.

En cambio, el iBGP se utiliza **dentro de un mismo sistema autónomo** para **distribuir la información de rutas** que recibió por eBGP hacia otros routers internos. A diferencia del eBGP, en iBGP no se modifica el AS_PATH, ya que todos los routers pertenecen al mismo AS. Además, los routers iBGP no necesariamente están conectados directamente, pero deben formar una red lógica de “full mesh” (o usar mecanismos como route reflectors para evitarlo) para asegurar la correcta propagación de rutas.

En este escenario, AS2 es un AS de tránsito, ya que enruta tráfico que pasa desde AS1 hacia AS3. No solo maneja sus propias rutas, sino que también permite el tráfico entre dos sistemas autónomos externos.