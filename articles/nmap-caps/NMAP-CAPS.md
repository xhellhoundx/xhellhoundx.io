---
title: "Uso de nmap con capabilities sin necesidad de usar sudo"
date:   2026-08-07
author: "Pedro Parmentier"
---

# Uso de 'nmap' con capabilities sin necesidad de usar 'sudo'
 
## Introducción: 

Tal vez muchos hemos experimentado en alguna distribución Debian-Based (o en mi caso son las que uso) que la herramienta `nmap` no ejecuta los *escaneos* debido a que no contamos con los permisos necesarios de `sudo` y nos lanza un mensaje tal como: 

  ```
  You requested a scan type which requires root privileges.
  QUITTING!
  ```

Por lo que nos vemos en la necesidad de ejecutar el comando como **super usuario** y de esta forma podrá lanzar el escaneo, esto es debido a una particulardidad de `nmap` de utilizar paquetes en crudo (raw), que a su vez viene por una característica de los lenguajes C y C++, los cuales conforman el núcleo de `nmap`.

Tras una larga investigación, pude notar que la mayoría de los tópicos que hablan sobre esto van a hacer siempre las mismas recomendaciones:
  - Asignar un alias/script que ejecute `nmap` con `sudo`
  - Asignar directorios a la **ENV VAR** `$PATH`
  - Asignar una contraseña de `sudo` sencilla y corta para que sea más eficiente
  - Explicaciones solamente de capabilities.
  - Explicaciones solamente de `nmap`.

Y una larga lista de "etc" disponible, pero realmente ¿Estas soluciones podrían llegar a ser efectivas con respecto a lo que realmente podríamos llegar a conocer la distribución que estemos usando actualmente? 

La respuesta es "Sí" todas las alternativas son completamente válidas y cada quien tiene el deber/derecho de usar su distribución como mejor le parezca y, por sobre todas las cosas, emplear sus herramientas/métodos de trabajo que le siente de la mejor forma. Sin embargo hay, todavía, una manera mucho más eficiente de poder interactuar con esta necesidad o característica, y es mediante el uso de «capabilities».

<br>

### Definición: qué es y que no es capabilities:

<br>

#### Definición:
"Con el propósito de realizar comprobaciones de permisos, las implementaciones tradicionales de Unix distinguen dos categorías de procesos: procesos privilegiados (cuyo identificador de usuario efectivo es 0, refiriéndose al superusuario o root) y procesos no privilegiados (cuyo identificador de usuario efectivo es distinto de cero). Los procesos privilegiados evitan todas las comprobaciones de permisos del núcleo, mientras que los procesos no privilegiados se ven sujetos a severas comprobaciones de permisos basadas en las credenciales del proceso (normalmente: ID de usuario efectivo, ID de grupo efectivo y lista de grupos adicionales).

Desde la versión 2.2 del núcleo, Linux ofrece un (hasta ahora incompleto) sistema de capacidades, que divide los privilegios asociados tradicionalmente al superusuario en unidades distintas que pueden ser activadas y desactivadas independientemente."

> *Véase más en*:
> - https://manpages.ubuntu.com/manpages/bionic/es/man7/capabilities.7.html (español)
> - man capabilities

<br>

#### Qué es:
  - Un mecanismo de seguridad del núcleo (kernel).
  - Comprueba permisos de los usuarios.
  - Divide privilegios del usuario root en unidades más pequeñas y específicas.
  - Sigue el concepto de "privilegio mínimo" (least privilege).

<br>

#### Qué NO es:
  - No son reemplazo de SUID/SGID.
  - No otorgan acceso total ilimitado (no dan acceso a root).
  - No son infalibles.

<br>

Entonces, habiendo dado la pequeña introducción a **capabilities** me gustaría resaltar que esto no es una guía del mecanismo sino una pequeña fracción del uso de este en conjunto con una herramienta de auditorías de seguridad.

<br>

### Definición, qué es y qué no es «nmap»: 

#### Definición:
<strong>nmap</strong> (“mapeador de redes”) es una herramienta de código abierto para exploración de red y auditoría de seguridad. Se diseñó para analizar rápidamente grandes redes, aunque funciona muy bien contra equipos individuales. `nmap` utiliza paquetes IP "crudos" («raw», N. del T.) en formas originales para determinar qué equipos se encuentran disponibles en una red, qué servicios (nombre y versión de la aplicación) ofrecen, qué sistemas operativos (y sus versiones) ejecutan, qué tipo de filtros de paquetes o cortafuegos se están utilizando así como docenas de otras características.

> *Vease más en*:
> - https://nmap.org/man/es/
> - man nmap

#### Qué es:
  - Herramienta de exploración de redes.
  - Herramienta para auditorías de seguridad.
  - Identificar activos y puertos abiertos.
  - Detectar servicios y sus versiones.
  - "Adivinar" el sistema operativo de los host.
  - Se centra en el descubrimiento de la infraestructura y evaluación de la superficie de ataque.

