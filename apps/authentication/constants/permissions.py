class Permissoes:
    buscar_item = 'buscar_item'
    criar_pedido = 'criar_pedido'

    consultar_item = 'consultar_item'
    excluir_item = 'excluir_item'

    atualizar_pedido = 'atualizar_pedido'
    analisar_pedido = 'analisar_pedido'
    excluir_pedido = 'excluir_pedido'

    analisar_demanda = 'analisar_demanda'
    criar_requisicao = 'criar_requisicao'


    @classmethod
    def get_all_permissoes(cls):
        return [value for key, value in vars(cls).items() if not key.startswith('__') and not callable(value)]
