import customtkinter as ctk
import tkinter as tk
import os
from logic.library_manager import GestorBiblioteca
from gui.frames.main_frame import MainFrame

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("BiblioHub - Sistema de Gestión Bibliotecaria")
        self.geometry("1400x800") 
        self.minsize(1200, 700)
        
        # Configurar icono personalizado
        self.set_custom_icon()
        
        # Configurar modo light y colores modernos
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        
        # Configurar colores personalizados
        self.configure(fg_color="#F8F9FA")
        
        self.gestor = GestorBiblioteca()
        
        self.current_frame = None
        self.switch_frame(MainFrame)

    def switch_frame(self, frame_class, **kwargs):
        """
        Cambia el frame visible. Acepta argumentos extra (**kwargs)
        y se los pasa al constructor del nuevo frame.
        """
        if self.current_frame:
            self.current_frame.destroy()
        
        self.current_frame = frame_class(self, self.gestor, **kwargs)
        self.current_frame.pack(fill="both", expand=True)

    def set_custom_icon(self):
        """Configura el icono personalizado de BiblioHub"""
        try:
            # Buscar el icono en la carpeta assets
            icon_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "bibliohub_icon.png")
            
            if os.path.exists(icon_path):
                # Para macOS/Linux - usar PhotoImage
                icon_image = tk.PhotoImage(file=icon_path)
                self.iconphoto(True, icon_image)
                
        except Exception as e:
            pass  # Continuar sin icono personalizado

    def destroy(self):
        self.gestor.cerrar()
        super().destroy()