#### Qué NO es:
  - Escáner de vulnerabilidades.
  - No evalúa riesgos específicos ni explota vulnerabilidades (aunque su motor motor de scripting NSE puede realizar PRUEBAS básicas de vulnerabilidades o fuerza bruta).
  - Una herramienta de monitoreo en tiempo real.
  - Reemplaza la gestión de configuraciones de red.


## ¿Cómo saber si tengo capabilities?

Todas las distruciones de Linux tienen incorporado **capabilities** (capacidades) sin embargo hay que hacer una distinción en este punto: soporte a nivel del núcleo (kernel) y las herramientas de espacio de usuario (setcap, getcap).

#### Suporte a nivel del núcleo (kernel):
El sistema de capabilities (capacidades) es una característica del kernel de Linux, no de alguna distribución en particular. Fue una implentación fija desde finales de los años 90 en el kernel 2.2.

#### Herramientas de espacio de usuario (*setcap*, *getcap*):
Lo que sí podría faltar es el paquete que provee `setcap` y `getcap` como comandos. En Debian y algunas distribuciones basadas en él, el paquete es `libcap2-bin`. En otras distribuciones es posible que tengas que instalarlo explícitamente antes de usarlos, aunque el kernel por debajo ya tiene soporte para el mecanismo.

Puedes verificar si tienes estos paquetes ejecutando:
  
  ```
  which setcap getcap
  ```
Ese comando te dará las rutas dónde están los binarios para cada comando. En caso de no tenerlos instalados se deberá instalar:
  ```
  sudo apt install libcap2-bin
  ```
O de la forma antigua:
  ```
  sudo apt-get install libcap2-bin
  ```

<br>

## ¿Cómo asignar capabilities a nmap y cuáles son los riesgos?

Para asignar capabilities tenemos que definir cuáles capacidades debemos asignar a `nmap` para que pueda trabajar con paquetes crudos sin ser super usuario:
  - **cap_net_raw**: Permite al usuario no privilegiado crear raw sockets y packets (conexiones y paquetes), lo que facilita la generación y envío de paquetes de red arbitrarios, así como la capacidad de enlazar (bind) a cualquier dirección de IP para fines tales como el enrutamiento transparente o captura de tráfico.
  - **cap_net_admin**: Capacidad que otorga privilegios para realizar operaciones de administración de red sin necesitar de ejecutar un proceso como usuario root. Esta capacidad permite: configurar interfaces de red y modificar tablas de enrutamiento; administrar el firewall IP, enmascarado y contabilidad de la red; establecer opciones avanzadas de sockets, como el tipo de servicio (TOS) o la prioridad fuera del rango estándar.

Para ver estas capacidades podemos hacer el comando: 

  ```
  capsh --print
  ```

Para mayor precisión:

  ```
  capsh --print | grep -E "cap_net_raw|cap_net_admin"
  ```

Una vez sepamos que contamos con el paquete y estemos preparados para añadir las nuevas capacidades debemos hacer el siguiente comando:

  ```
  sudo setcap cap_net_raw,cap_net_admin+eip /usr/bin/nmap
  ```

o también:
  ```
  sudo setcap cap_net_raw,cap_net_admin+eip $(which `nmap`)
  ```

<br>

### ¿Qué sería "+eip"?

Estas serían las capacidades del archivo (*File Capabilities*) o capacidades de los procesos. Cada proceso tiene tres conjuntos de capacidades:
  - Efectivas (*e*): Capacidades usadas por el núcleo para llevar a cabo comprobaciones de permisos para el proceso.
  - Permitidas (*p*): Las capacidades que un proceso puede asumir. Si un proceso elimina una capacidad de su conjunto permitidas, no puede volver nunca más a adquirir esa capacidad (al menos que se ejecute como SUID-root).
  - Heredadas (*i*): Las capacidades que se conservan tras llamadas (ver execve(2)).

    Ejecutar `nmap` con privilegios:

Ahora que tenemos las capacidades configuradas, podremos ejecutar `nmap` sin los privilegios de `sudo` ya que el binario tendría los privilegios necesarios asignados con capabilities, por lo que se puede usar el flag `--privileged`, por ejemplo:
  
  ```
  nmap --privileged -sS 192.168.122.0/24
  ```

De igual forma podemos no usar el flag `--privileged` y seguir usando la herramienta sin necesidad de usar `sudo`.

<br>

## Aspectos importantes sobre la asignación de capacidades a los binarios de usuarios:

Hay que destacar algo muy importante con respecto a esto. Cuando asignamos capacidades a los binarios desde el directorio raiz, por ejemplo `/usr/bin/nmap`, hay que considerar que las capacidades quedarían establecidas para todos los usuarios pertenecientes al sistema. Es decir que persisten en el sistema de archivos (kernel) no en la sesión. Si compartes computadora con otra persona y asignas capacidades estas quedarán asignadas hasta que se remuevan de forma manual. El problema con esto es que si no se maneja con cuidado, algún usuario podría usar las capacidades para explotar vulnerabilidades o reemplazar el binario por uno malicioso, por ejemplo **cap_setuid** es particularmente peligrosa porque permite a un proceso cambiar su propio UID y podría ser abusado para escalar privilegios a root.

