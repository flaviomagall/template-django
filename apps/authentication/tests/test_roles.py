import pytest
from django.contrib.auth import get_user_model
from rolepermissions.roles import assign_role, clear_roles
from rolepermissions.checkers import has_permission
from apps.authentication.constants.permissions import Permissoes
from apps.authentication.roles import Usuario, Solicitante, TPRC, TPOB

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
        PERMISSOES.excluir_pedido
    ],
    'tprc': [
        PERMISSOES.buscar_item,
        PERMISSOES.consultar_item,
        PERMISSOES.criar_pedido,
        PERMISSOES.atualizar_pedido,
        PERMISSOES.excluir_pedido,
        PERMISSOES.excluir_item,
        PERMISSOES.analisar_pedido,
        PERMISSOES.analisar_demanda
    ],
    'tpob': [
        PERMISSOES.buscar_item,
        PERMISSOES.consultar_item,
        PERMISSOES.criar_pedido,
        PERMISSOES.atualizar_pedido,
        PERMISSOES.excluir_pedido,
        PERMISSOES.excluir_item,
        PERMISSOES.analisar_pedido,
        PERMISSOES.criar_requisicao
    ]
}

# Função auxiliar para verificar permissões
def verificar_permissoes(user, permissoes_esperadas):
    permissoes_nao_esperadas = [p for p in todas_permissoes if p not in permissoes_esperadas]
    for permissao in permissoes_esperadas:
        assert has_permission(user, permissao), f"O Usuário deveria ter a permissão de {permissao}"
    for permissao in permissoes_nao_esperadas:
        assert not has_permission(user, permissao), f"O Usuário não deveria ter a permissão de {permissao}"

# Função auxiliar para alterar roles e verificar permissões
def alterar_role_e_verificar(usuario, role_name, permissoes_esperadas):
    clear_roles(usuario)
    assign_role(usuario, role_name)
    verificar_permissoes(usuario, permissoes_esperadas)

@pytest.fixture
def usuario():
    user = User.objects.create_user(username='nickname', password='password')
    return user

@pytest.mark.django_db
def test_usuario_permissoes(usuario):
    assign_role(usuario, Usuario.__name__.lower())
    verificar_permissoes(usuario, lista_permissoes['usuario'])

@pytest.mark.django_db
def test_solicitante_permissoes(usuario):
    assign_role(usuario, Solicitante.__name__.lower())
    verificar_permissoes(usuario, lista_permissoes['solicitante'])

@pytest.mark.django_db
def test_tprc_permissoes(usuario):
    assign_role(usuario, TPRC.__name__.lower())
    verificar_permissoes(usuario, lista_permissoes['tprc'])

@pytest.mark.django_db
def test_tpob_permissoes(usuario):
    assign_role(usuario, TPOB.__name__.lower())
    verificar_permissoes(usuario, lista_permissoes['tpob'])

@pytest.mark.parametrize("role, permissoes", [
    ('solicitante', lista_permissoes['solicitante']),
    ('tprc', lista_permissoes['tprc']),
    ('tpob', lista_permissoes['tpob']),
])
@pytest.mark.django_db
def test_alterar_role_para_usuario(usuario, role, permissoes):
    assign_role(usuario, role)
    verificar_permissoes(usuario, permissoes)

    # Alterar a role do usuário de volta para Usuario
    alterar_role_e_verificar(usuario, Usuario.__name__.lower(), lista_permissoes['usuario'])

@pytest.mark.parametrize("role, permissoes_iniciais, permissoes_finais", [
    (Solicitante.__name__.lower(), lista_permissoes['usuario'], lista_permissoes['solicitante']),
    (TPRC.__name__.lower(), lista_permissoes['usuario'], lista_permissoes['tprc']),
    (TPOB.__name__.lower(), lista_permissoes['usuario'], lista_permissoes['tpob']),
])
@pytest.mark.django_db
def test_alterar_role_do_usuario_para_outros(usuario, role, permissoes_iniciais, permissoes_finais):
    assign_role(usuario, Usuario.__name__.lower())
    verificar_permissoes(usuario, permissoes_iniciais)

    # Alterar a role do usuário
    alterar_role_e_verificar(usuario, role, permissoes_finais)
