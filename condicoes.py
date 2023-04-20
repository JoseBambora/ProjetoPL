from resultado import Resultado
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
        if isinstance(self.struct[1], Resultado):
            then = f'{tabs}\t{self.struct[1].toPython()}'
        else:
            then = self.struct[1].toPythonAux(tab+1)
        if isinstance(self.struct[2], Resultado):
            corpoelse = f'{tabs}\t{self.struct[2].toPython()}'
        else:
            corpoelse = self.struct[2].toPythonAux(tab+1)
        return f'{tabs}if {cond}:\n{then}\n{tabs}else:\n{corpoelse}'
    def toPython(self):
        return self.toPythonAux(1)

    def __str__(self):
        return self.toPython()
        