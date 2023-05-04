class Funcao:

    def __init__(self, nome, args, resultado):
        self.struct = (nome, args, resultado)

    def nova_funcao(self):
        res = {"nome": self.struct[0],
               "implementação": [{"args": self.struct[1], "res": self.struct[2]}]
               }
        return res
