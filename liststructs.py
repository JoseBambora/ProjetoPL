from imutable import getImut
from resultado import Resultado

class ListVar:
    def __init__(self,elem,rest,leter):
        self.l = [elem] + list(filter(lambda s : s != ':',rest))
        self.leter = leter
    def toPythonArgs(self,numtabs=1):
        res = []
        t = '\t'*numtabs
        for e in range(0,len(self.l)-1):
            res.append(f'{t}{self.l[e]} = {self.leter}[{e}]')
        res.append(f'{t}{self.l[-1]} = {self.leter}[{e+1}:]')
        return '\n'.join(res)
    def toPythonRes(self):
        aux = list(map(lambda l: Resultado(None,l,None).toPython(0)[7:],self.l))
        res = aux[:-1]
        cab = ','.join(res)
        return f'[{cab}] + {aux[-1]}'
    def getName(self):
        return self.leter
    def setName(self,leter):
        self.leter = leter
    def __str__(self):
        return self.toPythonRes()
    
class ListStatic:
    def __init__(self,elems,leter):
        self.l = list(filter(lambda s : s != ',',elems))
        self.leter = leter 
    def toPythonArgs(self,numtabs=1):
        res = []
        t = '\t'*numtabs
        for e in range(0,len(self.l)):
            res.append(f'{t}{self.l[e]} = {self.leter}[{e}]')
        return '\n'.join(res)
    def toPythonRes(self):
        aux = list(map(lambda l: Resultado(None,l,None).toPython(0)[7:],self.l))
        content = ','.join(aux)
        return f'[{content}]'
    def getName(self):
        return self.leter
    def setName(self,leter):
        self.leter = leter
    def __str__(self):
        return self.toPythonRes()
