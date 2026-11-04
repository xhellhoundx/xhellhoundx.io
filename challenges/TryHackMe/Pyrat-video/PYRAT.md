<div align="center">
    <figure>
        <img src="./assets/pyrat-icon.png" width="400" height="400">
    </figure>
</div>

<div align="center">

# Pyrat <!-- omit in toc -->
<!-- Fácil-#228B06 | Media-#BFA907 | Difícil-#A62100 -->
![TryHackMe](https://img.shields.io/badge/Plataforma-TryHackMe-A20606)
![Fácil](https://img.shields.io/badge/Dificultad-Fácil-228B06)

</div>

<br>

<div align="center">

  ## Video de resolución <!-- omit in toc -->

  <a href="https://youtu.be/1O0StBgQnEs">
    <img src="./assets/pyrat-video-icon.png" width=500>
    <br>
    Ver video en Youtube
  </a>
</div>

<br><br>

# Informe de Amenazas- Máquina "Pyrat" <!-- omit in toc -->

<br>

## Índice <!-- omit in toc -->
- [RESUMEN (Summary)](#resumen-summary)
- [ENTORNO OBJETIVO](#entorno-objetivo)
- [RECONOCIMIENTO Y RECOLECCIÓN (Recon­naissance \& Enumeration)](#reconocimiento-y-recolección-reconnaissance--enumeration)
  - [Escaneo de Red y Servicios Expuestos](#escaneo-de-red-y-servicios-expuestos)
- [ACTIVOS ENCONTRADOS](#activos-encontrados)
  - [Script procesando conexiones](#script-procesando-conexiones)
  - [Llaves id\_rsa](#llaves-id_rsa)
- [CADENA DE ATAQUE (Kill Chain)](#cadena-de-ataque-kill-chain)
  - [Exploit](#exploit)


<br>

### RESUMEN (Summary)
Durante el ataque al host `Pyrat`, se identificó la presencia de los servicios SSH y SimpleHTTP. Mediante una conexión **TCP/IP** básica (propuesta por el documento HTML en el servicio web) por `nc` se logró ingresar a través de una shell reversa a la máquina objetivo, para posteriormente descubrir un proyecto gestionado por Git en un directorio con permisos abiertos, en el cual se pudo extraer las credenciales del usuario `think` y una porción del script en Python que procesa directamente las conexiones entrantes en el puerto 8000.

--- 

### ENTORNO OBJETIVO
* **Nombre de la Amenaza / Host**: TryHackMe - Pyrat
* **Dirección IP / Alcance**: `10.114.152.117`
* **Sistema Operativo**: Linux Ubuntu 20.04.6 LTS (Focal Fossa)
* **Objetivo Comercial/Función**: Servidor web de producción simulado

---

### RECONOCIMIENTO Y RECOLECCIÓN (Recon­naissance & Enumeration)

####  Escaneo de Red y Servicios Expuestos
Se ejecutó un escaneo completo de puertos mediante `Nmap` para determinar los servicios expuestos en la red:

```bash
nmap -p- --open -Pn -n -vvv -oN target.log 10.114.152.117
```
```bash
nmap -p22,8000 -sV -sC -vvv -oN openPorts.log 10.114.152.117
```

| Puerto | Servicio | Versión | Estado |
|---|---|---|---|
| 22/TCP | ssh | OpenSSH 8.2p1 Ubuntu 4ubuntu0.13 | Abierto |
| 8000/TCP | http | SimpleHTTP/0.6 Python/3.11.2 | Abierto |

---

### ACTIVOS ENCONTRADOS

#### Script procesando conexiones

> [!TIP]
> [📜🐍 Revisa el script](./assets/pyrat.py)
> 

#### Llaves id_rsa

* Llave del usuario **think**

```
-----BEGIN OPENSSH PRIVATE KEY-----
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
-----END OPENSSH PRIVATE KEY-----
```

* Llave del usuario **root**

```
-----BEGIN OPENSSH PRIVATE KEY-----
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
-----END OPENSSH PRIVATE KEY-----
```

---

### CADENA DE ATAQUE (Kill Chain)

#### Exploit

[⚙️ EXPLOIT](./assets/exploit-pyrat.sh)

<br><br>

---

<div align="center">

**HellHound DevSecOps**<br>
*Ciberseguridad, Análisis de Sistemas & Reports*

[![GitHub](https://img.shields.io/badge/GitHub-181717?style=flat&logo=github&logoColor=white)](https://github.com/xhellhoundx/)
[![YouTube](https://img.shields.io/badge/YouTube-FF0000?style=flat&logo=youtube&logoColor=white)](https://www.youtube.com/@H3llH0undDSO)
[![X](https://img.shields.io/badge/X-000000?style=flat&logo=x&logoColor=white)](https://x.com/hellhoundso)

</div>

