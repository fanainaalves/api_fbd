import psycopg2

class Connect:

    def __init__(self):
        config = dict(
            dbname="estoque_fbd_2023_1",
            user="postgres", password="fanaina",
            host="localhost", port="5432"
        )
        self._connection = psycopg2.connect(**config)

    def create_tables(self):
        from modules.categoria.dao import DAOCategoria
        from modules.marca.dao import DAOMarca
        from modules.produto.dao import DAOProduto

        cursor = self._connection.cursor()
        cursor.execute(DAOMarca().create_table())
        cursor.execute(DAOCategoria().create_table())
        cursor.execute(DAOProduto().create_table())
        self._connection.commit()
        cursor.close()

    def get_instance(self):
        return self._connection

    def init_database(self, version='v1'):
        if version == 'v1':
            self.create_tables()
        if version == 'v2':
            self.update_database()
    def update_database(self):
        pass
