class Base:
    def __init__(self, *variaveis):
        self.struct = (variaveis)

    def toPythonBase(self):
        args = ', '.join(self.struct[0])
        return f'({args})'
