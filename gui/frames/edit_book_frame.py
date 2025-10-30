import customtkinter as ctk
from tkinter import messagebox
from typing import TYPE_CHECKING, Optional
from logic.models import Libro, Autor, Genero
from gui.utils.dialogs import confirmar

if TYPE_CHECKING:
    from gui.app import App
    from logic.library_manager import GestorBiblioteca

class EditBookFrame(ctk.CTkFrame):
    def __init__(self, master: 'App', gestor: 'GestorBiblioteca', libro: Libro):
        super().__init__(master)
        self.master = master
        self.gestor = gestor
        self.libro = libro
        
        # Crear ventana principal con scroll
        self.setup_scrollable_window()
        
        # Inicializar variables de entrada
        self.init_variables()
        
        # Crear la interfaz
        self.create_interface()
        
        # Cargar datos del libro
        self.load_book_data()

    def setup_scrollable_window(self):
        """Configura una ventana con scroll vertical."""
        # Frame principal scrollable
        self.main_scroll = ctk.CTkScrollableFrame(self, height=600)
        self.main_scroll.pack(fill="both", expand=True, padx=20, pady=20)
        
    def init_variables(self):
        """Inicializa las variables de entrada."""
        self.codigo_var = ctk.StringVar()
        self.titulo_var = ctk.StringVar()
        self.isbn_var = ctk.StringVar()
        self.anio_var = ctk.StringVar()
        self.editorial_var = ctk.StringVar()
        self.numero_paginas_var = ctk.StringVar()
        self.descripcion_var = ctk.StringVar()
        self.autor_nombre_var = ctk.StringVar()
        self.autor_apellido_var = ctk.StringVar()
        self.genero_var = ctk.StringVar()
        self.estanteria_var = ctk.StringVar()

    def create_interface(self):
        """Crea la interfaz de usuario."""
        # Título
        title_frame = ctk.CTkFrame(self.main_scroll, fg_color="darkblue")
        title_frame.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(title_frame, 
                    text=f"✏️ Editar Libro: {self.libro.titulo}", 
                    font=("Arial", 20, "bold"), 
                    text_color="white").pack(pady=15)

        # Información del libro actual
        info_frame = ctk.CTkFrame(self.main_scroll, fg_color="#F28705")
        info_frame.pack(fill="x", pady=(0, 20))
        
        autor_actual = self.libro.autor.nombre_completo if self.libro.autor else "Sin autor"
        
        # Obtener cantidad de ejemplares de forma segura
        try:
            if hasattr(self.libro, 'ejemplares') and self.libro.ejemplares:
                cantidad_ejemplares = len(self.libro.ejemplares)
            else:
                # Fallback: obtener ejemplares de la base de datos
                ejemplares = self.gestor.get_ejemplares_por_libro(self.libro.id if hasattr(self.libro, 'id') else None)
                cantidad_ejemplares = len(ejemplares) if ejemplares else 0
        except:
            cantidad_ejemplares = 0
            
        info_text = f"📚 Editando: {self.libro.codigo} | 👨‍💼 Autor actual: {autor_actual} | 📊 {cantidad_ejemplares} ejemplares"
        ctk.CTkLabel(info_frame, text=info_text, text_color="white").pack(pady=10)

        # Formulario en secciones
        self.create_basic_info_section()
        self.create_author_section()
        self.create_publication_section()
        self.create_description_section()
        self.create_location_section()
        self.create_action_buttons()

    def create_basic_info_section(self):
        """Crea la sección de información básica."""
        section_frame = ctk.CTkFrame(self.main_scroll)
        section_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(section_frame, text="📖 INFORMACIÓN BÁSICA", 
                    font=("Arial", 14, "bold")).pack(pady=10)

        # Grid para campos básicos
        grid_frame = ctk.CTkFrame(section_frame, fg_color="transparent")
        grid_frame.pack(fill="x", padx=20, pady=10)

        # Código (solo lectura)
        ctk.CTkLabel(grid_frame, text="Código *").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        codigo_entry = ctk.CTkEntry(grid_frame, textvariable=self.codigo_var, state="disabled", width=200)
        codigo_entry.grid(row=0, column=1, padx=10, pady=5)

        # Título
        ctk.CTkLabel(grid_frame, text="Título *").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.titulo_entry = ctk.CTkEntry(grid_frame, textvariable=self.titulo_var, width=400)
        self.titulo_entry.grid(row=1, column=1, columnspan=2, padx=10, pady=5)

        # ISBN
        ctk.CTkLabel(grid_frame, text="ISBN").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        self.isbn_entry = ctk.CTkEntry(grid_frame, textvariable=self.isbn_var, width=200)
        self.isbn_entry.grid(row=2, column=1, padx=10, pady=5)

    def create_author_section(self):
        """Crea la sección de autor."""
        section_frame = ctk.CTkFrame(self.main_scroll)
        section_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(section_frame, text="👨‍💼 INFORMACIÓN DEL AUTOR", 
                    font=("Arial", 14, "bold")).pack(pady=10)

        grid_frame = ctk.CTkFrame(section_frame, fg_color="transparent")
        grid_frame.pack(fill="x", padx=20, pady=10)

        # Nombre del autor
        ctk.CTkLabel(grid_frame, text="Nombre *").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.autor_nombre_entry = ctk.CTkEntry(grid_frame, textvariable=self.autor_nombre_var, width=200)
        self.autor_nombre_entry.grid(row=0, column=1, padx=10, pady=5)

        # Apellido del autor
        ctk.CTkLabel(grid_frame, text="Apellido *").grid(row=0, column=2, sticky="w", padx=10, pady=5)
        self.autor_apellido_entry = ctk.CTkEntry(grid_frame, textvariable=self.autor_apellido_var, width=200)
        self.autor_apellido_entry.grid(row=0, column=3, padx=10, pady=5)

    def create_publication_section(self):
        """Crea la sección de publicación."""
        section_frame = ctk.CTkFrame(self.main_scroll)
        section_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(section_frame, text="📅 INFORMACIÓN DE PUBLICACIÓN", 
                    font=("Arial", 14, "bold")).pack(pady=10)

        grid_frame = ctk.CTkFrame(section_frame, fg_color="transparent")
        grid_frame.pack(fill="x", padx=20, pady=10)

        # Año
        ctk.CTkLabel(grid_frame, text="Año *").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.anio_entry = ctk.CTkEntry(grid_frame, textvariable=self.anio_var, width=100)
        self.anio_entry.grid(row=0, column=1, padx=10, pady=5)

        # Editorial
        ctk.CTkLabel(grid_frame, text="Editorial").grid(row=0, column=2, sticky="w", padx=10, pady=5)
        self.editorial_entry = ctk.CTkEntry(grid_frame, textvariable=self.editorial_var, width=200)
        self.editorial_entry.grid(row=0, column=3, padx=10, pady=5)

        # Número de páginas
        ctk.CTkLabel(grid_frame, text="Páginas").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.paginas_entry = ctk.CTkEntry(grid_frame, textvariable=self.numero_paginas_var, width=100)
        self.paginas_entry.grid(row=1, column=1, padx=10, pady=5)

        # Género
        ctk.CTkLabel(grid_frame, text="Género").grid(row=1, column=2, sticky="w", padx=10, pady=5)
        try:
            generos = self.gestor.get_todos_generos()
            genero_names = [g.nombre for g in generos] + ["Otro (especificar)"]
            self.genero_combo = ctk.CTkComboBox(grid_frame, values=genero_names, width=200, variable=self.genero_var)
            self.genero_combo.grid(row=1, column=3, padx=10, pady=5)
        except:
            self.genero_combo = ctk.CTkEntry(grid_frame, textvariable=self.genero_var, width=200)
            self.genero_combo.grid(row=1, column=3, padx=10, pady=5)

    def create_description_section(self):
        """Crea la sección de descripción."""
        section_frame = ctk.CTkFrame(self.main_scroll)
        section_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(section_frame, text="📝 DESCRIPCIÓN", 
                    font=("Arial", 14, "bold")).pack(pady=10)

        # Descripción
        ctk.CTkLabel(section_frame, text="Descripción del libro:").pack(anchor="w", padx=20)
        self.descripcion_text = ctk.CTkTextbox(section_frame, height=100, width=600)
        self.descripcion_text.pack(padx=20, pady=10, fill="x")

    def create_location_section(self):
        """Crea la sección de ubicación."""
        section_frame = ctk.CTkFrame(self.main_scroll)
        section_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(section_frame, text="📍 UBICACIÓN", 
                    font=("Arial", 14, "bold")).pack(pady=10)

        grid_frame = ctk.CTkFrame(section_frame, fg_color="transparent")
        grid_frame.pack(fill="x", padx=20, pady=10)

        # Estantería
        ctk.CTkLabel(grid_frame, text="Estantería *").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        try:
            estanterias = self.gestor.get_todas_estanterias()
            estanteria_names = [f"{e.id} - {e.nombre}" for e in estanterias]
            self.estanteria_combo = ctk.CTkComboBox(grid_frame, values=estanteria_names, width=300, variable=self.estanteria_var)
            self.estanteria_combo.grid(row=0, column=1, padx=10, pady=5)
        except:
            self.estanteria_combo = ctk.CTkEntry(grid_frame, textvariable=self.estanteria_var, width=300)
            self.estanteria_combo.grid(row=0, column=1, padx=10, pady=5)

        # Información de ejemplares
        info_ejemplares = ctk.CTkFrame(grid_frame, fg_color="#002333")
        info_ejemplares.grid(row=1, column=0, columnspan=2, pady=10, sticky="ew")
        
        # Obtener cantidad de ejemplares de forma segura
        try:
            if hasattr(self.libro, 'ejemplares') and self.libro.ejemplares:
                cantidad_ejemplares = len(self.libro.ejemplares)
            else:
                ejemplares = self.gestor.get_ejemplares_por_libro(self.libro.id if hasattr(self.libro, 'id') else None)
                cantidad_ejemplares = len(ejemplares) if ejemplares else 0
        except:
            cantidad_ejemplares = 0
            
        ctk.CTkLabel(info_ejemplares, 
                    text=f"📦 Este libro tiene {cantidad_ejemplares} ejemplares. Cambiar la estantería moverá TODOS los ejemplares.", 
                    text_color="white").pack(pady=5)

    def create_action_buttons(self):
        """Crea los botones de acción."""
        buttons_frame = ctk.CTkFrame(self.main_scroll, fg_color="transparent")
        buttons_frame.pack(fill="x", pady=20)

        # Botones centrados
        center_frame = ctk.CTkFrame(buttons_frame, fg_color="transparent")
        center_frame.pack()

        ctk.CTkButton(center_frame, text="💾 Guardar Cambios", width=150, height=40,
                     fg_color="#267365", hover_color="darkgreen",
                     command=self.guardar_cambios).pack(side="left", padx=10)

        ctk.CTkButton(center_frame, text="🚫 Cancelar", width=150, height=40,
                     fg_color="#F23030", hover_color="darkred",
                     command=self.cancelar).pack(side="left", padx=10)

        ctk.CTkButton(center_frame, text="🔄 Restaurar", width=150, height=40,
                     fg_color="#F28705", hover_color="darkorange",
                     command=self.load_book_data).pack(side="left", padx=10)

    def load_book_data(self):
        """Carga los datos actuales del libro en el formulario."""
        try:
            # Datos básicos
            self.codigo_var.set(self.libro.codigo)
            self.titulo_var.set(self.libro.titulo)
            self.isbn_var.set(self.libro.isbn or "")
            self.anio_var.set(str(self.libro.anio))
            self.editorial_var.set(self.libro.editorial or "")
            self.numero_paginas_var.set(str(self.libro.numero_paginas) if self.libro.numero_paginas else "")
            
            # Descripción
            self.descripcion_text.delete("1.0", "end")
            if self.libro.descripcion:
                self.descripcion_text.insert("1.0", self.libro.descripcion)
            
            # Autor
            if self.libro.autor:
                self.autor_nombre_var.set(self.libro.autor.nombre)
                self.autor_apellido_var.set(self.libro.autor.apellido)
            
            # Género
            if self.libro.genero:
                self.genero_var.set(self.libro.genero.nombre)
            
            # Estantería
            estanteria_actual = f"{self.libro.estanteria_id} - "
            try:
                estanteria_obj = self.gestor.get_estanteria(self.libro.estanteria_id)
                if estanteria_obj:
                    estanteria_actual += estanteria_obj.nombre
                    self.estanteria_var.set(estanteria_actual)
            except:
                pass

        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar datos del libro: {str(e)}")

    def guardar_cambios(self):
        """Guarda los cambios realizados al libro."""
        try:
            # Validaciones básicas
            if not self.titulo_var.get().strip():
                messagebox.showerror("Error", "El título es obligatorio")
                return
            
            if not self.autor_nombre_var.get().strip() or not self.autor_apellido_var.get().strip():
                messagebox.showerror("Error", "Nombre y apellido del autor son obligatorios")
                return
            
            try:
                anio = int(self.anio_var.get())
                if anio < 1000 or anio > 2100:
                    raise ValueError()
            except ValueError:
                messagebox.showerror("Error", "Año debe ser un número válido entre 1000 y 2100")
                return

            # Obtener estantería ID
            estanteria_str = self.estanteria_var.get()
            try:
                estanteria_id = int(estanteria_str.split(" - ")[0])
            except:
                messagebox.showerror("Error", "Seleccione una estantería válida")
                return

            # Preparar datos para actualización
            cambios = {
                'titulo': self.titulo_var.get().strip(),
                'isbn': self.isbn_var.get().strip() or None,
                'anio': anio,
                'editorial': self.editorial_var.get().strip() or None,
                'numero_paginas': int(self.numero_paginas_var.get()) if self.numero_paginas_var.get().strip() else None,
                'descripcion': self.descripcion_text.get("1.0", "end").strip() or None,
                'autor_nombre': self.autor_nombre_var.get().strip(),
                'autor_apellido': self.autor_apellido_var.get().strip(),
                'genero': self.genero_var.get().strip() if self.genero_var.get().strip() else None,
                'estanteria_id': estanteria_id
            }

            # Confirmar cambios
            if confirmar("Confirmar Cambios", 
                        f"¿Está seguro de guardar los cambios en '{self.libro.titulo}'?\n\n"
                        f"Esto actualizará la información del libro y todos sus ejemplares.", 
                        parent=self):
                
                # Aquí llamaríamos a la función de actualización
                self.gestor.modificar_libro_completo(self.libro.id, cambios)
                
                messagebox.showinfo("Éxito", "Libro actualizado correctamente")
                
                # Volver a la lista
                self.volver_a_lista()

        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar cambios: {str(e)}")

    def cancelar(self):
        """Cancela la edición y vuelve a la lista."""
        if confirmar("Confirmar Cancelación", 
                    "¿Está seguro de cancelar? Se perderán los cambios no guardados.", 
                    parent=self):
            self.volver_a_lista()

    def volver_a_lista(self):
        """Vuelve a la lista de libros."""
        from gui.frames.list_frame import ListFrame
        libros = self.gestor.get_libros_disponibles()  # O la lista que corresponda
        self.master.switch_frame(ListFrame, titulo="Libros Disponibles", libros=libros)
