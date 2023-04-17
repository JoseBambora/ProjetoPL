class Condicoes:
    def __init__(self,condicao,corpothen,corpoelse):
        self.struct = (condicao,corpothen,corpoelse)
    def getThen(self):
        return self.struct[1]
    def getElse(self):
        return self.struct[1]
    def toPythonAux(self,tab):
        tabs = '\t'*tab
        print(self.struct[0])
        cond = ' '.join(self.struct[0])
        if isinstance(self.struct[1], str):
            then = f'{tabs}\tResultado'
        else:
            then = self.struct[1].toPythonAux(tab+1)
        if isinstance(self.struct[2], str):
            corpoelse = f'{tabs}\tResultado'
        else:
            corpoelse = self.struct[2].toPythonAux(tab+1)
        return f'{tabs}if {cond}:\n{then}\n{tabs}else:\n{corpoelse}'
    def toPython(self):
        return self.toPythonAux(1)

    def __str__(self):
        c1 = str(self.struct[0])
        c2 = str(self.struct[1])
        c3 = str(self.struct[2])
        return f'({c1},{c2},{c3})'
        