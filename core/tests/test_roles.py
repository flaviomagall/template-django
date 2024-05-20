# core/tests/test_roles.py

import pytest
from django.contrib.auth import get_user_model
from rolepermissions.roles import assign_role, clear_roles
from rolepermissions.checkers import has_permission
from core.constants.permissions import CONSULTAR_ITEM, CRIAR_PEDIDO

User = get_user_model()

@pytest.mark.django_db
def test_usuario_permissao_consultar_item():
    user = User.objects.create_user(username='usuario', password='password')
    assign_role(user, 'usuario')

    assert has_permission(user, CONSULTAR_ITEM)
    assert not has_permission(user, CRIAR_PEDIDO)

@pytest.mark.django_db
def test_cliente_permissao_consultar_item_e_criar_pedido():
    user = User.objects.create_user(username='cliente', password='password')
    assign_role(user, 'cliente')

    assert has_permission(user, CONSULTAR_ITEM)
    assert has_permission(user, CRIAR_PEDIDO)

@pytest.mark.django_db
def test_alterar_role_do_usuario():
    user = User.objects.create_user(username='usuario', password='password')
    assign_role(user, 'usuario')

    assert has_permission(user, CONSULTAR_ITEM)
    assert not has_permission(user, CRIAR_PEDIDO)

    # Alterar a role do usuário
    clear_roles(user)
    assign_role(user, 'cliente')

    assert has_permission(user, CONSULTAR_ITEM)
    assert has_permission(user, CRIAR_PEDIDO)
