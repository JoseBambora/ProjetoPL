from resultado import Resultado
class Condicoes:
    def __init__(self,condicao,corpothen,corpoelse):
        self.struct = (condicao,corpothen,corpoelse)
    def getThen(self):
        return self.struct[1]
    def getElse(self):
        return self.struct[1]
    def toPython(self,tab=1):
        tabs = '\t'*tab
        print(self.struct[0])
        cond = ' '.join(self.struct[0])
        if isinstance(self.struct[1], Resultado):
            then = f' {self.struct[1].toPython(tab+1)}'
        else:
            then = self.struct[1].toPython(tab+1)
        if isinstance(self.struct[2], Resultado):
            corpoelse = f' {self.struct[2].toPython(tab+1)}'
        else:
            corpoelse = self.struct[2].toPython(tab+1)
        return f'{tabs}if {cond}:\n{then}\n{tabs}else:\n{corpoelse}'

    def __str__(self):
        return self.toPython()
        