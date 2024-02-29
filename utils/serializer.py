
def serialize(obj, campo_fk='id'):
    serialized_object = obj.__dict__
    for chave, valor in serialized_object.items():
        try:
            if hasattr(valor, 'to_json'):
                serialized_object[chave] = getattr(valor, 'to_json')()
            else:
                serialized_object[chave] = str(valor)
        except (Exception,):
            pass
    return serialized_object

