"""
Utilidades para diálogos personalizados
"""
import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
import os

def confirmar(titulo: str, mensaje: str, parent=None) -> bool:
    """
    Muestra un diálogo de confirmación personalizado en español.
    
    Args:
        titulo: Título del diálogo
        mensaje: Mensaje a mostrar
        parent: Ventana padre (opcional)
    
    Returns:
        True si el usuario confirma, False si cancela
    """
    # Crear ventana personalizada - Más grande para que los botones no se aplasten
    dialog = ctk.CTkToplevel(parent)
    dialog.title(titulo)
    dialog.geometry("500x280")  # Más ancha y más alta
    dialog.resizable(False, False)
    dialog.transient(parent)
    dialog.grab_set()
    
    # Aplicar icono personalizado
    try:
        # Buscar el icono en la carpeta assets (3 niveles arriba desde gui/utils/)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(current_dir, "..", "..", "assets", "bibliohub_icon.png")
        icon_path = os.path.normpath(icon_path)
        
        if os.path.exists(icon_path):
            icon_image = tk.PhotoImage(file=icon_path)
            dialog.iconphoto(True, icon_image)
    except Exception:
        pass  # Continuar sin icono si hay error
    
    # Centrar la ventana
    dialog.update_idletasks()
    x = (dialog.winfo_screenwidth() // 2) - (500 // 2)
    y = (dialog.winfo_screenheight() // 2) - (280 // 2)
    dialog.geometry(f"500x280+{x}+{y}")
    
    # Variable para el resultado
    result = tk.BooleanVar()
    result.set(False)
    
    # Colores personalizados
    colors = {
        'primary': '#002333',
        'success': '#267365',
        'danger': '#F23030',
        'warning': '#F28705',
        'white': '#FFFFFF'
    }
    
    # Frame principal con más espacio
    main_frame = ctk.CTkFrame(dialog, fg_color=colors['white'])
    main_frame.pack(fill="both", expand=True, padx=25, pady=25)
    
    # Icono y título - Header más visible
    header_frame = ctk.CTkFrame(main_frame, fg_color="#1E40AF")  # Azul más claro
    header_frame.pack(fill="x", pady=(0, 20))
    
    ctk.CTkLabel(header_frame, 
                text=f"❓ {titulo}", 
                font=("Segoe UI", 18, "bold"),
                text_color="white").pack(pady=15)
    
    # Mensaje con más espacio
    ctk.CTkLabel(main_frame, 
                text=mensaje, 
                font=("Segoe UI", 13),
                wraplength=420,
                justify="center").pack(pady=20)
    
    # Botones con más espacio
    button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
    button_frame.pack(pady=20)
    
    def on_si():
        result.set(True)
        dialog.destroy()
    
    def on_no():
        result.set(False)
        dialog.destroy()
    
    # Botón Sí - Más grande y con mejor espaciado
    ctk.CTkButton(button_frame,
                 text="✅ Sí",
                 width=120,  # Más ancho
                 height=45,  # Más alto
                 fg_color="#10B981",  # Verde más claro
                 hover_color="#059669",  # Verde más oscuro al hover
                 text_color="white",
                 font=("Segoe UI", 14, "bold"),  # Fuente más grande
                 corner_radius=10,
                 command=on_si).pack(side="left", padx=15)  # Más separación
    
    # Botón No - Más grande y con mejor espaciado
    ctk.CTkButton(button_frame,
                 text="❌ No",
                 width=120,  # Más ancho
                 height=45,  # Más alto
                 fg_color="#EF4444",  # Rojo más claro
                 hover_color="#DC2626",  # Rojo más oscuro al hover
                 text_color="white",
                 font=("Segoe UI", 14, "bold"),  # Fuente más grande
                 corner_radius=10,
                 command=on_no).pack(side="left", padx=15)  # Más separación
    
    # Manejar cierre de ventana
    dialog.protocol("WM_DELETE_WINDOW", on_no)
    
    # Esperar a que se cierre el diálogo
    dialog.wait_window()
    
    return result.get()

def mostrar_info(titulo: str, mensaje: str, parent=None):
    """Muestra un diálogo de información personalizado."""
    messagebox.showinfo(titulo, mensaje, parent=parent)

def mostrar_error(titulo: str, mensaje: str, parent=None):
    """Muestra un diálogo de error personalizado."""
    messagebox.showerror(titulo, mensaje, parent=parent)

def mostrar_advertencia(titulo: str, mensaje: str, parent=None):
    """Muestra un diálogo de advertencia personalizado."""
    messagebox.showwarning(titulo, mensaje, parent=parent)
