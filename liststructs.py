from imutable import getImut
from resultado import Resultado
from base import Base


class ListVar:
    def __init__(self, elem, rest, letter):
        self.l = [elem] + list(filter(lambda s: s != ':', rest))
        self.letter = letter

    def toPythonArgs(self, numtabs=1):
        res = []
        t = '\t' * numtabs
        for e in range(0, len(self.l) - 1):
            res.append(f'{t}{self.l[e]} = {self.letter}[{e}]')
        res.append(f'{t}{self.l[-1]} = {self.letter}[{e + 1}:]')
        res = Base(res).toPythonBase()
        return res

    def toPythonRes(self):
        aux = list(map(lambda l: Resultado(None, l, None).toPython(0)[7:], self.l))
        res = aux[:-1]
        cab = ','.join(res)
        return f'[{cab}] + {aux[-1]}'

    def getName(self):
        return self.letter

    def setName(self, letter):
        self.letter = letter

    def __str__(self):
        return self.toPythonRes()


class ListStatic:
    def __init__(self, elems, letter):
        self.l = list(filter(lambda s: s != ',', elems))
        self.letter = letter

    def toPythonArgs(self, numtabs=1):
        res = []
        t = '\t' * numtabs
        for e in range(0, len(self.l)):
            res.append(f'{t}{self.l[e]} = {self.letter}[{e}]')
        return '\n'.join(res)

    def toPythonRes(self):
        aux = list(map(lambda l: Resultado(None, l, None).toPython(0)[7:], self.l))
        content = ','.join(aux)
        return f'[{content}]'

    def getName(self):
        return self.letter

    def setName(self, letter):
        self.letter = letter

    def __str__(self):
        return self.toPythonRes()
