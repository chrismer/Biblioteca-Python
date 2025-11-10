from typing import TYPE_CHECKING
from .book_form_frame import BookFormFrame
from logic.models import Libro

if TYPE_CHECKING:
    from gui.app import App
    from logic.library_manager import GestorBiblioteca

class EditBookFrame(BookFormFrame):
    def __init__(self, master: 'App', gestor: 'GestorBiblioteca', libro: Libro):
        super().__init__(master, gestor, libro=libro)
