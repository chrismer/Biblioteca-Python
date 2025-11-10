import customtkinter as ctk
from tkinter import messagebox
from typing import TYPE_CHECKING, Optional
from .base_frame import BaseFrame
from logic.models import Libro

if TYPE_CHECKING:
    from gui.app import App
    from logic.library_manager import GestorBiblioteca

class BookFormFrame(BaseFrame):
    def __init__(self, master: 'App', gestor: 'GestorBiblioteca', libro: Optional[Libro] = None):
        super().__init__(master, gestor)
        self.libro = libro
        self.is_edit_mode = self.libro is not None

        self.setup_interface()
        if self.is_edit_mode:
            self.load_book_data()

    def setup_interface(self):
        """Configura la interfaz del formulario de libro."""
        header_title = "✏️ Editar Libro" if self.is_edit_mode else "📚 Agregar Nuevo Libro"
        header_subtitle = "Actualiza la información del libro" if self.is_edit_mode else "Completa el formulario para agregar un nuevo libro"
        self.create_header(header_title, header_subtitle)

        form_frame = ctk.CTkFrame(self.content_frame, fg_color=self.colors['white'], corner_radius=15)
        form_frame.pack(padx=40, pady=10, fill="both", expand=True)
        form_frame.grid_columnconfigure(1, weight=1)

        self.estanterias = self.gestor.get_todas_estanterias()
        self.selected_shelf_id = ctk.StringVar()
        self.capacidad_info_label = None  # Para mostrar capacidad disponible

        # --- Campos del formulario ---
        ctk.CTkLabel(form_frame, text="Código *").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.codigo_entry = ctk.CTkEntry(form_frame, placeholder_text="Ej: LIB001", width=350)
        self.codigo_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        ctk.CTkLabel(form_frame, text="Título *").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.titulo_entry = ctk.CTkEntry(form_frame, placeholder_text="Ej: Cien Años de Soledad")
        self.titulo_entry.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

        ctk.CTkLabel(form_frame, text="Nombre Autor *").grid(row=3, column=0, padx=10, pady=5, sticky="e")
        self.autor_nombre_entry = ctk.CTkEntry(form_frame, placeholder_text="Ej: Gabriel")
        self.autor_nombre_entry.grid(row=3, column=1, padx=10, pady=5, sticky="ew")

        ctk.CTkLabel(form_frame, text="Apellido Autor *").grid(row=4, column=0, padx=10, pady=5, sticky="e")
        self.autor_apellido_entry = ctk.CTkEntry(form_frame, placeholder_text="Ej: García Márquez")
        self.autor_apellido_entry.grid(row=4, column=1, padx=10, pady=5, sticky="ew")

        ctk.CTkLabel(form_frame, text="Año *").grid(row=5, column=0, padx=10, pady=5, sticky="e")
        self.anio_entry = ctk.CTkEntry(form_frame, placeholder_text="Ej: 1967")
        self.anio_entry.grid(row=5, column=1, padx=10, pady=5, sticky="ew")

        # Estanterías
        ctk.CTkLabel(form_frame, text="Estanteria *").grid(row=6, column=0, padx=10, pady=5, sticky="e")
        shelf_names = [e.nombre for e in self.estanterias] if self.estanterias else ["No hay estanterías"]
        self.shelf_menu = ctk.CTkOptionMenu(
            form_frame, 
            variable=self.selected_shelf_id, 
            values=shelf_names,
            command=self.actualizar_capacidad_disponible  # Callback cuando cambia
        )
        self.shelf_menu.grid(row=6, column=1, padx=10, pady=5, sticky="ew")

        # --- Campos que solo se muestran en modo 'Añadir' ---
        if not self.is_edit_mode:
            # Label informativo de capacidad debajo del dropdown
            self.capacidad_info_label = ctk.CTkLabel(
                form_frame, 
                text="", 
                font=("Segoe UI", 10, "italic"),
                text_color=self.colors['warning'],
                anchor="w"
            )
            self.capacidad_info_label.grid(row=7, column=1, padx=10, pady=(0, 10), sticky="ew")
            
            ctk.CTkLabel(form_frame, text="Cantidad de Ejemplares *").grid(row=8, column=0, padx=10, pady=5, sticky="e")
            self.cantidad_entry = ctk.CTkEntry(form_frame, placeholder_text="Ej: 3")
            self.cantidad_entry.grid(row=8, column=1, padx=10, pady=5, sticky="ew")
            
            # Actualizar capacidad disponible al iniciar
            if self.estanterias:
                self.selected_shelf_id.set(self.estanterias[0].nombre)
                self.actualizar_capacidad_disponible(self.estanterias[0].nombre)

        # --- Botones de acción ---
        button_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        button_frame.pack(fill="x", pady=20)

        ctk.CTkButton(button_frame, text="💾 Guardar", command=self.guardar, width=150, height=40).pack(pady=10)
        self.create_back_button()

    def load_book_data(self):
        """Carga los datos del libro en el formulario en modo edición."""
        if not self.libro:
            return

        self.codigo_entry.insert(0, self.libro.codigo)
        self.codigo_entry.configure(state="disabled") # El código no se puede editar
        self.titulo_entry.insert(0, self.libro.titulo)

        if self.libro.autor:
            self.autor_nombre_entry.insert(0, self.libro.autor.nombre)
            self.autor_apellido_entry.insert(0, self.libro.autor.apellido)

        self.anio_entry.insert(0, str(self.libro.anio))

        # Seleccionar la estantería actual
        current_shelf = next((e for e in self.estanterias if e.id == self.libro.estanteria_id), None)
        if current_shelf:
            self.selected_shelf_id.set(current_shelf.nombre)

    def guardar(self):
        try:
            if self.is_edit_mode:
                self.actualizar_libro()
            else:
                self.crear_libro()
        except (ValueError, TypeError) as ve:
            messagebox.showerror("Error de Entrada", f"❌ Dato inválido: {ve}")
        except Exception as e:
            messagebox.showerror("Error", f"❌ Error al guardar: {str(e)}")

    def crear_libro(self):
        # Lógica de `add_book_frame`
        codigo = self.codigo_entry.get().strip()
        titulo = self.titulo_entry.get().strip()
        autor_nombre = self.autor_nombre_entry.get().strip()
        autor_apellido = self.autor_apellido_entry.get().strip()
        anio = int(self.anio_entry.get())
        cantidad = int(self.cantidad_entry.get())

        selected_shelf_name = self.selected_shelf_id.get()
        shelf_id = next((e.id for e in self.estanterias if e.nombre == selected_shelf_name), None)

        if not all([codigo, titulo, autor_nombre, autor_apellido, anio, cantidad, shelf_id]):
            raise ValueError("Todos los campos con * son obligatorios.")
        
        # Validación adicional de capacidad
        estanteria = next((e for e in self.estanterias if e.id == shelf_id), None)
        if estanteria:
            ocupados = self.gestor.get_count_ejemplares_en_estanteria(shelf_id)
            disponibles = estanteria.capacidad - ocupados
            
            if cantidad > disponibles:
                raise ValueError(
                    f"No hay suficiente espacio en la estantería '{estanteria.nombre}'.\n\n"
                    f"📊 Espacios disponibles: {disponibles}\n"
                    f"📦 Intentando agregar: {cantidad}\n\n"
                    f"Por favor, reduce la cantidad de ejemplares o elige otra estantería."
                )

        self.gestor.agregar_libro_simple(
            codigo=codigo, titulo=titulo, autor_nombre=autor_nombre, autor_apellido=autor_apellido,
            anio=anio, cantidad_ejemplares=cantidad, estanteria_id=shelf_id
        )
        messagebox.showinfo("Éxito", f"Libro '{titulo}' agregado correctamente.")
        self._go_to_main_frame()

    def actualizar_libro(self):
        # Lógica de `edit_book_frame`
        titulo = self.titulo_entry.get().strip()
        autor_nombre = self.autor_nombre_entry.get().strip()
        autor_apellido = self.autor_apellido_entry.get().strip()
        anio = int(self.anio_entry.get())

        selected_shelf_name = self.selected_shelf_id.get()
        shelf_id = next((e.id for e in self.estanterias if e.nombre == selected_shelf_name), None)

        if not all([titulo, autor_nombre, autor_apellido, anio, shelf_id]):
            raise ValueError("Todos los campos con * son obligatorios.")

        datos_nuevos = {
            "titulo": titulo,
            "autor_nombre": autor_nombre,
            "autor_apellido": autor_apellido,
            "anio": anio,
            "estanteria_id": shelf_id
        }
        self.gestor.modificar_libro_completo(self.libro.id, datos_nuevos)
        messagebox.showinfo("Éxito", f"Libro '{titulo}' actualizado correctamente.")
        self._go_to_main_frame()

    def actualizar_capacidad_disponible(self, shelf_name: str):
        """Actualiza el label con la capacidad disponible de la estantería seleccionada."""
        if self.is_edit_mode or not self.capacidad_info_label:
            return
        
        try:
            # Buscar la estantería seleccionada
            estanteria = next((e for e in self.estanterias if e.nombre == shelf_name), None)
            
            if not estanteria:
                self.capacidad_info_label.configure(text="")
                return
            
            # Obtener ejemplares ocupados
            ocupados = self.gestor.get_count_ejemplares_en_estanteria(estanteria.id)
            disponibles = estanteria.capacidad - ocupados
            
            # Actualizar label con información
            if disponibles > 0:
                self.capacidad_info_label.configure(
                    text=f"📊 Capacidad disponible: {disponibles} ejemplares (máximo a agregar)",
                    text_color=self.colors['success']
                )
            else:
                self.capacidad_info_label.configure(
                    text=f"⚠️ Estantería llena (0 espacios disponibles)",
                    text_color=self.colors['danger']
                )
        except Exception as e:
            self.capacidad_info_label.configure(text="")

    def _go_to_main_frame(self):
        """Navega al MainFrame, usando una importación local para evitar ciclos."""
        from .main_frame import MainFrame
        self.master.switch_frame(MainFrame)
