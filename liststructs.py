class ListVar:
    def __init__(self,elem,rest,leter):
        self.l = list(filter(lambda s : s != ':',rest))
        self.l.insert(0,elem)
        self.leter = leter
    def toPythonArgs(self,numtabs=1):
        res = []
        t = '\t'*numtabs
        for e in range(0,len(self.l)-1):
            res.append(f'{t}{self.l[e]} = {self.leter}[{e}]')
        res.append(f'{t}{self.l[-1]} = {self.leter}[{e+1}:]')
        return '\n'.join(res)
    def toPythonRes(self):
        res = self.l[:-1]
        cab = ','.join(res)
        return f'[{cab}] + copy.deepcopy({self.l[-1]})'
    def getName(self):
        return self.leter
    def setName(self,leter):
        self.leter = leter
    def __str__(self):
        return str(self.l)
    
class ListStatic:
    def __init__(self,elems,leter):
        self.l = list(filter(lambda s : s != ',',elems))
        self.leter = leter 
    def toPythonArgs(self,numtabs=1):
        t = '\t'*numtabs
        return f'{t}if len({self.leter}) == {len(self.l)}:'
    def toPythonRes(self):
        return f'copy.deepcopy({self.leter})'
    def getName(self):
        return self.leter
    def setName(self,leter):
        self.leter = leter
    def __str__(self):
        return str(self.l)
