# 🌱 EcoAnalyzer Web

**Versión web moderna del proyecto EcoAnalyzer original**

Esta es una migración completa de la aplicación de escritorio tkinter a una aplicación web moderna usando Flask. Mantiene toda la funcionalidad original con una interfaz web responsive y moderna.

## 🎯 ¿Qué es esto?

EcoAnalyzer Web es la evolución de mi proyecto de primer año universitario. Originalmente desarrollado en Python con tkinter, ahora está disponible como una aplicación web completa que puede ejecutarse en cualquier navegador.

## ✨ Características

### Funcionalidades originales mantenidas:
- 🔐 **Sistema de autenticación** - Login seguro con sesiones
- 📊 **Gestión de productos** - CRUD completo (Crear, Leer, Actualizar, Eliminar)
- 💰 **Cálculo automático de ganancias** - Precio × Cantidad vendida
- 📈 **Gráficos interactivos** - Visualización de ganancias por producto
- 🗄️ **Base de datos SQLite** - Persistencia de datos (compatible con versión original)
- ⏰ **Registro de tiempo** - Timestamp automático de transacciones

### Nuevas características web:
- 📱 **Responsive design** - Funciona en móviles, tablets y desktop
- 🎨 **UI moderna** - Interfaz actualizada manteniendo los colores originales
- 🌐 **Acceso desde navegador** - No requiere instalación de aplicación
- ⚡ **Interacciones en tiempo real** - Validación de formularios y notificaciones
- 📊 **Gráficos web interactivos** - Chart.js para visualizaciones modernas

## 🚀 Instalación y uso

### Opción 1: Inicio rápido
```bash
# Clonar el repositorio
git clone https://github.com/sebitabravo/EcoAnalyzer.git
cd EcoAnalyzer

# Ejecutar directamente (instala dependencias automáticamente)
python start_web.py
```

### Opción 2: Instalación manual
```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar servidor Flask
python web_app.py
```

La aplicación se abrirá automáticamente en tu navegador en `http://localhost:8080`

## ⚙️ Configuración de variables de entorno

Para un funcionamiento óptimo y seguro de la aplicación, configura estas variables de entorno:

### Variables requeridas

```bash
FLASK_ENV=production
SECRET_KEY=tu_clave_secreta_super_segura_aqui
PORT=8081
```

### Métodos de configuración

#### Opción 1: Archivo .env (Recomendado)

Crea un archivo `.env` en la raíz del proyecto:

```bash
# .env
FLASK_ENV=production
SECRET_KEY=mi_aplicacion_ecoanalyzer_2025_clave_ultra_segura_123456789
PORT=8081
```

#### Opción 2: Terminal (Temporal)

```bash
export FLASK_ENV=production
export SECRET_KEY=tu_clave_secreta_super_segura_aqui
export PORT=8081
python web_app.py
```

#### Opción 3: Shell profile (Permanente)

```bash
# Para zsh (macOS/Linux)
echo 'export FLASK_ENV=production' >> ~/.zshrc
echo 'export SECRET_KEY=tu_clave_secreta_super_segura_aqui' >> ~/.zshrc
echo 'export PORT=8081' >> ~/.zshrc
source ~/.zshrc
```

#### Opción 4: Para desarrollo

```bash
# Modo desarrollo con debug activado
FLASK_ENV=development python web_app.py
```

### Descripción de variables

- **`FLASK_ENV`**: Configura el entorno (production/development)
- **`SECRET_KEY`**: Clave secreta para sesiones (¡cámbiala por una segura!)
- **`PORT`**: Puerto donde se ejecuta la aplicación (por defecto 8081)

⚠️ **Importante**: Nunca subas el archivo `.env` a repositorios públicos. Ya está incluido en `.gitignore`.

## 🔑 Credenciales por defecto

- **Usuario:** admin
- **Contraseña:** 1234

## 📋 Funcionalidades disponibles

### 1. Login seguro
- Autenticación con base de datos SQLite
- Sesiones persistentes
- Validación de credenciales

### 2. Dashboard principal
- Formulario para agregar productos
- Tabla interactiva con todos los productos
- Opciones de editar y eliminar
- Cálculo automático de ganancias

