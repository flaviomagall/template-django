class TemplateLayout:

    class LayoutsDisplay:
        layout_blank = 'layout/layout_blank.html'
        layout_vertical_menu = 'layout/layout_vertical_menu.html'
        # Adicione outros layouts aqui

    @staticmethod
    def set_layout(layout):
        """
        Define o layout baseado no nome fornecido.

        Args:
            layout (str): O nome do layout a ser definido.

        Returns:
            str: O caminho do layout correspondente.
        """
        return layout if layout in TemplateLayout.LayoutsDisplay.__dict__.values() else TemplateLayout.LayoutsDisplay.layout_blank

    @staticmethod
    def init(view, context):
        """
        Inicializa o contexto com variáveis globais e o layout padrão.

        Args:
            view (View): A instância da view.
            context (dict): O dicionário de contexto a ser atualizado.

        Returns:
            dict: O contexto atualizado.
        """
        context.update({
            'site_name': 'Meu Projeto Django',  # Exemplo de variável global
            'layout_path': TemplateLayout.LayoutsDisplay.layout_blank,  # Define um layout padrão
            # Adicione outras variáveis globais aqui
        })
        return context
