from rolepermissions.roles import AbstractUserRole
from apps.authentication.constants.permissions import Permissoes

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

class TPRC(Solicitante):
    available_permissions = Solicitante.available_permissions.copy()
    available_permissions.update({
        PERMISSOES.excluir_item : True,
        PERMISSOES.analisar_pedido : True,
        PERMISSOES.analisar_demanda : True,
    })

class TPOB(Solicitante):
    available_permissions = Solicitante.available_permissions.copy()
    available_permissions.update({
        PERMISSOES.excluir_item : True,
        PERMISSOES.analisar_pedido : True,
        PERMISSOES.criar_requisicao : True,
    })
