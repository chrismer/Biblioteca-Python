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
    # Crear ventana personalizada
    dialog = ctk.CTkToplevel(parent)
    dialog.title(titulo)
    dialog.geometry("520x320")
    dialog.resizable(False, False)
    dialog.transient(parent)
    dialog.grab_set()
    
    # Aplicar icono personalizado
    try:
        # Buscar el icono en la carpeta assets
        current_dir = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(current_dir, "..", "..", "assets", "bibliohub_icon.png")
        icon_path = os.path.normpath(icon_path)
        
        if os.path.exists(icon_path):
            icon_image = tk.PhotoImage(file=icon_path)
            dialog.iconphoto(True, icon_image)
    except Exception:
        pass  
    
    # Centrar la ventana
    dialog.update_idletasks()
    x = (dialog.winfo_screenwidth() // 2) - (520 // 2)
    y = (dialog.winfo_screenheight() // 2) - (320 // 2)
    dialog.geometry(f"520x320+{x}+{y}")
    
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
    
    # Frame principal
    main_frame = ctk.CTkFrame(dialog, fg_color=colors['white'])
    main_frame.pack(fill="both", expand=True, padx=20, pady=20)
    
    # Icono y título
    header_frame = ctk.CTkFrame(main_frame, fg_color="#1E40AF") 
    header_frame.pack(fill="x", pady=(0, 15))
    
    ctk.CTkLabel(header_frame, 
                text=f"❓ {titulo}", 
                font=("Segoe UI", 18, "bold"),
                text_color="white").pack(pady=12)
    
    ctk.CTkLabel(main_frame, 
                text=mensaje, 
                font=("Segoe UI", 13),
                wraplength=450,
                justify="center").pack(pady=15)
    
    button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
    button_frame.pack(pady=15)
    
    # centrar
    button_frame.grid_columnconfigure(0, weight=1)
    button_frame.grid_columnconfigure(1, weight=1)
    
    def on_si():
        result.set(True)
        dialog.destroy()
    
    def on_no():
        result.set(False)
        dialog.destroy()
    
    # Botón Sí 
    btn_si = ctk.CTkButton(button_frame,
                           text="✅ Sí",
                           width=140,
                           height=45, 
                           fg_color="#10B981",
                           hover_color="#059669",
                           text_color="white",
                           font=("Segoe UI", 14, "bold"), 
                           corner_radius=10,
                           command=on_si)
    btn_si.grid(row=0, column=0, padx=10, pady=5)
    
    # Botón No 
    btn_no = ctk.CTkButton(button_frame,
                           text="❌ No",
                           width=140,  
                           height=45,  
                           fg_color="#EF4444",  
                           hover_color="#DC2626",  
                           text_color="white",
                           font=("Segoe UI", 14, "bold"),  
                           corner_radius=10,
                           command=on_no)
    btn_no.grid(row=0, column=1, padx=10, pady=5) 
    
    # Manejar cierre de ventana
    dialog.protocol("WM_DELETE_WINDOW", on_no)
    
    # Esperar a que se cierre el diálogo
    dialog.wait_window()
    
    return result.get()
