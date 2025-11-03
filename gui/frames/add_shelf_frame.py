import customtkinter as ctk
from tkinter import messagebox
from typing import TYPE_CHECKING
from .main_frame import MainFrame

if TYPE_CHECKING:
    from gui.app import App
    from logic.library_manager import GestorBiblioteca

class AddShelfFrame(ctk.CTkFrame):
    def __init__(self, master: 'App', gestor: 'GestorBiblioteca'):
        super().__init__(master)
        self.master = master
        self.gestor = gestor

        # Título
        ctk.CTkLabel(self, text="Agregar Nueva Estantería", font=("Arial", 20, "bold")).pack(pady=20)
        
        # --- Frame contenedor para el formulario ---
        form_frame = ctk.CTkFrame(self)
        form_frame.pack(pady=10, padx=50)

        form_frame.grid_columnconfigure(0, weight=0)
        form_frame.grid_columnconfigure(1, weight=1)

        # Formulario
        ctk.CTkLabel(form_frame, text="Nombre:").grid(row=1, column=0, padx=(20, 5), pady=10, sticky="e")
        self.nombre_entry = ctk.CTkEntry(form_frame, placeholder_text="Ej: Fantasía")
        self.nombre_entry.grid(row=0, column=1, padx=(5, 20), pady=10, sticky="ew")

        ctk.CTkLabel(form_frame, text="Capacidad:").grid(row=2, column=0, padx=(20, 5), pady=10, sticky="e")
        self.capacidad_entry = ctk.CTkEntry(form_frame, placeholder_text="Ej: 50")
        self.capacidad_entry.grid(row=1, column=1, padx=(5, 20), pady=10, sticky="ew")

        # Botones
        button_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        button_frame.grid(row=2, column=0, columnspan=2, pady=20)

        ctk.CTkButton(button_frame, text="Guardar Estantería", command=self.guardar_estanteria).pack(side="left", padx=10)
        ctk.CTkButton(button_frame, text="Volver", fg_color="gray", command=lambda: self.master.switch_frame(MainFrame)).pack(side="left", padx=10)

    def guardar_estanteria(self):
        nombre = self.nombre_entry.get()
        capacidad_str = self.capacidad_entry.get()

        try:
            if not capacidad_str.isdigit():
                raise ValueError("La capacidad debe ser un número entero.")
            capacidad = int(capacidad_str)

            self.gestor.agregar_estanteria(nombre, capacidad)
            messagebox.showinfo("Éxito", f"Estantería '{nombre}' agregada correctamente.")
            self.master.switch_frame(MainFrame) # Vuelve al menú principal

        except Exception as e:
            messagebox.showerror("Error de Validación", str(e))