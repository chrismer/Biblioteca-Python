import customtkinter as ctk
from tkinter import messagebox
from typing import TYPE_CHECKING, List
from logic.models import Libro
from gui.utils.dialogs import confirmar

# Importaciones para navegación
from .book_form_frame import BookFormFrame

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
        ctk.CTkButton(self, text="Volver", fg_color="gray", command=self._go_to_main_frame).pack(pady=20)

    def _go_to_main_frame(self):
        """Navega al MainFrame, usando una importación local para evitar ciclos."""
        from .main_frame import MainFrame
        self.master.switch_frame(MainFrame)

    def prestar(self, libro: Libro):
        # Verificar si hay usuarios registrados
        usuarios_disponibles = self.gestor.get_todos_usuarios()
        if not usuarios_disponibles:
            respuesta = confirmar(
                "Sin Usuarios Registrados",
                "⚠️ No hay usuarios registrados en el sistema.\n\n"
                "Para realizar préstamos, primero debes registrar al menos un usuario.\n\n"
                "¿Deseas ir a 'Gestionar Usuarios' ahora?",
                parent=self
            )
            if respuesta:
                from .users_frame import UsersFrame
                self.master.switch_frame(UsersFrame)
            return
        
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
        """Muestra los ejemplares individuales de un libro en una ventana emergente."""
        ejemplares_window = ctk.CTkToplevel(self)
        ejemplares_window.title(f"Ejemplares de '{libro.titulo}'")
        ejemplares_window.geometry("800x600")
        ejemplares_window.lift()
        ejemplares_window.focus_force()
        ejemplares_window.grab_set()

        ctk.CTkLabel(ejemplares_window, text=f"📚 Gestión de Ejemplares: {libro.titulo}", font=("Arial", 16, "bold")).pack(pady=10)

        # Frame para botones de acción globales
        top_actions_frame = ctk.CTkFrame(ejemplares_window, fg_color="transparent")
        top_actions_frame.pack(pady=5, padx=20, fill="x")

        # Frame para la lista de ejemplares
        scroll_frame = ctk.CTkScrollableFrame(ejemplares_window)
        scroll_frame.pack(pady=10, padx=10, fill="both", expand=True)

        ctk.CTkButton(top_actions_frame, text="➕ Añadir Nuevo Ejemplar", fg_color="green",
                     command=lambda: self.agregar_ejemplar_action(libro, ejemplares_window, scroll_frame)).pack(side="left")

        self.redraw_ejemplares_list(scroll_frame, libro)

        ctk.CTkButton(ejemplares_window, text="Cerrar", command=ejemplares_window.destroy).pack(pady=10)

    def redraw_ejemplares_list(self, frame, libro):
        """Limpia y redibuja la lista de ejemplares."""
        for widget in frame.winfo_children():
            widget.destroy()

        headers = ["Código", "Estado", "Ubicación", "Adquisición", "Acciones"]
        for i, header in enumerate(headers):
            ctk.CTkLabel(frame, text=header, font=("Arial", 12, "bold")).grid(row=0, column=i, padx=10, pady=5)

        ejemplares = self.gestor.get_ejemplares_por_libro(libro.id)
        for row_num, ejemplar in enumerate(ejemplares, start=1):
            ctk.CTkLabel(frame, text=ejemplar.codigo_ejemplar).grid(row=row_num, column=0, padx=10, pady=2)
            
            estado_color = 'green' if ejemplar.estado == 'disponible' else 'orange'
            ctk.CTkLabel(frame, text=f"{'✅' if ejemplar.estado == 'disponible' else '📤'} {ejemplar.estado.title()}", text_color=estado_color).grid(row=row_num, column=1, padx=10, pady=2)
            
            ctk.CTkLabel(frame, text=ejemplar.ubicacion_fisica or "N/A").grid(row=row_num, column=2, padx=10, pady=2)
            ctk.CTkLabel(frame, text=str(ejemplar.fecha_adquisicion)).grid(row=row_num, column=3, padx=10, pady=2)
            
            actions_frame = ctk.CTkFrame(frame, fg_color="transparent")
            actions_frame.grid(row=row_num, column=4, padx=10)

            if ejemplar.estado == 'disponible':
                ctk.CTkButton(actions_frame, text="🗑️", fg_color="red", width=30,
                             command=lambda e=ejemplar, l=libro, f=frame: self.eliminar_ejemplar_action(e, l, f)).pack()
            else:
                ctk.CTkButton(actions_frame, text="🚫", fg_color="gray", width=30, state="disabled").pack()

    def agregar_ejemplar_action(self, libro, window, scroll_frame):
        try:
            if confirmar("Confirmar", f"¿Desea añadir un nuevo ejemplar para '{libro.titulo}'?", parent=window):
                self.gestor.agregar_nuevo_ejemplar(libro.id)
                messagebox.showinfo("Éxito", "Nuevo ejemplar añadido correctamente.", parent=window)
                self.redraw_ejemplares_list(scroll_frame, libro) 
        except Exception as e:
            messagebox.showerror("Error", str(e), parent=window)

    def eliminar_ejemplar_action(self, ejemplar, libro, frame):
        try:
            if confirmar("Confirmar Eliminación", f"¿Está seguro de eliminar el ejemplar {ejemplar.codigo_ejemplar}?", parent=frame):
                self.gestor.eliminar_ejemplar(ejemplar.id)
                messagebox.showinfo("Éxito", "Ejemplar eliminado.", parent=frame)
                self.redraw_ejemplares_list(frame, libro)
        except Exception as e:
            messagebox.showerror("Error", str(e), parent=frame)

    def prestar_ejemplar_individual(self, ejemplar, window):
        """Presta un ejemplar específico."""
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
            self.master.switch_frame(BookFormFrame, libro=libro)
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
                
                # Recargar la vista según el título actual
                if "Disponibles" in self.titulo:
                    libros_actualizados = self.gestor.get_libros_disponibles()
                elif "Prestados" in self.titulo:
                    libros_actualizados = self.gestor.get_libros_prestados()
                else:
                    # Por defecto, buscar todos
                    libros_actualizados = self.gestor.get_todos_los_libros()
                
                self.master.switch_frame(ListFrame, titulo=self.titulo, libros=libros_actualizados)
        except Exception as e:
            messagebox.showerror("Error", str(e))