### 3. Visualización de datos
- Gráficos de barras interactivos
- Agrupación de ganancias por producto
- Toggle para mostrar/ocultar gráficos

### 4. Gestión de productos
- ✅ **Agregar** - Día, nombre, precio, cantidad
- ✏️ **Editar** - Modificar cualquier campo
- 🗑️ **Eliminar** - Con confirmación de seguridad
- 👁️ **Visualizar** - Tabla ordenada por fecha

## 🛠️ Tecnologías utilizadas

- **Backend:** Flask (Python)
- **Frontend:** HTML5, CSS3, JavaScript
- **UI Framework:** Bootstrap 5
- **Gráficos:** Chart.js
- **Base de datos:** SQLite (compatible con versión original)
- **Estilos:** CSS custom basado en el diseño original de tkinter

## 📁 Estructura del proyecto

```
EcoAnalyzer/
├── web_app.py              # Aplicación Flask principal
├── start_web.py            # Script de inicio con auto-instalación
├── requirements.txt        # Dependencias Python
├── templates/              # Plantillas HTML
│   ├── base.html          # Plantilla base
│   ├── login.html         # Página de login
│   └── dashboard.html     # Dashboard principal
├── static/                # Archivos estáticos
│   ├── css/style.css      # Estilos personalizados
│   └── js/app.js          # JavaScript de la aplicación
├── database/              # Bases de datos (compatibles con versión original)
│   ├── productos.db       # Productos y ventas
│   └── usuario.db         # Usuarios del sistema
└── [archivos originales]  # Tu proyecto tkinter original intacto
```

## 🎨 Diseño y UI

La interfaz web mantiene la identidad visual de tu aplicación original:
- **Colores primarios:** Violet (#601E88), Verde (#2cb67d)
- **Esquema:** Tema oscuro como la aplicación original
- **Tipografía:** Arial Bold para mantener consistencia
- **Layout:** Responsive design que se adapta a cualquier pantalla

## 🔄 Compatibilidad con versión original

✅ **Las bases de datos son 100% compatibles** entre ambas versiones
✅ **Puedes usar ambas aplicaciones alternadamente**
✅ **Los datos se comparten automáticamente**

## 🌟 ¿Por qué migrar a web?

1. **Portabilidad** - Funciona en cualquier dispositivo con navegador
2. **No requiere instalación** - Solo abrir en navegador
3. **Fácil demostración** - Perfecto para mostrar en entrevistas/portafolio
4. **Escalabilidad** - Base para futuras mejoras (multi-usuario, API, etc.)
5. **Tecnologías modernas** - Stack web actual y demandado

## 🎯 Casos de uso

- **Portafolio profesional** - Mostrar evolución de tus habilidades
- **Demostración académica** - Presentar proyecto universitario modernizado
- **Aprendizaje web** - Base para aprender desarrollo web
- **Uso personal** - Gestión de ventas desde cualquier dispositivo

## 🔧 Desarrollo y personalización

El código está estructurado para ser fácil de entender y modificar:

- `web_app.py` - Lógica del servidor y rutas
- `templates/` - HTML con Jinja2 templating
- `static/css/style.css` - Estilos personalizables
- `static/js/app.js` - Funcionalidades del frontend

## 📈 Próximas mejoras posibles

- [ ] API REST para integración con otras aplicaciones
- [ ] Exportación de datos (Excel, PDF)
- [ ] Dashboard con más estadísticas
- [ ] Modo multi-usuario
- [ ] Notificaciones en tiempo real
- [ ] Integración con servicios en la nube

## 📝 Notas del desarrollador

Este proyecto representa la evolución natural de mi primer proyecto universitario. Demuestra:

- **Capacidad de migración** de tecnologías desktop a web
- **Mantenimiento de funcionalidad** durante la migración
- **Mejora de UX/UI** usando tecnologías modernas
- **Compatibilidad backward** con sistemas existentes

---

**Desarrollado por:** Sebastian Bravo  
**Proyecto original:** Primer año universitario (tkinter)  
**Migración web:** 2025 (Flask + HTML/CSS/JS)  

🚀 **¡De tkinter a web en una sola migración!**