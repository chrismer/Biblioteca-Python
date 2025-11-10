import customtkinter as ctk
from typing import TYPE_CHECKING
from tkinter import messagebox
from logic.models import Usuario
from gui.utils.dialogs import confirmar

if TYPE_CHECKING:
    from gui.app import App
    from logic.library_manager import GestorBiblioteca

class UsersFrame(ctk.CTkFrame):
    def __init__(self, master: 'App', gestor: 'GestorBiblioteca'):
        super().__init__(master)
        self.master = master
        self.gestor = gestor
        
        # Título
        ctk.CTkLabel(self, text="Gestión de Usuarios", font=("Arial", 20, "bold")).pack(pady=20)
        
        # Frame para botones principales
        buttons_frame = ctk.CTkFrame(self)
        buttons_frame.pack(pady=10, padx=20, fill="x")
        
        ctk.CTkButton(buttons_frame, text="➕ Agregar Usuario", 
                     command=self.mostrar_agregar_usuario).pack(side="left", padx=10, pady=10)
        ctk.CTkButton(buttons_frame, text="📋 Listar Usuarios", 
                     command=self.mostrar_lista_usuarios).pack(side="left", padx=10, pady=10)
        ctk.CTkButton(buttons_frame, text="🔍 Buscar Usuario", 
                     command=self.mostrar_buscar_usuario).pack(side="left", padx=10, pady=10)
        
        # Frame principal para contenido dinámico
        self.content_frame = ctk.CTkFrame(self)
        self.content_frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        # Botón volver
        ctk.CTkButton(self, text="← Volver", fg_color="gray", 
                     command=self._go_to_main_frame).pack(pady=20)
        
        # Mostrar lista por defecto
        self.mostrar_lista_usuarios()

    def _go_to_main_frame(self):
        """Navega al MainFrame, usando una importación local para evitar ciclos."""
        from .main_frame import MainFrame
        self.master.switch_frame(MainFrame)

    def mostrar_agregar_usuario(self):
        """Muestra el formulario para agregar usuario."""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        ctk.CTkLabel(self.content_frame, text="Agregar Nuevo Usuario", 
                    font=("Arial", 16, "bold")).pack(pady=10)
        
        # Formulario
        form_frame = ctk.CTkFrame(self.content_frame)
        form_frame.pack(pady=20, padx=20, fill="x")
        
        # Campos del formulario
        ctk.CTkLabel(form_frame, text="Nombre *").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.entry_nombre = ctk.CTkEntry(form_frame, width=300)
        self.entry_nombre.grid(row=0, column=1, padx=10, pady=5)
        
        ctk.CTkLabel(form_frame, text="Email").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.entry_email = ctk.CTkEntry(form_frame, width=300)
        self.entry_email.grid(row=1, column=1, padx=10, pady=5)
        
        ctk.CTkLabel(form_frame, text="Teléfono").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.entry_telefono = ctk.CTkEntry(form_frame, width=300)
        self.entry_telefono.grid(row=2, column=1, padx=10, pady=5)
        
        ctk.CTkLabel(form_frame, text="Dirección").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.entry_direccion = ctk.CTkEntry(form_frame, width=300)
        self.entry_direccion.grid(row=3, column=1, padx=10, pady=5)
        
        # Botones
        buttons_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        buttons_frame.grid(row=4, column=0, columnspan=2, pady=20)
        
        ctk.CTkButton(buttons_frame, text="Guardar Usuario", 
                     command=self.guardar_usuario).pack(side="left", padx=10)
        ctk.CTkButton(buttons_frame, text="Limpiar", fg_color="orange",
                     command=self.limpiar_formulario).pack(side="left", padx=10)

    def guardar_usuario(self):
        """Guarda un nuevo usuario."""
        try:
            nombre = self.entry_nombre.get().strip()
            email = self.entry_email.get().strip() if self.entry_email.get().strip() else None
            telefono = self.entry_telefono.get().strip() if self.entry_telefono.get().strip() else None
            direccion = self.entry_direccion.get().strip() if self.entry_direccion.get().strip() else None
            
            if not nombre:
                raise ValueError("El nombre es obligatorio")
            
            usuario_id = self.gestor.agregar_usuario(nombre, email, telefono, direccion)
            messagebox.showinfo("Éxito", f"Usuario '{nombre}' agregado correctamente (ID: {usuario_id})")
            self.limpiar_formulario()
            
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def limpiar_formulario(self):
        """Limpia el formulario de usuario."""
        self.entry_nombre.delete(0, 'end')
        self.entry_email.delete(0, 'end')
        self.entry_telefono.delete(0, 'end')
        self.entry_direccion.delete(0, 'end')

    def mostrar_lista_usuarios(self):
        """Muestra la lista de todos los usuarios."""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        ctk.CTkLabel(self.content_frame, text="Lista de Usuarios", 
                    font=("Arial", 16, "bold")).pack(pady=10)
        
        try:
            usuarios = self.gestor.get_todos_usuarios()
            
            if not usuarios:
                ctk.CTkLabel(self.content_frame, text="No hay usuarios registrados.", 
                           fg_color="orange").pack(pady=20)
                return
            
            # Frame con scroll para la tabla
            scroll_frame = ctk.CTkScrollableFrame(self.content_frame)
            scroll_frame.pack(pady=10, padx=10, fill="both", expand=True)
            
            # Encabezados
            headers = ["ID", "Nombre", "Email", "Teléfono", "Fecha Registro", "Estado", "Acciones"]
            for i, header in enumerate(headers):
                ctk.CTkLabel(scroll_frame, text=header, font=("Arial", 12, "bold")).grid(
                    row=0, column=i, padx=10, pady=5, sticky="w")
            
            # Datos de usuarios
            for row_num, usuario in enumerate(usuarios, start=1):
                ctk.CTkLabel(scroll_frame, text=str(usuario.id)).grid(row=row_num, column=0, padx=10, pady=2)
                ctk.CTkLabel(scroll_frame, text=usuario.nombre).grid(row=row_num, column=1, padx=10, pady=2)
                ctk.CTkLabel(scroll_frame, text=usuario.email or "N/A").grid(row=row_num, column=2, padx=10, pady=2)
                ctk.CTkLabel(scroll_frame, text=usuario.telefono or "N/A").grid(row=row_num, column=3, padx=10, pady=2)
                ctk.CTkLabel(scroll_frame, text=str(usuario.fecha_registro)).grid(row=row_num, column=4, padx=10, pady=2)
                
                estado_color = "green" if usuario.activo else "red"
                estado_texto = "Activo" if usuario.activo else "Inactivo"
                ctk.CTkLabel(scroll_frame, text=estado_texto, text_color=estado_color).grid(
                    row=row_num, column=5, padx=10, pady=2)
                
                # Botones de acción
                actions_frame = ctk.CTkFrame(scroll_frame, fg_color="transparent")
                actions_frame.grid(row=row_num, column=6, padx=10, pady=2)
                
                ctk.CTkButton(actions_frame, text="Ver Préstamos", width=100,
                             command=lambda u=usuario: self.ver_prestamos_usuario(u)).pack(side="left", padx=2)
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar usuarios: {str(e)}")

    def ver_prestamos_usuario(self, usuario: Usuario):
        """Muestra los préstamos de un usuario específico."""
        try:
            prestamos = self.gestor.get_prestamos_usuario(usuario.id)
            
            # Crear ventana emergente
            prestamos_window = ctk.CTkToplevel(self)
            prestamos_window.title(f"Préstamos de {usuario.nombre}")
            prestamos_window.geometry("800x600")
            
            ctk.CTkLabel(prestamos_window, text=f"Préstamos de {usuario.nombre}", 
                        font=("Arial", 16, "bold")).pack(pady=10)
            
            if not prestamos:
                ctk.CTkLabel(prestamos_window, text="Este usuario no tiene préstamos.", 
                           fg_color="blue").pack(pady=20)
                return
            
            # Frame con scroll
            scroll_frame = ctk.CTkScrollableFrame(prestamos_window)
            scroll_frame.pack(pady=10, padx=10, fill="both", expand=True)
            
            # Encabezados
            headers = ["ID", "Ejemplar", "Fecha Préstamo", "Fecha Vencimiento", "Estado", "Acciones"]
            for i, header in enumerate(headers):
                ctk.CTkLabel(scroll_frame, text=header, font=("Arial", 12, "bold")).grid(
                    row=0, column=i, padx=10, pady=5)
            
            # Datos de préstamos
            for row_num, prestamo in enumerate(prestamos, start=1):
                ctk.CTkLabel(scroll_frame, text=str(prestamo.id)).grid(row=row_num, column=0, padx=10, pady=2)
                ctk.CTkLabel(scroll_frame, text=f"Ejemplar #{prestamo.ejemplar_id}").grid(row=row_num, column=1, padx=10, pady=2)
                ctk.CTkLabel(scroll_frame, text=str(prestamo.fecha_prestamo)).grid(row=row_num, column=2, padx=10, pady=2)
                ctk.CTkLabel(scroll_frame, text=str(prestamo.fecha_devolucion_esperada)).grid(row=row_num, column=3, padx=10, pady=2)
                
                # Estado con color
                estado_color = "green" if prestamo.estado == "devuelto" else ("red" if prestamo.esta_vencido else "blue")
                ctk.CTkLabel(scroll_frame, text=prestamo.estado.title(), text_color=estado_color).grid(
                    row=row_num, column=4, padx=10, pady=2)
                
                # Botón devolver si está activo
                if prestamo.estado == "activo":
                    ctk.CTkButton(scroll_frame, text="Devolver", width=80,
                                 command=lambda p=prestamo: self.devolver_prestamo(p, prestamos_window)).grid(
                                 row=row_num, column=5, padx=10, pady=2)
                else:
                    ctk.CTkLabel(scroll_frame, text="—").grid(row=row_num, column=5, padx=10, pady=2)
            
            ctk.CTkButton(prestamos_window, text="Cerrar", 
                         command=prestamos_window.destroy).pack(pady=10)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar préstamos: {str(e)}")

    def devolver_prestamo(self, prestamo, window):
        """Devuelve un préstamo específico."""
        try:
            if confirmar("Confirmar Devolución", 
                         f"¿Seguro que quieres devolver este préstamo?", 
                         parent=window):
                
                if self.gestor.devolver_ejemplar(prestamo.ejemplar_id):
                    messagebox.showinfo("Éxito", "Préstamo devuelto correctamente.", parent=window)
                    window.destroy()
                    self.mostrar_lista_usuarios() 
                else:
                    messagebox.showerror("Error", "No se pudo devolver el préstamo.", parent=window)
        except Exception as e:
            messagebox.showerror("Error", str(e), parent=window)

    def mostrar_buscar_usuario(self):
        """Muestra el formulario para buscar usuario."""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        search_panel = ctk.CTkFrame(self.content_frame)
        search_panel.pack(pady=10, padx=10, fill="x")
        
        ctk.CTkLabel(search_panel, text="Buscar por nombre:").pack(side="left", padx=10)
        self.entry_buscar = ctk.CTkEntry(search_panel, width=300)
        self.entry_buscar.pack(side="left", padx=10, expand=True, fill="x")
        ctk.CTkButton(search_panel, text="Buscar", command=self.buscar_usuario).pack(side="left", padx=10)
        
        self.results_panel = ctk.CTkScrollableFrame(self.content_frame)
        self.results_panel.pack(pady=10, padx=10, fill="both", expand=True)
        ctk.CTkLabel(self.results_panel, text="Ingrese un término de búsqueda y presione 'Buscar'").pack(pady=20)

    def buscar_usuario(self):
        """Busca usuarios por nombre."""
        for widget in self.results_panel.winfo_children():
            widget.destroy()

        try:
            termino = self.entry_buscar.get().strip().lower()
            if not termino:
                messagebox.showwarning("Advertencia", "Ingrese un término de búsqueda")
                return
            
            usuarios = self.gestor.get_todos_usuarios()
            resultados = [u for u in usuarios if termino in u.nombre.lower()]
            
            if not resultados:
                ctk.CTkLabel(self.results_panel, text="No se encontraron usuarios.", 
                           fg_color="orange").pack(pady=20)
                return
            
            headers = ["ID", "Nombre", "Email", "Acciones"]
            for i, header in enumerate(headers):
                 ctk.CTkLabel(self.results_panel, text=header, font=("Arial", 12, "bold")).grid(row=0, column=i, padx=10, pady=5)

            for row_num, usuario in enumerate(resultados, start=1):
                ctk.CTkLabel(self.results_panel, text=str(usuario.id)).grid(row=row_num, column=0, padx=10, pady=2)
                ctk.CTkLabel(self.results_panel, text=usuario.nombre).grid(row=row_num, column=1, padx=10, pady=2)
                ctk.CTkLabel(self.results_panel, text=usuario.email or "N/A").grid(row=row_num, column=2, padx=10, pady=2)
                ctk.CTkButton(self.results_panel, text="Ver Préstamos", width=100, command=lambda u=usuario: self.ver_prestamos_usuario(u)).grid(row=row_num, column=3, padx=10, pady=2)
                
        except Exception as e:
            messagebox.showerror("Error", f"Error en la búsqueda: {str(e)}")
