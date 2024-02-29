class Marca:
    def __init__(self, nome=None, cnpj=None, id=None):
        self.nome = nome
        self.cnpj = cnpj
        self.id = id

    def __str__(self):
        return f'[{self.id}] {self.nome}'
