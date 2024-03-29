from flask import Blueprint, request, jsonify
from modules.marca.dao import DAOMarca
from modules.marca.modelo import Marca
from modules.marca.sql import SQLMarca

marca_controller = Blueprint('marca_controller', __name__)
dao_marca = DAOMarca()
module_name = 'marca'

def get_marcas():
    marcas = dao_marca.get_all()
    results = [marca.__dict__ for marca in marcas]
    response = jsonify(results)
    response.status_code = 200
    return response

def create_marca():
    data = request.json
    erros = []
    for campo in SQLMarca._CAMPOS_OBRIGATORIOS:
        if campo not in data.keys() or not data.get(campo, '').strip():
            erros.append(f"O campo {campo} é obrigatorio")

    cnpj = data.get('cnpj')
    if cnpj and not cnpj.isnumeric():
        erros.append(f"O campo cnpj só aceita números")

    if not erros and dao_marca.get_by_cnpj(cnpj):
        erros.append(f"Já existe uma marca com esse CNPJ")
    if erros:
        response = jsonify(erros)
        response.status_code = 401
        return response

    marca = Marca(**data)
    dao_marca.add(marca)
    response = jsonify('OK')
    response.status_code = 201
    return response

@marca_controller.route('/marca/', methods=['GET', 'POST'])
def get_or_create_marca():
    if request.method == 'GET':
        return get_marcas()
    else:
        return create_marca()

@marca_controller.route(f'/{module_name}/<cnpj>/', methods=['GET', 'PUT', 'DELETE'])
def get_marca_update_delete_categoria(cnpj: int):
    if request.method == 'GET':
        marca = dao_marca.get_marca_by_cnpj(cnpj)
        if marca:
            return marca
        response = jsonify({})
        response.status_code = 404
        return response
    elif request.method == 'PUT':
        dados = request.json
        dados_existem = dao_marca.get_marca_by_cnpj(cnpj)
        if not dados_existem:
            response = jsonify(f'Marca com CNPJ {cnpj} não foi encontrada!')
            response.status_code = 404
            return response
        for campo in dados:
            setattr(dados_existem, campo, dados[campo])
            dao_marca.add(dados_existem)
            response = jsonify('Marca atualizada com sucesso!')
            response.status_code = 200
            return response
    elif request.method == 'DELETE':
        marca_existe = dao_marca.get_marca_by_cnpj(cnpj)
        if not marca_existe:
            response = jsonify(f'Marca com CNPJ {cnpj} não foi encontrada!')
            response.status_code = 404
            return response
        marca = Marca(**marca_existe)
        dao_marca.deletar(marca)
        response = jsonify('Marca excluída com sucesso!')
        response.status_code = 200
        return response
