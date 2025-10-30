import customtkinter as ctk
from PIL import Image
import os
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from gui.app import App
    from logic.library_manager import GestorBiblioteca

class BaseFrame(ctk.CTkFrame):
    """Clase base para todos los frames con fondo de imagen común."""
    
    def __init__(self, master: 'App', gestor: 'GestorBiblioteca', **kwargs):
        super().__init__(master, fg_color="#F8F9FA", **kwargs)
        self.master = master
        self.gestor = gestor
        
        # Colores compartidos - Paleta personalizada
        self.colors = {
            'primary': '#002333',      # Azul personalizado
            'secondary': '#64748B',    # Gris azulado
            'accent': '#002333',       # Azul personalizado
            'success': '#267365',      # Verde personalizado
            'warning': '#F28705',      # Naranja personalizado
            'danger': '#F23030',       # Rojo personalizado
            'light': '#F8FAFC',        # Gris muy claro
            'white': '#FFFFFF',        # Blanco
            'dark': '#1E293B',         # Gris oscuro
            'muted': '#94A3B8'         # Gris medio
        }
        
        # Configurar fondo de imagen
        self.setup_background()
        
        # Frame principal con scroll para el contenido
        self.setup_content_area()
    
    def setup_background(self):
        """Configura la imagen de fondo para toda la ventana."""
        try:
            if os.path.exists("assets/bg-bibliohub.png"):
                # Cargar imagen de fondo
                bg_image = Image.open("assets/bg-bibliohub.png")
                
                # Redimensionar imagen para cubrir toda la ventana
                bg_ctk_image = ctk.CTkImage(bg_image, size=(1400, 800))
                
                # Label con imagen de fondo que cubre toda la ventana
                self.bg_label = ctk.CTkLabel(self, image=bg_ctk_image, text="")
                self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
                
                print("✅ Fondo de imagen aplicado correctamente")
            else:
                print("ℹ️ Imagen de fondo no encontrada")
                
        except Exception as e:
            print(f"Error al cargar fondo: {e}")
    
    def setup_content_area(self):
        """Configura el área de contenido con scroll."""
        # Frame de contenido scrollable con fondo semitransparente
        self.content_frame = ctk.CTkScrollableFrame(
            self,
            fg_color=self.colors['light'],
            scrollbar_button_color=self.colors['primary'],
            scrollbar_button_hover_color=self.colors['accent'],
            corner_radius=0
        )
        self.content_frame.pack(fill="both", expand=True, padx=20, pady=20)
    
    def create_header(self, title: str, subtitle: str = ""):
        """Crea un header estándar para la ventana."""
        header_frame = ctk.CTkFrame(self.content_frame, fg_color=self.colors['primary'], corner_radius=15)
        header_frame.pack(fill="x", pady=(0, 20))
        
        # Título principal
        ctk.CTkLabel(header_frame, 
                    text=title, 
                    font=("Segoe UI", 24, "bold"),
                    text_color="white").pack(pady=(15, 5))
        
        # Subtítulo si se proporciona
        if subtitle:
            ctk.CTkLabel(header_frame, 
                        text=subtitle, 
                        font=("Segoe UI", 12),
                        text_color="white").pack(pady=(0, 15))
    
    def create_back_button(self, text="← Volver al Menú Principal"):
        """Crea un botón para volver al menú principal."""
        back_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        back_frame.pack(fill="x", pady=(20, 0))
        
        ctk.CTkButton(back_frame,
                     text=text,
                     font=("Segoe UI", 12),
                     width=200,
                     height=40,
                     fg_color=self.colors['secondary'],
                     hover_color=self.colors['muted'],
                     corner_radius=20,
                     command=lambda: self.master.switch_frame(self.master.main_frame_class)).pack()