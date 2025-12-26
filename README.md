# 📊 Automación de Aprobaciones para Power BI

Sistema automatizado para extraer datos de Microsoft Teams Approvals y subirlos a SharePoint para su posterior análisis en Power BI.

## 📋 Descripción General

Este proyecto automatiza el proceso de extracción, transformación y carga (ETL) de datos de aprobaciones desde Microsoft Teams hacia SharePoint. El sistema utiliza las APIs de Microsoft Graph para acceder a los datos de aprobaciones de cada usuario mediante autenticación basada en tokens OAuth 2.0.

### Funcionalidades Principales

- ✅ Extracción de datos de Microsoft Teams Approvals mediante Microsoft Graph API
- 🔐 Autenticación segura con Microsoft Azure AD (MSAL)
- 🔄 Transformación y limpieza de datos automática
- ☁️ Carga automática de archivos CSV a SharePoint
- 📈 Interfaz web para visualizar reportes de Power BI
- 🏷️ Clasificación inteligente de aprobaciones por tipo y categoría

## 🏗️ Arquitectura del Sistema

El proyecto está compuesto por tres componentes principales:

```
┌─────────────────┐      ┌─────────────────┐      ┌─────────────────┐
│   Frontend      │ ───▶ │    Backend      │ ───▶ │  Microsoft      │
│   (Vue.js)      │      │   (FastAPI)     │      │  Graph API      │
└─────────────────┘      └─────────────────┘      └─────────────────┘
                                 │
                                 ▼
                         ┌─────────────────┐
                         │   SharePoint    │
                         │   (Storage)     │
                         └─────────────────┘
```

### Componentes

1. **Frontend (Vue.js 3 + MSAL)**
   - Autenticación de usuarios con Microsoft Azure AD
   - Interfaz para disparar el proceso de extracción
   - Visualización integrada de reportes de Power BI

2. **Backend (FastAPI + Python)**
   - API REST para gestionar las solicitudes
   - Extracción de datos desde Microsoft Graph API
   - Transformación y limpieza de datos
   - Carga de archivos CSV a SharePoint

3. **Microsoft Graph API**
   - Acceso a datos de Microsoft Teams Approvals
   - Autenticación OAuth 2.0

4. **SharePoint**
   - Almacenamiento de archivos CSV procesados
   - Fuente de datos para Power BI

## 🛠️ Tecnologías Utilizadas

### Frontend
- **Vue.js 3** - Framework JavaScript progresivo
- **MSAL Browser** - Librería de autenticación de Microsoft
- **Vite** - Build tool y dev server
- **Nginx** - Servidor web para producción (Docker)

### Backend
- **Python 3.11**
- **FastAPI** - Framework web moderno y de alto rendimiento
- **Uvicorn** - Servidor ASGI
- **MSAL** - Microsoft Authentication Library
- **Requests** - Cliente HTTP
- **python-dotenv** - Gestión de variables de entorno

### Infraestructura
- **Docker** - Contenedorización
- **Docker Compose** - Orquestación de contenedores

## 📦 Requisitos Previos

- Docker y Docker Compose instalados
- Node.js 20.19+ o 22.12+ (para desarrollo local)
- Python 3.11+ (para desarrollo local)
- Cuenta de Azure con una aplicación registrada
- Permisos de Microsoft Graph API:
  - `User.Read`
  - `Approvals.Read.All`
  - `Sites.ReadWrite.All`

## 🔧 Configuración

### 1. Registro de Aplicación en Azure AD

