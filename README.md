# 🏢 JCDecaux | Visor Unificado de Seguridad (VUS)

> **Solución "In-House" para la visualización centralizada de cámaras de seguridad (Axis, IProNet y Genéricas) en entorno web sin dependencias de software propietario.**

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![Django](https://img.shields.io/badge/Django-5.0-green.svg)
![SQL Server](https://img.shields.io/badge/Database-SQL%20Server-red.svg)
![Status](https://img.shields.io/badge/Status-Producci%C3%B3n%20On--Premise-orange)

---

## 📋 Contexto y Motivación

Este proyecto nace de la necesidad crítica de actualizar la infraestructura de seguridad de JCDecaux ante la migración a **Windows 11**.

* **Problemática:** El software de visualización actual (Ipronet) es incompatible con Windows 11 y el fabricante se encuentra en concurso de acreedores (sin soporte).
* **Solución:** Desarrollo de una aplicación web nativa capaz de unificar señales RTSP de distintos fabricantes, eliminando la necesidad de instalar software cliente en los PCs de los operadores.
* **Infraestructura:** Despliegue 100% On-Premise en el servidor `MAD128NS218`.

## 🛠️ Arquitectura Técnica

El sistema sigue una arquitectura monolítica ligera optimizada para Windows Server, sin uso de contenedores (Docker) para simplificar el mantenimiento por parte del equipo de Sistemas.

* **Frontend:** HTML5, Bootstrap 5 (Grid Responsivo 4x), **HLS.js** (Reproducción de vídeo compatible con Firewall).
* **Backend:** Python / Django (Gestión de usuarios, inventario y seguridad).
* **Base de Datos:** Microsoft SQL Server (Integración con infraestructura corporativa).
* **Streaming Engine:** MediaMTX (Transmuxing RTSP -> HLS en tiempo real de baja latencia).

## 🚀 Requisitos Previos

Para ejecutar el proyecto en el servidor `MAD128NS218` o en local:

1.  **Sistema Operativo:** Windows 10/11 o Windows Server 2019/2022.
2.  **Python:** Versión 3.10 o superior.
3.  **Drivers BBDD:** [ODBC Driver 17 for SQL Server](https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server).
4.  **MediaMTX:** Binario ejecutable (incluido en la carpeta `/MediaServer`).

## ⚙️ Instalación y Configuración

### 1. Clonado y Entorno Virtual
```bash
# Clonar repositorio (o copiar carpeta)
cd VisorCamaras_JCD

# Crear entorno virtual
python -m venv .venv

# Activar entorno (PowerShell)
.venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

```

### 2. Configuración de Base de Datos

El sistema espera una conexión a SQL Server. Configurar en `VisorCamaras_JCD/settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'mssql',
        'NAME': 'JCDecaux_Visor',
        'HOST': r'(localdb)\MSSQLLocalDB', # O IP del servidor MAD128NS218
        'OPTIONS': {
            'driver': 'ODBC Driver 17 for SQL Server',
            'extra_params': 'Trusted_Connection=yes',
        },
    }
}

```

### 3. Configuración de Cámaras (MediaMTX)

Editar el archivo `MediaServer/mediamtx.yml`. Aquí se definen las rutas RTSP físicas de las cámaras:

```yaml
paths:
  # Ejemplo Axis
  axis_reception:
    source: rtsp://root:pass@10.70.81.90/axis-media/media.amp
  
  # Ejemplo IProNet/Genérica
  parking_entrada:
    source: rtsp://admin:pass@10.70.81.3:554/stream0

```

## ▶️ Ejecución

El sistema requiere dos procesos corriendo simultáneamente:

**1. Motor de Vídeo (Terminal 1):**

```powershell
cd MediaServer
.\mediamtx.exe

```

**2. Servidor Web (Terminal 2):**

```powershell
# En desarrollo
python manage.py runserver 0.0.0.0:8000

```

Acceso web: `http://localhost:8000` (o IP del servidor).

## 🛡️ Administración y Gestión

El sistema cuenta con un panel de administración para dar de alta/baja cámaras sin tocar código.

* **URL:** `/admin`
* **Funcionalidades:**
* Crear nueva cámara (Asignar Nombre y URL HLS).
* Activar/Desactivar cámaras (Checkbox "Activa").
* Modificar nombres visibles en el videowall.



**Nota sobre URLs en Admin:**
Las URLs deben apuntar al servicio HLS local.

* Formato: `http://[IP_SERVIDOR]:8888/[NOMBRE_EN_YML]/index.m3u8`

## 📦 Despliegue en Producción (MAD128NS218)

Para el entorno productivo definitivo:

1. **MediaMTX:** Configurar como Servicio de Windows (inicio automático).
2. **Django:** Servir mediante **IIS** (Internet Information Services) o como servicio Windows usando `Waitress`.
3. **Firewall:** Permitir reglas de entrada TCP en puertos `8000` (Web) y `8888` (Vídeo).

## 👤 Autor

Desarrollado por **Yago Menéndez** para el departamento de IT/Seguridad de JCDecaux.
