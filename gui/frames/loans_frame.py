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
                     command=lambda: self.master.switch_frame(self.master.main_frame_class)).pack(pady=20)
        
        # Mostrar préstamos activos por defecto
        self.mostrar_prestamos_activos()

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
        
        try:
            usuarios = self.gestor.get_todos_usuarios()
            if not usuarios:
                ctk.CTkLabel(form_frame, text="No hay usuarios registrados. Agregue un usuario primero.", 
                           fg_color="red").grid(row=0, column=1, padx=10, pady=5)
                return
            
            usuario_options = [f"{u.id} - {u.nombre}" for u in usuarios]
            self.usuario_combo = ctk.CTkComboBox(form_frame, values=usuario_options, width=300)
            self.usuario_combo.grid(row=0, column=1, padx=10, pady=5)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar usuarios: {str(e)}")
            return
        
        # Selección de ejemplar disponible
        ctk.CTkLabel(form_frame, text="Ejemplar *").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        
        try:
            ejemplares = self.gestor.get_ejemplares_disponibles()
            if not ejemplares:
                ctk.CTkLabel(form_frame, text="No hay ejemplares disponibles para préstamo.", 
                           fg_color="red").grid(row=1, column=1, padx=10, pady=5)
                return
            
            ejemplar_options = [f"{e.id} - {e.codigo_ejemplar}" for e in ejemplares]
            self.ejemplar_combo = ctk.CTkComboBox(form_frame, values=ejemplar_options, width=300)
            self.ejemplar_combo.grid(row=1, column=1, padx=10, pady=5)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar ejemplares: {str(e)}")
            return
        
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
        info_frame = ctk.CTkFrame(form_frame, fg_color="blue")
        info_frame.grid(row=4, column=0, columnspan=2, pady=10, padx=10, sticky="ew")
        
        fecha_devolucion = date.today() + timedelta(days=15)
        ctk.CTkLabel(info_frame, text=f"📅 Fecha de devolución esperada: {fecha_devolucion}", 
                    text_color="white").pack(pady=5)
        
        # Botones
        buttons_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        buttons_frame.grid(row=5, column=0, columnspan=2, pady=20)
        
        ctk.CTkButton(buttons_frame, text="Crear Préstamo", 
                     command=self.crear_prestamo).pack(side="left", padx=10)
        ctk.CTkButton(buttons_frame, text="Limpiar", fg_color="orange",
                     command=self.limpiar_formulario_prestamo).pack(side="left", padx=10)

    def crear_prestamo(self):
        """Crea un nuevo préstamo."""
        try:
            # Obtener datos del formulario
            usuario_selection = self.usuario_combo.get()
            ejemplar_selection = self.ejemplar_combo.get()
            dias_str = self.dias_spinbox.get()
            observaciones = self.observaciones_text.get("1.0", "end-1c").strip()
            
            if not usuario_selection or not ejemplar_selection:
                raise ValueError("Debe seleccionar usuario y ejemplar")
            
            # Extraer IDs
            usuario_id = int(usuario_selection.split(" - ")[0])
            ejemplar_id = int(ejemplar_selection.split(" - ")[0])
            
            try:
                dias_prestamo = int(dias_str)
                if dias_prestamo < 1 or dias_prestamo > 90:
                    raise ValueError("Los días de préstamo deben estar entre 1 y 90")
            except ValueError:
                raise ValueError("Los días de préstamo deben ser un número válido")
            
            # Crear préstamo
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
        self.usuario_combo.set("")
        self.ejemplar_combo.set("")
        self.dias_spinbox.delete(0, 'end')
        self.dias_spinbox.insert(0, "15")
        self.observaciones_text.delete("1.0", "end")

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
