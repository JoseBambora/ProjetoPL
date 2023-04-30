import resultado
import re

def getArgs(numtabs,self):
    res = []
    t = numtabs * '\t'
    for e in range(0, len(self.l) - 1):
        elem = self.l[e]
        if not isinstance(elem,str):
            if isinstance(elem,ListVar) or isinstance(elem,ListStatic):
                res.append(f'{t}{elem.letter} = {self.letter}[{e}]')
                res.append(elem.toPythonArgs())
        elif not exp.match(elem):
            res.append(f'{t}{elem} = {self.letter}[{e}]')    
    return res

def getIf(self):
    res = []
    index = 0
    for elem in self.l:
        if not isinstance(elem,str):
            if isinstance(elem,ListVar) or isinstance(elem,ListStatic):
                res.append(f'({elem.toPythonIf()})')
        elif exp.match(elem):
            res.append(f'{self.letter}[{index}] == {elem}')
        index +=1 
    return res

exp = re.compile(r'((\+|\-)?\d+(\.\d+)?|True|False)')

class ListVar:
    def __init__(self, elem, rest, letter):
        self.l = [elem] + list(filter(lambda s: s != ':', rest))
        self.letter = letter

    def toPythonIf(self):
        res = []
        res.append(f'len({self.letter}) >= {len(self.l)-1}')
        res.extend(getIf(self))
        return ' and '.join(res)

    def toPythonArgs(self, numtabs=2):
        t = '\t' * numtabs
        res = getArgs(numtabs,self)
        res.append(f'{t}{self.l[-1]} = {self.letter}[{len(self.l)-1}:]')
        # res = Base(res).toPythonBase()
        # res.reverse()
        res = '\n'.join(res)
        return res

    def toPythonRes(self):
        aux = list(map(lambda l: resultado.Resultado(None, l, None).toPython(0)[7:], self.l))
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

    def toPythonArgs(self, numtabs=2):
        res = getArgs(numtabs,self)
        return '\n'.join(res)

    def toPythonRes(self):
        aux = list(map(lambda l: resultado.Resultado(None, l, None).toPython(0)[7:], self.l))
        content = ','.join(aux)
        return f'[{content}]'
    
    def toPythonIf(self):
        res = []
        res.append(f'len({self.letter}) == {len(self.l)}')
        res.extend(getIf(self))
        return ' and '.join(res)

    def getName(self):
        return self.letter

    def setName(self, letter):
        self.letter = letter

    def __str__(self):
        return self.toPythonRes()