<br>

## ¿Cómo evitar que todos los usuarios tengan las mismas capacidades?

Para evitar entregar capacidades por igual a todos los usuarios sin considerar su **UID** o **GID** podemos usar algunas de estas soluciones:
  - Permisos tradicionales de archivo + grupo: Crear grupos específicos que recibiran permisos de ejecución para el binario.
  - Usar `pam_cap.so`: Un módulo PAM de Linux que asigna capacidades específicas de seguridad a las sesiones de los usuarios durante el proceso de autenticación. Podría resumirse a que es un módulo que actúa de la misma forma que setcap pero granulado para usuarios.

<br>

## Utilidades:

### ¿Qué me llevó al uso de este mecanismo?
Cuando estoy resolviendo máquinas/retos en plataformas como TryHackMe o HackTheBox, una de las primeras cosas que hago, luego de inspeccionar de forma pasiva todo lo que estoy a punto de vulnerar, es el uso de `nmap` para mapear los puertos abiertos y dislumbrar mis posibles entradas, obtener información sobre los servicios corriendo detrás y de ser posible, saber con qué sistema operativo estoy lidiando.

Al principio (hace unos meses atrás) usaba Kali Linux para resolver estos retos en las plataformas, sin embargo en este momento aún tenía un conocimiento mucho más básico sobre Linux en general y, como todos, corría Kali en una máquina virtual porque me gustaba la sensación de tener el poder de un sistema operativo como este. Sin embargo, pasado el tiempo ya empecé a razonar un poco más la situación y me di cuenta que Kali era un sistema operativo demasiado poderoso para el uso que un principiante le puede dar, por lo que me asinceré conmigo mismo y decidí ir por algo más básico y generoso hacia el usuario: Parrot. 

Tras la llegada del nuevo sistema operativo, configuración de entorno y nuevas experiencias, cuando resolví la primera máquina, me di cuenta que no me permitía usar `nmap` con mi usuario normal y me arrojaba el mensaje de requerimientos de root. Por lo que me fastidió un poco tener que estar todo el rato usando *sudo nmap, ingresar contraseña... sudo nmap, ingresar contraseña...*, ya que venía acostumbrado a Kali que no me solicitaba el uso de root para este análisis, al finalizar el reto en cuestión decidí investigar cómo evitar el uso de `sudo` para `nmap`. Para mi sorpresa me costó mucho encontrar una solución, como lo comenté anteriormente, los tópicos siempre son unidireccionales con respecto a esto y pocos se atreven a adentrarse en el tema. No obstante, como creía haber dejado Kali atrás (o así me lo planteé a mí mismo), había eliminado la imágen que contenía Kali, por lo que no alcancé a ver qué era lo que me permitía hacer mis tareas sin tener que teclar la contraseña por cada comando nuevo (prácticamente). Así que tras una búsqueda exhaustiva, me encontré a nuestro querido amigo "setcap" y "getcap" que son comandos para gestionar las capacidades de archivos en Linux (como ya sabemos en Linux todo es tratado como un archivo).

### ¿Por qué no necesitaba usar root en Kali?
Es importante resaltar esto ya que antes de esta experiencia, no conocía a fondo el uso de «capabilities», de hecho creo que lo usé una sola vez en un reto de TryHackMe y leí el CVE correspondiente sin dar la atención necesaria a lo que realmente representaba, y menos mal me ocurrió esto ya que de no haber sido así no tendría ni la menor idea contra qué estaba lidiando.

El motivo por el cuál ocurría esto es simple: Kali está preconfigurado para que el usuario predeterminado tenga privilegios de `sudo`. Al ser un sistema operativo especializado en pruebas de penetración (pentesting) no se complican la vida limitando las herramientas/capacidades de los usuarios, así que dan por sentado que quien esté usando este sistema operativo va por "todo o nada".
Todo esto podríamos resumirlo a varios aspectos clave: 
  * Requerimientos de privilegios: `nmap` requiere acceso al nivel de root para ejecutar escaneos SYN, Detección de SO, y escaneos UDP, por lo que necesita "crear" conexiones crudas (raw sockets) y utilizar paquetes crudos (raw packets).
  * Configuración de Kali: A diferencia de las distribuciones estandar de Linux, Kali está diseñado para "pentesting" y típicamente concede derechos administrativos al usuario predeterminado, removiendo la necesidad de ingresar como root.
  * Modo sin privilegios: Puedes ejectuar `nmap` sin `sudo`, pero la herramienta se conectará de forma predeterminada mediante el protocolo TCP (los cuales son más lentos, ruidosos y con menos precisión) y desactivará características como escaneos UDP y las huellas del SO como conexiones crudas (raw sockets) y utilizar paquetes crudos (raw packets).




