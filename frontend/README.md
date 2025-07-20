# TUYA Fast-Data - Panel de Administración

## Descripción

TUYA Fast-Data es una aplicación web SPA (Single Page Application) desarrollada con **JavaScript vanilla** y Bulma CSS, utilizando **Vite** como bundler y servidor de desarrollo. Es un panel de administración interno diseñado para empleados que necesitan acceso rápido a información crítica del negocio.

**Tecnologías**: JavaScript ES6+ Modules + Bulma CSS + Vite

## Características Principales

### 🎨 Diseño y UI/UX
- **Paleta de colores**: Sigue estrictamente la paleta de colores de tuya.com.co (blanco, rojo y negro)
- **Diseño responsivo**: Funciona perfectamente en desktop, tablet y móvil
- **Interfaz intuitiva**: Navegación fluida y accesible
- **Animaciones suaves**: Transiciones y efectos visuales modernos

### 🔧 Funcionalidades Técnicas
- **SPA completa**: Navegación sin recargas de página
- **JavaScript ES6+**: Módulos modernos con import/export
- **Vite**: Bundler rápido y servidor de desarrollo
- **Bulma CSS**: Framework CSS moderno y responsive
- **Persistencia local**: Datos guardados en localStorage
- **Modularidad**: Código organizado en componentes reutilizables

### 📊 Sistema de Navegación
- **Sidebar colapsable**: Se puede minimizar/expandir con el botón de hamburguesa
- **Navegación por secciones**: Saldos, Ventas, Inventario, Clientes, Reportes, Configuración
- **Estado persistente**: La sidebar mantiene su estado al recargar la página

### 🔍 Sistema de Búsqueda
- **Búsqueda global**: Busca en todas las secciones desde el navbar superior
- **Búsqueda por sección**: Cada sección tiene su propia barra de búsqueda
- **Resultados inteligentes**: Ordenados por relevancia

### 📈 Áreas de Contenido
- **Indicadores visuales**: Áreas vacías preparadas para mostrar gráficos/indicadores
- **Contenido dinámico**: Se carga según la sección seleccionada
- **Búsqueda contextual**: Cada sección tiene su propio sistema de búsqueda

## Estructura de Archivos

```
frontend/
├── index.html                 # Archivo principal HTML
├── package.json               # Configuración de Vite y dependencias
├── src/
│   ├── main.js               # Punto de entrada de la aplicación
│   ├── app.js                # Aplicación principal
│   ├── utils.js              # Funciones utilitarias
│   ├── style.css             # Estilos personalizados
│   └── components/
│       ├── Sidebar.js        # Componente de barra lateral
│       ├── Navbar.js         # Componente de navegación superior
│       └── SectionContent.js # Contenido de secciones
├── public/
│   └── assets/
│       └── images/
│           └── logo.svg      # Logo de la aplicación
└── README.md                 # Este archivo
```

## Instalación y Uso

### Requisitos
- Node.js 16+ 
- npm o yarn

### Instalación
1. Clona el proyecto
2. Instala las dependencias:
   ```bash
   cd frontend
   npm install
   ```

### Desarrollo
```bash
# Iniciar servidor de desarrollo
npm run dev

# La aplicación estará disponible en http://localhost:5173
```

### Build para producción
```bash
# Construir para producción
npm run build

# Previsualizar build de producción
npm run preview
```

## Funcionalidades Detalladas

### Sidebar
- **Colapso/Expansión**: Click en el botón de hamburguesa
- **Navegación**: Click en cualquier elemento del menú
- **Estado persistente**: Se recuerda si estaba colapsada
- **Responsive**: En móvil se oculta automáticamente

### Búsqueda Global
- **Ubicación**: Barra superior derecha
- **Funcionamiento**: Busca en todas las secciones simultáneamente
- **Resultados**: Muestra coincidencias por sección
- **Navegación**: Click en resultado para ir a esa sección

### Sección Test
- **Funcionalidad**: Permite enviar archivos Excel al backend
- **Formatos soportados**: .xlsx, .xls, .csv
- **Validación**: Verifica el tipo de archivo antes de enviar
- **Respuesta**: Muestra la respuesta del backend en tiempo real

## Personalización

### Actualizar Colores
Los colores se definen en `src/style.css`:

```css
:root {
    --tuya-white: #ffffff;
    --tuya-red: #e31837;
    --tuya-dark-red: #c41230;
    --tuya-black: #000000;
    /* ... */
}
```

### Agregar Nuevas Secciones
1. Editar `src/components/Sidebar.js` - agregar sección al array `sections`
2. Actualizar títulos en `getSectionTitle()` de los componentes
3. Agregar método de contenido en `SectionContent.js`

## API y Funciones Globales

### Funciones Disponibles
- `showAppInfo()`: Muestra información de la aplicación
- `restartApp()`: Reinicia la aplicación
- `exportAppData()`: Exporta datos en JSON
- `importAppData()`: Importa datos desde JSON

### Objetos Globales
- `TUYAApp.app`: Instancia principal de la aplicación
- `TUYAApp.sidebar`: Componente de sidebar
- `TUYAApp.navbar`: Componente de navbar
- `TUYAApp.sectionContent`: Componente de contenido de secciones

## Compatibilidad

### Navegadores Soportados
- Chrome 60+
- Firefox 55+
- Safari 12+
- Edge 79+

### Características Requeridas
- ES6+ (Arrow functions, const/let, modules)
- Fetch API
- localStorage
- CSS Grid y Flexbox

## Ventajas de Vite + JavaScript Vanilla

### ✅ Desarrollo Rápido
- Hot Module Replacement (HMR)
- Recarga automática en cambios
- Compilación instantánea
- No configuración compleja

### ✅ Build Optimizado
- Tree shaking automático
- Minificación y compresión
- Code splitting inteligente
- Assets optimizados

### ✅ Modularidad
- ES6 modules nativos
- Import/export limpios
- Dependencias claras
- Fácil mantenimiento

### ✅ Flexibilidad
- Sin framework lock-in
- JavaScript puro
- Fácil de entender y debuggear
- Control total del código

## Scripts Disponibles

```bash
# Desarrollo
npm run dev          # Inicia servidor de desarrollo
npm run build        # Construye para producción
npm run preview      # Previsualiza build de producción
```

## Mantenimiento

### Logs y Debugging
- Abrir consola del navegador (F12)
- Los errores se muestran automáticamente
- Usar `console.log()` para debugging

### Backup de Datos
- Los datos se guardan automáticamente en localStorage
- Usar `exportAppData()` para backup manual
- Los archivos JSON se pueden editar directamente

### Actualizaciones
- Modificar archivos según necesidades
- Los cambios se reflejan inmediatamente con HMR
- Build optimizado para producción

## Soporte

### Contacto
Para soporte técnico o preguntas:
- **Creador**: Carlos Martínez
- **Email**: [email del creador]
- **Sistema**: Usar función "Contactar a Carlos Martínez" en la app

### Problemas Comunes
1. **La aplicación no carga**: Verificar que Vite esté corriendo (`npm run dev`)
2. **Búsqueda no funciona**: Verificar que los archivos JSON estén en `/public/data/responses/`
3. **Datos no se guardan**: Verificar que localStorage esté habilitado en el navegador

## Licencia

Este proyecto es propiedad de TUYA Fast-Data y está destinado para uso interno de la empresa.

---

**Desarrollado con ❤️ para TUYA Fast-Data**

*Tecnologías: JavaScript ES6+ + Bulma CSS + Vite* 