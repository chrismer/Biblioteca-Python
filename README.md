# BiblioHub - Sistema de Gestión Bibliotecaria

![BiblioHub Logo](assets/bg-bibliohub.png)

**BiblioHub** es una aplicación de escritorio moderna y robusta para la gestión integral de bibliotecas. Desarrollada en Python con una interfaz gráfica de usuario (GUI) construida sobre CustomTkinter, ofrece una solución completa para administrar el inventario de libros, los usuarios y el ciclo de vida de los préstamos.

---

## 📜 Índice

* [🌟 Características Principales](#-características-principales)
* [🏗️ Arquitectura del Proyecto](#️-arquitectura-del-proyecto)
* [🛠️ Tecnologías Utilizadas](#️-tecnologías-utilizadas)
* [🚀 Instalación y Puesta en Marcha](#-instalación-y-puesta-en-marcha)
* [⚙️ Scripts de Mantenimiento](#️-scripts-de-mantenimiento)

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
#### **5. Inicializar la Base de Datos**
Para crear la base de datos y poblarla con datos de prueba, ejecuta el siguiente script una sola vez:

```bash
python init_database.py
```
#### **6. Ejecutar la Aplicación**
Una vez instaladas las dependencias y creada la base de datos, inicia la aplicación con:

```bash
python3 main.py
```

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