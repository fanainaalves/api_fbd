class Categoria():
    def __init__(self, descricao = None, id=None):
        self.id = id
        self.descricao = descricao

    def __str__(self):
        return f'[{self.id}] {self.descricao}'
