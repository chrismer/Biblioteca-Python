import customtkinter as ctk
from tkinter import messagebox
from typing import TYPE_CHECKING, List, Optional
from logic.models import Libro, Estanteria
from gui.frames.base_frame import BaseFrame

if TYPE_CHECKING:
    from gui.app import App
    from logic.library_manager import GestorBiblioteca

class MoveBookFrame(BaseFrame):
    def __init__(self, master: 'App', gestor: 'GestorBiblioteca'):
        super().__init__(master, gestor)
        self.estanterias = self.gestor.get_todas_estanterias()
        self.libro_seleccionado: Optional[Libro] = None
        self.libros_encontrados: List[Libro] = []
        self.setup_interface()

    def setup_interface(self):
        """Configura la interfaz del formulario de mover libro."""
        # Header
        self.create_header("📦 Mover Libro de Estantería", "Busca un libro y muévelo junto con todos sus ejemplares a otra estantería")
        
        # --- Frame contenedor para el formulario ---
        form_frame = ctk.CTkFrame(self.content_frame, fg_color=self.colors['white'], corner_radius=15)
        form_frame.pack(padx=40, pady=10, fill="both", expand=True)
        
        # --- PASO 1: Buscar Libro ---
        step1_frame = ctk.CTkFrame(form_frame, fg_color=self.colors['light'], corner_radius=10)
        step1_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        ctk.CTkLabel(step1_frame, text="🔍 PASO 1: Buscar el Libro", 
                    font=("Segoe UI", 14, "bold"), 
                    text_color=self.colors['primary']).pack(pady=(15, 10), padx=20, anchor="w")
        
        search_container = ctk.CTkFrame(step1_frame, fg_color="transparent")
        search_container.pack(fill="x", padx=20, pady=(0, 15))
        
        self.search_entry = ctk.CTkEntry(search_container, 
                                         placeholder_text="Buscar por título, autor o código...",
                                         height=40)
        self.search_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.search_entry.bind("<KeyRelease>", self.buscar_libro_en_tiempo_real)
        
        ctk.CTkButton(search_container, text="🔍 Buscar", 
                     command=self.buscar_libros,
                     height=40, width=120,
                     fg_color=self.colors['primary'],
                     hover_color=self.colors['accent']).pack(side="left")
        
        # Resultados de búsqueda
        self.results_frame = ctk.CTkScrollableFrame(step1_frame, height=150, fg_color="white")
        self.results_frame.pack(fill="both", padx=20, pady=(0, 15))
        self.results_frame.pack_forget()  # Ocultar inicialmente
        
        # --- PASO 2: Información del libro seleccionado ---
        self.step2_frame = ctk.CTkFrame(form_frame, fg_color=self.colors['light'], corner_radius=10)
        self.step2_frame.pack(fill="x", padx=20, pady=10)
        self.step2_frame.pack_forget()  # Ocultar inicialmente
        
        ctk.CTkLabel(self.step2_frame, text="📚 PASO 2: Libro Seleccionado", 
                    font=("Segoe UI", 14, "bold"), 
                    text_color=self.colors['primary']).pack(pady=(15, 10), padx=20, anchor="w")
        
        info_container = ctk.CTkFrame(self.step2_frame, fg_color="white", corner_radius=8)
        info_container.pack(fill="x", padx=20, pady=(0, 15))
        
        # Grid para información
        info_container.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(info_container, text="Título:", font=("Segoe UI", 11, "bold")).grid(
            row=0, column=0, padx=15, pady=8, sticky="e")
        self.titulo_label = ctk.CTkLabel(info_container, text="---", font=("Segoe UI", 11))
        self.titulo_label.grid(row=0, column=1, padx=15, pady=8, sticky="w")
        
        ctk.CTkLabel(info_container, text="Autor:", font=("Segoe UI", 11, "bold")).grid(
            row=1, column=0, padx=15, pady=8, sticky="e")
        self.autor_label = ctk.CTkLabel(info_container, text="---", font=("Segoe UI", 11))
        self.autor_label.grid(row=1, column=1, padx=15, pady=8, sticky="w")
        
        ctk.CTkLabel(info_container, text="Estantería Actual:", font=("Segoe UI", 11, "bold")).grid(
            row=2, column=0, padx=15, pady=8, sticky="e")
        self.estanteria_actual_label = ctk.CTkLabel(info_container, text="---", 
                                                     font=("Segoe UI", 11, "bold"),
                                                     text_color=self.colors['warning'])
        self.estanteria_actual_label.grid(row=2, column=1, padx=15, pady=8, sticky="w")
        
        ctk.CTkLabel(info_container, text="Ejemplares:", font=("Segoe UI", 11, "bold")).grid(
            row=3, column=0, padx=15, pady=8, sticky="e")
        self.ejemplares_label = ctk.CTkLabel(info_container, text="---", font=("Segoe UI", 11))
        self.ejemplares_label.grid(row=3, column=1, padx=15, pady=8, sticky="w")
        
        # --- PASO 3: Seleccionar estantería destino ---
        self.step3_frame = ctk.CTkFrame(form_frame, fg_color=self.colors['light'], corner_radius=10)
        self.step3_frame.pack(fill="x", padx=20, pady=10)
        self.step3_frame.pack_forget()  # Ocultar inicialmente
        
        ctk.CTkLabel(self.step3_frame, text="🎯 PASO 3: Seleccionar Estantería Destino", 
                    font=("Segoe UI", 14, "bold"), 
                    text_color=self.colors['primary']).pack(pady=(15, 10), padx=20, anchor="w")
        
        self.shelf_container = ctk.CTkFrame(self.step3_frame, fg_color="white", corner_radius=8)
        self.shelf_container.pack(fill="x", padx=20, pady=(0, 15))
        
        self.selected_shelf = ctk.StringVar(value="Seleccione estantería destino...")
        
        # --- Botón de acción (al final, se mostrará solo al seleccionar libro) ---
        self.button_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        self.button_frame.pack(fill="x", padx=20, pady=20)
        self.button_frame.pack_forget()  # Ocultar inicialmente
        
        self.move_button = ctk.CTkButton(self.button_frame, text="📦 Mover Libro y Ejemplares", 
                                        command=self.mover_libro,
                                        height=45,
                                        font=("Segoe UI", 13, "bold"),
                                        fg_color=self.colors['success'],
                                        hover_color="#1e5f4e")
        self.move_button.pack(side="left", padx=(0, 10))
        
        # Botón volver
        self.create_back_button()

    def buscar_libro_en_tiempo_real(self, event=None):
        """Búsqueda en tiempo real mientras el usuario escribe."""
        termino = self.search_entry.get().strip()
        if len(termino) >= 2:  # Buscar solo si hay al menos 2 caracteres
            self.buscar_libros()
        elif len(termino) == 0:
            self.results_frame.pack_forget()
    
    def buscar_libros(self):
        """Realiza la búsqueda de libros."""
        termino = self.search_entry.get().strip()
        
        if not termino:
            messagebox.showwarning("Advertencia", "Por favor ingresa un término de búsqueda")
            return
        
        try:
            # Buscar libros
            self.libros_encontrados = self.gestor.buscar_libros(termino)
            
            # Limpiar resultados anteriores
            for widget in self.results_frame.winfo_children():
                widget.destroy()
            
            if not self.libros_encontrados:
                self.results_frame.pack(fill="both", padx=20, pady=(0, 15))
                ctk.CTkLabel(self.results_frame, 
                           text="❌ No se encontraron libros",
                           text_color=self.colors['danger'],
                           font=("Segoe UI", 12)).pack(pady=20)
            else:
                self.results_frame.pack(fill="both", padx=20, pady=(0, 15))
                
                # Mostrar resultados
                for libro in self.libros_encontrados:
                    self.crear_fila_resultado(libro)
                    
        except Exception as e:
            messagebox.showerror("Error", f"Error al buscar libros: {str(e)}")
    
    def crear_fila_resultado(self, libro: Libro):
        """Crea una fila con el resultado de búsqueda."""
        row_frame = ctk.CTkFrame(self.results_frame, fg_color=self.colors['light'], corner_radius=8)
        row_frame.pack(fill="x", pady=5, padx=10)
        
        # Información del libro
        info_frame = ctk.CTkFrame(row_frame, fg_color="transparent")
        info_frame.pack(side="left", fill="both", expand=True, padx=15, pady=10)
        
        titulo_text = f"📚 {libro.titulo}"
        ctk.CTkLabel(info_frame, text=titulo_text, 
                    font=("Segoe UI", 12, "bold"),
                    anchor="w").pack(anchor="w")
        
        autor_text = f"✍️ {libro.autor.nombre} {libro.autor.apellido}" if libro.autor else "Autor desconocido"
        ctk.CTkLabel(info_frame, text=autor_text, 
                    font=("Segoe UI", 10),
                    text_color=self.colors['secondary'],
                    anchor="w").pack(anchor="w")
        
        codigo_text = f"🔢 Código: {libro.codigo}"
        ctk.CTkLabel(info_frame, text=codigo_text, 
                    font=("Segoe UI", 9),
                    text_color=self.colors['muted'],
                    anchor="w").pack(anchor="w")
        
        # Botón seleccionar
        ctk.CTkButton(row_frame, text="Seleccionar", 
                     command=lambda: self.seleccionar_libro(libro),
                     width=120,
                     fg_color=self.colors['success'],
                     hover_color="#1e5f4e").pack(side="right", padx=15, pady=10)
    
    def seleccionar_libro(self, libro: Libro):
        """Selecciona un libro y muestra su información."""
        self.libro_seleccionado = libro
        
        # Obtener estantería actual
        estanteria_actual = next((e for e in self.estanterias if e.id == libro.estanteria_id), None)
        
        # Actualizar información del libro
        self.titulo_label.configure(text=libro.titulo)
        autor_nombre = f"{libro.autor.nombre} {libro.autor.apellido}" if libro.autor else "Desconocido"
        self.autor_label.configure(text=autor_nombre)
        self.estanteria_actual_label.configure(
            text=estanteria_actual.nombre if estanteria_actual else "Sin estantería"
        )
        
        # Mostrar cantidad de ejemplares
        num_ejemplares = len(libro.ejemplares) if libro.ejemplares else 0
        self.ejemplares_label.configure(text=f"{num_ejemplares} ejemplar(es) se moverán")
        
        # Mostrar paso 2
        self.step2_frame.pack(fill="x", padx=20, pady=10)
        
        # Crear opciones de estanterías destino (todas menos la actual)
        self.crear_opciones_estanterias(estanteria_actual.id if estanteria_actual else None)
        
        # Mostrar paso 3
        self.step3_frame.pack(fill="x", padx=20, pady=10)
        
        # Mostrar y habilitar botón de mover (al final)
        self.button_frame.pack(fill="x", padx=20, pady=20)
        self.move_button.configure(state="normal")
    
    def crear_opciones_estanterias(self, estanteria_actual_id: int):
        """Crea las opciones de estanterías destino."""
        # Limpiar contenedor
        for widget in self.shelf_container.winfo_children():
            widget.destroy()
        
        # Filtrar estanterías (todas menos la actual)
        estanterias_disponibles = [e for e in self.estanterias if e.id != estanteria_actual_id]
        
        if not estanterias_disponibles:
            ctk.CTkLabel(self.shelf_container, 
                       text="⚠️ No hay otras estanterías disponibles",
                       text_color=self.colors['warning'],
                       font=("Segoe UI", 11)).pack(pady=15)
            self.move_button.configure(state="disabled")
            return
        
        # Crear opciones de estanterías con dropdown
        shelf_options = [f"{e.nombre} (Capacidad: {e.capacidad})" for e in estanterias_disponibles]
        
        self.shelf_menu = ctk.CTkOptionMenu(self.shelf_container, 
                                            variable=self.selected_shelf,
                                            values=shelf_options,
                                            height=40,
                                            font=("Segoe UI", 12),
                                            fg_color=self.colors['primary'],
                                            button_color=self.colors['accent'],
                                            button_hover_color=self.colors['primary'])
        self.shelf_menu.pack(fill="x", padx=15, pady=15)
        self.selected_shelf.set(shelf_options[0] if shelf_options else "")
        
        # Guardar mapeo de nombres a IDs
        self.estanterias_map = {e.nombre: e for e in estanterias_disponibles}

    def mover_libro(self):
        """Mueve el libro y todos sus ejemplares a la estantería destino."""
        if not self.libro_seleccionado:
            messagebox.showwarning("Advertencia", "Por favor selecciona un libro primero")
            return
        
        try:
            # Extraer nombre de estantería del formato "Nombre (Capacidad: X)"
            shelf_text = self.selected_shelf.get()
            shelf_nombre = shelf_text.split(" (Capacidad:")[0]
            
            if shelf_nombre not in self.estanterias_map:
                raise ValueError("Por favor selecciona una estantería de destino válida")
            
            estanteria_destino = self.estanterias_map[shelf_nombre]
            
            # Mover el libro
            self.gestor.mover_libro(self.libro_seleccionado.id, estanteria_destino.id)
            
            num_ejemplares = len(self.libro_seleccionado.ejemplares) if self.libro_seleccionado.ejemplares else 0
            
            messagebox.showinfo("✅ Éxito", 
                              f"El libro '{self.libro_seleccionado.titulo}' y sus {num_ejemplares} ejemplar(es)\n"
                              f"han sido movidos a '{estanteria_destino.nombre}' correctamente.")
            
            self.master.switch_frame(self.master.main_frame_class)
            
        except Exception as e:
            messagebox.showerror("❌ Error", f"Error al mover el libro:\n{str(e)}")