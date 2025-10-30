"""
Frame para gestión completa de estanterías (crear, modificar, eliminar)
"""
import customtkinter as ctk
from tkinter import messagebox
from typing import List, TYPE_CHECKING
from logic.models import Estanteria
from gui.frames.base_frame import BaseFrame
from gui.utils.dialogs import confirmar

if TYPE_CHECKING:
    from gui.app import App
    from logic.library_manager import GestorBiblioteca

class ManageShelvesFrame(BaseFrame):
    def __init__(self, master: 'App', gestor: 'GestorBiblioteca'):
        super().__init__(master, gestor)
        self.setup_interface()

    def setup_interface(self):
        """Configura la interfaz de gestión de estanterías."""
        # Header
        self.create_header("🏛️ Gestión de Estanterías", "Crear, modificar y eliminar estanterías")
        
        # Contenedor principal
        main_container = ctk.CTkFrame(self.content_frame, fg_color=self.colors['white'], corner_radius=15)
        main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Sección de nueva estantería
        self.create_new_shelf_section(main_container)
        
        # Separador
        separator = ctk.CTkFrame(main_container, height=2, fg_color=self.colors['light'])
        separator.pack(fill="x", padx=20, pady=20)
        
        # Sección de estanterías existentes
        self.create_existing_shelves_section(main_container)
        
        # Botón volver
        self.create_back_button()

    def create_new_shelf_section(self, parent):
        """Crea la sección para agregar nueva estantería."""
        # Título de sección
        title_frame = ctk.CTkFrame(parent, fg_color="transparent")
        title_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        ctk.CTkLabel(title_frame, 
                    text="➕ Nueva Estantería", 
                    font=("Segoe UI", 18, "bold"),
                    text_color=self.colors['primary']).pack(anchor="w")
        
        # Formulario
        form_frame = ctk.CTkFrame(parent, fg_color=self.colors['light'], corner_radius=10)
        form_frame.pack(fill="x", padx=20, pady=10)
        
        # Grid para el formulario
        form_frame.grid_columnconfigure(1, weight=1)
        
        # Nombre
        ctk.CTkLabel(form_frame, text="Nombre *", font=("Segoe UI", 12, "bold")).grid(
            row=0, column=0, padx=20, pady=15, sticky="w")
        self.nombre_entry = ctk.CTkEntry(form_frame, placeholder_text="Ej: Estantería A", width=300)
        self.nombre_entry.grid(row=0, column=1, padx=20, pady=15, sticky="ew")
        
        # Capacidad
        ctk.CTkLabel(form_frame, text="Capacidad *", font=("Segoe UI", 12, "bold")).grid(
            row=1, column=0, padx=20, pady=15, sticky="w")
        self.capacidad_entry = ctk.CTkEntry(form_frame, placeholder_text="Ej: 50", width=150)
        self.capacidad_entry.grid(row=1, column=1, padx=20, pady=15, sticky="w")
        
        # Botón agregar
        ctk.CTkButton(form_frame, text="➕ Agregar Estantería", 
                     command=self.agregar_estanteria,
                     fg_color=self.colors['success'], hover_color="#1e5f4e",
                     width=200, height=40).grid(row=2, column=0, columnspan=2, pady=20)

    def create_existing_shelves_section(self, parent):
        """Crea la sección de estanterías existentes."""
        # Título de sección
        title_frame = ctk.CTkFrame(parent, fg_color="transparent")
        title_frame.pack(fill="x", padx=20, pady=(10, 10))
        
        ctk.CTkLabel(title_frame, 
                    text="📋 Estanterías Existentes", 
                    font=("Segoe UI", 18, "bold"),
                    text_color=self.colors['primary']).pack(anchor="w")
        
        # Frame para la lista
        self.list_frame = ctk.CTkScrollableFrame(parent, fg_color=self.colors['light'], corner_radius=10)
        self.list_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Cargar estanterías
        self.load_shelves()

    def load_shelves(self):
        """Carga y muestra las estanterías existentes."""
        # Limpiar contenido anterior
        for widget in self.list_frame.winfo_children():
            widget.destroy()
        
        try:
            estanterias = self.gestor.get_todas_estanterias()
            
            if not estanterias:
                ctk.CTkLabel(self.list_frame, 
                           text="No hay estanterías registradas",
                           font=("Segoe UI", 14),
                           text_color=self.colors['secondary']).pack(pady=20)
                return
            
            # Headers
            header_frame = ctk.CTkFrame(self.list_frame, fg_color=self.colors['primary'], corner_radius=8)
            header_frame.pack(fill="x", pady=(0, 10))
            
            headers = ["ID", "Nombre", "Capacidad", "Ocupados", "Libres", "Acciones"]
            widths = [50, 200, 100, 100, 100, 200]  # Anchos fijos para cada columna
            
            for i, header in enumerate(headers):
                ctk.CTkLabel(header_frame, text=header, 
                           font=("Segoe UI", 12, "bold"),
                           text_color="white",
                           width=widths[i]).grid(row=0, column=i, padx=10, pady=10)
            
            # Datos de estanterías
            for estanteria in estanterias:
                self.create_shelf_row(estanteria)
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar estanterías: {str(e)}")

    def create_shelf_row(self, estanteria: Estanteria):
        """Crea una fila para una estantería."""
        # Obtener estadísticas
        try:
            ocupados = self.gestor.get_count_libros_en_estanteria(estanteria.id)
            libres = estanteria.capacidad - ocupados
        except:
            ocupados = 0
            libres = estanteria.capacidad
        
        # Frame para la fila
        row_frame = ctk.CTkFrame(self.list_frame, fg_color="white", corner_radius=8)
        row_frame.pack(fill="x", pady=2)
        
        # Anchos fijos para alineación (mismos que los headers)
        widths = [50, 200, 100, 100, 100, 200]
        
        # Datos
        ctk.CTkLabel(row_frame, text=str(estanteria.id), width=widths[0]).grid(row=0, column=0, padx=10, pady=10)
        ctk.CTkLabel(row_frame, text=estanteria.nombre, font=("Segoe UI", 11, "bold"), width=widths[1], anchor="w").grid(row=0, column=1, padx=10, pady=10)
        ctk.CTkLabel(row_frame, text=str(estanteria.capacidad), width=widths[2]).grid(row=0, column=2, padx=10, pady=10)
        
        # Ocupados con color
        color_ocupados = self.colors['danger'] if ocupados >= estanteria.capacidad else self.colors['primary']
        ctk.CTkLabel(row_frame, text=str(ocupados), text_color=color_ocupados, width=widths[3]).grid(row=0, column=3, padx=10, pady=10)
        
        # Libres con color
        color_libres = self.colors['success'] if libres > 0 else self.colors['danger']
        ctk.CTkLabel(row_frame, text=str(libres), text_color=color_libres, width=widths[4]).grid(row=0, column=4, padx=10, pady=10)
        
        # Botones de acción
        actions_frame = ctk.CTkFrame(row_frame, fg_color="transparent")
        actions_frame.grid(row=0, column=5, padx=10, pady=5, sticky="e")
        
        # Botón editar
        ctk.CTkButton(actions_frame, text="✏️ Editar", width=80, height=30,
                     fg_color=self.colors['warning'], hover_color="#d67e00",
                     command=lambda e=estanteria: self.editar_estanteria(e)).pack(side="left", padx=2)
        
        # Botón eliminar (solo si está vacía)
        if ocupados == 0:
            ctk.CTkButton(actions_frame, text="🗑️ Eliminar", width=80, height=30,
                         fg_color=self.colors['danger'], hover_color="#c12e2a",
                         command=lambda e=estanteria: self.eliminar_estanteria(e)).pack(side="left", padx=2)
        else:
            ctk.CTkButton(actions_frame, text="🚫 Ocupada", width=80, height=30,
                         fg_color="gray", hover_color="gray",
                         state="disabled").pack(side="left", padx=2)

    def agregar_estanteria(self):
        """Agrega una nueva estantería."""
        try:
            nombre = self.nombre_entry.get().strip()
            capacidad_str = self.capacidad_entry.get().strip()
            
            if not nombre:
                raise ValueError("El nombre es obligatorio")
            
            if not capacidad_str.isdigit():
                raise ValueError("La capacidad debe ser un número entero")
            
            capacidad = int(capacidad_str)
            if capacidad < 1:
                raise ValueError("La capacidad debe ser mayor a 0")
            
            # Agregar estantería
            self.gestor.agregar_estanteria(nombre, capacidad)
            
            # Limpiar formulario
            self.nombre_entry.delete(0, "end")
            self.capacidad_entry.delete(0, "end")
            
            # Recargar lista
            self.load_shelves()
            
            messagebox.showinfo("Éxito", f"Estantería '{nombre}' agregada correctamente")
            
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def editar_estanteria(self, estanteria: Estanteria):
        """Abre ventana para editar estantería."""
        # Crear ventana de edición
        edit_window = ctk.CTkToplevel(self)
        edit_window.title(f"Editar Estantería - {estanteria.nombre}")
        edit_window.geometry("520x500")
        edit_window.transient(self)
        edit_window.grab_set()
        
        # Aplicar icono personalizado
        try:
            import os
            import tkinter as tk
            current_dir = os.path.dirname(os.path.abspath(__file__))
            icon_path = os.path.join(current_dir, "..", "..", "assets", "bibliohub_icon.png")
            icon_path = os.path.normpath(icon_path)
            
            if os.path.exists(icon_path):
                icon_image = tk.PhotoImage(file=icon_path)
                edit_window.iconphoto(True, icon_image)
        except Exception:
            pass
        
        # Centrar ventana
        edit_window.update_idletasks()
        x = (edit_window.winfo_screenwidth() // 2) - (520 // 2)
        y = (edit_window.winfo_screenheight() // 2) - (500 // 2)
        edit_window.geometry(f"520x500+{x}+{y}")
        
        # Frame principal con scroll
        main_scroll = ctk.CTkScrollableFrame(edit_window, fg_color=self.colors['white'])
        main_scroll.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        title_frame = ctk.CTkFrame(main_scroll, fg_color=self.colors['primary'], corner_radius=10)
        title_frame.pack(fill="x", pady=(0, 20))
        ctk.CTkLabel(title_frame, text=f"✏️ Editar Estantería", 
                    font=("Segoe UI", 20, "bold"),
                    text_color="white").pack(pady=15)
        
        # Formulario
        form_frame = ctk.CTkFrame(main_scroll, fg_color=self.colors['light'], corner_radius=10)
        form_frame.pack(fill="x", padx=10, pady=10)
        
        # Nombre
        ctk.CTkLabel(form_frame, text="Nombre:", font=("Segoe UI", 13, "bold")).pack(anchor="w", padx=20, pady=(20, 5))
        nombre_entry = ctk.CTkEntry(form_frame, width=420, height=35, font=("Segoe UI", 12))
        nombre_entry.pack(padx=20, pady=(0, 15))
        nombre_entry.insert(0, estanteria.nombre)
        
        # Capacidad
        ctk.CTkLabel(form_frame, text="Capacidad:", font=("Segoe UI", 13, "bold")).pack(anchor="w", padx=20, pady=(10, 5))
        capacidad_entry = ctk.CTkEntry(form_frame, width=200, height=35, font=("Segoe UI", 12))
        capacidad_entry.pack(anchor="w", padx=20, pady=(0, 15))
        capacidad_entry.insert(0, str(estanteria.capacidad))
        
        # Información actual
        try:
            ocupados = self.gestor.get_count_libros_en_estanteria(estanteria.id)
            info_text = f"📊 Actualmente: {ocupados} ejemplares ocupados"
            if ocupados > 0:
                info_text += f"\n⚠️ Capacidad mínima: {ocupados} (no puede ser menor)"
        except:
            info_text = "📊 No se pudo obtener información de ocupación"
        
        info_frame = ctk.CTkFrame(form_frame, fg_color="#FFF3CD", corner_radius=8)
        info_frame.pack(fill="x", padx=20, pady=(10, 20))
        ctk.CTkLabel(info_frame, text=info_text, 
                    text_color="#856404",
                    font=("Segoe UI", 11),
                    justify="left").pack(pady=12, padx=12)
        
        # Botones (más grandes y visibles)
        buttons_frame = ctk.CTkFrame(main_scroll, fg_color="transparent")
        buttons_frame.pack(pady=20)
        
        def guardar_cambios():
            try:
                nuevo_nombre = nombre_entry.get().strip()
                nueva_capacidad_str = capacidad_entry.get().strip()
                
                if not nuevo_nombre:
                    raise ValueError("El nombre es obligatorio")
                
                if not nueva_capacidad_str.isdigit():
                    raise ValueError("La capacidad debe ser un número entero")
                
                nueva_capacidad = int(nueva_capacidad_str)
                if nueva_capacidad < 1:
                    raise ValueError("La capacidad debe ser mayor a 0")
                
                # Modificar estantería
                self.gestor.modificar_estanteria(estanteria.id, nuevo_nombre, nueva_capacidad)
                
                edit_window.destroy()
                self.load_shelves()
                messagebox.showinfo("Éxito", "Estantería modificada correctamente")
                
            except Exception as e:
                messagebox.showerror("Error", str(e))
        
        ctk.CTkButton(buttons_frame, text="💾 Guardar Cambios", 
                     command=guardar_cambios,
                     fg_color=self.colors['success'], 
                     hover_color="#1e5f4e",
                     width=180,
                     height=45,
                     font=("Segoe UI", 13, "bold")).pack(side="left", padx=10)
        
        ctk.CTkButton(buttons_frame, text="❌ Cancelar", 
                     command=edit_window.destroy,
                     fg_color=self.colors['danger'], 
                     hover_color="#c12e2a",
                     width=140,
                     height=45,
                     font=("Segoe UI", 13, "bold")).pack(side="left", padx=10)

    def eliminar_estanteria(self, estanteria: Estanteria):
        """Elimina una estantería."""
        try:
            # Verificar que esté vacía
            ocupados = self.gestor.get_count_libros_en_estanteria(estanteria.id)
            if ocupados > 0:
                messagebox.showerror("Error", 
                                   f"No se puede eliminar la estantería '{estanteria.nombre}' "
                                   f"porque tiene {ocupados} ejemplares.")
                return
            
            # Confirmar eliminación
            if confirmar("Confirmar Eliminación", 
                        f"¿Está seguro de que desea eliminar la estantería '{estanteria.nombre}'?\n\n"
                        f"Esta acción no se puede deshacer.", self):
                
                self.gestor.eliminar_estanteria(estanteria.id)
                self.load_shelves()
                messagebox.showinfo("Éxito", f"Estantería '{estanteria.nombre}' eliminada correctamente")
                
        except Exception as e:
            messagebox.showerror("Error", str(e))
