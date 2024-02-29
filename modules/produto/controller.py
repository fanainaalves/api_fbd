from flask import Blueprint, request, jsonify
from modules.produto.dao import DAOProduto
from modules.produto.modelo import Produto
from modules.produto.sql import SQLProduto

produto_controller = Blueprint('produto_controller', __name__)
dao_produto = DAOProduto
module_name = 'produto'


def get_produto():
    produtos = dao_produto.get_all()
    results = [produto.__dict__ for produto in produtos]
    response = jsonify(results)
    response.status_code = 200
    return response

def create_produto():
    data = request.json
    erros = []
    for campo in SQLProduto._CAMPOS_OBRIGATORIOS:
        if campo not in data.keys() or not data.get(campo, '').strip():
            erros.append(f"O campo {campo} é obrigatorio")

    if not erros and dao_produto.get_produto_by_description(**data):
        erros.append(f"Já existe um produto com essa descrição")
    if erros:
        response = jsonify(erros)
        response.status_code = 401
        return response

    produto = Produto(**data)
    dao_produto.salvar(produto)
    response = jsonify('OK')
    response.status_code = 201
    return response

@produto_controller.route(f'/{module_name}/', methods=['GET', 'POST'])
def get_or_create_produto_by_id():
    if request.method == 'GET':
        return get_produto()
    else:
        return create_produto()

@produto_controller.route(f'/{module_name}/<id>/', methods=['GET', 'PUT', 'DELETE'])
def get_update_delete_produto(id: int):
    if request.method == 'GET':
        produto = dao_produto.get_produto_por_id(id)
        if produto:
            return produto
        response = jsonify({})
        response.status_code = 404
        return response
    elif request.method == 'PUT':
        dados = request.json
        dados_existem = dao_produto.get_produto_por_id(id)
        if not dados_existem:
            response = jsonify(f'Produto com ID {id} não foi encontrada!')
            response.status_code = 404
            return response
        for campo in dados:
            setattr(dados_existem, campo, dados[campo])
            dao_produto.salvar(dados_existem)
            response = jsonify('Produto atualizada com sucesso!')
            response.status_code = 200
            return response
    elif request.method == 'DELETE':
        produto_existe = dao_produto.get_produto_por_id(id)
        if not produto_existe:
            response = jsonify(f'Produto com ID {id} não foi encontrada!')
            response.status_code = 404
            return response
        produto = Produto(**produto_existe)
        dao_produto.deletar(produto)
        response = jsonify('Produto excluída com sucesso!')
        response.status_code = 200
        return response

































