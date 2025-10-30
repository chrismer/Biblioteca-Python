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

* **Gestión de Libros**: Creación, edición y eliminación de libros con información detallada (ISBN, editorial, año, etc.).
* **Gestión de Ejemplares**: El sistema distingue entre el "libro" como obra y el "ejemplar" como copia física, permitiendo un seguimiento individual de cada copia.
* **Administración de Estanterías**: Creación, modificación y eliminación de estanterías, con control de capacidad para evitar la sobrecarga.
* **Movimiento de Libros**: Interfaz dedicada para mover un libro y todos sus ejemplares de una estantería a otra, actualizando automáticamente sus ubicaciones físicas.

#### **🔄 Sistema de Préstamos Profesional**

* **Gestión de Préstamos**: Módulo completo para crear nuevos préstamos, asociando un usuario a un ejemplar específico.
* **Control de Activos y Vencidos**: Vistas separadas para monitorear los préstamos activos y aquellos que ya han vencido, con alertas visuales.
* **Devoluciones y Renovaciones**: Funcionalidad para registrar devoluciones y renovar préstamos por un período adicional.

#### **👥 Administración de Usuarios**

* **CRUD de Usuarios**: Sistema para agregar, listar, buscar y gestionar la información de los usuarios de la biblioteca.
* **Historial de Préstamos por Usuario**: Acceso rápido al historial de préstamos de cada usuario.

#### **🔍 Búsqueda y Reportes**

* **Búsqueda Inteligente**: Un potente motor de búsqueda que encuentra libros por título, autor, código o ISBN, priorizando las coincidencias exactas.
* **Dashboard de Estadísticas**: La pantalla principal ofrece un resumen en tiempo real del estado de la biblioteca (total de libros, ejemplares disponibles, préstamos activos y vencidos).

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

### Scripts Activos

- **init_database.py**: Inicializa la base de datos y la puebla con datos de prueba (autores, géneros, estanterías, libros, ejemplares y usuarios).
- **update_ubicaciones.py**: Genera y asigna ubicaciones físicas descriptivas a todos los ejemplares que no tienen una ubicación asignada.
- **test_debug.py**: Script de pruebas para depurar funciones específicas sin levantar la interfaz gráfica.

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

BiblioHub cumple con todos los requisitos especificados para el proyecto:

### ✅ Requisitos Básicos (Verde)
- Crear, modificar y eliminar libros
- Crear, modificar y eliminar estanterías
- Prestar y devolver ejemplares de libros
- Buscar libros por código, título y autor
- Validaciones: estanterías únicas, códigos únicos, control de capacidad

### ✅ Requisitos Intermedios (Naranja)
- Mostrar libros disponibles y prestados
- Mostrar libro más prestado
- Validación de préstamos (no prestar sin ejemplares disponibles)
- Interfaz gráfica completa con CustomTkinter

### ✅ Requisitos Avanzados (Violeta)
- Mover libros entre estanterías (con actualización de ubicaciones físicas)
- Base de datos SQLite con modelo normalizado

---

## 🎨 Capturas de Pantalla

BiblioHub cuenta con una interfaz moderna y amigable:

- **Dashboard principal** con estadísticas en tiempo real
- **Búsqueda inteligente** con resultados instantáneos
- **Gestión de préstamos** con alertas visuales para vencimientos
- **Formularios intuitivos** con validación en tiempo real
- **Tema oscuro moderno** con colores suaves y diseño profesional

---

## 🤝 Contribuciones

Este proyecto fue desarrollado como parte de un trabajo académico. Si deseas contribuir o reportar problemas, no dudes en crear un issue o pull request.

---

## 📄 Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.