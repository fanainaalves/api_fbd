from modules.categoria.modelo import Categoria
from modules.marca.modelo import Marca

class Produto:
    def __init__(self, nome, marca: Marca | int = None, categoria: Categoria | int = None, id=None, **extra):
        self.nome = nome
        self.marca = marca
        self.categoria = categoria
        self.id = id
        self.get_extra_data(**extra)

    def get_extra_data(self, marca_id=None, categoria_id=None, **extra):
        if marca_id:
            marca_extra = {
                'nome': extra.get('marca_nome', ''),
            }
            self.marca = Marca(id=marca_id, **marca_extra)
        if categoria_id:
            categoria_extra = {
                'descricao': extra.get('categoria_descricao', ''),
            }
            self.categoria = Categoria(id=categoria_id, **categoria_extra)

    @property
    def marca_id(self):
        if type(self.marca) is Marca:
            return self.marca.id
        return self.marca

    @property
    def categoria_id(self):
        if type(self.categoria) is Categoria:
            return self.categoria.id
        return self.categoria
