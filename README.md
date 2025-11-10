# BiblioHub - Sistema de Gestión Bibliotecaria

![BiblioHub Logo](assets/bg-bibliohub.png)

**BiblioHub** es una aplicación de escritorio moderna y robusta para la gestión integral de bibliotecas. Desarrollada en Python con una interfaz gráfica de usuario (GUI) construida sobre CustomTkinter, ofrece una solución completa para administrar el inventario de libros, los usuarios y el ciclo de vida de los préstamos.

---

## 📜 Índice

* [🚀 Guía de Inicio Rápido (5 minutos)](#-guía-de-inicio-rápido-5-minutos)
* [🌟 Características Principales](#-características-principales)
* [🏗️ Arquitectura del Proyecto](#️-arquitectura-del-proyecto)
* [🛠️ Tecnologías Utilizadas](#️-tecnologías-utilizadas)
* [🚀 Instalación y Puesta en Marcha](#-instalación-y-puesta-en-marcha)
* [⚙️ Scripts de Mantenimiento](#️-scripts-de-mantenimiento)

---

## 🚀 Guía de Inicio Rápido

### **📥 Instalación Express**

```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Ejecutar la aplicación
python3 main.py
```

**¡Eso es todo!** La base de datos se creará automáticamente la primera vez.

---

### **🎯 Tu Primera Biblioteca (4 pasos)**

#### **Paso 1: Crear tu Primera Estantería** 📚

1. Click en **"Gestionar Estanterías"**
2. Click en **"Crear Nueva Estantería"**
3. Completa el formulario:
   - **Nombre**: Ej: "Ciencias"
   - **Capacidad**: Ej: 50 (máximo 150)
4. Click en **"Crear Estantería"**

✅ **¡Listo!** Ya tienes tu primera estantería.

---

#### **Paso 2: Agregar tu Primer Libro** 📖

1. Vuelve al inicio (botón **"🏠 Inicio"**)
2. Click en **"Agregar Libro"**
3. Completa el formulario:
   - **Código**: Ej: "LIB001" (debe ser único)
   - **Título**: Ej: "Cien Años de Soledad"
   - **Autor Nombre**: Ej: "Gabriel"
   - **Autor Apellido**: Ej: "García Márquez"
   - **Año**: Ej: 1967
   - **Estantería**: Selecciona "Ciencias"
   - **Cantidad de Ejemplares**: Ej: 3
4. Click en **"Crear Libro"**

✅ **¡Perfecto!** Ya tienes tu primer libro con 3 ejemplares.

**💡 Tip**: El sistema te mostrará automáticamente cuántos espacios libres tiene la estantería seleccionada.

---

#### **Paso 3: Registrar tu Primer Usuario** 👤

1. Click en **"Gestionar Usuarios"**
2. Click en **"Agregar Usuario"**
3. Completa el formulario:
   - **Nombre**: Ej: "Ana García"
   - **Email**: Ej: "ana@email.com"
   - **Teléfono**: Ej: "0981234567" (opcional)
   - **Dirección**: Ej: "Av. Principal 123" (opcional)
4. Click en **"Crear Usuario"**

✅ **¡Excelente!** Ya puedes realizar préstamos.

---

#### **Paso 4: Realizar tu Primer Préstamo** 📤

1. Click en **"Gestión de Préstamos"**
2. Click en **"Realizar Préstamo"**
3. Completa el formulario:
   - **Usuario**: Selecciona "Ana García"
   - **Ejemplar**: Selecciona un ejemplar disponible (Ej: "LIB001-001")
   - **Días de préstamo**: Ej: 15
4. Click en **"Realizar Préstamo"**

✅ **¡Genial!** Has completado el flujo básico de BiblioHub.

---

### **⚡ Funcionalidades Rápidas**

| Acción | Cómo hacerlo |
|--------|--------------|
| **Ver estadísticas** | Dashboard principal (se actualiza automáticamente) |
| **Buscar libros** | "Buscar Libros" → Escribe título, autor, código o ISBN |
| **Ver reportes** | "📊 Ver Reportes" en el dashboard |
| **Devolver libro** | "Gestión de Préstamos" → "Préstamos Activos" → "Devolver" |
| **Renovar préstamo** | "Gestión de Préstamos" → "Préstamos Activos" → "Renovar" |
| **Mover libros** | "Mover Libros" → Buscar libro → Seleccionar estantería destino |

---

### **⚠️ Solución de Problemas Comunes**

#### **"No hay estanterías disponibles"**
**Solución**: Crea al menos una estantería primero en **"Gestionar Estanterías"**.

#### **"No hay usuarios registrados"**
**Solución**: Registra al menos un usuario en **"Gestionar Usuarios"** antes de hacer préstamos.

#### **"Ya existe un libro con este código"**
**Solución**: Usa un código diferente. Si eliminaste un libro y lo vuelves a agregar, usa un código nuevo (Ej: "LIB001v2" o "LIB001_nuevo").

#### **"No hay suficiente espacio en la estantería"**
**Solución**: 
- Reduce la cantidad de ejemplares a agregar
- Elige otra estantería con más espacio
- Aumenta la capacidad de la estantería en **"Gestionar Estanterías"** → **"Editar"**

---

### **🎁 Datos de Prueba (Opcional)**

Si prefieres empezar con datos de ejemplo en lugar de crear todo manualmente:

```bash
python init_database.py
```

Esto creará:
- ✅ 3 estanterías de ejemplo
- ✅ 10 libros con ejemplares
- ✅ 3 usuarios
- ✅ Algunos préstamos de ejemplo

---

### **🎉 ¡Ya estás listo!**

Ahora conoces los conceptos básicos de BiblioHub. Para más detalles sobre características avanzadas, continúa leyendo las secciones siguientes.

---

## <a name="-características-principales"></a> 🌟 Características Principales

BiblioHub está diseñado para ser intuitivo y potente, ofreciendo un conjunto completo de herramientas para el bibliotecario moderno.

#### **📚 Gestión de Inventario**

* **Gestión de Libros**: Creación, edición y eliminación de libros con información detallada (ISBN, editorial, año, descripción, etc.).
* **Gestión de Ejemplares**: El sistema distingue entre el "libro" como obra y el "ejemplar" como copia física, permitiendo un seguimiento individual de cada copia con ubicaciones físicas específicas.
* **Administración de Estanterías**: 
  - Creación, modificación y eliminación de estanterías
  - Control de capacidad máxima (límite de 150 ejemplares por estantería)
  - Validación automática: no se puede eliminar una estantería ocupada
  - Solo se pueden eliminar estanterías vacías (sin ejemplares)
* **Movimiento de Libros**: 
  - Interfaz con búsqueda inteligente en tiempo real para seleccionar libros
  - Mueve un libro y todos sus ejemplares de una estantería a otra
  - Actualiza automáticamente las ubicaciones físicas de todos los ejemplares
  - Validación de capacidad: impide mover libros si la estantería destino no tiene espacio suficiente

#### **🔄 Sistema de Préstamos Profesional**

* **Gestión de Préstamos**: Módulo completo para crear nuevos préstamos, asociando un usuario a un ejemplar específico.
* **Control de Activos y Vencidos**: Vistas separadas para monitorear los préstamos activos y aquellos que ya han vencido, con alertas visuales.
* **Devoluciones y Renovaciones**: Funcionalidad para registrar devoluciones y renovar préstamos por un período adicional.

#### **👥 Administración de Usuarios**

* **CRUD de Usuarios**: Sistema para agregar, listar, buscar y gestionar la información de los usuarios de la biblioteca.
* **Historial de Préstamos por Usuario**: Acceso rápido al historial de préstamos de cada usuario.

#### **🔍 Búsqueda y Reportes**

* **Búsqueda Unificada**: A través de la función `buscar_libros(termino)`, el sistema ofrece una búsqueda potente y flexible por título, autor, código o ISBN. Si el término es puramente numérico, se realiza una búsqueda parcial sobre el código del libro.
* **Búsqueda en Tiempo Real**: Búsqueda dinámica en la interfaz de "Mover Libros" que actualiza resultados mientras escribes.
* **Dashboard de Estadísticas**: La pantalla principal ofrece un resumen en tiempo real del estado de la biblioteca (total de libros, ejemplares disponibles, préstamos activos y vencidos).
* **Vistas Especializadas**: Listados dedicados para libros disponibles, libros prestados, y libro más prestado.

---

## <a name="️-arquitectura-del-proyecto"></a> 🏗️ Arquitectura del Proyecto

BiblioHub está desarrollado siguiendo una **arquitectura en tres capas** para garantizar la separación de responsabilidades, facilitar el mantenimiento y promover la escalabilidad.

1.  **Capa de Presentación (GUI)** - `carpeta /gui`
    * Construida con **CustomTkinter**, es responsable de toda la interacción con el usuario.
    * Está completamente modularizada; cada pantalla (frame) es una clase independiente, lo que permite un desarrollo y depuración eficientes.

2.  **Capa de Lógica de Negocio (Logic)** - `carpeta /logic`
    * Es el cerebro de la aplicación. La clase `GestorBiblioteca` orquesta todas las operaciones y contiene las reglas de negocio (ej: no se puede prestar un libro sin ejemplares).
    * Utiliza los **modelos de datos** definidos en `models.py` para trabajar con objetos de Python en lugar de datos crudos.

3.  **Capa de Acceso a Datos (Database)** - `carpeta /database`
    * Abstrae toda la comunicación con la base de datos **SQLite**.
    * El `DBManager` centraliza todas las consultas SQL, garantizando que el resto de la aplicación no necesite "hablar" SQL directamente.
    * Implementa un gestor de **transacciones** para asegurar la integridad de los datos en todas las operaciones de escritura.

---

## <a name="️-tecnologías-utilizadas"></a> 🛠️ Tecnologías Utilizadas

* **Lenguaje**: Python 3
* **Base de Datos**: SQLite 3
* **Interfaz Gráfica**: [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)
* **Imágenes**: Pillow (dependencia de CustomTkinter)

---

## <a name="-instalación-y-puesta-en-marcha"></a> 🚀 Instalación y Puesta en Marcha

Sigue estos pasos para ejecutar BiblioHub en tu sistema local.

#### **1. Prerrequisitos**

* Tener instalado **Python 3.8** o superior.
* **Ubuntu/Debian**: Instalar `tkinter` (requerido por CustomTkinter):

```bash
sudo apt update
sudo apt install python3-tk -y
```

#### **2. Clonar el Repositorio**

```bash
git clone <URL_DEL_REPOSITORIO>
cd Biblioteca
```

#### **3. Crear un Entorno Virtual (Recomendado)**

```bash
# Windows (PowerShell)
python -m venv venv
.\venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

#### **4. Instalar Dependencias**
El proyecto incluye un archivo `requirements.txt` para una fácil instalación.

```bash
pip install -r requirements.txt
```
#### **5. Inicializar la Base de Datos (Opcional)**

**🎉 NUEVO**: La base de datos se inicializa automáticamente la primera vez que ejecutas la aplicación.

Si deseas poblar la base de datos con datos de prueba, ejecuta el siguiente script:

```bash
python init_database.py
```

#### **6. Ejecutar la Aplicación**

Simplemente inicia la aplicación con:

```bash
python3 main.py
```

**Nota**: La aplicación creará automáticamente la base de datos vacía si no existe. Verás el mensaje "📊 Inicializando base de datos por primera vez..." en la consola la primera vez que ejecutes la aplicación.

---

## <a name="️-scripts-de-mantenimiento"></a> ⚙️ Scripts de Mantenimiento

El proyecto incluye scripts adicionales para tareas de desarrollo y mantenimiento:

### Scripts de Uso General

- **`init_database.py`**: **(Ejecutar una sola vez)**. Crea el archivo de base de datos (`biblioteca.db`) y lo puebla con un conjunto de datos inicial para pruebas. Es fundamental ejecutarlo antes de iniciar la aplicación por primera vez.

### Scripts de Desarrollo y Mantenimiento

- **`update_ubicaciones.py`**: **(Opcional)**. Este script recorre todos los ejemplares de la base de datos y asigna una ubicación física descriptiva (ej: "Estantería A - Nivel 1 - Pos 3") a aquellos que no la tengan. Es útil para mantener la consistencia del catálogo si se han importado datos manualmente o si se usaron versiones antiguas de la aplicación. No es necesario ejecutarlo durante el uso normal de la GUI.
- **`test_debug.py`**: Script de desarrollo utilizado para probar funciones específicas del backend sin necesidad de iniciar la interfaz gráfica.

### Scripts Obsoletos

Los siguientes scripts han sido movidos a la carpeta `scripts_obsoletos/` ya que no son necesarios en el sistema actual:

- **migrate_to_new_system.py**: Script de migración de esquema antiguo al nuevo (ya no necesario, la base de datos ya está en el nuevo formato).

---

## 📁 Estructura del Proyecto

```
Biblioteca/
├── assets/                    # Recursos visuales (imágenes, iconos)
├── database/                  # Capa de acceso a datos
│   ├── db_manager.py         # Gestor de base de datos SQLite
│   └── biblioteca.db         # Base de datos (se genera al inicializar)
├── logic/                     # Capa de lógica de negocio
│   ├── library_manager.py    # GestorBiblioteca (Facade)
│   └── models.py             # Modelos de datos (Libro, Autor, Usuario, etc.)
├── gui/                       # Capa de presentación (interfaz gráfica)
│   ├── app.py                # Aplicación principal
│   ├── frames/               # Pantallas/vistas modulares
│   └── utils/                # Utilidades (diálogos, helpers)
├── scripts_obsoletos/         # Scripts antiguos (archivados)
├── config.ini                # Configuración de la base de datos
├── requirements.txt          # Dependencias del proyecto
├── init_database.py          # Script de inicialización
└── README.md                 # Este archivo
```

---

## 📊 Requisitos Cumplidos

BiblioHub cumple con todos los requisitos especificados para el proyecto. Para más detalles sobre la implementación, consulta la sección de [Arquitectura del Proyecto](#️-arquitectura-del-proyecto).

### ✅ Requisitos Básicos (Verde)
- ✅ Crear, modificar y eliminar libros
- ✅ Crear, modificar y eliminar estanterías (solo se eliminan si están vacías)
- ✅ Prestar y devolver ejemplares de libros
- ✅ Buscar libros por código, título y autor
- ✅ Validaciones implementadas:
  - Nombres de estanterías únicos
  - Códigos de libros únicos
  - Los nombres de libros SÍ pueden repetirse
  - Control de capacidad de estanterías (máximo 150 ejemplares)
  - No se pueden guardar ejemplares en estanterías llenas

### ✅ Requisitos Intermedios (Naranja)
- ✅ Mostrar libros disponibles (vista dedicada)
- ✅ Mostrar libros prestados (vista dedicada)
- ✅ Mostrar libro más prestado (con estadísticas)
- ✅ Validación de préstamos: no se puede prestar un libro sin ejemplares disponibles
- ✅ Interfaz gráfica completa con CustomTkinter:
  - Diseño moderno con tema oscuro
  - Navegación intuitiva entre pantallas
  - Formularios con validación en tiempo real
  - Diálogos de confirmación personalizados
  - Búsqueda en tiempo real

### ✅ Requisitos Avanzados (Violeta)
- ✅ Mover libros entre estanterías:
  - Interfaz con búsqueda en tiempo real
  - Mueve el libro con TODOS sus ejemplares
  - Actualiza automáticamente las ubicaciones físicas descriptivas
  - Validación de capacidad (impide mover si no hay espacio)
- ✅ Base de datos SQLite con modelo normalizado:
  - Separación de libros, autores, géneros, estanterías y ejemplares
  - Sistema de préstamos con usuarios
  - Integridad referencial con claves foráneas
  - Transacciones para garantizar consistencia de datos

---

## 💪 Robustez y Experiencia de Usuario

BiblioHub está diseñado para ser robusto y amigable, incluso con usuarios nuevos:

### **🛡️ Características de Robustez**

- **Auto-inicialización de Base de Datos**: La aplicación detecta automáticamente si la base de datos no existe y la crea al iniciar.
- **Validación Inteligente**: 
  - Mensajes de error descriptivos y amigables en lugar de errores técnicos
  - Guías paso a paso para resolver problemas comunes
  - Advertencias preventivas antes de acciones críticas
- **Manejo de Estados Vacíos**: 
  - Pantallas informativas cuando no hay datos (ej: biblioteca vacía, sin préstamos)
  - Guías de inicio para nuevos usuarios
  - Navegación directa a las pantallas necesarias para comenzar
- **Validaciones en Tiempo Real**: 
  - Capacidad de estanterías mostrada dinámicamente
  - Prevención de errores antes de intentar guardar
  - Mensajes contextuales según el estado actual

### **🎯 Mensajes de Error Mejorados**

BiblioHub convierte errores técnicos en mensajes útiles:

- **"UNIQUE constraint failed"** → "Ya existe un libro con este código. Sugerencia: usa 'LIB001v2' o 'LIB001_nuevo'"
- **Error al buscar libros** → "No hay libros disponibles. Paso 1: Crea una estantería..."
- **Estantería llena** → "No hay espacio suficiente. Disponibles: 5, Intentando agregar: 10"

## 🎨 Interfaz de Usuario

BiblioHub cuenta con una interfaz moderna y amigable:

- **Dashboard principal** con estadísticas en tiempo real y acceso rápido a todas las funcionalidades
- **Búsqueda inteligente** con resultados instantáneos desde el menú principal
- **Gestión de libros**: Agregar, editar y eliminar con formularios completos y validación en tiempo real
- **Gestión de estanterías**: 
  - Crear nuevas estanterías con nombre y capacidad
  - Editar estanterías existentes (ventana modal con scroll)
  - Eliminar estanterías vacías con confirmación
  - Vista en tabla con información de ocupación en tiempo real
- **Mover libros**: Interfaz intuitiva con búsqueda en tiempo real y selección por pasos
- **Gestión de préstamos** con alertas visuales para vencimientos
- **Vistas de ejemplares**: Información detallada de cada copia física con su ubicación
- **Diálogos de confirmación** personalizados para acciones críticas
- **Tema oscuro moderno** con colores suaves y diseño profesional

---

## 🤝 Contribuciones

Este proyecto fue desarrollado como parte de un trabajo académico. Si deseas contribuir o reportar problemas, no dudes en crear un issue o pull request.

---

## 📄 Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.