1. Accede al [Portal de Azure](https://portal.azure.com)
2. Navega a **Azure Active Directory** > **App registrations**
3. Crea una nueva aplicación o usa una existente
4. Configura los permisos de API necesarios
5. Genera un **Client Secret**
6. Obtén los siguientes valores:
   - Client ID
   - Tenant ID
   - Client Secret

### 2. Obtener IDs de SharePoint

Para obtener el `SITE_ID` y `DRIVE_ID` de SharePoint:

```bash
# Obtener Site ID
https://graph.microsoft.com/v1.0/sites/{your-sharepoint-domain}:/sites/{site-name}

# Obtener Drive ID
https://graph.microsoft.com/v1.0/sites/{site-id}/drives
```

### 3. Variables de Entorno

Crea un archivo `.env` en la raíz del proyecto con las siguientes variables:

```env
# Azure AD Configuration
MS_TENANT_ID=tu-tenant-id
MS_CLIENT_ID=tu-client-id
MS_CLIENT_SECRET=tu-client-secret

# SharePoint Configuration
SITE_ID=tu-site-id-de-sharepoint
DRIVE_ID=tu-drive-id-de-sharepoint

# Frontend Configuration
FRONTEND_ORIGIN=http://localhost:8080

# Output Files
OUTPUT_FILENAME=approvals.csv
CLEAN_OUTPUT_FILENAME=datos_completos_power_bi.csv

# Power BI (opcional)
VITE_POWERBI_REPORT_URL=tu-url-de-power-bi

# Logging
LOG_LEVEL=INFO
```

## 🚀 Instalación y Ejecución

### Con Docker (Recomendado)

1. Clona el repositorio:
```bash
git clone https://github.com/AndresProano/automateApprovalsInPowerBi.git
cd automateApprovalsInPowerBi
```

2. Crea el archivo `.env` con tus credenciales

3. Inicia los contenedores:
```bash
docker-compose up --build
```

4. Accede a la aplicación:
   - Frontend: http://localhost:8080
   - Backend API: http://localhost:8000

### Desarrollo Local

#### Backend

```bash
cd back
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend

```bash
cd front/vue-project
npm install
npm run dev
```

## 📖 Uso del Sistema

### 1. Autenticación

1. Accede a http://localhost:8080
2. Haz clic en **"Iniciar Sesión con Microsoft"**
3. Ingresa tus credenciales de Microsoft
4. Autoriza los permisos solicitados

### 2. Generar Reporte

1. Una vez autenticado, haz clic en **"Generar Reporte y Actualizar"**
2. El sistema ejecutará automáticamente:
   - Extracción de datos de Teams Approvals
   - Transformación y limpieza de datos
   - Carga del archivo CSV a SharePoint
3. Se mostrará el reporte de Power BI embebido

### 3. Visualización en Power BI

El archivo CSV generado se sube automáticamente a SharePoint y puede ser consumido por Power BI para crear visualizaciones y dashboards.

## 📂 Estructura del Proyecto

```
automateApprovalsInPowerBi/
├── back/                          # Backend (Python/FastAPI)
│   ├── app/
│   │   ├── main.py               # Punto de entrada de la API
│   │   ├── config.py             # Configuración y variables de entorno
│   │   ├── graph_extractor.py   # Extracción de datos desde Graph API
│   │   ├── csv_transformer.py   # Conversión a formato CSV
│   │   ├── limpiarSimplificado.py # Limpieza y clasificación de datos
│   │   └── sharepoint_uploader.py # Carga a SharePoint
│   ├── Dockerfile
│   └── requirements.txt
├── front/                         # Frontend (Vue.js)
│   └── vue-project/
│       ├── src/
│       │   ├── App.vue           # Componente principal
│       │   ├── authConfig.js     # Configuración MSAL
│       │   └── main.js
│       ├── Dockerfile
│       ├── nginx.conf
│       └── package.json
├── docker-compose.yaml            # Orquestación de contenedores
└── README.md
```

## 🔐 Flujo de Autenticación

### Frontend (Usuario)
1. El usuario inicia sesión con MSAL (Microsoft Authentication Library)
2. Se obtiene un `access_token` con los scopes necesarios
3. El token se envía en el header `Authorization: Bearer {token}`

### Backend (Aplicación)
1. El backend valida el token recibido del frontend
2. Usa el token para acceder a Microsoft Graph API
3. Para subir a SharePoint, el backend obtiene su propio token usando **Client Credentials Flow**

## 🔄 Proceso de Transformación de Datos

### 1. Extracción (`graph_extractor.py`)
- Consulta a Microsoft Graph API: `/beta/solutions/approval/approvalItems`
- Manejo de paginación automático
- Extracción de todos los campos relevantes

### 2. Transformación (`csv_transformer.py`)
Convierte los datos JSON a formato CSV con los siguientes campos:
- ID de aprobación
- Título
- Tipo de aprobación
- Fechas (creación, completado)
- Estado y resultado
- Aprobadores
- Propietario

### 3. Limpieza (`limpiarSimplificado.py`)
- Clasificación automática por tipo:
  - Control de Cambios (CDC)
  - Paso a Producción
  - Publicación
  - Análisis Funcional
  - Gestión de Identidades
  - Conectividad (VPN)
- Extracción de metadata:
  - Ticket ID
  - Área responsable
  - Fechas estructuradas (año, mes, día)
  - Asignaciones por email

### 4. Carga (`sharepoint_uploader.py`)
- Obtención de token con Client Credentials
- Upload del archivo CSV a SharePoint
- Sobrescritura automática si el archivo existe

## 📡 API Endpoints

### `GET /api/approvals`

Extrae las aprobaciones del usuario autenticado, las procesa y las sube a SharePoint.

**Headers:**
```
Authorization: Bearer {access_token}
```

**Respuesta exitosa (200):**
```json
{
  "ok": true,
  "count": 150,
  "items": [...],
  "message": "Process completed successfully"
}
```

**Errores:**
- `401` - Token faltante o inválido
- `500` - Error en el procesamiento

## 🔍 Clasificación de Aprobaciones

El sistema clasifica automáticamente las aprobaciones en las siguientes categorías:

| Macro Categoría | Micro Categoría | Palabras Clave |
|-----------------|-----------------|----------------|
| Control de Cambios (CDC) | Base de Datos, Seguridad, Infraestructura | CDC, CONTROL DE CAMBIOS, BDD, SEGURIDAD |
| Paso a Producción | App Terceros, Producción | PASO A PRODUCCIÓN, TERCEROS |
| Publicación | App Terceros, Otros | PUBLICACIÓN |
| Análisis Funcional | Aplicaciones | ANALISIS FUNCIONAL DEL SERVICIO |
| Gestión de Identidades | Cuenta Genérica, Cuenta de Servicio, Cuenta Privilegiada | CUENTA, GENÉRICA, SERVICIO, PRIVILEGIADA |
| Conectividad | VPN | VPN |
| Levantamiento | General | SOLICITUD DE LEVANTAMIENTO |

## 🐛 Troubleshooting

### Error: "Graph error: 401"
- Verifica que el token no haya expirado
- Confirma que los permisos en Azure AD estén correctamente configurados

### Error al subir a SharePoint
- Verifica que `SITE_ID` y `DRIVE_ID` sean correctos
- Confirma que el Client Secret no haya expirado
- Verifica que la aplicación tenga permisos `Sites.ReadWrite.All`

### Frontend no conecta con Backend
- Verifica que `FRONTEND_ORIGIN` en `.env` coincida con la URL del frontend
- Revisa la configuración de CORS en `main.py`

## 🤝 Contribución

Las contribuciones son bienvenidas. Por favor:

1. Haz fork del proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto es privado y de uso interno.

## 👥 Autores

- Andrés Proaño - [@AndresProano](https://github.com/AndresProano)

## 📞 Soporte

Para preguntas o soporte, por favor abre un issue en el repositorio de GitHub.

---

**Nota:** Este sistema maneja datos sensibles. Asegúrate de nunca commitear el archivo `.env` o exponer las credenciales de Azure AD.
