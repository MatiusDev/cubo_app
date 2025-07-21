# 🔧 Configuración de Cubo App

## 📋 Resumen

Cubo App usa archivos **YAML** para la configuración. Este formato es más legible, estructurado y permite comentarios nativos.

**⚠️ Importante**: Esta aplicación está diseñada para ejecutarse **solo localmente** por razones de seguridad. Todas las configuraciones mantienen `localhost` como host, tanto en desarrollo como en producción.

## 🎯 Modos de Operación

### **frontend** (Recomendado por defecto)
- ✅ Solo aplicación frontend
- ✅ Desarrollo con Vite
- ✅ Requiere Node.js
- ✅ Configuración por defecto

### **backend**
- ✅ Solo servidor backend
- ✅ API REST con FastAPI
- ✅ No requiere Node.js

### **full**
- ✅ Backend + Frontend completos
- ✅ Desarrollo y producción
- ✅ Requiere Node.js para frontend

## 📁 Estructura del Archivo

El archivo `config.yml` debe estar en la raíz del proyecto:

```yaml
# config.yml
mode: full  # backend, frontend, full

backend:
  port: 8000
  host: localhost
  debug: false
  reload: true

frontend:
  port: 5173
  host: localhost
  hot_reload: true
  open_browser: true

build:
  mode: development  # development, production
  clean_after_build: true
  pyinstaller:
    onefile: true
    windowed: true
    icon: null

development:
  auto_open_browser: true
  debug_mode: false
  service_timeout: 30

wsl:
  auto_detect: true
  use_wsl_browser: true

logging:
  level: INFO  # DEBUG, INFO, WARNING, ERROR
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
  file: null
```

## 🚀 Configuraciones Listas para Usar

### **1. Frontend - Desarrollo (Recomendado por defecto)**

```yaml
mode: frontend
backend:
  port: 8000
  host: localhost
  debug: false
  reload: true
frontend:
  port: 5173
  host: localhost
  hot_reload: true
  open_browser: true
build:
  mode: development
  clean_after_build: true
  pyinstaller:
    onefile: true
    windowed: true
    icon: null
development:
  auto_open_browser: true
  debug_mode: false
  service_timeout: 30
wsl:
  auto_detect: true
  use_wsl_browser: true
logging:
  level: INFO
  format: '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
  file: null
```

**Uso**: Desarrollo frontend con hot reload (configuración por defecto)

### **2. Full - Producción**

```yaml
mode: full
backend:
  port: 8000
  host: localhost
  debug: false
  reload: false
frontend:
  port: 5173
  host: localhost
  hot_reload: false
  open_browser: false
build:
  mode: production
  clean_after_build: true
  pyinstaller:
    onefile: true
    windowed: true
    icon: null
development:
  auto_open_browser: false
  debug_mode: false
  service_timeout: 60
wsl:
  auto_detect: true
  use_wsl_browser: false
logging:
  level: WARNING
  format: '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
  file: logs/app.log
```

**Cambios principales**:
- `host: localhost` (solo acceso local por seguridad)
- `debug: false` y `reload: false`
- `hot_reload: false`
- `auto_open_browser: false`
- `build.mode: production`
- `service_timeout: 60`
- `logging.level: WARNING`
- `logging.file: logs/app.log`

### **3. Solo Backend - Desarrollo**

```yaml
mode: backend
backend:
  port: 8000
  host: localhost
  debug: true
  reload: true
frontend:
  port: 5173
  host: localhost
  hot_reload: true
  open_browser: true
build:
  mode: development
  clean_after_build: true
  pyinstaller:
    onefile: true
    windowed: true
    icon: null
development:
  auto_open_browser: true
  debug_mode: true
  service_timeout: 30
wsl:
  auto_detect: true
  use_wsl_browser: true
logging:
  level: DEBUG
  format: '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
  file: null
```

**Uso**: Solo API backend para desarrollo y testing

### **4. Solo Backend - Producción**

```yaml
mode: backend
backend:
  port: 8000
  host: localhost
  debug: false
  reload: false
frontend:
  port: 5173
  host: localhost
  hot_reload: true
  open_browser: true
build:
  mode: production
  clean_after_build: true
  pyinstaller:
    onefile: true
    windowed: true
    icon: null
development:
  auto_open_browser: false
  debug_mode: false
  service_timeout: 60
wsl:
  auto_detect: true
  use_wsl_browser: false
logging:
  level: WARNING
  format: '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
  file: logs/backend.log
```

**Cambios principales**:
- `mode: backend`
- `backend.host: localhost` (solo acceso local por seguridad)
- `backend.debug: false`
- `backend.reload: false`
- `development.auto_open_browser: false`
- `logging.file: logs/backend.log`

### **5. Solo Frontend - Desarrollo**

```yaml
mode: frontend
backend:
  port: 8000
  host: localhost
  debug: false
  reload: true
frontend:
  port: 5173
  host: localhost
  hot_reload: true
  open_browser: true
build:
  mode: development
  clean_after_build: true
  pyinstaller:
    onefile: true
    windowed: true
    icon: null
development:
  auto_open_browser: true
  debug_mode: true
  service_timeout: 30
wsl:
  auto_detect: true
  use_wsl_browser: true
logging:
  level: DEBUG
  format: '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
  file: null
```

