from typing import TYPE_CHECKING
from .book_form_frame import BookFormFrame

if TYPE_CHECKING:
    from gui.app import App
    from logic.library_manager import GestorBiblioteca

class AddBookFrame(BookFormFrame):
    def __init__(self, master: 'App', gestor: 'GestorBiblioteca'):
        super().__init__(master, gestor, libro=None)
