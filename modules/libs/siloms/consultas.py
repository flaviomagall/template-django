import pandas as pd
import logging
from .oracle_connection import OracleConnection
from .queries import Queries
from apps.dashboards.models import ProgressoRequisicoesExterior


class ConsultasSiloms():

    def __init__(self):
        self.connection = OracleConnection()

    def consulta_pn_preferencial(self, part_number, cff, projeto) -> dict:
        result = Queries.query_pn_preferencial(part_number, cff, projeto, self.connection)
        if result.empty:
            logging.error(f"O Resultado da consulta do PN Preferencial para o PN:{part_number} CFF: {cff} PROJETO: {projeto} retornou vazio")
            colunas_esperadas = ['MATERIAL_PREFERENCIAL_PN', 'MATERIAL_PREFERENCIAL_CFF', 'NSN', 'QT_DMM_TOTAL', 'CATEGORIA', 'ORG_PROVEDOR', 'NOMENCLATURA']
            dados_iniciais = {coluna: [None] for coluna in colunas_esperadas}
            result = pd.DataFrame(dados_iniciais)

        return {
            'pn_preferencial': result.at[0, 'MATERIAL_PREFERENCIAL_PN'],
            'cff_preferencial': result.at[0, 'MATERIAL_PREFERENCIAL_CFF'],
            'dmm_familia': result.at[0, 'QT_DMM_TOTAL'],
            'categoria': result.at[0, 'CATEGORIA'],
            'nsn': result.at[0, 'NSN'],
            'org_provedor': result.at[0, 'ORG_PROVEDOR'],
            'nomenclatura': result.at[0, 'NOMENCLATURA']
        }

    def consulta_alternados(self, pn_preferencial, cff_preferencial, projeto) -> dict:
        result = Queries.query_alternados(pn_preferencial, cff_preferencial, projeto, self.connection)
        if result.empty:
            logging.error(f"O Resultado da consulta de alternados do PN Preferencial:{pn_preferencial} CFF: {cff_preferencial} PROJETO: {projeto} retornou vazio")
            colunas_esperadas = ['MATERIAL_PN', 'MATERIAL_CFF']
            dados_iniciais = {coluna: [None] for coluna in colunas_esperadas}
            result = pd.DataFrame(dados_iniciais)
        else:
            # Criando uma coluna de ordem baseada na correspondência com os valores preferenciais
            result['is_preferencial'] = (result['MATERIAL_PN'] == pn_preferencial) & (result['MATERIAL_CFF'] == cff_preferencial)
            # Ordenando os dados para que os preferenciais venham primeiro
            result.sort_values('is_preferencial', ascending=False, inplace=True)
            # Removendo a coluna temporária após a ordenação
            result.drop('is_preferencial', axis=1, inplace=True)
        return result.to_dict('records')

    def consulta_dados_primarios(self, familia, projeto, pn_preferencial, cff_preferencial) -> dict:

        def ordenar_por_preferencia(lista, pn_preferencial, cff_preferencial):
            # Reordena a lista para colocar itens preferenciais no início
            return sorted(lista, key=lambda x: not (x['PN'] == pn_preferencial and x['CFF'] == cff_preferencial))

        try:
            result = Queries.query_dados_primarios(familia, projeto, self.connection)
            if not result.empty and {"PN", "CFF", "ESTOQUE_TOTAL", "EMERGENCIA_TOTAL", "REQUISICAO_TOTAL"}.issubset(result.columns):
                # Processa os dados uma única vez
                processado = result.to_dict('records')
                # Cria listas com condições específicas e inclui apenas as colunas relevantes
                estoque_list = [{'PN': item['PN'], 'CFF': item['CFF'], 'ESTOQUE_TOTAL': item['ESTOQUE_TOTAL']}
                                for item in processado if item.get('ESTOQUE_TOTAL', 0) > 0]
                unidades_estoque = Queries.query_unidade_estoque(estoque_list, projeto, self.connection)
                dicts_unidades_estoque = unidades_estoque.to_dict('records')
                unidades_estoque = [{'PN': item['PN'], 'CFF': item['CFF'], 'ESTOQUE_TOTAL': item['TOTAL_ESTOQUE'], 'Unidades': item['UNIDADES']}
                                for item in dicts_unidades_estoque]
                estoque_list = ordenar_por_preferencia(unidades_estoque, pn_preferencial, cff_preferencial)
                soma_estoque = sum(item['ESTOQUE_TOTAL'] for item in estoque_list)
                emergencia_list = [{'PN': item['PN'], 'CFF': item['CFF'], 'EMERGENCIA_TOTAL': item['EMERGENCIA_TOTAL']}
                                for item in processado if item.get('EMERGENCIA_TOTAL', 0) > 0]
                emergencia_list = ordenar_por_preferencia(emergencia_list, pn_preferencial, cff_preferencial)
                if emergencia_list:
                    status_emergencias = Queries.query_status_emergencia(emergencia_list, projeto, self.connection)
                    soma_emergencia_familia = sum(item['Qtde'] for item in (status_emergencias.get('Emergencia') if status_emergencias else []))
                    soma_pedido_normal_familia = sum(item['Qtde'] for item in (status_emergencias.get('PedidoNormal') if status_emergencias else []))
                else:
                    status_emergencias = {
                        'Emergencia': [],
                        'PedidoNormal': []
                    }
                    soma_emergencia_familia = 0
                    soma_pedido_normal_familia = 0
                requisicao_list = [{'PN': item['PN'], 'CFF': item['CFF'], 'REQUISICAO_TOTAL': item['REQUISICAO_TOTAL']}
                                for item in processado if item.get('REQUISICAO_TOTAL', 0) > 0]
                requisicao_list = ordenar_por_preferencia(requisicao_list, pn_preferencial, cff_preferencial)
                soma_requisicao = sum(item['REQUISICAO_TOTAL'] for item in requisicao_list)
                if requisicao_list:
                    status_requisicoes = Queries.query_status_requisicao(requisicao_list, projeto, self.connection)
                else:
                    status_requisicoes = None
                return {
                    'estoque_familia': estoque_list,
                    'soma_estoque_familia': soma_estoque,
                    'emergencia_familia': status_emergencias['Emergencia'],
                    'soma_emergencia_familia': soma_emergencia_familia,
                    'pedido_normal_familia': status_emergencias['PedidoNormal'],
                    'soma_pedido_normal_familia': soma_pedido_normal_familia,
                    'requisicao_familia': status_requisicoes,
                    'soma_requisicao_familia': soma_requisicao,
                }
            else:
                return {}

        except Exception as e:
            logging.error(f"Erro ao consultar dados primários: {e}")
            return {}


    def consulta_estoque_pama(self, estoque_list, pn_preferencial, cff_preferencial):
        result = Queries.query_estoque_PAMA(estoque_list, self.connection)
        if not result.empty:
            result_filtrado = result.query('TOTAL_ESTOQUE > 0')
            # Converte o DataFrame filtrado para uma lista de dicionários
            processado = result_filtrado.to_dict('records')
            # Reordena os itens de modo que os preferenciais venham primeiro
            processado = sorted(processado, key=lambda x: not (x['PN'] == pn_preferencial and x['CFF'] == cff_preferencial))
            return processado
        else:
            # Retorna uma lista vazia se o DataFrame original estiver vazio
            return []


    def consulta_progresso_requisicoes(self):
        tb_progresso = Queries.query_progresso_requisicoes_exterior(self.connection)
        status_groups = {
            'Requisições canceladas': ['6', 'C'],
            'Requisições em processo': ['F', 'V', 'S', 'G', 'O', '3', 'A'],
            'Aguardando empenho': ['M', 'N'],
            'Empenhado': ['W'],
            'Em trânsito': ['Y', 'J', 'X', 'I', '1', '2', '4'],
            'Concluída': ['Z']
        }
        status_icons = {
            'Requisições canceladas': {
                'progress_label': 'on-the-way-text',
                'progress_bar': 'bg-lighter text-body rounded-start',
                'icon': 'bx bx-x-circle'
                },
            'Requisições em processo': {
                'progress_label': 'unloading-text',
                'progress_bar': 'bg-primary',
                'icon': 'bx bx-sync'
                },
            'Aguardando empenho': {
                'progress_label': 'loading-text',
                'progress_bar': 'text-bg-info',
                'icon': 'bx bx-time-five'
                },
            'Empenhado': {
                'progress_label': 'waiting-text',
                'progress_bar': 'bg-gray-900',
                'icon': 'bx bx-check-circle'
                },
            'Em trânsito': {
                'progress_label': 'loading-text',
                'progress_bar': 'bg-success',
                'icon': 'bx bx-right-arrow-circle'
                },
            'Concluída': {
                'progress_label': 'waiting-text',
                'progress_bar': 'bg-success rounded-end',
                'icon': 'bx bx-flag'
                },
        }

        plan_codes = {'CABW': 'CW', 'FMS': 'FM'}

        for segment_name, code in plan_codes.items():

            segment = tb_progresso[tb_progresso['CD_ORG_PROVEDOR_PLANO'] == code]
            # Inicializa os dicionários
            status_counts = {}
            total_count = segment.shape[0]
            resumo = {}
            grupos = {}
            outros_total = 0  # Inicia a soma para "Outros"

            for group, statuses in status_groups.items():
                count = segment[segment['ST_REQUISICAO'].isin(statuses)].shape[0]
                percentage = (count / total_count * 100) if total_count > 0 else 0
                status_counts[group] = {
                    'quantidade': count,
                    'porcentagem': round(percentage, 1),
                    'progress_label': status_icons[group]['progress_label'],
                    'progress_bar': status_icons[group]['progress_bar'],
                    'icon': status_icons[group]['icon']
                }
                # Adiciona ao resumo se necessário
                if group in ['Requisições canceladas', 'Concluída']:
                    grupos[group] = {
                        'porcentagem': round(percentage, 1),
                        'progress_label': status_icons[group]['progress_label'],
                        'progress_bar': status_icons[group]['progress_bar']
                    }
                else:
                    outros_total += count  # Soma as contagens para "Outros"

            resumo['Requisições canceladas'] = grupos['Requisições canceladas']
            # Calcula os "Outros" após o loop
            outros_percentage = (outros_total / total_count * 100) if total_count > 0 else 0
            resumo['Outros'] = {
                'quantidade': outros_total,
                'porcentagem': round(outros_percentage, 1),
                'progress_label': 'loading-text',
                'progress_bar': 'bg-primary'
            }

            resumo['Concluída'] = grupos['Concluída']
            try:
                obj, created = ProgressoRequisicoesExterior.objects.update_or_create(
                    tipo=segment_name,
                    defaults={
                        'dados_requisicoes': status_counts,
                        'resumo': resumo
                    }
                )
            except Exception:
                ...

    def consulta_ordem_servico(self, familia, projeto):
        result = Queries.query_consulta_ordem_servico(familia, projeto, self.connection)
        if not result.empty:
            dict_result = result.to_dict('records')
            os_familia = [{
                'PN': item['PN'],
                'CFF': item['CFF'],
                'NR_OS': item['NR_OS'],
                'ST_OS': item['ST_OS'],
                'DT_OS': item['DT_OS'].strftime('%d-%m-%Y') if item['DT_OS'] else None,
                'QT_OS': item['QT_OS']
                } for item in dict_result if item.get('QT_OS', 0) > 0]
            return os_familia
        else:
            return None
