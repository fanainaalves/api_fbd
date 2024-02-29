from modules.produto.sql import SQLProduto
from modules.produto.modelo import Produto
from service.connect import Connect

class DAOProduto(SQLProduto):
    def __init__(self):
        self._connection = Connect.get_instance()

    def create_table(self):
        return self._CREATE_TABLE

    def salvar(self, produto: Produto):
        if not isinstance(produto, Produto):
            raise Exception("Tipo inválido")
        query = self._INSERT_INTO
        cursor = self.connection.cursor()
        cursor.execute(query, (produto.descricao,))
        self.connection.commit()
        return produto

    def get_produto_by_description(self, descricao):
        query = self._SELECT_BY_DESCRICAO
        cursor = self.connection.cursor()
        cursor.execute(query, (descricao,))
        results = cursor.fetchall()
        cols = [desc[0] for desc in cursor.description]
        results = [dict(zip(cols, i)) for i in results]
        results = [Produto(**i) for i in results]
        return results

    def get_all(self):
        query = self._SELECT_ALL
        cursor = self.connection.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        cols = [desc[0] for desc in cursor.description]
        results = [dict(zip(cols, i)) for i in results]
        results = [Produto(**i) for i in results]
        return results

    def get_produto_por_id(self, id):
        query = self._SELECT_BY_ID
        cursor = self.connection.cursor()
        cursor.execute(query, (id,))
        results = cursor.fetchone()
        if not results:
            return None
        cols = [desc[0] for desc in cursor.description]
        results = dict(zip(cols, results))
        return results

    def deletar(self, produto: Produto):
        if not isinstance(produto, Produto):
            raise Exception("Tipo inválido")
        query = self._DELETE_BY_ID
        cursor = self.connection.cursor()
        cursor.execute(query, (produto.id,))
        self.connection.commit()
        return True
