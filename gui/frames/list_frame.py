import customtkinter as ctk
from tkinter import messagebox
from typing import TYPE_CHECKING, List
from logic.models import Libro
from gui.utils.dialogs import confirmar

if TYPE_CHECKING:
    from gui.app import App
    from logic.library_manager import GestorBiblioteca

class ListFrame(ctk.CTkFrame):
    def __init__(self, master: 'App', gestor: 'GestorBiblioteca', titulo: str, libros: List[Libro]):
        super().__init__(master)
        self.master = master
        self.gestor = gestor
        self.titulo = titulo 

        # Título dinámico (ej: "Libros Disponibles")
        ctk.CTkLabel(self, text=titulo, font=("Arial", 20, "bold")).pack(pady=20)

        # Frame con scroll para la lista de libros
        scroll_frame = ctk.CTkScrollableFrame(self)
        scroll_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Encabezados de la tabla
        headers = ["Código", "Título", "Autor", "Disponibles", "Acciones"]
        for i, header in enumerate(headers):
            ctk.CTkLabel(scroll_frame, text=header, font=("Arial", 12, "bold")).grid(row=0, column=i, padx=10, pady=5)

        # Llenar la tabla con los libros
        for row_num, libro in enumerate(libros, start=1):
            ctk.CTkLabel(scroll_frame, text=libro.codigo).grid(row=row_num, column=0, padx=10)
            ctk.CTkLabel(scroll_frame, text=libro.titulo).grid(row=row_num, column=1, padx=10)
            ctk.CTkLabel(scroll_frame, text=libro.autor.nombre_completo if libro.autor else "N/A").grid(row=row_num, column=2, padx=10)
            
            # Mostrar disponibles con color según el estado
            disponibles = libro.cantidad_disponibles
            prestados = libro.cantidad_prestados

            color_disponibles = "green" if disponibles > 0 else "red"
            
            # Creamos el texto a mostrar
            disponibles_text = f"{disponibles}"
            if prestados > 0:
                 disponibles_text += f" (Prestados: {prestados})"

            ctk.CTkLabel(scroll_frame, text=disponibles_text, text_color=color_disponibles).grid(row=row_num, column=3, padx=10)

            # Frame para los botones de acción
            actions_frame = ctk.CTkFrame(scroll_frame, fg_color="transparent")
            actions_frame.grid(row=row_num, column=4, padx=10)

            # Botón Prestar - Solo activo si hay ejemplares disponibles
            if disponibles > 0:
                prestar_btn = ctk.CTkButton(
                    actions_frame, 
                    text="📤 Prestar", 
                    width=80, 
                    fg_color="green",
                    hover_color="darkgreen",
                    command=lambda l=libro: self.prestar(l)
                )
            else:
                prestar_btn = ctk.CTkButton(
                    actions_frame, 
                    text="❌ Agotado", 
                    width=80, 
                    fg_color="gray",
                    hover_color="gray",
                    state="disabled"
                )
            prestar_btn.pack(side="left", padx=2)
            
            # Botón Devolver - Solo activo si hay ejemplares prestados
            if prestados > 0:
                devolver_btn = ctk.CTkButton(
                    actions_frame, 
                    text="📥 Devolver", 
                    width=80, 
                    fg_color="orange",
                    hover_color="darkorange",
                    command=lambda l=libro: self.devolver(l)
                )
            else:
                devolver_btn = ctk.CTkButton(
                    actions_frame, 
                    text="➖ N/A", 
                    width=80, 
                    fg_color="gray",
                    hover_color="gray",
                    state="disabled"
                )
            devolver_btn.pack(side="left", padx=2)

            # Botones de acción
            ctk.CTkButton(actions_frame, text="📋 Detalles", width=70, fg_color="blue", hover_color="darkblue", command=lambda l=libro: self.ver_ejemplares(l)).pack(side="left", padx=2)
            ctk.CTkButton(actions_frame, text="✏️ Editar", width=70, fg_color="purple", command=lambda l=libro: self.editar_libro(l)).pack(side="left", padx=2)
            ctk.CTkButton(actions_frame, text="🗑️ Eliminar", width=70, fg_color="red", command=lambda l=libro: self.eliminar_libro(l)).pack(side="left", padx=2)

        # Botón para volver al menú principal
        ctk.CTkButton(self, text="Volver", fg_color="gray", command=lambda: self.master.switch_frame(self.master.main_frame_class)).pack(pady=20)

    def prestar(self, libro: Libro):
        try:
            self.gestor.prestar_libro(libro.codigo)
            messagebox.showinfo("Éxito", f"Se ha prestado un ejemplar de '{libro.titulo}'.")
            # Recargar la vista actual para reflejar el cambio
            self.recargar_vista_actual()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def devolver(self, libro: Libro):
        try:
            self.gestor.devolver_libro(libro.codigo)
            messagebox.showinfo("Éxito", f"Se ha devuelto un ejemplar de '{libro.titulo}'.")
            # Recargar la vista actual
            self.recargar_vista_actual()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def recargar_vista_actual(self):
        """Recarga la vista actual detectando automáticamente qué tipo de lista mostrar."""
        try:
            # Detectar qué vista estamos mostrando según el título
            titulo_actual = self.titulo.lower()
            
            if "disponible" in titulo_actual:
                # Estamos en la vista de libros disponibles
                libros = self.gestor.get_libros_disponibles()
                titulo = "Libros Disponibles"
            elif "prestado" in titulo_actual:
                # Estamos en la vista de libros prestados
                libros = self.gestor.get_libros_prestados()
                titulo = "Libros Prestados"
            else:
                # Vista genérica, obtener todos los libros
                libros = self.gestor.get_todos_los_libros()
                titulo = self.titulo
            
            # Recargar el frame con los datos correctos
            self.master.switch_frame(self.__class__, titulo=titulo, libros=libros)
        except Exception as e:
            messagebox.showerror("Error", f"Error al recargar la vista: {str(e)}")

    def ver_ejemplares(self, libro: Libro):
        """Muestra los ejemplares individuales de un libro."""
        try:
            # Crear ventana emergente para mostrar ejemplares
            ejemplares_window = ctk.CTkToplevel(self)
            ejemplares_window.title(f"Ejemplares de '{libro.titulo}'")
            ejemplares_window.geometry("800x600")
            
            # Forzar que la ventana aparezca al frente
            ejemplares_window.lift()
            ejemplares_window.focus_force()
            ejemplares_window.grab_set()
            
            ctk.CTkLabel(ejemplares_window, text=f"📚 Ejemplares de '{libro.titulo}'", 
                        font=("Arial", 16, "bold")).pack(pady=10)
            
            # Información del libro
            info_frame = ctk.CTkFrame(ejemplares_window, fg_color="blue")
            info_frame.pack(pady=10, padx=20, fill="x")
            
            # Información del libro con datos seguros
            autor_nombre = libro.autor.nombre_completo if libro.autor else "Autor Desconocido"
            disponibles_count = libro.cantidad_disponibles
            info_text = f"📖 Código: {libro.codigo} | 👨‍💼 Autor: {autor_nombre} | 📊 Disponibles: {disponibles_count}"
            ctk.CTkLabel(info_frame, text=info_text, text_color="white").pack(pady=5)
            
            # Intentar obtener ejemplares del nuevo sistema
            ejemplares = []
            libro_id = None
            
            try:
                # Primero intentar con el ID directo si existe
                if hasattr(libro, 'id') and libro.id and libro.id > 0:
                    libro_id = libro.id
                else:
                    # Buscar por código en la base de datos
                    cursor = self.gestor.db.conn.cursor()
                    cursor.execute("SELECT id FROM libros WHERE codigo = ?", (libro.codigo,))
                    row = cursor.fetchone()
                    if row:
                        libro_id = row['id']
                
                # Si tenemos libro_id, obtener ejemplares
                if libro_id:
                    ejemplares = self.gestor.get_ejemplares_por_libro(libro_id)
                    
            except Exception as e:
                print(f"Error obteniendo ejemplares: {e}")
                import traceback
                traceback.print_exc()
                ejemplares = []
            
            if len(ejemplares) > 0:
                # Frame con scroll para ejemplares
                scroll_frame = ctk.CTkScrollableFrame(ejemplares_window)
                scroll_frame.pack(pady=10, padx=10, fill="both", expand=True)
                
                # Encabezados (sin columna de Acciones)
                headers = ["Código Ejemplar", "Estado", "Ubicación", "Fecha Adquisición"]
                for i, header in enumerate(headers):
                    ctk.CTkLabel(scroll_frame, text=header, font=("Arial", 12, "bold")).grid(
                        row=0, column=i, padx=10, pady=5)
                
                # Datos de ejemplares (solo información, sin botones)
                for row_num, ejemplar in enumerate(ejemplares, start=1):
                    ctk.CTkLabel(scroll_frame, text=ejemplar.codigo_ejemplar).grid(row=row_num, column=0, padx=10, pady=2)
                    
                    # Estado con color
                    estado_color = {
                        'disponible': 'green',
                        'prestado': 'orange',
                        'dañado': 'red',
                        'perdido': 'purple',
                        'en_reparacion': 'yellow'
                    }.get(ejemplar.estado, 'gray')
                    
                    estado_emoji = {
                        'disponible': '✅',
                        'prestado': '📤',
                        'dañado': '🔧',
                        'perdido': '❌',
                        'en_reparacion': '⚠️'
                    }.get(ejemplar.estado, '❓')
                    
                    ctk.CTkLabel(scroll_frame, text=f"{estado_emoji} {ejemplar.estado.title()}", 
                               text_color=estado_color).grid(row=row_num, column=1, padx=10, pady=2)
                    
                    ctk.CTkLabel(scroll_frame, text=ejemplar.ubicacion_fisica or "No especificada").grid(
                        row=row_num, column=2, padx=10, pady=2)
                    ctk.CTkLabel(scroll_frame, text=str(ejemplar.fecha_adquisicion)).grid(
                        row=row_num, column=3, padx=10, pady=2)
                
                print(f"✅ Interfaz de ejemplares creada: {len(ejemplares)} ejemplares mostrados")
            else:
                # Mostrar información legacy
                legacy_frame = ctk.CTkFrame(ejemplares_window, fg_color="orange")
                legacy_frame.pack(pady=20, padx=20, fill="x")
                
                # Obtener datos de manera segura
                total = 0
                if hasattr(libro, '_cantidad_total_legacy'):
                    total = libro._cantidad_total_legacy
                elif hasattr(libro, 'cantidad_total'):
                    total = libro.cantidad_total
                
                prestados_legacy = 0
                if hasattr(libro, '_cantidad_prestados_legacy'):
                    prestados_legacy = libro._cantidad_prestados_legacy
                elif hasattr(libro, 'cantidad_prestados'):
                    prestados_legacy = libro.cantidad_prestados
                
                disponibles = getattr(libro, 'disponibles', libro.cantidad_disponibles)
                
                legacy_text = f"📋 VISTA SIMPLIFICADA (Sistema Legacy)\n\n"
                legacy_text += f"📦 Total de ejemplares: {total}\n"
                legacy_text += f"✅ Disponibles: {disponibles}\n"
                legacy_text += f"📤 Prestados: {prestados_legacy}\n\n"
                legacy_text += f"💡 Para ver ejemplares individuales, use el nuevo sistema de gestión de préstamos."
                
                ctk.CTkLabel(legacy_frame, text=legacy_text, text_color="white").pack(pady=10)
            
            # Botón cerrar
            ctk.CTkButton(ejemplares_window, text="Cerrar", 
                         command=ejemplares_window.destroy).pack(pady=10)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al mostrar ejemplares: {str(e)}")

    def prestar_ejemplar_individual(self, ejemplar, window):
        """Presta un ejemplar específico."""
        # Esta función se conectaría con el sistema de préstamos nuevo
        messagebox.showinfo("Función Avanzada", 
                           f"Para prestar ejemplares individuales, use:\n"
                           f"📤 Gestionar Préstamos → ➕ Nuevo Préstamo\n\n"
                           f"Ejemplar: {ejemplar.codigo_ejemplar}")
        window.destroy()

    def devolver_ejemplar_individual(self, ejemplar, window):
        """Devuelve un ejemplar específico."""
        messagebox.showinfo("Función Avanzada", 
                           f"Para devolver ejemplares individuales, use:\n"
                           f"📤 Gestionar Préstamos → 📋 Préstamos Activos\n\n"
                           f"Ejemplar: {ejemplar.codigo_ejemplar}")
        window.destroy()
        try:
            libros = self.gestor.get_libros_disponibles()
            self.master.switch_frame(ListFrame, titulo="Libros Disponibles", libros=libros)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def editar_libro(self, libro: Libro):
        """Abre la ventana de edición para el libro."""
        try:
            from gui.frames.edit_book_frame import EditBookFrame
            self.master.switch_frame(EditBookFrame, libro=libro)
        except Exception as e:
            messagebox.showerror("Error", f"Error al abrir editor: {str(e)}")

    def eliminar_libro(self, libro: Libro):
        try:
            if confirmar("Confirmar Eliminación", 
                        f"¿Está seguro de que desea eliminar '{libro.titulo}' y todos sus ejemplares?\n\n"
                        f"Esta acción no se puede deshacer.", 
                        parent=self):
                self.gestor.eliminar_libro_y_ejemplares(libro.id)
                messagebox.showinfo("Éxito", "Libro eliminado correctamente.")
                # Recargar la vista
                libros_actualizados = self.gestor.buscar_libros("") # Vuelve a cargar todos los libros
                self.master.switch_frame(self.__class__, titulo=self.master.current_frame_title, libros=libros_actualizados)
        except Exception as e:
            messagebox.showerror("Error", str(e))