import customtkinter as ctk
from tkinter import messagebox
from typing import TYPE_CHECKING, List
from logic.models import Libro, Estanteria

if TYPE_CHECKING:
    from gui.app import App
    from logic.library_manager import GestorBiblioteca

class MoveBookFrame(ctk.CTkFrame):
    def __init__(self, master: 'App', gestor: 'GestorBiblioteca'):
        super().__init__(master)
        self.master = master
        self.gestor = gestor
        self.libros = self.gestor.get_todos_los_libros()
        self.estanterias = self.gestor.get_todas_las_estanterias()
        self.selected_book = ctk.StringVar(value="Seleccione un libro...")
        self.selected_shelf = ctk.StringVar(value="Seleccione destino...")

        ctk.CTkLabel(self, text="Mover Libro de Estantería", font=("Arial", 20, "bold")).pack(pady=20)

        form_frame = ctk.CTkFrame(self)
        form_frame.pack(pady=20, padx=100)

        # 1. Selección de Libro
        ctk.CTkLabel(form_frame, text="Libro a Mover:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        libro_options = [f"{libro.id}: {libro.titulo}" for libro in self.libros]
        self.book_menu = ctk.CTkOptionMenu(form_frame, variable=self.selected_book, values=libro_options, command=self.on_book_select, width=350)
        self.book_menu.grid(row=0, column=1, padx=10, pady=10)

        # 2. Info de Estantería Actual
        ctk.CTkLabel(form_frame, text="Estantería Actual:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.current_shelf_label = ctk.CTkLabel(form_frame, text="---", fg_color="gray", corner_radius=5, width=350, height=28)
        self.current_shelf_label.grid(row=1, column=1, padx=10, pady=10)

        # 3. Selección de Estantería Destino
        ctk.CTkLabel(form_frame, text="Mover a:").grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.shelf_menu = ctk.CTkOptionMenu(form_frame, variable=self.selected_shelf, values=["Seleccione un libro primero..."], state="disabled", width=350)
        self.shelf_menu.grid(row=2, column=1, padx=10, pady=10)

        # --- Botones ---
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.pack(pady=30)
        
        ctk.CTkButton(button_frame, text="Mover Libro", command=self.mover_libro).pack(side="left", padx=10)
        ctk.CTkButton(button_frame, text="Volver", fg_color="gray", command=lambda: self.master.switch_frame(self.master.main_frame_class)).pack(side="left", padx=10)

    def on_book_select(self, selected_book_str: str):
        """Se activa cuando el usuario selecciona un libro."""
        book_id = int(selected_book_str.split(":")[0])
        libro_seleccionado = next((b for b in self.libros if b.id == book_id), None)
        
        if libro_seleccionado:
            estanteria_actual = next((e for e in self.estanterias if e.id == libro_seleccionado.estanteria_id), None)
            
            # Actualizar label de estantería actual
            if estanteria_actual:
                self.current_shelf_label.configure(text=estanteria_actual.nombre)
            
            # Actualizar opciones de estantería destino (todas menos la actual)
            shelf_options = [f"{e.id}: {e.nombre}" for e in self.estanterias if e.id != estanteria_actual.id]
            self.shelf_menu.configure(values=shelf_options, state="normal")
            self.selected_shelf.set("Seleccione destino...")

    def mover_libro(self):
        try:
            book_id_str = self.selected_book.get().split(":")[0]
            shelf_id_str = self.selected_shelf.get().split(":")[0]
            
            if not book_id_str.isdigit() or not shelf_id_str.isdigit():
                raise ValueError("Por favor, seleccione un libro y una estantería de destino.")
                
            book_id = int(book_id_str)
            shelf_id = int(shelf_id_str)
            
            self.gestor.mover_libro(book_id, shelf_id)
            
            messagebox.showinfo("Éxito", f"El libro ha sido movido correctamente.")
            self.master.switch_frame(self.master.main_frame_class)

        except Exception as e:
            messagebox.showerror("Error", str(e))