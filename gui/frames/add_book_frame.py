import customtkinter as ctk
from tkinter import messagebox
from typing import TYPE_CHECKING
from .base_frame import BaseFrame

if TYPE_CHECKING:
    from gui.app import App
    from logic.library_manager import GestorBiblioteca

class AddBookFrame(BaseFrame):
    def __init__(self, master: 'App', gestor: 'GestorBiblioteca'):
        super().__init__(master, gestor)
        
        # Crear la interfaz
        self.setup_interface()

    def setup_interface(self):
        """Configura la interfaz del formulario de agregar libro."""
        # Header
        self.create_header("📚 Agregar Nuevo Libro", "Completa el formulario para agregar un nuevo libro al sistema")
        
        # --- Frame contenedor para el formulario ---
        form_frame = ctk.CTkFrame(self.content_frame, fg_color=self.colors['white'], corner_radius=15)
        form_frame.pack(padx=40, pady=10, fill="both", expand=True)

        form_frame.grid_columnconfigure(0, weight=0)
        form_frame.grid_columnconfigure(1, weight=1)


        self.estanterias = self.gestor.get_todas_estanterias()
        self.selected_shelf_id = ctk.StringVar()

        # Información del libro
        ctk.CTkLabel(form_frame, text="📖 INFORMACIÓN DEL LIBRO", font=("Arial", 14, "bold"), text_color="#4158D0").grid(row=0, column=0, columnspan=2, pady=(10, 15), sticky="w")

        ctk.CTkLabel(form_frame, text="Código *").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.codigo_entry = ctk.CTkEntry(form_frame, placeholder_text="Ej: LIB001", width=350)
        self.codigo_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        ctk.CTkLabel(form_frame, text="Título *").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.titulo_entry = ctk.CTkEntry(form_frame, placeholder_text="Ej: Cien Años de Soledad")
        self.titulo_entry.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

        ctk.CTkLabel(form_frame, text="ISBN").grid(row=3, column=0, padx=10, pady=5, sticky="e")
        self.isbn_entry = ctk.CTkEntry(form_frame, placeholder_text="Ej: 978-84-376-0494-7")
        self.isbn_entry.grid(row=3, column=1, padx=10, pady=5, sticky="ew")

        ctk.CTkLabel(form_frame, text="Editorial").grid(row=4, column=0, padx=10, pady=5, sticky="e")
        self.editorial_entry = ctk.CTkEntry(form_frame, placeholder_text="Ej: Sudamericana")
        self.editorial_entry.grid(row=4, column=1, padx=10, pady=5, sticky="ew")

        ctk.CTkLabel(form_frame, text="Año *").grid(row=5, column=0, padx=10, pady=5, sticky="e")
        self.anio_entry = ctk.CTkEntry(form_frame, placeholder_text="Ej: 1967")
        self.anio_entry.grid(row=5, column=1, padx=10, pady=5, sticky="ew")

        # Información del autor
        ctk.CTkLabel(form_frame, text="👨‍💼 INFORMACIÓN DEL AUTOR", font=("Arial", 14, "bold"), text_color="#4158D0").grid(row=6, column=0, columnspan=2, pady=(20, 15), sticky="w")

        ctk.CTkLabel(form_frame, text="Nombre *").grid(row=7, column=0, padx=10, pady=5, sticky="e")
        self.autor_nombre_entry = ctk.CTkEntry(form_frame, placeholder_text="Ej: Gabriel")
        self.autor_nombre_entry.grid(row=7, column=1, padx=10, pady=5, sticky="ew")

        ctk.CTkLabel(form_frame, text="Apellido *").grid(row=8, column=0, padx=10, pady=5, sticky="e")
        self.autor_apellido_entry = ctk.CTkEntry(form_frame, placeholder_text="Ej: García Márquez")
        self.autor_apellido_entry.grid(row=8, column=1, padx=10, pady=5, sticky="ew")

        # Categorización
        ctk.CTkLabel(form_frame, text="🎭 CATEGORIZACIÓN", font=("Arial", 14, "bold"), text_color="#4158D0").grid(row=9, column=0, columnspan=2, pady=(20, 15), sticky="w")

        ctk.CTkLabel(form_frame, text="Género").grid(row=10, column=0, padx=10, pady=5, sticky="e")
        self.genero_entry = ctk.CTkEntry(form_frame, placeholder_text="Ej: Realismo Mágico")
        self.genero_entry.grid(row=10, column=1, padx=10, pady=5, sticky="ew")

        # Ubicación física
        ctk.CTkLabel(form_frame, text="📍 UBICACIÓN FÍSICA", font=("Arial", 14, "bold"), text_color="#4158D0").grid(row=11, column=0, columnspan=2, pady=(20, 15), sticky="w")

        ctk.CTkLabel(form_frame, text="Estantería *").grid(row=12, column=0, padx=10, pady=5, sticky="e")
        shelf_names = [e.nombre for e in self.estanterias] if self.estanterias else ["No hay estanterías"]
        self.shelf_menu = ctk.CTkOptionMenu(form_frame, variable=self.selected_shelf_id, values=shelf_names)
        self.shelf_menu.grid(row=12, column=1, padx=10, pady=5, sticky="ew")

        ctk.CTkLabel(form_frame, text="Cantidad de Ejemplares *").grid(row=13, column=0, padx=10, pady=5, sticky="e")
        self.cantidad_entry = ctk.CTkEntry(form_frame, placeholder_text="Ej: 3")
        self.cantidad_entry.grid(row=13, column=1, padx=10, pady=5, sticky="ew")

        # Información adicional
        info_frame = ctk.CTkFrame(form_frame, fg_color="blue")
        info_frame.grid(row=14, column=0, columnspan=2, pady=15, padx=10, sticky="ew")
        
        info_text = "ℹ️ Los campos marcados con * son obligatorios.\n"
        info_text += "Se crearán automáticamente los ejemplares individuales para el control de préstamos."
        ctk.CTkLabel(info_frame, text=info_text, text_color="white", font=("Arial", 10)).pack(pady=8)

        # --- Botones de acción ---
        button_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        button_frame.pack(fill="x", pady=20)
        
        buttons_container = ctk.CTkFrame(button_frame, fg_color="transparent")
        buttons_container.pack()
        
        ctk.CTkButton(buttons_container, text="💾 Guardar Libro", command=self.guardar_libro, 
                     width=150, height=40, fg_color=self.colors['success']).pack(side="left", padx=10)
        ctk.CTkButton(buttons_container, text="🗑️ Limpiar", fg_color=self.colors['warning'], 
                     command=self.limpiar_formulario, width=120, height=40).pack(side="left", padx=10)
        
        # Botón volver usando la función de la clase base
        self.create_back_button()

    def guardar_libro(self):
        try:
            # Recolección de datos obligatorios
            codigo = self.codigo_entry.get().strip()
            titulo = self.titulo_entry.get().strip()
            autor_nombre = self.autor_nombre_entry.get().strip()
            autor_apellido = self.autor_apellido_entry.get().strip()
            anio = int(self.anio_entry.get())
            cantidad = int(self.cantidad_entry.get())

            # Datos opcionales
            isbn = self.isbn_entry.get().strip() if self.isbn_entry.get().strip() else None
            editorial = self.editorial_entry.get().strip() if self.editorial_entry.get().strip() else None
            genero_nombre = self.genero_entry.get().strip() if self.genero_entry.get().strip() else None

            # Validaciones básicas
            if not all([codigo, titulo, autor_nombre, autor_apellido]):
                raise ValueError("Los campos marcados con * son obligatorios")

            # Obtener ID de la estantería seleccionada
            selected_shelf_name = self.selected_shelf_id.get()
            shelf_id = next((e.id for e in self.estanterias if e.nombre == selected_shelf_name), None)

            if shelf_id is None:
                raise ValueError("Debe seleccionar una estantería válida.")

            # Usar la nueva función mejorada
            libro_id = self.gestor.agregar_libro_simple(
                codigo=codigo,
                titulo=titulo,
                autor_nombre=autor_nombre,
                autor_apellido=autor_apellido,
                anio=anio,
                cantidad_ejemplares=cantidad,
                estanteria_id=shelf_id,
                genero_nombre=genero_nombre,
                isbn=isbn,
                editorial=editorial
            )

            messagebox.showinfo("Éxito", 
                               f"✅ Libro '{titulo}' agregado correctamente!\n\n"
                               f"📖 Libro ID: {libro_id}\n"
                               f"👨‍💼 Autor: {autor_nombre} {autor_apellido}\n"
                               f"📦 Ejemplares creados: {cantidad}\n"
                               f"📍 Estantería: {selected_shelf_name}")
            
            self.limpiar_formulario()

        except (ValueError, TypeError) as ve:
            messagebox.showerror("Error de Entrada", f"❌ Dato inválido: {ve}")
        except Exception as e:
            messagebox.showerror("Error", f"❌ Error al guardar: {str(e)}")

    def limpiar_formulario(self):
        """Limpia todos los campos del formulario."""
        self.codigo_entry.delete(0, 'end')
        self.titulo_entry.delete(0, 'end')
        self.isbn_entry.delete(0, 'end')
        self.editorial_entry.delete(0, 'end')
        self.anio_entry.delete(0, 'end')
        self.autor_nombre_entry.delete(0, 'end')
        self.autor_apellido_entry.delete(0, 'end')
        self.genero_entry.delete(0, 'end')
        self.cantidad_entry.delete(0, 'end')
        self.selected_shelf_id.set("")