**Uso**: Solo frontend para desarrollo de UI/UX

### **6. Solo Frontend - Producción**

```yaml
mode: frontend
backend:
  port: 8000
  host: localhost
  debug: false
  reload: true
frontend:
  port: 5173
  host: localhost
  hot_reload: false
  open_browser: false
build:
  mode: production
  clean_after_build: true
  pyinstaller:
    onefile: true
    windowed: true
    icon: null
development:
  auto_open_browser: false
  debug_mode: false
  service_timeout: 60
wsl:
  auto_detect: true
  use_wsl_browser: false
logging:
  level: WARNING
  format: '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
  file: logs/frontend.log
```

**Cambios principales**:
- `mode: frontend`
- `frontend.port: 5173` (mantiene puerto de desarrollo por seguridad)
- `frontend.host: localhost` (solo acceso local por seguridad)
- `frontend.hot_reload: false`
- `frontend.open_browser: false`
- `development.auto_open_browser: false`
- `logging.file: logs/frontend.log`

## 🔧 Configuración Rápida

### **Crear configuración interactiva:**
```bash
python3 configure.py
```

### **Crear configuración específica:**
```bash
python3 configure.py           # Frontend (por defecto)
python3 configure.py frontend  # Solo Frontend
python3 configure.py backend   # Solo Backend
python3 configure.py full      # Backend + Frontend
```

### **Editar configuración manualmente:**
```bash
# Linux/Mac
nano config.yml
# o
code config.yml

# Windows
notepad config.yml
# o
code config.yml
```

## 📊 Parámetros Importantes

### **Backend**
- `port`: Puerto del servidor (8000 por defecto)
- `host`: Host del servidor (localhost para desarrollo y producción por seguridad)
- `debug`: Modo debug (true para desarrollo, false para producción)
- `reload`: Auto-reload (true para desarrollo, false para producción)

### **Frontend**
- `port`: Puerto del servidor (5173 por defecto, mantiene puerto de desarrollo por seguridad)
- `host`: Host del servidor (localhost para desarrollo y producción por seguridad)
- `hot_reload`: Recarga automática (true para desarrollo, false para producción)
- `open_browser`: Abrir navegador automáticamente

### **Build**
- `mode`: Modo de construcción (development/production)
- `clean_after_build`: Limpiar archivos temporales
- `pyinstaller`: Configuración para crear ejecutables

### **Development**
- `auto_open_browser`: Abrir navegador automáticamente
- `debug_mode`: Modo debug general
- `service_timeout`: Timeout para servicios (30s desarrollo, 60s producción)

### **WSL**
- `auto_detect`: Detectar automáticamente WSL
- `use_wsl_browser`: Usar navegador WSL

### **Logging**
- `level`: Nivel de log (DEBUG, INFO, WARNING, ERROR)
- `format`: Formato de los logs
- `file`: Archivo de log (null para solo consola)

## 🚨 Notas Importantes

### **Producción**
- **Mantiene `host: localhost` por seguridad** (no accesible desde red)
- Desactiva `debug` y `reload`
- Usa `logging.file` para archivos de log
- Aumenta `service_timeout` a 60 segundos
- Mantiene puertos de desarrollo por seguridad

### **Desarrollo**
- Usa `host: localhost` para seguridad
- Activa `debug` y `reload`
- Usa `logging.file: null` para logs en consola
- `service_timeout: 30` es suficiente

### **WSL**
- La detección automática funciona en la mayoría de casos
- Si tienes problemas, ajusta `use_wsl_browser`

## 💡 Tips

1. **Backup**: Haz backup antes de cambiar configuración
2. **Pruebas**: Prueba la configuración antes de producción
3. **Logs**: Revisa los logs para debugging
4. **Puertos**: Asegúrate de que los puertos estén libres
5. **Seguridad**: La aplicación solo se ejecuta localmente por diseño
6. **Permisos**: En Linux, puertos < 1024 requieren permisos de root

## 🔒 Seguridad

### **Diseño de Seguridad**
- **Acceso Local**: La aplicación está diseñada para ejecutarse solo en `localhost`
- **Sin Acceso de Red**: No se expone a la red por razones de seguridad
- **Puertos Estándar**: Usa puertos de desarrollo (8000, 5173) incluso en producción
- **Sin Autenticación**: No incluye sistema de autenticación por ser aplicación local

### **Configuración Segura**
- ✅ `host: localhost` - Solo acceso local
- ✅ `debug: false` en producción - Sin información sensible
- ✅ `logging.file` en producción - Logs en archivos locales
- ✅ Puertos de desarrollo - Evita conflictos con servicios del sistema

### **Recomendaciones**
- **No cambiar a `0.0.0.0`** - Mantener seguridad local
- **No exponer a internet** - Usar solo en redes confiables
- **Revisar logs** - Monitorear actividad local
- **Backup regular** - Mantener copias de configuración 