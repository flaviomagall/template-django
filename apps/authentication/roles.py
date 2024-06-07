from rolepermissions.roles import AbstractUserRole


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


PERMISSOES = Permissoes()

class Usuario(AbstractUserRole):
    available_permissions = {
        PERMISSOES.buscar_item : True,
        PERMISSOES.consultar_item : True,
    }

class Solicitante(Usuario):
    available_permissions = Usuario.available_permissions.copy()
    available_permissions.update({
        PERMISSOES.criar_pedido : True,
        PERMISSOES.atualizar_pedido : True,
        PERMISSOES.excluir_pedido : True,
    })

class Demanda(Solicitante):
    available_permissions = Solicitante.available_permissions.copy()
    available_permissions.update({
        PERMISSOES.excluir_item : True,
        PERMISSOES.analisar_pedido : True,
        PERMISSOES.analisar_demanda : True,
    })

class Obtencao(Solicitante):
    available_permissions = Solicitante.available_permissions.copy()
    available_permissions.update({
        PERMISSOES.excluir_item : True,
        PERMISSOES.analisar_pedido : True,
        PERMISSOES.criar_requisicao : True,
    })

class Administrador(AbstractUserRole):
    available_permissions = {
        PERMISSOES.buscar_item : True,
        PERMISSOES.criar_pedido : True,

        PERMISSOES.consultar_item : True,
        PERMISSOES.excluir_item : True,

        PERMISSOES.atualizar_pedido : True,
        PERMISSOES.analisar_pedido : True,
        PERMISSOES.excluir_pedido : True,

        PERMISSOES.analisar_demanda : True,
        PERMISSOES.criar_requisicao : True,
    }
