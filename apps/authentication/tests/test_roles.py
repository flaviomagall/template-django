import pytest
from django.contrib.auth import get_user_model
from rolepermissions.roles import assign_role, clear_roles
from rolepermissions.checkers import has_permission
from apps.authentication.roles import Permissoes, UsuarioRole, SolicitanteRole, DemandaRole, ObtencaoRole

PERMISSOES = Permissoes()
User = get_user_model()

# Obter todas as permissões dinamicamente
todas_permissoes = Permissoes.get_all_permissoes()

lista_permissoes = {
    'usuario': [
        PERMISSOES.buscar_item,
        PERMISSOES.consultar_item,
    ],
    'solicitante': [
        PERMISSOES.buscar_item,
        PERMISSOES.consultar_item,
        PERMISSOES.criar_pedido,
        PERMISSOES.atualizar_pedido,
        PERMISSOES.excluir_pedido,
    ],
    'tprc': [
        PERMISSOES.buscar_item,
        PERMISSOES.consultar_item,
        PERMISSOES.criar_pedido,
        PERMISSOES.atualizar_pedido,
        PERMISSOES.excluir_pedido,
        PERMISSOES.excluir_item,
        PERMISSOES.analisar_pedido,
        PERMISSOES.analisar_demanda,
    ],
    'tpob': [
        PERMISSOES.buscar_item,
        PERMISSOES.consultar_item,
        PERMISSOES.criar_pedido,
        PERMISSOES.atualizar_pedido,
        PERMISSOES.excluir_pedido,
        PERMISSOES.excluir_item,
        PERMISSOES.analisar_pedido,
        PERMISSOES.criar_requisicao,
    ],
}

# Função auxiliar para verificar permissões
def verificar_permissoes(user, permissoes_esperadas):
    permissoes_nao_esperadas = [p for p in todas_permissoes if p not in permissoes_esperadas]
    for permissao in permissoes_esperadas:
        assert has_permission(user, permissao), f"O usuário deveria ter a permissão {permissao}"
    for permissao in permissoes_nao_esperadas:
        assert not has_permission(user, permissao), f"O usuário não deveria ter a permissão {permissao}"

# Função auxiliar para alterar roles e verificar permissões
def alterar_role_e_verificar(usuario, role_name, permissoes_esperadas):
    clear_roles(usuario)
    assign_role(usuario, role_name)
    verificar_permissoes(usuario, permissoes_esperadas)

@pytest.fixture
def usuario():
    return User.objects.create_user(username='nickname', password='password')

@pytest.mark.django_db
@pytest.mark.parametrize("role, permissoes_esperadas", [
    (UsuarioRole, lista_permissoes['usuario']),
    (SolicitanteRole, lista_permissoes['solicitante']),
    (DemandaRole, lista_permissoes['tprc']),
    (ObtencaoRole, lista_permissoes['tpob']),
])
def test_permissoes_por_role(usuario, role, permissoes_esperadas):
    assign_role(usuario, role.__name__.lower())
    verificar_permissoes(usuario, permissoes_esperadas)

@pytest.mark.django_db
@pytest.mark.parametrize("role, permissoes_iniciais, permissoes_finais", [
    (SolicitanteRole, lista_permissoes['usuario'], lista_permissoes['solicitante']),
    (DemandaRole, lista_permissoes['usuario'], lista_permissoes['tprc']),
    (ObtencaoRole, lista_permissoes['usuario'], lista_permissoes['tpob']),
])
def test_alterar_role(usuario, role, permissoes_iniciais, permissoes_finais):
    assign_role(usuario, UsuarioRole.__name__.lower())
    verificar_permissoes(usuario, permissoes_iniciais)

    # Alterar a role do usuário
    alterar_role_e_verificar(usuario, role.__name__.lower(), permissoes_finais)
