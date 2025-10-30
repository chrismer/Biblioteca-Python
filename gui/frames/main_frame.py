import customtkinter as ctk
from tkinter import messagebox
from typing import TYPE_CHECKING
from .add_book_frame import AddBookFrame
from .add_shelf_frame import AddShelfFrame
from .manage_shelves_frame import ManageShelvesFrame
from .list_frame import ListFrame
from .users_frame import UsersFrame
from .loans_frame import LoansFrame
from PIL import Image
from .move_book_frame import MoveBookFrame
from .search_book_frame import SearchBookFrame
import os

if TYPE_CHECKING:
    from logic.library_manager import GestorBiblioteca

class MainFrame(ctk.CTkFrame):
    def __init__(self, master, gestor: 'GestorBiblioteca'):
        super().__init__(master, fg_color="#F8F9FA")
        self.master = master
        self.gestor = gestor
        
        # Colores modernos - Paleta personalizada
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

        # Crear layout moderno con scroll
        self.setup_scrollable_layout()

    def setup_scrollable_layout(self):
        """Configura el layout con scroll vertical para monitores pequeños."""
        
        # === HEADER FIJO (sin scroll) ===
        self.create_header()
        
        # === CONTENIDO SCROLLABLE ===
        # Frame principal con scroll
        self.main_scroll = ctk.CTkScrollableFrame(self, 
                                                 fg_color="transparent",
                                                 scrollbar_button_color=self.colors['primary'],
                                                 scrollbar_button_hover_color=self.colors['accent'])
        self.main_scroll.pack(fill="both", expand=True, padx=0, pady=0)
        
        # === HERO SECTION CON IMAGEN DE FONDO ===
        self.create_hero_section()
        
        # === CARDS DE FUNCIONALIDADES ===
        self.create_feature_cards()
        
        # === ESTADÍSTICAS ===
        self.create_stats_section()

    def create_header(self):
        """Crea el header superior estilo web."""
        header = ctk.CTkFrame(self, height=80, fg_color=self.colors['white'], corner_radius=0)
        header.pack(fill="x", padx=0, pady=0)
        header.pack_propagate(False)
        
        # Container para centrar contenido
        header_content = ctk.CTkFrame(header, fg_color="transparent")
        header_content.pack(fill="both", expand=True, padx=40, pady=20)
        
        # Logo y título
        title_frame = ctk.CTkFrame(header_content, fg_color="transparent")
        title_frame.pack(side="left")
        
        try:
            # Cargar icono de BiblioHub
            current_dir = os.path.dirname(os.path.abspath(__file__))
            icon_path = os.path.join(current_dir, "..", "..", "assets", "bibliohub_icon_small.png")
            
            bibliohub_logo = ctk.CTkImage(Image.open(icon_path), size=(40, 40))
            
            # Label para el icono
            icon_label = ctk.CTkLabel(title_frame, image=bibliohub_logo, text="")
            icon_label.pack(side="left", padx=(0, 10))
            
        except Exception as e:
            print(f"Error cargando icono del header, usando texto de fallback: {e}")
            
        # Título principal
        ctk.CTkLabel(title_frame, 
                    text="BiblioHub", 
                    font=("Segoe UI", 28, "bold"),
                    text_color=self.colors['primary']).pack(side="left")
        
        ctk.CTkLabel(title_frame, 
                    text="Sistema de Gestión Bibliotecaria", 
                    font=("Segoe UI", 14),
                    text_color=self.colors['secondary']).pack(side="left", padx=(20, 0))
        
        # Barra de búsqueda en el header
        search_frame = ctk.CTkFrame(header_content, fg_color="transparent")
        search_frame.pack(side="right", padx=(20, 0))
        
        self.search_entry = ctk.CTkEntry(search_frame, 
                                        placeholder_text="🔍 Buscar libros...",
                                        width=300,
                                        height=35,
                                        font=("Segoe UI", 12),
                                        fg_color=self.colors['light'],
                                        border_color=self.colors['primary'],
                                        corner_radius=20)
        self.search_entry.pack(side="left", padx=(0, 10))
        self.search_entry.bind("<Return>", self.buscar_desde_header)

    def create_hero_section(self):
        """Crea la sección hero con imagen de fondo."""
        # Frame transparente para contener solo la imagen
        hero_frame = ctk.CTkFrame(self.main_scroll, height=300, fg_color="transparent", corner_radius=20)
        hero_frame.pack(fill="x", padx=40, pady=(20, 30))
        hero_frame.pack_propagate(False)
        
        # Intentar cargar imagen de fondo
        try:
            if os.path.exists("assets/bg-bibliohub.png"):
                bg_image = Image.open("assets/bg-bibliohub.png")
                bg_ctk_image = ctk.CTkImage(bg_image, size=(1320, 500))
                
                # Label con imagen de fondo (sin overlay azul)
                bg_label = ctk.CTkLabel(hero_frame, image=bg_ctk_image, text="", corner_radius=20)
                bg_label.place(x=0.5, y=0, anchor="nw")
                
        except Exception as e:
            pass  # Continuar con fallback si no hay imagen
            # Fallback: mostrar solo un mensaje simple
            fallback_frame = ctk.CTkFrame(hero_frame, fg_color=self.colors['light'], corner_radius=20)
            fallback_frame.pack(fill="both", expand=True)
            
            ctk.CTkLabel(fallback_frame, 
                        text="📚 Bienvenido a BiblioHub", 
                        font=("Segoe UI", 24, "bold"),
                        text_color=self.colors['primary']).pack(expand=True)

    def buscar_desde_header(self, event=None):
        """Realiza búsqueda inteligente desde el input del header."""
        termino = self.search_entry.get().strip()
        if termino:
            try:
                # Realizar la búsqueda directamente aquí
                libros_encontrados = self.gestor.buscar_libros(termino)
                
                # Cambiar a SearchBookFrame con los resultados ya listos
                self.master.switch_frame(SearchBookFrame)
                
                # Establecer el término y mostrar resultados inmediatamente
                if hasattr(self.master.current_frame, 'entry_buscar'):
                    self.master.current_frame.entry_buscar.delete(0, 'end')
                    self.master.current_frame.entry_buscar.insert(0, termino)
                
                # Mostrar resultados directamente
                if hasattr(self.master.current_frame, 'mostrar_resultados'):
                    self.master.current_frame.mostrar_resultados(libros_encontrados, termino)
                elif hasattr(self.master.current_frame, 'buscar_libros'):
                    # Fallback: ejecutar búsqueda automáticamente
                    self.master.current_frame.buscar_libros()
                
            except Exception as e:
                pass  # Fallback silencioso
                # Fallback: ir a la pantalla de búsqueda normal
                self.master.switch_frame(SearchBookFrame)
        else:
            # Si no hay término, solo ir a la pantalla de búsqueda
            self.master.switch_frame(SearchBookFrame)

    def create_feature_cards(self):
        """Crea las tarjetas de funcionalidades."""
        # Container principal para las cards
        cards_container = ctk.CTkFrame(self.main_scroll, fg_color="transparent")
        cards_container.pack(fill="x", padx=40, pady=(0, 30))
        
        # Título de sección
        ctk.CTkLabel(cards_container, 
                    text="Funcionalidades Principales", 
                    font=("Segoe UI", 24, "bold"),
                    text_color=self.colors['dark']).pack(pady=(0, 20))
        
        # Frame para las cards
        cards_frame = ctk.CTkFrame(cards_container, fg_color="transparent")
        cards_frame.pack(fill="x")
        
        # Configurar grid
        cards_frame.grid_columnconfigure(0, weight=1)
        cards_frame.grid_columnconfigure(1, weight=1)
        cards_frame.grid_columnconfigure(2, weight=1)
        
        # Definir las tarjetas
        cards_data = [
            {
                'title': 'Gestión de Libros',
                'description': 'Agregar, editar y organizar tu colección',
                'icon': '📚',
                'color': self.colors['primary'],
                'actions': [
                    ('Agregar Libro', lambda: self.master.switch_frame(AddBookFrame)),
                    ('Listar Disponibles', self.mostrar_disponibles),
                    ('Buscar Libro', lambda: self.master.switch_frame(SearchBookFrame))
                ]
            },
            {
                'title': 'Sistema de Préstamos',
                'description': 'Control completo de préstamos y devoluciones',
                'icon': '🔄',
                'color': self.colors['success'],
                'actions': [
                    ('Gestionar Préstamos', lambda: self.master.switch_frame(LoansFrame)),
                    ('Libros Prestados', self.mostrar_prestados),
                    ('Reportes', self.mostrar_reportes)
                ]
            },
            {
                'title': 'Administración',
                'description': 'Usuarios, estanterías y configuración',
                'icon': '⚙️',
                'color': self.colors['warning'],
                'actions': [
                    ('Gestionar Usuarios', lambda: self.master.switch_frame(UsersFrame)),
                    ('Gestionar Estanterías', lambda: self.master.switch_frame(ManageShelvesFrame)),
                    ('Mover Libros', lambda: self.master.switch_frame(MoveBookFrame))
                ]
            }
        ]
        
        # Crear las tarjetas
        for i, card_data in enumerate(cards_data):
            self.create_feature_card(cards_frame, card_data, row=0, column=i)

    def create_feature_card(self, parent, card_data, row, column):
        """Crea una tarjeta individual de funcionalidad."""
        card = ctk.CTkFrame(parent, 
                           fg_color=self.colors['white'], 
                           corner_radius=15,
                           border_width=1,
                           border_color="#E2E8F0")
        card.grid(row=row, column=column, padx=15, pady=15, sticky="nsew")
        
        # Header de la tarjeta
        header = ctk.CTkFrame(card, fg_color="transparent", height=80)
        header.pack(fill="x", padx=20, pady=(20, 10))
        header.pack_propagate(False)
        
        # Icono
        icon_frame = ctk.CTkFrame(header, 
                                 width=50, height=50,
                                 fg_color=card_data['color'],
                                 corner_radius=25)
        icon_frame.pack(pady=(0, 10))
        icon_frame.pack_propagate(False)
        
        ctk.CTkLabel(icon_frame, 
                    text=card_data['icon'], 
                    font=("Segoe UI", 20)).pack(expand=True)
        
        # Título
        ctk.CTkLabel(header, 
                    text=card_data['title'], 
                    font=("Segoe UI", 16, "bold"),
                    text_color=self.colors['dark']).pack()
        
        # Descripción
        ctk.CTkLabel(card, 
                    text=card_data['description'], 
                    font=("Segoe UI", 11),
                    text_color=self.colors['secondary'],
                    wraplength=200).pack(padx=20, pady=(0, 15))
        
        # Botones de acción
        actions_frame = ctk.CTkFrame(card, fg_color="transparent")
        actions_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        for action_text, action_command in card_data['actions']:
            btn = ctk.CTkButton(actions_frame,
                               text=action_text,
                               text_color="white",
                               font=("Segoe UI", 14),
                               width=180, height=35,
                               fg_color=card_data['color'],
                               corner_radius=10,
                               command=action_command)
            btn.pack(pady=2, fill="x")

    def create_stats_section(self):
        """Crea la sección de estadísticas."""
        stats_frame = ctk.CTkFrame(self.main_scroll, fg_color=self.colors['white'], corner_radius=15)
        stats_frame.pack(fill="x", padx=40, pady=(0, 40))
        
        # Título
        ctk.CTkLabel(stats_frame, 
                    text="📊 Estadísticas del Sistema", 
                    font=("Segoe UI", 18, "bold"),
                    text_color=self.colors['dark']).pack(pady=(20, 15))
        
        # Container para estadísticas
        stats_container = ctk.CTkFrame(stats_frame, fg_color="transparent")
        stats_container.pack(fill="x", padx=40, pady=(0, 20))
        
        # Configurar grid
        stats_container.grid_columnconfigure(0, weight=1)
        stats_container.grid_columnconfigure(1, weight=1)
        stats_container.grid_columnconfigure(2, weight=1)
        stats_container.grid_columnconfigure(3, weight=1)
        
        # Obtener estadísticas
        try:
            resumen = self.gestor.get_resumen_biblioteca()
            stats_data = [
                ('Total de Libros', resumen.get('total_libros', 0), self.colors['primary']),
                ('Ejemplares Disponibles', resumen.get('ejemplares_disponibles', 0), self.colors['success']),
                ('Préstamos Activos', resumen.get('prestamos_activos', 0), self.colors['warning']),
                ('Préstamos Vencidos', resumen.get('prestamos_vencidos', 0), self.colors['danger'])
            ]
        except:
            stats_data = [
                ('Total de Libros', 0, self.colors['primary']),
                ('Ejemplares Disponibles', 0, self.colors['success']),
                ('Préstamos Activos', 0, self.colors['warning']),
                ('Préstamos Vencidos', 0, self.colors['danger'])
            ]
        
        # Crear estadísticas
        for i, (label, value, color) in enumerate(stats_data):
            stat_frame = ctk.CTkFrame(stats_container, fg_color=self.colors['light'], corner_radius=10)
            stat_frame.grid(row=0, column=i, padx=8, pady=10, sticky="ew")
            
            ctk.CTkLabel(stat_frame, 
                        text=str(value), 
                        font=("Segoe UI", 24, "bold"),
                        text_color=color).pack(pady=(15, 5))
            
            ctk.CTkLabel(stat_frame, 
                        text=label, 
                        font=("Segoe UI", 10),
                        text_color=self.colors['secondary']).pack(pady=(0, 15))

    def mostrar_disponibles(self):
        try:
            libros = self.gestor.get_libros_disponibles()
            self.master.switch_frame(ListFrame, titulo="Libros Disponibles", libros=libros)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def mostrar_prestados(self):
        try:
            libros = self.gestor.get_libros_prestados()
            self.master.switch_frame(ListFrame, titulo="Libros Prestados", libros=libros)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def mostrar_mas_prestado(self):
        try:
            libro = self.gestor.get_libro_mas_prestado()
            if libro:
                autor_nombre = libro.autor.nombre_completo if libro.autor else "Autor Desconocido"
                messagebox.showinfo("Libro Más Popular", f"El libro más prestado es:\n\n'{libro.titulo}' de {autor_nombre}\n\nHa sido prestado {libro.historial_prestamos} veces.")
            else:
                messagebox.showinfo("Información", "Aún no se han registrado préstamos.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def mostrar_reportes(self):
        """Muestra los reportes avanzados del sistema."""
        try:
            resumen = self.gestor.get_resumen_biblioteca()
            
            reporte_text = "📊 RESUMEN DE LA BIBLIOTECA\n\n"
            reporte_text += f"📚 Total de libros: {resumen['total_libros']}\n"
            reporte_text += f"📖 Total de ejemplares: {resumen['total_ejemplares']}\n"
            reporte_text += f"✅ Ejemplares disponibles: {resumen['ejemplares_disponibles']}\n"
            reporte_text += f"📤 Ejemplares prestados: {resumen['ejemplares_prestados']}\n"
            reporte_text += f"🔄 Préstamos activos: {resumen['prestamos_activos']}\n"
            reporte_text += f"⚠️ Préstamos vencidos: {resumen['prestamos_vencidos']}\n"
            reporte_text += f"👥 Usuarios activos: {resumen['usuarios_activos']}\n"
            
            messagebox.showinfo("Reportes de la Biblioteca", reporte_text)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar reportes: {str(e)}")