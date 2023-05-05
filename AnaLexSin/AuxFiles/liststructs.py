import AnaLexSin.AuxFiles.resultado as resultado
import re

def getArgs(numtabs,self,bool):
    res = []
    aux = []
    t = numtabs * '\t'
    lim = len(self.l)
    if bool:
        lim -= 1
    for e in range(0, lim):
        elem = self.l[e]
        if not isinstance(elem,str):
            if isinstance(elem,ListVar) or isinstance(elem,ListStatic):
                res.append(f'{t}{elem.letter} = {self.letter}[{e}]')
                aux.append(elem.toPythonArgs())
        elif not exp.match(elem):
            res.append(f'{t}{elem} = {self.letter}[{e}]')  
    res.extend(aux)  
    return res

def getIf(self,aux):
    res = []
    index = 0
    for elem in self.l:
        if not isinstance(elem,str):
            if isinstance(elem,ListVar) or isinstance(elem,ListStatic):
                subcond = elem.toPythonIf(f'{aux}[{index}]')
                res.append(f'({subcond})')
        elif exp.match(elem):
            res.append(f'{aux}[{index}] == {elem}')
        index +=1 
    return res

exp = re.compile(r'((\+|\-)?\d+(\.\d+)?|True|False)')

class ListVar:
    def __init__(self, elem, rest, letter):
        self.l = [elem] + list(filter(lambda s: s != ':', rest))
        self.letter = letter

    def toPythonIf(self,aux=''):
        if(aux == ''):
            aux = self.letter
        res = []
        res.append(f'len({aux}) >= {len(self.l)-1}')
        res.extend(getIf(self,aux))
        return ' and '.join(res)

    def toPythonArgs(self, numtabs=2):
        t = '\t' * numtabs
        res = getArgs(numtabs,self,True)
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
        res = getArgs(numtabs,self,False)
        return '\n'.join(res)

    def toPythonRes(self):
        aux = list(map(lambda l: resultado.Resultado(None, l, None).toPython(0)[7:], self.l))
        content = ','.join(aux)
        return f'[{content}]'
    
    def toPythonIf(self,aux=''):
        if(aux == ''):
            aux = self.letter
        res = []
        res.append(f'len({aux}) == {len(self.l)}')
        res.extend(getIf(self,aux))
        return ' and '.join(res)

    def getName(self):
        return self.letter

    def setName(self, letter):
        self.letter = letter

    def __str__(self):
        return self.toPythonRes()
