from modules.categoria.sql import SQLCategoria
from modules.marca.sql import SQLMarca

class SQLProduto:
    _TABLE_NAME = 'produto'
    _COL_ID = 'id'
    _COL_NOME = 'nome'
    _COL_MARCA_ID = 'marca_id'
    _COL_CATEGORIA_ID = 'categoria_id'
    _CAMPOS_OBRIGATORIOS = [_COL_NOME]

    _REFERENCES_MARCA = f'{SQLMarca._TABLE_NAME}({SQLMarca._COL_ID})'
    _REFERENCES_CATEGORIA = f'{SQLCategoria._TABLE_NAME}({SQLCategoria._COL_ID})'

    _CREATE_TABLE = f'CREATE TABLE IF NOT EXISTS {_TABLE_NAME} ' \
                    f'(id serial primary key, ' \
                    f'{_COL_NOME} varchar(255), ' \
                    f'{_COL_MARCA_ID} int REFERENCES {_REFERENCES_MARCA}, ' \
                    f'{_COL_CATEGORIA_ID} int REFERENCES {_REFERENCES_CATEGORIA}' \
                    f');'

    _INSERT_INTO = f'INSERT INTO {_TABLE_NAME} ({_COL_NOME},  {_COL_MARCA_ID}, {_COL_CATEGORIA_ID}) VALUES (%s, %s, %s)'
    _SELECT_BY_CATEGORIA_ID = f"SELECT * from {_TABLE_NAME} where {_COL_CATEGORIA_ID} ilike %s"
    _SELECT_ALL = f"""
        SELECT 
            {_TABLE_NAME}.*,
            {SQLCategoria._TABLE_NAME}.{SQLCategoria._COL_DESCRICAO} as categoria_descricao,
            {SQLMarca._TABLE_NAME}.{SQLMarca._COL_NOME} as marca_nome
        from {_TABLE_NAME} 
        LEFT OUTER JOIN {SQLMarca._TABLE_NAME} on {_TABLE_NAME}.{_COL_MARCA_ID} = {SQLMarca._TABLE_NAME}.{SQLMarca._COL_ID}
        LEFT OUTER JOIN {SQLCategoria._TABLE_NAME} on {_TABLE_NAME}.{_COL_CATEGORIA_ID} = {SQLCategoria._TABLE_NAME}.{SQLCategoria._COL_ID}
    """
    _SELECT_BY_ID = f"SELECT * from {_TABLE_NAME} where id=%s"
    _SELECT_BY_NOME = f"SELECT * from {_TABLE_NAME} where {_COL_NOME} ilike %s"
    _DELETE_BY_ID = f"DELETE FROM {_TABLE_NAME} WHERE id=%s"
