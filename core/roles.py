from rolepermissions.roles import AbstractUserRole
from core.constants.permissions import CONSULTAR_ITEM, CRIAR_PEDIDO


class Usuario(AbstractUserRole):
    available_permissions = {
        CONSULTAR_ITEM : True,
    }

class Cliente(AbstractUserRole):
    available_permissions = {
        CONSULTAR_ITEM: True,
        CRIAR_PEDIDO: True,
    }
