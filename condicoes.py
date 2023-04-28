class Condicoes:
    def __init__(self,condicao,corpothen,corpoelse):
        self.struct = (condicao,corpothen,corpoelse)
    def getThen(self):
        return self.struct[1]
    def getElse(self):
        return self.struct[1]
    def toPython(self,tab=2):
        tabs = '\t'*tab
        cond = ' '.join(self.struct[0])
        then = self.struct[1].toPython(tab+1)
        corpoelse = self.struct[2].toPython(tab+1)
        return f'{tabs}if {cond}:\n{then}\n{tabs}else:\n{corpoelse}'

    def __str__(self):
        return self.toPython()
        