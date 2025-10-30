import customtkinter as ctk
from tkinter import messagebox
from typing import TYPE_CHECKING, List
from gui.utils.helpers import borrar_widgets
from .base_frame import BaseFrame
from logic.models import Libro, Ejemplar # Importar modelos
from gui.utils.dialogs import confirmar # Importar diálogos

if TYPE_CHECKING:
    from gui.app import App
    from logic.library_manager import GestorBiblioteca

class SearchBookFrame(BaseFrame):
    def __init__(self, master: 'App', gestor: 'GestorBiblioteca'):
        super().__init__(master, gestor)
        self.setup_interface()

    def setup_interface(self):
        """Configura la interfaz de búsqueda."""
        # Header
        self.create_header("🔍 Buscar Libros", "Encuentra libros por título, autor, código o ISBN")

        # Panel de Búsqueda
        search_panel = ctk.CTkFrame(self.content_frame, fg_color=self.colors['white'], corner_radius=15)
        search_panel.pack(pady=(10, 5), fill="x", padx=20)
        
        ctk.CTkLabel(search_panel, text="Término de Búsqueda:", font=("Segoe UI", 14, "bold"), text_color=self.colors['primary']).pack(side="left", padx=(20, 10), pady=15)
        self.entry_buscar = ctk.CTkEntry(search_panel, width=300, placeholder_text="Escribe aquí y presiona Enter...", font=("Segoe UI", 12))
        self.entry_buscar.pack(side="left", padx=10, expand=True, fill="x", pady=15)
        self.entry_buscar.bind("<Return>", lambda event: self.buscar_libros())
        
        ctk.CTkButton(search_panel, text="🔍 Buscar", 
                     command=self.buscar_libros,
                     font=("Segoe UI", 12, "bold"),
                     fg_color=self.colors['primary'],
                     hover_color=self.colors['accent']).pack(side="left", padx=(0, 20), pady=15)
     
        # Panel de Resultados (dinámico)
        self.results_panel = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        self.results_panel.pack(pady=10, fill="both", expand=True, padx=20)
        
        # Mensaje inicial
        ctk.CTkLabel(self.results_panel, text="Ingrese un término de búsqueda para comenzar...", 
                    font=("Segoe UI", 14), text_color=self.colors['secondary']).pack(pady=40)
        
        # Botón volver
        self.create_back_button()

    def buscar_libros(self):
        """Inicia el proceso de búsqueda y actualiza la UI."""
        termino = self.entry_buscar.get().strip()
        if not termino:
            borrar_widgets(self.results_panel)
            ctk.CTkLabel(self.results_panel, text="Por favor, ingrese un término de búsqueda.", 
                        font=("Segoe UI", 14), text_color=self.colors['warning']).pack(pady=40)
            return

        # Mostrar indicador de búsqueda
        borrar_widgets(self.results_panel)
        ctk.CTkLabel(self.results_panel, text=f"🔍 Buscando '{termino}'...", 
                    font=("Segoe UI", 14), text_color=self.colors['secondary']).pack(pady=40)
        
        # Usar 'after' para permitir que la UI se actualice antes de la búsqueda
        self.after(50, lambda: self._perform_search(termino))

    def _perform_search(self, termino):
        """Ejecuta la búsqueda en segundo plano y llama a mostrar_resultados."""
        try:
            resultados = self.gestor.buscar_libros(termino)
            self.mostrar_resultados(resultados, termino)
        except Exception as e:
            self.mostrar_resultados([], termino, error=str(e))

    def mostrar_resultados(self, resultados: List[Libro], termino: str, error: str = None):
        """Muestra los resultados de la búsqueda o un mensaje de error/no encontrado."""
        borrar_widgets(self.results_panel)

        # Manejo de errores
        if error:
            error_frame = ctk.CTkFrame(self.results_panel, fg_color=self.colors['danger'], corner_radius=15)
            error_frame.pack(pady=20, padx=20, fill="x")
            ctk.CTkLabel(error_frame, text=f"💥 Error en la búsqueda: {error}", 
                        text_color="white", font=("Segoe UI", 12)).pack(pady=15)
            return

        # Mensaje de no encontrados
        if not resultados:
            no_results_frame = ctk.CTkFrame(self.results_panel, fg_color=self.colors['warning'], corner_radius=15)
            no_results_frame.pack(pady=20, padx=20, fill="x")
            ctk.CTkLabel(no_results_frame, 
                       text=f"❌ No se encontraron libros para '{termino}'\n\n💡 Sugerencias:\n• Verifica la ortografía\n• Usa términos más generales\n• Prueba con el nombre del autor", 
                       text_color="white", justify="left", font=("Segoe UI", 12)).pack(pady=15, padx=20)
            return

        # Header de resultados
        results_header = ctk.CTkFrame(self.results_panel, fg_color=self.colors['success'], corner_radius=10)
        results_header.pack(pady=(0, 10), fill="x")
        ctk.CTkLabel(results_header, 
                    text=f"✅ {len(resultados)} resultado(s) encontrado(s) para '{termino}'", 
                    text_color="white", font=("Segoe UI", 14, "bold")).pack(pady=10)

        # --- Tabla de resultados con GRID para alineación perfecta ---
        table_container = ctk.CTkScrollableFrame(self.results_panel, fg_color=self.colors['light'], corner_radius=10)
        table_container.pack(fill="both", expand=True)

        # Configurar columnas para que se expandan
        table_container.grid_columnconfigure(1, weight=3) # Título
        table_container.grid_columnconfigure(2, weight=2) # Autor

        # Encabezados
        headers = ["Código", "Título", "Autor", "Disponibles", "Acciones"]
        column_paddings = [(10, 5), (5, 5), (5, 5), (5, 5), (5, 20)]

        header_frame = ctk.CTkFrame(table_container, fg_color=self.colors['primary'], corner_radius=0)
        header_frame.grid(row=0, column=0, columnspan=len(headers), sticky="ew", pady=(0, 5))
        header_frame.grid_columnconfigure(1, weight=3)
        header_frame.grid_columnconfigure(2, weight=2)

        for i, header in enumerate(headers):
            ctk.CTkLabel(header_frame, text=header, font=("Segoe UI", 12, "bold"), text_color="white").grid(
                row=0, column=i, padx=column_paddings[i], pady=10, sticky="w")

        # Filas de datos
        for i, libro in enumerate(resultados, start=1):
            row_color = self.colors['white'] if i % 2 == 0 else "transparent"
            
            # Código
            ctk.CTkLabel(table_container, text=libro.codigo, wraplength=100, justify="left", fg_color=row_color).grid(
                row=i, column=0, padx=column_paddings[0], pady=5, sticky="w")
            
            # Título
            ctk.CTkLabel(table_container, text=libro.titulo, wraplength=300, justify="left", fg_color=row_color).grid(
                row=i, column=1, padx=column_paddings[1], pady=5, sticky="w")
            
            # Autor
            autor_nombre = libro.autor.nombre_completo if libro.autor else "N/A"
            ctk.CTkLabel(table_container, text=autor_nombre, wraplength=200, justify="left", fg_color=row_color).grid(
                row=i, column=2, padx=column_paddings[2], pady=5, sticky="w")
            
            # Disponibles/Prestados
            disponibles_text = f"{libro.cantidad_disponibles} de {len(libro.ejemplares)}"
            color = self.colors['success'] if libro.cantidad_disponibles > 0 else self.colors['danger']
            ctk.CTkLabel(table_container, text=disponibles_text, text_color=color, fg_color=row_color).grid(
                row=i, column=3, padx=column_paddings[3], pady=5, sticky="w")
            
            # Botón Detalles
            ctk.CTkButton(table_container, text="📋 Detalles", width=80, height=30,
                         fg_color=self.colors['accent'], hover_color=self.colors['primary'],
                         command=lambda l=libro: self.ver_ejemplares(l)).grid(
                row=i, column=4, padx=column_paddings[4], pady=5, sticky="e")

    def ver_ejemplares(self, libro: Libro):
        """Muestra una ventana con los detalles y ejemplares del libro."""
        ejemplares_window = ctk.CTkToplevel(self)
        ejemplares_window.title(f"Detalles de: {libro.titulo}")
        ejemplares_window.geometry("700x500")
        ejemplares_window.transient(self)
        ejemplares_window.grab_set()

        try:
            ejemplares = self.gestor.get_ejemplares_por_libro(libro.id)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar los ejemplares: {e}", parent=ejemplares_window)
            ejemplares_window.destroy()
            return
            
        # Info General
        info_frame = ctk.CTkFrame(ejemplares_window, fg_color=self.colors['light'])
        info_frame.pack(fill="x", padx=20, pady=20)
        info_text = (f"**Título:** {libro.titulo}\n"
                     f"**Autor:** {libro.autor.nombre_completo if libro.autor else 'N/A'}\n"
                     f"**Disponibles:** {libro.cantidad_disponibles} de {len(ejemplares)} ejemplares")
        ctk.CTkLabel(info_frame, text=info_text, justify="left", font=("Segoe UI", 12)).pack(padx=15, pady=15, anchor="w")

        # Lista de Ejemplares
        ctk.CTkLabel(ejemplares_window, text="Ejemplares Individuales", font=("Segoe UI", 14, "bold")).pack(pady=(0, 10))

        if not ejemplares:
            ctk.CTkLabel(ejemplares_window, text="No hay ejemplares registrados para este libro.").pack()
        else:
            scroll_frame = ctk.CTkScrollableFrame(ejemplares_window)
            scroll_frame.pack(fill="both", expand=True, padx=20, pady=10)

            # Headers
            headers = ["Código Ejemplar", "Estado", "Ubicación Física"]
            for i, header in enumerate(headers):
                ctk.CTkLabel(scroll_frame, text=header, font=("Segoe UI", 12, "bold")).grid(row=0, column=i, padx=10, pady=5)

            # Datos
            for i, ejemplar in enumerate(ejemplares, start=1):
                color = self.colors['success'] if ejemplar.estado == 'disponible' else self.colors['danger']
                ctk.CTkLabel(scroll_frame, text=ejemplar.codigo_ejemplar).grid(row=i, column=0, padx=10, pady=2)
                ctk.CTkLabel(scroll_frame, text=ejemplar.estado.title(), text_color=color).grid(row=i, column=1, padx=10, pady=2)
                ctk.CTkLabel(scroll_frame, text=ejemplar.ubicacion_fisica or "No especificada").grid(row=i, column=2, padx=10, pady=2)
        
        ctk.CTkButton(ejemplares_window, text="Cerrar", command=ejemplares_window.destroy).pack(pady=20)