import logging
import pandas as pd


class Queries:
    @staticmethod
    def query_pn_preferencial(part_number, cff, projeto, connection) -> pd.DataFrame:
        """
        Recupera o PN preferencial, o CFF do PN informado e outras informações relacionadas.
        Args:
            item (Item): Item do pedido a ser consultado.
        Returns:
            Dataframe contendo as informações do PN preferencial.
        """
        colunas_esperadas = ['MATERIAL_PREFERENCIAL_PN', 'MATERIAL_PREFERENCIAL_CFF', 'QT_DMM_TOTAL', 'CATEGORIA']
        try:
            cff_condition = "AND T_FORNECEDOR_MATERIAL.CD_CFF = :cff" if cff else "AND ROWNUM = 1"
            params = {'pn': part_number, 'cff': cff, 'projeto': projeto} if cff else {'pn': part_number, 'projeto': projeto}

            base_query = """
                    SELECT
                        T_MATERIAL_PREFERENCIAL.NR_PN AS MATERIAL_PREFERENCIAL_PN,
                        T_FORNECEDOR_MATERIAL_PREFERENCIAL.CD_CFF AS MATERIAL_PREFERENCIAL_CFF,
                        CONCAT(T_NSN.CD_CLASSE,NR_IDENT_ITEM) AS NSN,
                        QT_DMM_TOTAL,
                        T_MATERIAL.CD_CATEGORIA AS CATEGORIA,
                        T_MATERIAL_PREFERENCIAL.CD_ORG_PROVEDOR AS ORG_PROVEDOR,
                        T_MATERIAL.NM_BASICO AS NOMENCLATURA
                    FROM
                        T_MATERIAL_FAIXA_CONSUMO
                        INNER JOIN T_MATERIAL ON T_MATERIAL_FAIXA_CONSUMO.CD_MATERIAL=T_MATERIAL.CD_MATERIAL
                        INNER JOIN T_MATERIAL T_MATERIAL_PREFERENCIAL ON T_MATERIAL_FAIXA_CONSUMO.CD_MATERIAL_PREFERENCIAL=T_MATERIAL_PREFERENCIAL.CD_MATERIAL
                        INNER JOIN T_FORNECEDOR T_FORNECEDOR_MATERIAL ON T_MATERIAL.CD_FORNECEDOR=T_FORNECEDOR_MATERIAL.CD_FORNECEDOR
                        INNER JOIN T_FORNECEDOR T_FORNECEDOR_MATERIAL_PREFERENCIAL ON T_MATERIAL_PREFERENCIAL.CD_FORNECEDOR=T_FORNECEDOR_MATERIAL_PREFERENCIAL.CD_FORNECEDOR
                        LEFT JOIN T_NSN ON T_NSN.CD_ITEM=T_MATERIAL_PREFERENCIAL.CD_ITEM
                    WHERE
                        T_MATERIAL_FAIXA_CONSUMO.CD_PROJETO = :projeto
                        AND T_MATERIAL.NR_PN = :pn
                """
            query = f"{base_query} {cff_condition}"
            result = connection.execute_query(query, params)
            return result
        except Exception as e:
            logging.error(f"Falha ao executar a consulta: {str(e)}")
            dados_iniciais = {coluna: [None] for coluna in colunas_esperadas}
            result = pd.DataFrame(dados_iniciais)
            return result


    @staticmethod
    def query_alternados(pn_preferencial, cff_preferencial, projeto, connection) -> pd.DataFrame:
        try:
            query = """
                SELECT
                    T_MATERIAL.NR_PN AS MATERIAL_PN, T_FORNECEDOR_MATERIAL.CD_CFF AS MATERIAL_CFF
                FROM
                    T_MATERIAL_FAIXA_CONSUMO
                    INNER JOIN T_MATERIAL ON T_MATERIAL_FAIXA_CONSUMO.CD_MATERIAL=T_MATERIAL.CD_MATERIAL
                    INNER JOIN T_MATERIAL T_MATERIAL_PREFERENCIAL ON T_MATERIAL_FAIXA_CONSUMO.CD_MATERIAL_PREFERENCIAL=T_MATERIAL_PREFERENCIAL.CD_MATERIAL
                    INNER JOIN T_FORNECEDOR T_FORNECEDOR_MATERIAL ON T_MATERIAL.CD_FORNECEDOR=T_FORNECEDOR_MATERIAL.CD_FORNECEDOR
                    INNER JOIN T_FORNECEDOR T_FORNECEDOR_MATERIAL_PREFERENCIAL ON T_MATERIAL_PREFERENCIAL.CD_FORNECEDOR=T_FORNECEDOR_MATERIAL_PREFERENCIAL.CD_FORNECEDOR
                WHERE
                    T_MATERIAL_FAIXA_CONSUMO.CD_PROJETO = :projeto
                    AND T_MATERIAL_PREFERENCIAL.NR_PN = :pn
                    AND T_FORNECEDOR_MATERIAL_PREFERENCIAL.CD_CFF = :cff
            """
            params = {'pn': pn_preferencial, 'cff': cff_preferencial, 'projeto': projeto}
            result = connection.execute_query(query, params)
            return result
        except Exception as e:
            logging.error(f"Falha ao executar a consulta: {str(e)}")


    @staticmethod
    def query_dados_primarios(familia, projeto, connection):
        try:
            # Transforma a lista de dicionários em uma lista de tuplas (PN, CFF)
            pares_pn_cff = [(item["MATERIAL_PN"], item["MATERIAL_CFF"]) for item in familia]

            # Inicializa a expressão WITH com os pares PN e CFF
            with_expression = "WITH pares_pn_cff AS ("
            with_expression += " UNION ALL ".join(
                f"SELECT '{pn}' AS pn, '{cff}' AS cff FROM dual" for pn, cff in pares_pn_cff
            )
            with_expression += ")"

            # Consulta principal que utiliza a expressão WITH
            query = f"""
            {with_expression}
            SELECT
                p.pn,
                p.cff,
                COALESCE((
                    SELECT SUM(e.QT_ESTOQUE)
                    FROM t_estoque_local e
                    INNER JOIN t_material m2 ON e.cd_material = m2.cd_material
                    INNER JOIN t_setor s ON e.cd_unidade = s.cd_unidade AND e.cd_setor = s.cd_setor
                    WHERE m2.nr_pn = p.pn
                    AND e.cd_projeto = '{projeto}'
                    AND s.tp_setor = 'AU'
                ), 0) AS ESTOQUE_TOTAL,
                COALESCE((
                    SELECT SUM(qt_em_emergencia)
                    FROM t_emergencia
                    INNER JOIN t_material ON t_emergencia.cd_material = t_material.cd_material
                    INNER JOIN t_fornecedor ON t_material.cd_fornecedor = t_fornecedor.cd_fornecedor
                    WHERE t_emergencia.st_emergencia IN ('S', 'B', 'X', 'P')
                    AND t_material.nr_pn = p.pn
                    AND t_fornecedor.cd_cff = p.cff
                    AND t_emergencia.cd_projeto = '{projeto}'
                ), 0) AS EMERGENCIA_TOTAL,
                COALESCE((
                    SELECT SUM(t_plano_requisicao.qt_requisicao)
                    FROM T_PLANO_REQUISICAO
                    INNER JOIN T_MATERIAL ON T_PLANO_REQUISICAO.CD_MATERIAL = T_MATERIAL.CD_MATERIAL
                    INNER JOIN T_FORNECEDOR ON T_MATERIAL.cd_fornecedor = t_fornecedor.cd_fornecedor
                    WHERE T_PLANO_REQUISICAO.CD_PROJETO = '{projeto}'
                    AND T_MATERIAL.nr_pn = p.pn
                    AND t_fornecedor.cd_cff = p.cff
                    AND T_PLANO_REQUISICAO.dt_plano_requisicao >= TO_DATE('01 Jan 2023', 'DD MON YYYY')
                    AND st_plano_requisicao NOT IN ('CAN', 'CON')
                    AND tp_plano_requisicao = 'M'
                ), 0) AS REQUISICAO_TOTAL
            FROM
                pares_pn_cff p
                JOIN t_material m ON p.pn = m.nr_pn
                JOIN t_fornecedor f ON m.cd_fornecedor = f.cd_fornecedor AND p.cff = f.cd_cff
                LEFT JOIN T_ESTOQUE_LOCAL e ON m.cd_material = e.cd_material AND e.cd_projeto = '{projeto}'
                LEFT JOIN t_setor s ON e.cd_unidade = s.cd_unidade AND e.cd_setor = s.cd_setor AND s.tp_setor = 'AU'
            WHERE
                (f.cd_cff = p.cff)
            GROUP BY
                p.pn, p.cff
            """
            result = connection.execute_query(query)
            return result
        except Exception as e:
            logging.error(f"Falha ao executar a consulta: {str(e)}")
            return None

    @staticmethod
    def query_unidade_estoque(estoque_fab, projeto, connection):
        try:
            # Transforma a lista de dicionários em uma lista de tuplas (PN, CFF)
            pares_pn_cff = [(item["PN"], item["CFF"]) for item in estoque_fab]

            # Inicializa a expressão WITH com os pares PN e CFF
            with_expression = "WITH pares_pn_cff AS ("
            with_expression += " UNION ALL ".join(
                f"SELECT '{pn}' AS pn, '{cff}' AS cff FROM dual" for pn, cff in pares_pn_cff
            )
            with_expression += ")"

            # Consulta principal que utiliza a expressão WITH
            query = f"""
            {with_expression}
            SELECT
                p.pn,
                p.cff,
                SUM(e.QT_ESTOQUE) AS total_estoque,
                LISTAGG(DISTINCT sg_unidade,',') WITHIN GROUP (ORDER BY sg_unidade) AS unidades
            FROM
                pares_pn_cff p
                INNER JOIN T_MATERIAL m ON p.pn = m.nr_pn
                INNER JOIN t_fornecedor f ON m.cd_fornecedor = f.cd_fornecedor AND p.cff = f.cd_cff
                INNER JOIN T_ESTOQUE_LOCAL e ON m.CD_MATERIAL = e.CD_MATERIAL
                INNER JOIN t_setor s ON e.cd_unidade = s.cd_unidade AND e.cd_setor = s.cd_setor
                INNER JOIN t_unidade u ON e.cd_unidade = u.cd_unidade
            WHERE
                s.tp_setor = 'AU' and e.qt_estoque>0 and e.cd_projeto = '{projeto}'
            GROUP BY
                p.pn,
                p.cff
            """
            result = connection.execute_query(query)
            return result
        except Exception as e:
            logging.error(f"Falha ao executar a consulta: {str(e)}")
            return None

    @staticmethod
    def query_status_emergencia(emergencia_list, projeto, connection):
        dicEmergencia ={
            'S':'Aguardando solução',
            'A':'Atendida total',
            'B':'Atendida parcial',
            'C':'Cancelada',
            'X':'Expedido parcial',
            'E':'Expedido total',
            'P':'Providência tomada',
            'R':'Redirecionado'
        }

        tipos_emergencia = {'AIFP', 'ANCE', 'EIFM', 'ENCE', 'INV', 'IPLR'}
        tipos_pnor = {'APE', 'APLI', 'EIF0', 'EIF1', 'EIF2', 'ENC4', 'EPL3', 'EPLR', 'INOP', 'MPCA', 'PNOR', 'REN', 'TBO', 'TLV'}

        try:
            # Transforma a lista de dicionários em uma lista de tuplas (PN, CFF)
            pares_pn_cff = [(item["PN"], item["CFF"]) for item in emergencia_list]

            # Inicializa a expressão WITH com os pares PN e CFF
            with_expression = "WITH pares_pn_cff AS ("
            with_expression += " UNION ALL ".join(
                f"SELECT '{pn}' AS pn, '{cff}' AS cff FROM dual" for pn, cff in pares_pn_cff
            )
            with_expression += ")"

            # Consulta principal que utiliza a expressão WITH
            query = f"""
            {with_expression}
            SELECT
                p.pn,
                p.cff,
                e_info.NR_EMERGENCIA,
                e_info.CD_TIPO,
                e_info.QT_EM_EMERGENCIA,
                e_info.ST_EMERGENCIA
            FROM
                pares_pn_cff p
                LEFT JOIN (
                    SELECT
                        T_MATERIAL.NR_PN,
                        T_FORNECEDOR.CD_CFF,
                        T_EMERGENCIA.NR_EMERGENCIA,
                        T_EMERGENCIA.CD_TIPO,
                        T_EMERGENCIA.QT_EM_EMERGENCIA,
                        T_EMERGENCIA.ST_EMERGENCIA
                    FROM
                        T_EMERGENCIA
                        INNER JOIN T_MATERIAL ON T_EMERGENCIA.CD_MATERIAL = T_MATERIAL.CD_MATERIAL
                        INNER JOIN T_FORNECEDOR ON T_MATERIAL.CD_FORNECEDOR = T_FORNECEDOR.CD_FORNECEDOR
                    WHERE
                        T_EMERGENCIA.ST_EMERGENCIA IN ('S', 'B', 'X', 'P')
                        AND T_EMERGENCIA.CD_PROJETO = '{projeto}'
                ) e_info ON e_info.NR_PN = p.pn AND e_info.CD_CFF = p.cff
            GROUP BY
                p.pn,
                p.cff,
                e_info.NR_EMERGENCIA,
                e_info.CD_TIPO,
                e_info.QT_EM_EMERGENCIA,
                e_info.ST_EMERGENCIA
            """
            result = connection.execute_query(query)
            # Agrupando por PN e CFF
            grouped = result.groupby(["PN", "CFF"])

            # Criando a lista final
            categorizado = {'Emergencia': [], 'PedidoNormal': []}

            for (pn, cff), group in grouped:
                group['ST_EMERGENCIA'] = group['ST_EMERGENCIA'].map(dicEmergencia)
                emergencias_df = group[group['CD_TIPO'].isin(tipos_emergencia)]
                pedidos_normais_df = group[group['CD_TIPO'].isin(tipos_pnor)]

                qt_emergencia = emergencias_df["QT_EM_EMERGENCIA"].sum()
                qt_pedido_normal = pedidos_normais_df["QT_EM_EMERGENCIA"].sum()

                dados_emergencia = emergencias_df.drop(["PN", "CFF"], axis=1).to_dict("records")
                dados_pedido_normal = pedidos_normais_df.drop(["PN", "CFF"], axis=1).to_dict("records")

                categorizado['Emergencia'].append({
                    'PN': pn,
                    'CFF': cff,
                    'Qtde': qt_emergencia,
                    'Dados': dados_emergencia
                })
                if dados_pedido_normal:
                    categorizado['PedidoNormal'].append({
                        'PN': pn,
                        'CFF': cff,
                        'Qtde': qt_pedido_normal,
                        'Dados': dados_pedido_normal
                    })
            return categorizado
        except Exception as e:
            logging.error(f"Falha ao executar a consulta: {str(e)}")
            return None

    @staticmethod
    def query_status_requisicao(requisicao_list, projeto, connection):
        dictRequisicao = {
            '6': 'Anulada',
            'F': 'Em cotação',
            'M': 'Mapa Gerado',
            'V': 'Validada',
            'W': 'Empenho Aprovado',
            'Z': 'Recebido Solicitante',
            'Y': 'Recebido Parcial',
            'S': 'Suspendido Temporariamente',
            'G': 'Seleção Cotação',
            'J': 'Recebido Comissão',
            'N': 'Mapa Aprovado',
            'O': 'Análise do Pedido',
            '3': 'Em discrepância',
            'Q': 'Controle de Qualidade',
            'X': 'Expedida',
            'C': 'Cancelada',
            'E': 'Empenho Gerado',
            'I': 'Embarcado',
            'L': 'Reparável expedido para fornecedor',
            'P': 'Publicação atendida',
            '2': 'Expedido pelo USG',
            '5': 'Item deserto',
            '1': 'Em serapação pelo USG',
            '4': 'Volume no Solicitante',
            'A': 'Aguardando Validação / Autorização'
        }
        try:
            # Transforma a lista de dicionários em uma lista de tuplas (PN, CFF)
            pares_pn_cff = [(item["PN"], item["CFF"]) for item in requisicao_list]

            # Inicializa a expressão WITH com os pares PN e CFF
            with_expression = "WITH pares_pn_cff AS ("
            with_expression += " UNION ALL ".join(
                f"SELECT '{pn}' AS pn, '{cff}' AS cff FROM dual" for pn, cff in pares_pn_cff
            )
            with_expression += ")"

            # Consulta principal que utiliza a expressão WITH
            query = f"""
            {with_expression}
            SELECT
                p.pn,
                p.cff,
                r_info.nr_requisicao,
                r_info.st_requisicao,
                r_info.dt_status_requisicao,
                r_info.QT_REQUISICAO
            FROM
                pares_pn_cff p
                LEFT JOIN (
                    SELECT
                        T_MATERIAL.NR_PN,
                        T_FORNECEDOR.CD_CFF,
                        T_PLANO_REQUISICAO.nr_requisicao,
                        T_PLANO_REQUISICAO.st_requisicao,
                        T_PLANO_REQUISICAO.dt_status_requisicao,
                        T_PLANO_REQUISICAO.QT_REQUISICAO
                    FROM
                        T_PLANO_REQUISICAO
                        INNER JOIN T_MATERIAL ON T_PLANO_REQUISICAO.CD_MATERIAL = T_MATERIAL.CD_MATERIAL
                        INNER JOIN T_FORNECEDOR ON T_MATERIAL.CD_FORNECEDOR = T_FORNECEDOR.CD_FORNECEDOR
                    WHERE
                        T_PLANO_REQUISICAO.CD_PROJETO = '{projeto}'
                        AND T_PLANO_REQUISICAO.DT_PLANO_REQUISICAO >= TO_DATE('01 Jan 2022', 'DD MON YYYY')
                        AND T_PLANO_REQUISICAO.ST_PLANO_REQUISICAO NOT IN ('CAN', 'CON')
                        AND T_PLANO_REQUISICAO.TP_PLANO_REQUISICAO = 'M'
                ) r_info ON r_info.NR_PN = p.pn AND r_info.CD_CFF = p.cff
            GROUP BY
                p.pn,
                p.cff,
                r_info.nr_requisicao,
                r_info.st_requisicao,
                r_info.dt_status_requisicao,
                r_info.QT_REQUISICAO
            """
            result = connection.execute_query(query)
            if not result.empty:
                result['DT_STATUS_REQUISICAO'] = result['DT_STATUS_REQUISICAO'].dt.strftime('%d-%m-%Y')
                grouped = result.groupby(["PN", "CFF"])
                result_list = []
                for (pn, cff), group in grouped:
                    # Calculando a soma de QT_EM_REQUISICAO para o grupo
                    qt_em_requisicaoa_total = group["QT_REQUISICAO"].sum()
                    group['ST_REQUISICAO'] = group['ST_REQUISICAO'].replace(dictRequisicao)
                    # Preparando os dados do grupo
                    dados = group.drop(["PN", "CFF"], axis=1).to_dict("records")
                    # Adicionando ao resultado
                    result_list.append({
                        "PN": pn,
                        "CFF": cff,
                        "REQUISICAO_TOTAL": qt_em_requisicaoa_total,
                        "Dados": dados
                    })

                return result_list
            else:
                return None
        except Exception as e:
            logging.error(f"Falha ao executar a consulta: {str(e)}")
            return None


    @staticmethod
    def query_estoque_PAMA(estoque_list, connection):
        # Transforma a lista de dicionários em uma lista de tuplas (PN, CFF)
        pares_pn_cff = [(item["MATERIAL_PN"], item["MATERIAL_CFF"]) for item in estoque_list]

        # Inicializa a expressão WITH com os pares PN e CFF
        with_expression = "WITH pares_pn_cff AS ("
        with_expression += " UNION ALL ".join(
            f"SELECT '{pn}' AS pn, '{cff}' AS cff FROM dual" for pn, cff in pares_pn_cff
        )
        with_expression += ")"

        # Consulta principal que utiliza a expressão WITH
        query = f"""
        {with_expression}
        SELECT
            e.CD_PROJETO, SUM(e.QT_ESTOQUE) AS total_estoque,
            p.pn,
            p.cff
        FROM
            pares_pn_cff p
            INNER JOIN T_MATERIAL m ON p.pn = m.nr_pn
            INNER JOIN t_fornecedor f ON m.cd_fornecedor = f.cd_fornecedor AND p.cff = f.cd_cff
            INNER JOIN T_ESTOQUE_LOCAL e ON m.CD_MATERIAL = e.CD_MATERIAL
            INNER JOIN t_setor s ON e.cd_unidade = s.cd_unidade AND e.cd_setor = s.cd_setor
        WHERE
            s.tp_setor = 'AU' AND e.cd_unidade = 304
        GROUP BY
            e.CD_PROJETO,
            p.pn,
            p.cff
        """
        result = connection.execute_query(query)
        return result


    @staticmethod
    def query_progresso_requisicoes_exterior(connection):
        query = """
        select nr_requisicao, cd_projeto, cd_org_provedor_plano, dt_requisicao, st_requisicao, dt_status_requisicao, cd_moeda,
        vl_preco_requisicao vl_unitario, qt_requisicao, ds_requisicao, tx_comentario from t_plano_requisicao where (cd_org_provedor_plano='CW' or  cd_org_provedor_plano='FM') and cd_unidade_cria=304 and tp_plano_requisicao='M'
        and (in_extra_sistema='N' or in_extra_sistema is null) and nr_requisicao not like 'LS%C%' and dt_requisicao>= (sysdate -365)
        """
        result = connection.execute_query(query)
        return result


    @staticmethod
    def query_consulta_ordem_servico(familia, projeto, connection):
        try:
            # Transforma a lista de dicionários em uma lista de tuplas (PN, CFF)
            pares_pn_cff = [(item["MATERIAL_PN"], item["MATERIAL_CFF"]) for item in familia]

            # Inicializa a expressão WITH com os pares PN e CFF
            with_expression = "WITH pares_pn_cff AS ("
            with_expression += " UNION ALL ".join(
                f"SELECT '{pn}' AS pn, '{cff}' AS cff FROM dual" for pn, cff in pares_pn_cff
            )
            with_expression += ")"

            # Consulta principal que utiliza a expressão WITH
            query = f"""
            {with_expression}
            SELECT
                p.pn,
                p.cff,
                os.nr_os,
                os.st_os,
                os.dt_os,
                os.qt_os
            FROM
                t_ordem_servico os
                LEFT JOIN ts_ctr_projecao_venc_aeronave tpa ON os.nr_equipamento = tpa.nr_equipamento_cjm
                LEFT JOIN t_material m ON os.cd_material = m.cd_material
                LEFT JOIN t_fornecedor f ON m.cd_fornecedor = f.cd_fornecedor
                JOIN pares_pn_cff p ON m.nr_pn = p.pn AND f.cd_cff = p.cff
            WHERE
                os.cd_setor_executante IN (
                    'L4H', 'LH4', 'LA4', 'L4V', 'LCM', 'L4G', 'L5P', 'LG4', 'LL4', 'L8X',
                    'L4N', 'L4Q', 'LC4', 'LB4', 'LC5', 'LMF', 'LI4', 'L4P', 'L4L', 'LK4', 'LAI'
                )
                AND os.st_os NOT IN ('CAN', 'CON')
                AND os.cd_projeto = '{projeto}'
            """
            result = connection.execute_query(query)
            return result
        except Exception as e:
            logging.error(f"Falha ao executar a consulta: {str(e)}")
            return None
