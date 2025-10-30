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
python main.py
```

## ⚙️ Scripts de Mantenimiento

El proyecto incluye scripts adicionales en la raíz para tareas de desarrollo y mantenimiento:

- **update_ubicaciones.py**: Genera y asigna ubicaciones físicas descriptivas a todos los ejemplares de la base.
- **migrate_to_new_system.py**: Migra una base antigua (por cantidad de libros) a la nueva estructura (por ejemplares individuales).
- **test_debug.py**: Permite probar y depurar funciones específicas sin levantar la interfaz gráfica.