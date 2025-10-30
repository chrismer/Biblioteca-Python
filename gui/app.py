import customtkinter as ctk
import tkinter as tk
import os
from logic.library_manager import GestorBiblioteca
from gui.frames.main_frame import MainFrame
from gui.frames.add_book_frame import AddBookFrame
from gui.frames.add_shelf_frame import AddShelfFrame 
from gui.frames.manage_shelves_frame import ManageShelvesFrame
from gui.frames.list_frame import ListFrame
from gui.frames.move_book_frame import MoveBookFrame
from gui.frames.search_book_frame import SearchBookFrame
from gui.frames.edit_book_frame import EditBookFrame

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
        
        self.main_frame_class = MainFrame 
        self.current_frame = None
        self.current_frame_title = ""
        self.switch_frame(self.main_frame_class)

    def switch_frame(self, frame_class, **kwargs):
        """
        Cambia el frame visible. Acepta argumentos extra (**kwargs)
        y se los pasa al constructor del nuevo frame.
        """
        if self.current_frame:
            self.current_frame.destroy()
        
        self.current_frame = frame_class(self, self.gestor, **kwargs)
        self.current_frame.pack(fill="both", expand=True)

        if 'titulo' in kwargs:
            self.current_frame_title = kwargs['titulo']

    def set_custom_icon(self):
        """Configura el icono personalizado de BiblioHub"""
        try:
            # Buscar el icono en la carpeta assets
            icon_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "bibliohub_icon.png")
            
            if os.path.exists(icon_path):
                # Para macOS/Linux - usar PhotoImage
                icon_image = tk.PhotoImage(file=icon_path)
                self.iconphoto(True, icon_image)
                print("✅ Icono personalizado aplicado")
            else:
                print("⚠️ No se encontró el icono personalizado")
                
        except Exception as e:
            print(f"⚠️ Error al cargar icono personalizado: {e}")
            # Continuar sin icono personalizado
            pass

    def destroy(self):
        self.gestor.cerrar()
        super().destroy()