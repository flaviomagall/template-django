import cx_Oracle
import pandas as pd
import warnings
from config.settings import ORACLE_CONFIG, LIB_DIR


class OracleConnection:
    """
    Inicializa uma instância da classe OracleConnection utilizando configurações centralizadas.
    """
    oracle_client_initialized = False

    def __init__(self):
        # Utiliza as configurações diretamente do oracle_config importado
        self.user = ORACLE_CONFIG["user"]
        self.password = ORACLE_CONFIG["password"]
        self.dsn = ORACLE_CONFIG["dsn"]
        # Padrão para UTF-8 se não especificado
        self.encoding = ORACLE_CONFIG.get("encoding", "UTF-8")
        self.connection = None
        if not OracleConnection.oracle_client_initialized:
            cx_Oracle.init_oracle_client(lib_dir=LIB_DIR)
            OracleConnection.oracle_client_initialized = True

    def connect(self):
        """
        Estabelece a conexão com o banco de dados Oracle utilizando as configurações fornecidas.
        """

        self.connection = cx_Oracle.connect(user=self.user, password=self.password,
                                            dsn=self.dsn, encoding=self.encoding)
        return self.connection

    def __enter__(self):
        """
        Permite o uso do objeto em um contexto de gerenciador de contexto (com statement).
        """
        return self.connect()

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Garante o fechamento adequado da conexão ao sair do contexto.
        """
        if self.connection:
            self.connection.close()

    def execute_query(self, query, params=None):
        """
        Executa uma consulta SQL e retorna os resultados como um DataFrame do pandas.
        """
        with self.connect() as connection:
            try:
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore", category=UserWarning)
                    return pd.read_sql(query, con=connection, params=params)
            except Exception as e:
                print(f"Falha ao executar a consulta: {str(e)}")
                return pd.DataFrame()  # Retorna um DataFrame vazio em caso de erro
