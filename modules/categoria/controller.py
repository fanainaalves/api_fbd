from flask import Blueprint, request, jsonify
from modules.categoria.dao import DAOCategoria
from modules.categoria.modelo import Categoria
from modules.categoria.sql import SQLCategoria

categoria_controller = Blueprint('categoria_controller', __name__)
dao_categoria = DAOCategoria()
module_name = 'categoria'


def get_categorias():
    categorias = dao_categoria.get_all()
    results = [categoria.__dict__ for categoria in categorias]
    response = jsonify(results)
    response.status_code = 200
    return response


def create_categoria():
    data = request.json
    erros = []
    for campo in SQLCategoria._CAMPOS_OBRIGATORIOS:
        if campo not in data.keys() or not data.get(campo, '').strip():
            erros.append(f"O campo {campo} é obrigatorio")

    if not erros and dao_categoria.get_by_description(**data):
        erros.append(f"Já existe uma categoria com essa descrição")
    if erros:
        response = jsonify(erros)
        response.status_code = 401
        return response

    categoria = Categoria(**data)
    dao_categoria.salvar(categoria)
    response = jsonify('OK')
    response.status_code = 201
    return response


@categoria_controller.route(f'/{module_name}/', methods=['GET', 'POST'])
def get_or_create_categorias():
    if request.method == 'GET':
        return get_categorias()
    else:
        return create_categoria()


@categoria_controller.route(f'/{module_name}/<id>/', methods=['GET', 'PUT', 'DELETE'])
def get_update_delete_categoria(id: int):
    if request.method == 'GET':
        category = dao_categoria.get_categoria_por_id(id)
        if category:
            return category
        response = jsonify({})
        response.status_code = 404
        return response
    elif request.method == 'PUT':
        dados = request.json
        dados_existem = dao_categoria.get_categoria_por_id(id)
        if not dados_existem:
            response = jsonify(f'Categoria com ID {id} não foi encontrada!')
            response.status_code = 404
            return response
        for campo in dados:
            setattr(dados_existem, campo, dados[campo])
            dao_categoria.salvar(dados_existem)
            response = jsonify('Categoria atualizada com sucesso!')
            response.status_code = 200
            return response
    elif request.method == 'DELETE':
        categoria_existe = dao_categoria.get_categoria_por_id(id)
        if not categoria_existe:
            response = jsonify(f'Categoria com ID {id} não foi encontrada!')
            response.status_code = 404
            return response
        categoria = Categoria(**categoria_existe)
        dao_categoria.deletar(categoria)
        response = jsonify('Categoria excluída com sucesso!')
        response.status_code = 200
        return response