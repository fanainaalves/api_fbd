from modules.produto.sql import SQLProduto
from modules.produto.modelo import Produto
from service.connect import Connect

class DAOProduto(SQLProduto):
    def __init__(self):
        self._connection = Connect().get_instance()

    def create_table(self):
        return self._CREATE_TABLE

    def add(self, produto: Produto):
        if not isinstance(produto, Produto):
            raise Exception("Tipo inválido")
        query = self._INSERT_INTO
        cursor = self._connection.cursor()
        valores = [produto.nome, produto.marca_id, produto.categoria_id]

        cursor.execute(query, valores)
        self._connection.commit()
        return produto

    def get_produtos_por_nome(self, nome):
        query = self._SELECT_BY_NOME
        cursor = self._connection.cursor()
        cursor.execute(query, [nome])
        results = cursor.fetchall()
        cols = [desc[0] for desc in cursor.description]
        results = [dict(zip(cols, i)) for i in results]
        results = [Produto(**i) for i in results]
        return results

    def get_all(self):
        query = self._SELECT_ALL
        cursor = self._connection.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        cols = [desc[0] for desc in cursor.description]
        results = [dict(zip(cols, i)) for i in results]
        results = [Produto(**i) for i in results]
        return results

    def get_produto_por_id(self, id):
        query = self._SELECT_BY_ID
        cursor = self._connection.cursor()
        cursor.execute(query, [id])
        results = cursor.fetchone()
        if not results:
            return None
        cols = [desc[0] for desc in cursor.description]
        results = dict(zip(cols, results))
        return results

    def deletar(self, id):
        query = self._DELETE_BY_ID
        cursor = self._connection.cursor()
        cursor.execute(query, [id])
        self._connection.commit()
        return True
