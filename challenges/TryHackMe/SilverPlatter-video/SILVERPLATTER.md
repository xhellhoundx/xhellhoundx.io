<div align="center">
  <img src="./assets/silverplatter-icon.png" width="400" height="400">
</div>

<div align="center">

# Silver Platter <!-- omit in toc -->
<!-- Fácil-#228B06 | Media-#BFA907 | Difícil-#A62100 -->
![TryHackMe](https://img.shields.io/badge/Plataforma-TryHackMe-A20606)
![Fácil](https://img.shields.io/badge/Dificultad-Fácil-228B06)

</div>

<br>

<div align="center">

  ## Video de resolución <!-- omit in toc -->

  <a href="https://youtu.be/i4IyfPT6HaI">
    <img src="./assets/silverplatter-video-icon.png" width=500>
    <br>
    Ver video en Youtube
  </a>
</div>

<br><br>

<div align="center">
  <a href="./assets/basicpentesting-cti.pdf">📄 Informe Oficial (PDF)</a>
</div>

<br><br>

# Informe de Inteligencia de Amenazas - Máquina "Silverplatter" <!-- omit in toc -->

<br>

## Índice <!-- omit in toc -->
- [RESUMEN EJECUTIVO (Executive Summary)](#resumen-ejecutivo-executive-summary)
- [ENTORNO OBJETIVO](#entorno-objetivo)
- [FASE DE RECONOCIMIENTO Y RECOLECCIÓN (Recon­naissance \& Enumeration)](#fase-de-reconocimiento-y-recolección-reconnaissance--enumeration)
  - [Escaneo de Red y Servicios Expuestos](#escaneo-de-red-y-servicios-expuestos)
- [Hallazgos de Enumeración Web, Parámeter Tampering, IDOR](#hallazgos-de-enumeración-web-parámeter-tampering-idor)
- [CADENA DE ATAQUE (Kill Chain \& Technical Analysis)](#cadena-de-ataque-kill-chain--technical-analysis)
  - [Acceso Inicial (Initial Access)](#acceso-inicial-initial-access)
  - [Puntuación y Métrica CVSS v3.1](#puntuación-y-métrica-cvss-v31)
  - [Acceso Inicial y Movimiento Lateral](#acceso-inicial-y-movimiento-lateral)
- [ESCALADA DE PRIVILEGIOS (Privilege Escalation)](#escalada-de-privilegios-privilege-escalation)
- [INDICADORES DE COMPROMISO (IoCs)](#indicadores-de-compromiso-iocs)
  - [Indicadores de Red (Network IoCs)](#indicadores-de-red-network-iocs)
  - [Indicadores en Host (Host-Based IoCs)](#indicadores-en-host-host-based-iocs)
- [MAPEO DE TÁCTICAS Y TÉCNICAS (MITRE ATT\&CK)](#mapeo-de-tácticas-y-técnicas-mitre-attck)
- [RECOMENDACIONES Y MITIGACIONES (Actionable Intel­ligence)](#recomendaciones-y-mitigaciones-actionable-intelligence)
  - [Mitigaciones Inmediatas (Tácticas)](#mitigaciones-inmediatas-tácticas)
  - [Mitigaciones a Largo Plazo (Estratégicas)](#mitigaciones-a-largo-plazo-estratégicas)


<br>

### RESUMEN EJECUTIVO (Executive Summary)
* **Propósito**: Proporcionar una visión técnica y operativa sobre la instrusión realizada contra el objetivo en el entorno controlado, detallando las vulnerabilidades explotadas, la escalada de privilegios y las medidas para mitigar los riesgos.
* **Impacto Principal**: Exposición total de la infraestructura crítica mediante la combinación de vulnerabilidades conocidas en servicios web expuestos y desconfiguraciones a nivel de sistema operativo.
* **Vector de Entrada**: Manipulación de Parámetros (_Parameter Tampering_) a través de la eliminación del parámetro `Password` en la ruta `http://silverplatter:8080/silverpeas/AuthenticationServlet` en el formulario de ingreso de usuarios.
* **Escalada de Privilegios**: Obtención de acceso como `root` mediante el reuso de creden­ciales expuestas en el sistema y permisos de sudo sin restricciones (`ALL`).
* **Resumen**: Se explotó una vulnerabilidad de _Parameter Tampering_ en el servicio web para acceder al usuario `scr1ptkiddy` y posteriormente explotar un _IDOR_ conocido en el sistema de mensajería interna y extraer credenciales `SSH` del usuario `tim`. Una vez en el sistema, la inspección de `/var/log/auth.log.1` reveló la contraseña del usuario `tyler`, permitiendo un movimiento lateral. Finalmente, se escalaron privilegios a `root` aprovechando que tyler contaba con permisos totales sin restricciones en el archivo `sudoers` (`(ALL : ALL) ALL`).

--- 

### ENTORNO OBJETIVO
* **Nombre de la Amenaza / Host**: TryHackMe - Silver Platter
* **Dirección IP / Alcance**: `10.114.162.145`
* **Sistema Operativo**: Linux Ubuntu 22.04.3 LTS (Jammy Jellyfish)
* **Objetivo Comercial/Función**: Servidor web de producción simulado

---

### FASE DE RECONOCIMIENTO Y RECOLECCIÓN (Recon­naissance & Enumeration)

####  Escaneo de Red y Servicios Expuestos
Se ejecutó un escaneo completo de puertos mediante `Nmap` para determinar los servicios expuestos en la red:

```bash
nmap -p- --open -T4 -Pn -n -vvv -oN target.log 10.114.162.145
```
```bash
nmap -p22,80,3306,5038 -sV -sC -vvv -oN openPorts.log 10.114.162.145
```

| Puerto | Servicio | Versión | Estado |
|---|---|---|---|
| 22/TCP | ssh | OpenSSH 9.2p1 Debian 2+deb12u6 | Abierto |
| 80/TCP | http | Apache httpd 2.4.62 ((Debian)) | Abierto |
| 8080/TCP | http-proxy | Desconocido | Abierto |

---

### Hallazgos de Enumeración Web, Parámeter Tampering, IDOR
* **Parameter Tampering documentado**: Tras conocer, mediante información plasmada en el servicio web del puerto 80, la existencia del portal de colaboración **Silverpeas v6.3.1** corriendo por el puerto `8080`, se encontraron vulnerabilidades conocidas (**CVE-2024-36042**) con respecto a este software para hacer _bypass_ de usuarios mediante la eliminación del parámetro (query) `Password` en el formulario de acceso en la ruta logrando acceder con el usuario `scr1ptkiddy`:

    - `http://10.114.162.145:8080/silverpeas/defaultLogin.jsp` → (HTTP 200) - Parameter Tampering en el formulario.

* **IDOR (en: Insecure Direct Object Reference; es: Referencia Directa a Objetos Insegura) documentado**: Una vez se logró acceder con las credenciales del usuario scr1ptkiddy, se realizó una búsqueda exhaustiva sobre vulnerabilidades conocidas para el softare Silverpeas estando autenticado y se encontró el CVE-2023-47323 el cual menciona una vulnerabilidad IDOR en la característica de mensajería/notificaciones que no aplica control de acceso al parámetro ?ID=X (siendo X un número entero), permitiendo el acceso/lectura arbitrario(a) de los mensajes del usuario:

    - `http://10.114.162.145:8080/silverpeas/RSILVERMAIL/jsp/ReadMessage.jsp?ID=6` → (HTTP 200) IDOR en el servicio de mensajes/notificaciones.

---

### CADENA DE ATAQUE (Kill Chain & Technical Analysis)

#### Acceso Inicial (Initial Access)

**Parameter Tampering**
* **Táctica MITRE ATT&CK**: Parameter Tampering: Initial Access / Exploit Public-Facing Application (T1190)
* **Vulnerabilidad Explotada**:

    - **CVE-2024-36042**: Parameter Tampering
    - **CWE-288**: Authentication Bypass Using an Alternate Path or Channel

* **Prueba de Concepto (PoC)**:

  - Solicitud normal:

```
POST /silverpeas/AuthenticationServlet HTTP/1.1
Host: 10.114.162.145:8080
# Otras cabeceras
Origin: https://10.114.162.145:8080
Content-Type: application/x-www-form-urlencoded

Login=scr1ptkiddy&Password=SilverAdmin&DomainId=0
```

  - Solicitud bajo Parameter Tampering:

```
POST /silverpeas/AuthenticationServlet HTTP/1.1
Host: 10.114.162.145:8080
# Otras cabeceras
Origin: https://10.114.162.145:8080
Content-Type: application/x-www-form-urlencoded

Login=scr1ptkiddy&DomainId=0
```

**IDOR**
* **Táctica MITRE ATT&CK**: Credential Access / Unsecured Credentials: Chat Messages (T1552.008)
* **Vulnerabilidad Explotada**:

    - **CVE-2023-47323**: IDOR (Insecure Direct Object Reference)

* **Prueba de Concepto (PoC)**:

    - Valor inicial encontrado (1)
    ```
    http://10.114.162.145:8080/silverpeas/RSILVERMAIL/jsp/ReadMessage.jsp?ID=1
    ```

    - Mensaje con información delicada - Credenciales del servicio SSH (6)

    ```
    http://10.114.162.145:8080/silverpeas/RSILVERMAIL/jsp/ReadMessage.jsp?ID=6
    ```


#### Puntuación y Métrica CVSS v3.1
* Puntuación Base: 6.5 (Medio)
* Vector CVSS: `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:N`

#### Acceso Inicial y Movimiento Lateral

**Acceso Inicial**
* **Descripción**: Mediante las credenciales SSH (`tim: cm0nt!md0ntf0rg3tth!spa$$w0rdagainlol`) obtenidas a través del hallazgo IDOR en el servicio web, se procedió al acceso inicial directo en el sistema operativo a través del servicio `SSH` (puerto `22`).
* **Payload Utilizado**:

```bash
ssh tim@10.114.162.145
```

* **Nota de Persistencia**: Durante esta fase no se requirió la implementación de mecanis­mos/exploits de persistencia adicionales (como creación de puertas traseras - backdoors, o modificación de `authorized_keys`) ya que las credenciales obtenidas garantizaron acceso directo al entorno del usuario `tim`.

**Movimiento Lateral**
* **Descripción**: Durante la fase de enumeración local, tras obtener acceso con el usuario `tim`, se hizo una primera enumeración que consistió en enumerar los usuarios mediante la lectura del archivo `/etc/passwd`, dislumbrando un segundo usuario llamado `tyler`, posteriormente se enumeraron los archivos relacionados al grupo `adm` (grupo encontrado y al que pertenecía el usuario `tim`) y se encontraron registros de autenticación en la ruta `/var/log` la cual contenía el archivo `auth.log.2`. La lectura de este archivo reveló la presencia de credenciales en texto claro pertenecientes al usuario `tyler`, expuestas mediante la ejecución del comando `docker` para montar la imagen correspondiente del portal **Silverpeas**.
* **Payload Utilizado**:

  - Enumeración de usuarios del sistema

    ```bash
    cat /etc/passwd | grep -i bash
    ```

  - Enumeración de archivos para grupo **adm**

    ```bash
    find / -group "adm" -type f 2>/dev/null
    ```

  - Lectura de credenciales

    ```bash
    cat /var/log/auth.log* | grep -iE "tyler|root"
    ```

* **Táctica MITRE ATT&CK**: Credential Access / Unsecured Credentials: Credentials In Files (T1552.001)

---

### ESCALADA DE PRIVILEGIOS (Privilege Escalation)

* **Táctica MITRE ATT&CK**: Privilege Escalation / Abuse Elevation Control Mechanism: Sudo and Sudo Caching (T1548.003)

* **Vector de Escalada**: Excesos de privilegios asignados al usuario tyler en el archivo de configuración `sudoers`. El usuario contaba con la directiva `(ALL: ALL) ALL` permitiendo la ejecución de cualquier comando con privilegios de super usuario (`root`) sin restricciones ni requerimientos.

* **Comando de Detección**:

```bash
sudo -l
```

---

### INDICADORES DE COMPROMISO (IoCs)

#### Indicadores de Red (Network IoCs)
* **IPs Maliciosas Relacionadas**: `192.168.128.68` (IP de la máquina atacante en la VPN)
* **URLs Afectadas**:

    - `http://10.114.162.145:8080/silverpeas/defaultLogin.jsp`
    - `http://10.114.162.145:8080/silverpeas/RSILVERMAIL/jsp/ReadMessage.jsp?ID=6` (Aut­enticado como usuario scr1ptkiddy)

* **Payload Inusual**: Login=scr1ptkiddy&DomainId=0

#### Indicadores en Host (Host-Based IoCs)

* **Rutas de Archivos Sensibles/Accesibles**:
  - `/var/log/auth.log.2`

* **Nuevos Procesos Anómalos**: Spawn de procesos shell (`/bin/bash`) con privilegios UID 0 (`root`) generados mediante la invocación de sudo desde la terminal interactiva del usuario `tyler`.

---

### MAPEO DE TÁCTICAS Y TÉCNICAS (MITRE ATT&CK)

| Fase de la Cadena | ID Técnica | Nombre de la Técnica |
|---|---|---|
| Reconnaissance | T1595.002 | Active Scanning: Vulnerability Scanning |
| Reconnaissance | T1592.002 | Gather Victim Host Information: Software |
| Initial Access | T1190 | Exploit Public-Facing Application |
| Credential Access | T1552.008 | Unsecured Credentials: Chat Messages |
| Credential Access | T1552.001 | Unsecured Credentials: Credentials In Files |
| Privilege Escalation | T1548.003 | Abuse Elevation Control Mechanism: Sudo and Sudo Caching |

---

### RECOMENDACIONES Y MITIGACIONES (Actionable Intel­ligence)

#### Mitigaciones Inmediatas (Tácticas)
* **Parchado de Software**: Actualizar el servicio Silverpeas a la versión 6.3.5 (o superi­ores) para solventar las vulnerabilidades CVE-2024-36042 y CVE-2023-47323.
    - **CVE-2024-36042** (_Parameter Tampering_): Solucionada en la versión 6.3.5.
    - **CVE-2023-47323** (_IDOR_): Solucionada en la versión 6.3.2.

* **Restricción de Privilegios sudo**: Revocar la directiva `(ALL: ALL) ALL` asignada al usuario `tyler` en el archivo `sudoers`. Aplicar el principio de menor privilegio (PoLP - __Principle of Least Privilege__) limitando los comandos ejecutables a los estrictamente necesarios y requiriendo siempre la re-autenticación por contraseña (`NOPASS` deshabil­itado).

* **Rotación y Gestión de Credenciales**: Rotar inmediatamente la contraseña del usuario `tyler` en el sistema operativo y la base de datos PostgreSQL. Erradicar la práctica de reutilización de contraseñas (_Password Reuse_) entre servicios y cuentas de usuario.
  
* **Saneamiento de Registros**: Sanitizar los comandos de despliegue (ej. `docker run`) e integrar filtros en el dominio de registros para evitar la captura.

#### Mitigaciones a Largo Plazo (Estratégicas)

* **Integración de seguridad en el Ciclo de Desarrollo (DevSecOps)**: Implementar herramientas de Análisis Estático de Código de aplicaciones (SAST) y Pruebas de Seguridad Dinámicas (DAST) en las canalizaciones CI/CD para identificar fallos de control de acceso (IDOR) y manipulación de parámetros de forma temprana.

  - Posibles herramientas de SAST: Semgrep, SonarQube.
  - Posibles herramientas de DAST: OWASP ZAP, Burp Suite Pro, StackHawk, Acunetix.

* **Auditoría y Monitoreo continuo en Host**: Configurar políticas de auditoría a nivel de Kernel mediante auditd (`auditctl`) para supervisar la ejecución de comandos con privilegios elevados (`sudo`), la inspección de archivos en `/var/log` por usuarios no privilegiados y la creación de procesos anómalos.

<br><br>

---

<div align="center">

**HellHound DevSecOps**<br>
*Ciberseguridad, Análisis de Sistemas & Reports*

[![GitHub](https://img.shields.io/badge/GitHub-181717?style=flat&logo=github&logoColor=white)](https://github.com/xhellhoundx/)
[![YouTube](https://img.shields.io/badge/YouTube-FF0000?style=flat&logo=youtube&logoColor=white)](https://www.youtube.com/@H3llH0undDSO)
[![X](https://img.shields.io/badge/X-000000?style=flat&logo=x&logoColor=white)](https://x.com/hellhoundso)

</div>