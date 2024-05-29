from django.contrib.auth import get_user_model

User = get_user_model()


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

class UsuarioRole(User):
    available_permissions = {
        PERMISSOES.buscar_item : True,
        PERMISSOES.consultar_item : True,
    }

class SolicitanteRole(UsuarioRole):
    available_permissions = UsuarioRole.available_permissions.copy()
    available_permissions.update({
        PERMISSOES.criar_pedido : True,
        PERMISSOES.atualizar_pedido : True,
        PERMISSOES.excluir_pedido : True,
    })

class DemandaRole(SolicitanteRole):
    available_permissions = SolicitanteRole.available_permissions.copy()
    available_permissions.update({
        PERMISSOES.excluir_item : True,
        PERMISSOES.analisar_pedido : True,
        PERMISSOES.analisar_demanda : True,
    })

class ObtencaoRole(SolicitanteRole):
    available_permissions = SolicitanteRole.available_permissions.copy()
    available_permissions.update({
        PERMISSOES.excluir_item : True,
        PERMISSOES.analisar_pedido : True,
        PERMISSOES.criar_requisicao : True,
    })
