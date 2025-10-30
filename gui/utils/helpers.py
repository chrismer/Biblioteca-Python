
def borrar_widgets(container, widgets_a_ignorar=None):
    """
    Borra todos los widgets de un contenedor, excepto los de la lista 'widgets_a_ignorar'.

    :param container: El frame o panel del cual borrar los widgets.
    :param widgets_a_ignorar: Una lista de widgets que se quieren conservar.
    """
    lista_a_ignorar = widgets_a_ignorar if widgets_a_ignorar else []
    
    # Creamos una copia de la lista de hijos para iterar de forma segura
    for widget in list(container.winfo_children()):
        if widget not in lista_a_ignorar:
            widget.destroy()