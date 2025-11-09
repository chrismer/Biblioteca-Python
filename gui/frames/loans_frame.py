import customtkinter as ctk
from typing import TYPE_CHECKING, List
from tkinter import messagebox, ttk
from datetime import date, timedelta
from logic.models import Prestamo, Usuario, Ejemplar
from gui.utils.dialogs import confirmar

if TYPE_CHECKING:
    from gui.app import App
    from logic.library_manager import GestorBiblioteca

class LoansFrame(ctk.CTkFrame):
    def __init__(self, master: 'App', gestor: 'GestorBiblioteca'):
        super().__init__(master)
        self.master = master
        self.gestor = gestor
        
        # Título
        ctk.CTkLabel(self, text="Gestión de Préstamos", font=("Arial", 20, "bold")).pack(pady=20)
        
        # Frame para botones principales
        buttons_frame = ctk.CTkFrame(self)
        buttons_frame.pack(pady=10, padx=20, fill="x")
        
        ctk.CTkButton(buttons_frame, text="➕ Nuevo Préstamo", 
                     command=self.mostrar_nuevo_prestamo).pack(side="left", padx=10, pady=10)
        ctk.CTkButton(buttons_frame, text="📋 Préstamos Activos", 
                     command=self.mostrar_prestamos_activos).pack(side="left", padx=10, pady=10)
        ctk.CTkButton(buttons_frame, text="⚠️ Préstamos Vencidos", 
                     command=self.mostrar_prestamos_vencidos).pack(side="left", padx=10, pady=10)
        ctk.CTkButton(buttons_frame, text="📊 Historial", 
                     command=self.mostrar_historial_prestamos).pack(side="left", padx=10, pady=10)
        
        # Frame principal para contenido dinámico
        self.content_frame = ctk.CTkFrame(self)
        self.content_frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        # Botón volver
        ctk.CTkButton(self, text="← Volver", fg_color="gray", 
                     command=self._go_to_main_frame).pack(pady=20)
        
        # Mostrar préstamos activos por defecto
        self.mostrar_prestamos_activos()

    def _go_to_main_frame(self):
        """Navega al MainFrame, usando una importación local para evitar ciclos."""
        from .main_frame import MainFrame
        self.master.switch_frame(MainFrame)

    def limpiar_content_frame(self):
        """Limpia el frame de contenido."""
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def mostrar_nuevo_prestamo(self):
        """Muestra el formulario para crear un nuevo préstamo."""
        self.limpiar_content_frame()
        
        ctk.CTkLabel(self.content_frame, text="Crear Nuevo Préstamo", 
                    font=("Arial", 16, "bold")).pack(pady=10)
        
        # Formulario
        form_frame = ctk.CTkFrame(self.content_frame)
        form_frame.pack(pady=20, padx=20, fill="x")
        
        # Selección de usuario
        ctk.CTkLabel(form_frame, text="Usuario *").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        
        # Campo de búsqueda de usuario con autocompletado
        self.usuario_entry = ctk.CTkEntry(form_frame, placeholder_text="Buscar por nombre...", width=300)
        self.usuario_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        self.sugerencias_frame = ctk.CTkScrollableFrame(form_frame, width=280, height=100)
        # El frame de sugerencias se mostrará cuando sea necesario

        self.usuario_entry.bind("<KeyRelease>", self.actualizar_sugerencias_usuario)
        
        # Variable para almacenar el ID del usuario seleccionado
        self.usuario_seleccionado_id = None
        self.usuarios_cache = self.gestor.get_todos_usuarios()

        # Búsqueda de ejemplar
        ctk.CTkLabel(form_frame, text="Ejemplar *").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        
        self.ejemplar_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        self.ejemplar_frame.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        self.ejemplar_entry = ctk.CTkEntry(self.ejemplar_frame, placeholder_text="Buscar por código o título...", width=300)
        self.ejemplar_entry.pack(side="left")

        self.sugerencias_ejemplar_frame = ctk.CTkScrollableFrame(form_frame, width=280, height=100)
        # Se mostrará cuando sea necesario

        # Vincular evento de tecleo a la búsqueda
        self.ejemplar_entry.bind("<KeyRelease>", self.buscar_ejemplar_on_typing)

        # Variable para almacenar el ID del ejemplar encontrado
        self.ejemplar_encontrado_id = None
        
        # Días de préstamo
        ctk.CTkLabel(form_frame, text="Días de préstamo").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.dias_spinbox = ctk.CTkEntry(form_frame, width=100)
        self.dias_spinbox.grid(row=2, column=1, padx=10, pady=5, sticky="w")
        self.dias_spinbox.insert(0, "15")  # Valor por defecto
        
        # Observaciones
        ctk.CTkLabel(form_frame, text="Observaciones").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.observaciones_text = ctk.CTkTextbox(form_frame, width=300, height=60)
        self.observaciones_text.grid(row=3, column=1, padx=10, pady=5)
        
        # Información adicional
        self.info_frame = ctk.CTkFrame(form_frame, fg_color="blue")
        self.info_frame.grid(row=4, column=0, columnspan=2, pady=10, padx=10, sticky="ew")

        self.fecha_devolucion_label = ctk.CTkLabel(self.info_frame, text="", text_color="white")
        self.fecha_devolucion_label.pack(pady=5)
        self.actualizar_fecha_devolucion() # Llamada inicial

        # Vincular evento al spinbox
        self.dias_spinbox.bind("<KeyRelease>", lambda event: self.actualizar_fecha_devolucion())
        
        # Botones
        buttons_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        buttons_frame.grid(row=5, column=0, columnspan=2, pady=20)
        
        ctk.CTkButton(buttons_frame, text="Crear Préstamo", 
                     command=self.crear_prestamo).pack(side="left", padx=10)
        ctk.CTkButton(buttons_frame, text="Limpiar", fg_color="orange",
                     command=self.limpiar_formulario_prestamo).pack(side="left", padx=10)

    def seleccionar_usuario(self, usuario):
        """Maneja la selección de un usuario de la lista de sugerencias."""
        self.usuario_entry.delete(0, 'end')
        self.usuario_entry.insert(0, f"{usuario.id} - {usuario.nombre}")
        self.usuario_seleccionado_id = usuario.id
        self.sugerencias_frame.place_forget()

    def actualizar_sugerencias_usuario(self, event):
        """Filtra y muestra las sugerencias de usuarios según el texto de entrada."""
        termino = self.usuario_entry.get().lower()

        for widget in self.sugerencias_frame.winfo_children():
            widget.destroy()

        if not termino:
            self.sugerencias_frame.place_forget()
            self.usuario_seleccionado_id = None
            return

        sugerencias = [u for u in self.usuarios_cache if termino in u.nombre.lower()]

        if sugerencias:
            entry_x = self.usuario_entry.winfo_x()
            entry_y = self.usuario_entry.winfo_y()
            entry_height = self.usuario_entry.winfo_height()

            self.sugerencias_frame.place(x=entry_x, y=entry_y + entry_height)
            self.sugerencias_frame.lift()

            for usuario in sugerencias:
                texto = f"{usuario.id} - {usuario.nombre}"
                ctk.CTkButton(
                    self.sugerencias_frame,
                    text=texto,
                    command=lambda u=usuario: self.seleccionar_usuario(u),
                    anchor="w"
                ).pack(fill="x", padx=2, pady=2)
        else:
            self.sugerencias_frame.place_forget()
            self.usuario_seleccionado_id = None

    def actualizar_fecha_devolucion(self):
        """Actualiza la etiqueta de fecha de devolución según los días introducidos."""
        try:
            dias = int(self.dias_spinbox.get())
            if dias > 0:
                fecha_devolucion = date.today() + timedelta(days=dias)
                self.fecha_devolucion_label.configure(text=f"📅 Fecha de devolución esperada: {fecha_devolucion}")
            else:
                self.fecha_devolucion_label.configure(text="📅 Ingrese un número de días válido")
        except (ValueError, TypeError):
            self.fecha_devolucion_label.configure(text="📅 Ingrese un número de días válido")

    def seleccionar_ejemplar(self, ejemplar, titulo_libro):
        """Maneja la selección de un ejemplar de la lista de sugerencias."""
        self.ejemplar_entry.delete(0, 'end')
        self.ejemplar_entry.insert(0, f"{ejemplar.codigo_ejemplar} - {titulo_libro}")
        self.ejemplar_encontrado_id = ejemplar.id
        self.sugerencias_ejemplar_frame.place_forget()

    def buscar_ejemplar_on_typing(self, event):
        """Filtra y muestra sugerencias de ejemplares."""
        termino = self.ejemplar_entry.get().strip()

        for widget in self.sugerencias_ejemplar_frame.winfo_children():
            widget.destroy()

        if not termino:
            self.sugerencias_ejemplar_frame.place_forget()
            self.ejemplar_encontrado_id = None
            return

        try:
            sugerencias = self.gestor.buscar_ejemplares_disponibles(termino)

            if sugerencias:
                frame_x = self.ejemplar_frame.winfo_x()
                frame_y = self.ejemplar_frame.winfo_y()
                entry_height = self.ejemplar_entry.winfo_height()

                self.sugerencias_ejemplar_frame.place(x=frame_x, y=frame_y + entry_height)
                self.sugerencias_ejemplar_frame.lift()

                for ejemplar, titulo_libro in sugerencias:
                    texto = f"{ejemplar.codigo_ejemplar} - {titulo_libro}"
                    ctk.CTkButton(
                        self.sugerencias_ejemplar_frame,
                        text=texto,
                        command=lambda e=ejemplar, t=titulo_libro: self.seleccionar_ejemplar(e, t),
                        anchor="w"
                    ).pack(fill="x", padx=2, pady=2)
            else:
                self.sugerencias_ejemplar_frame.place_forget()
                self.ejemplar_encontrado_id = None
        except Exception as e:
            print(f"Error buscando ejemplares: {e}")

    def crear_prestamo(self):
        """Crea un nuevo préstamo."""
        try:
            dias_str = self.dias_spinbox.get()
            observaciones = self.observaciones_text.get("1.0", "end-1c").strip()
            
            if self.usuario_seleccionado_id is None or self.ejemplar_encontrado_id is None:
                raise ValueError("Debe seleccionar un usuario y un ejemplar válido y disponible")
            
            usuario_id = self.usuario_seleccionado_id
            ejemplar_id = self.ejemplar_encontrado_id
            
            try:
                dias_prestamo = int(dias_str)
                if dias_prestamo < 1 or dias_prestamo > 90:
                    raise ValueError("Los días de préstamo deben estar entre 1 y 90")
            except (ValueError, TypeError):
                raise ValueError("Los días de préstamo deben ser un número válido")
            
            prestamo_id = self.gestor.prestar_ejemplar(
                ejemplar_id, usuario_id, dias_prestamo,
                observaciones if observaciones else None
            )
            
            messagebox.showinfo("Éxito", f"Préstamo creado correctamente (ID: {prestamo_id})")
            self.mostrar_prestamos_activos()
            
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def limpiar_formulario_prestamo(self):
        """Limpia el formulario de préstamo."""
        self.usuario_entry.delete(0, 'end')
        self.usuario_seleccionado_id = None
        self.sugerencias_frame.grid_remove()
        self.ejemplar_entry.delete(0, 'end')
        self.ejemplar_encontrado_id = None
        self.dias_spinbox.delete(0, 'end')
        self.dias_spinbox.insert(0, "15")
        self.observaciones_text.delete("1.0", "end")
        self.actualizar_fecha_devolucion()

    def mostrar_prestamos_activos(self):
        """Muestra la lista de préstamos activos."""
        self.limpiar_content_frame()
        
        ctk.CTkLabel(self.content_frame, text="Préstamos Activos", 
                    font=("Arial", 16, "bold")).pack(pady=10)
        
        try:
            prestamos = self.gestor.get_prestamos_activos()
            
            if not prestamos:
                ctk.CTkLabel(self.content_frame, text="No hay préstamos activos.", 
                           fg_color="blue").pack(pady=20)
                return
            
            # Frame con scroll para la tabla
            scroll_frame = ctk.CTkScrollableFrame(self.content_frame)
            scroll_frame.pack(pady=10, padx=10, fill="both", expand=True)
            
            # Encabezados
            headers = ["ID", "Usuario", "Libro/Ejemplar", "Fecha Préstamo", "Vencimiento", "Días Restantes", "Estado", "Acciones"]
            for i, header in enumerate(headers):
                ctk.CTkLabel(scroll_frame, text=header, font=("Arial", 12, "bold")).grid(
                    row=0, column=i, padx=5, pady=5, sticky="w")
            
            # Datos de préstamos
            for row_num, prestamo in enumerate(prestamos, start=1):
                # Obtener información adicional
                usuario = self.gestor.get_usuario(prestamo.usuario_id)
                ejemplar = self.gestor.db.get_ejemplar(prestamo.ejemplar_id)
                
                # Obtener información del libro
                libro_info = "N/A"
                if ejemplar:
                    libro = self.gestor.db.get_libro_por_id(ejemplar.libro_id)
                    if libro:
                        libro_info = f"{libro.titulo}\n{ejemplar.codigo_ejemplar}"
                    else:
                        libro_info = ejemplar.codigo_ejemplar
                
                dias_restantes = (prestamo.fecha_devolucion_esperada - date.today()).days
                
                ctk.CTkLabel(scroll_frame, text=str(prestamo.id)).grid(row=row_num, column=0, padx=5, pady=2)
                ctk.CTkLabel(scroll_frame, text=usuario.nombre if usuario else "N/A").grid(row=row_num, column=1, padx=5, pady=2)
                ctk.CTkLabel(scroll_frame, text=libro_info, justify="left").grid(row=row_num, column=2, padx=5, pady=2)
                ctk.CTkLabel(scroll_frame, text=str(prestamo.fecha_prestamo)).grid(row=row_num, column=3, padx=5, pady=2)
                ctk.CTkLabel(scroll_frame, text=str(prestamo.fecha_devolucion_esperada)).grid(row=row_num, column=4, padx=5, pady=2)
                
                # Días restantes con color
                color_dias = "red" if dias_restantes < 0 else ("orange" if dias_restantes <= 3 else "green")
                ctk.CTkLabel(scroll_frame, text=str(dias_restantes), text_color=color_dias).grid(row=row_num, column=5, padx=5, pady=2)
                
                # Estado
                estado_text = "Vencido" if prestamo.esta_vencido else "Activo"
                estado_color = "red" if prestamo.esta_vencido else "green"
                ctk.CTkLabel(scroll_frame, text=estado_text, text_color=estado_color).grid(row=row_num, column=6, padx=5, pady=2)
                
                # Botones de acción
                actions_frame = ctk.CTkFrame(scroll_frame, fg_color="transparent")
                actions_frame.grid(row=row_num, column=7, padx=5, pady=2)
                
                ctk.CTkButton(actions_frame, text="Devolver", width=80,
                             command=lambda p=prestamo: self.devolver_prestamo(p)).pack(side="left", padx=2)
                
                if not prestamo.esta_vencido:
                    ctk.CTkButton(actions_frame, text="Renovar", width=70, fg_color="orange",
                                 command=lambda p=prestamo: self.renovar_prestamo(p)).pack(side="left", padx=2)
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar préstamos: {str(e)}")

    def mostrar_prestamos_vencidos(self):
        """Muestra la lista de préstamos vencidos."""
        self.limpiar_content_frame()
        
        ctk.CTkLabel(self.content_frame, text="⚠️ Préstamos Vencidos", 
                    font=("Arial", 16, "bold"), text_color="red").pack(pady=10)
        
        try:
            prestamos = self.gestor.get_prestamos_vencidos()
            
            if not prestamos:
                ctk.CTkLabel(self.content_frame, text="¡Excelente! No hay préstamos vencidos.", 
                           fg_color="green").pack(pady=20)
                return
            
            # Alerta
            alert_frame = ctk.CTkFrame(self.content_frame, fg_color="red")
            alert_frame.pack(pady=10, padx=20, fill="x")
            ctk.CTkLabel(alert_frame, text=f"⚠️ Hay {len(prestamos)} préstamos vencidos que requieren atención inmediata", 
                        text_color="white", font=("Arial", 14, "bold")).pack(pady=10)
            
            # Frame con scroll para la tabla
            scroll_frame = ctk.CTkScrollableFrame(self.content_frame)
            scroll_frame.pack(pady=10, padx=10, fill="both", expand=True)
            
            # Encabezados
            headers = ["ID", "Usuario", "Ejemplar", "Fecha Préstamo", "Vencimiento", "Días Vencido", "Acciones"]
            for i, header in enumerate(headers):
                ctk.CTkLabel(scroll_frame, text=header, font=("Arial", 12, "bold")).grid(
                    row=0, column=i, padx=5, pady=5, sticky="w")
            
            # Datos de préstamos vencidos
            for row_num, prestamo in enumerate(prestamos, start=1):
                usuario = self.gestor.get_usuario(prestamo.usuario_id)
                ejemplar = self.gestor.db.get_ejemplar(prestamo.ejemplar_id)
                
                dias_vencido = prestamo.dias_vencimiento
                
                ctk.CTkLabel(scroll_frame, text=str(prestamo.id)).grid(row=row_num, column=0, padx=5, pady=2)
                ctk.CTkLabel(scroll_frame, text=usuario.nombre if usuario else "N/A").grid(row=row_num, column=1, padx=5, pady=2)
                ctk.CTkLabel(scroll_frame, text=ejemplar.codigo_ejemplar if ejemplar else "N/A").grid(row=row_num, column=2, padx=5, pady=2)
                ctk.CTkLabel(scroll_frame, text=str(prestamo.fecha_prestamo)).grid(row=row_num, column=3, padx=5, pady=2)
                ctk.CTkLabel(scroll_frame, text=str(prestamo.fecha_devolucion_esperada)).grid(row=row_num, column=4, padx=5, pady=2)
                ctk.CTkLabel(scroll_frame, text=str(dias_vencido), text_color="red", font=("Arial", 12, "bold")).grid(row=row_num, column=5, padx=5, pady=2)
                
                # Botones de acción
                actions_frame = ctk.CTkFrame(scroll_frame, fg_color="transparent")
                actions_frame.grid(row=row_num, column=6, padx=5, pady=2)
                
                ctk.CTkButton(actions_frame, text="Devolver", width=80, fg_color="red",
                             command=lambda p=prestamo: self.devolver_prestamo(p)).pack(side="left", padx=2)
                ctk.CTkButton(actions_frame, text="Contactar", width=80, fg_color="orange",
                             command=lambda u=usuario: self.contactar_usuario(u)).pack(side="left", padx=2)
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar préstamos vencidos: {str(e)}")

    def devolver_prestamo(self, prestamo: Prestamo):
        """Devuelve un préstamo específico."""
        confirmado = False
        try:
            usuario = self.gestor.get_usuario(prestamo.usuario_id)
            ejemplar = self.gestor.db.get_ejemplar(prestamo.ejemplar_id)
            
            confirmado = confirmar(
                "Confirmar Devolución", 
                f"¿Confirma la devolución del ejemplar {ejemplar.codigo_ejemplar if ejemplar else 'N/A'} "
                f"por {usuario.nombre if usuario else 'N/A'}?", 
                parent=self
            )
            
            if confirmado:
                if self.gestor.devolver_ejemplar(prestamo.ejemplar_id):
                    messagebox.showinfo("Éxito", "Préstamo devuelto correctamente.")
                else:
                    messagebox.showerror("Error", "No se pudo procesar la devolución en la base de datos.")
            else:
                # El usuario canceló, no mostrar ningún mensaje.
                pass

        except Exception as e:
            messagebox.showerror("Error Crítico", f"Ocurrió un error inesperado: {str(e)}")
        finally:
            self.mostrar_prestamos_activos()

    def renovar_prestamo(self, prestamo: Prestamo):
        """Renueva un préstamo por días adicionales."""
        try:
            # Ventana para renovación
            renovar_window = ctk.CTkToplevel(self)
            renovar_window.title("Renovar Préstamo")
            renovar_window.geometry("400x300")
            
            ctk.CTkLabel(renovar_window, text="Renovar Préstamo", 
                        font=("Arial", 16, "bold")).pack(pady=10)
            
            usuario = self.gestor.get_usuario(prestamo.usuario_id)
            ejemplar = self.gestor.db.get_ejemplar(prestamo.ejemplar_id)
            
            info_text = f"Usuario: {usuario.nombre if usuario else 'N/A'}\n"
            info_text += f"Ejemplar: {ejemplar.codigo_ejemplar if ejemplar else 'N/A'}\n"
            info_text += f"Vencimiento actual: {prestamo.fecha_devolucion_esperada}"
            
            ctk.CTkLabel(renovar_window, text=info_text).pack(pady=10)
            
            ctk.CTkLabel(renovar_window, text="Días adicionales:").pack(pady=5)
            dias_entry = ctk.CTkEntry(renovar_window, width=100)
            dias_entry.pack(pady=5)
            dias_entry.insert(0, "15")
            
            def confirmar_renovacion():
                try:
                    dias_adicionales = int(dias_entry.get())
                    if dias_adicionales < 1 or dias_adicionales > 30:
                        raise ValueError("Los días adicionales deben estar entre 1 y 30")
                    
                    if prestamo.renovar(dias_adicionales):
                        messagebox.showinfo("Éxito", f"Préstamo renovado por {dias_adicionales} días")
                        renovar_window.destroy()
                        self.mostrar_prestamos_activos()
                    else:
                        messagebox.showerror("Error", "No se pudo renovar el préstamo")
                        
                except ValueError as e:
                    messagebox.showerror("Error", str(e))
            
            ctk.CTkButton(renovar_window, text="Renovar", 
                         command=confirmar_renovacion).pack(pady=10)
            ctk.CTkButton(renovar_window, text="Cancelar", fg_color="gray",
                         command=renovar_window.destroy).pack(pady=5)
            
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def contactar_usuario(self, usuario: Usuario):
        """Muestra información de contacto del usuario."""
        if not usuario:
            messagebox.showwarning("Advertencia", "Información de usuario no disponible")
            return
        
        info_text = f"Información de contacto:\n\n"
        info_text += f"Nombre: {usuario.nombre}\n"
        info_text += f"Email: {usuario.email or 'No proporcionado'}\n"
        info_text += f"Teléfono: {usuario.telefono or 'No proporcionado'}\n"
        info_text += f"Dirección: {usuario.direccion or 'No proporcionada'}"
        
        messagebox.showinfo(f"Contactar a {usuario.nombre}", info_text)

    def mostrar_historial_prestamos(self):
        """Muestra el historial completo de préstamos."""
        self.limpiar_content_frame()
        
        ctk.CTkLabel(self.content_frame, text="📊 Historial de Préstamos", 
                    font=("Arial", 16, "bold")).pack(pady=10)
        
        
        ctk.CTkLabel(self.content_frame, text="Funcionalidad en desarrollo...\n\nAquí se mostrará el historial completo de préstamos con filtros avanzados.", 
                    fg_color="blue").pack(pady=50)
