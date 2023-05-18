import copy

def getReservadas():
    reservadas = set()
    reservadas.add('map')
    reservadas.add('filter')
    reservadas.add('reverse')
    reservadas.add('sort')
    reservadas.add('foldr')
    reservadas.add('foldl')
    return reservadas

def getPreDefined():
    reservadas = getReservadas()
    reservadas.add('fold')
    return reservadas

def mapFun(arg0,arg1):
    cp = copy.deepcopy(arg1)
    return list(map(arg0,cp))

def filterFun(arg0,arg1):
    cp = copy.deepcopy(arg1)
    return list(filter(arg0,cp))

def reverseFun(arg0):
    cp = copy.deepcopy(arg0)
    cp.reverse()
    return cp

def sortFun(arg0,arg1):
    cp = copy.deepcopy(arg1)
    cp.sort(key=arg0)
    return cp

def foldFun(arg0,arg1,arg2):
    res = arg1
    for elem in arg2:
        res = arg0(elem,res)
    return res

def foldrFun(arg0,arg1,arg2):
    return foldFun(arg0,arg1,copy.deepcopy(arg2))
    
def foldlFun(arg0,arg1,arg2):
    return foldFun(arg0,arg1,reverseFun(arg2))

def getName(name):
    return name + 'Fun'

def getCodigo():
    codigoPython = []
    for name in ['map','filter']:
        codigoPython.append(f'# arg0: Função a aplicar')
        codigoPython.append(f'# arg1: Lista a percorrer')
        codigoPython.append(f'def {name}Fun(arg0,arg1):')
        codigoPython.append(f'\tcp = copy.deepcopy(arg1)')
        codigoPython.append(f'\treturn list({name}(arg0,cp))\n')
    codigoPython.append(f'# arg0: Lista a inverter')
    codigoPython.append(f'def reverseFun(arg0):')
    codigoPython.append(f'\tcp = copy.deepcopy(arg0)')
    codigoPython.append(f'\tcp.reverse()')
    codigoPython.append(f'\treturn cp\n')
    codigoPython.append(f'# arg0: Função de comparação')
    codigoPython.append(f'# arg1: Lista para ordenar')
    codigoPython.append(f'def sortFun(arg0,arg1):')
    codigoPython.append(f'\tcp = copy.deepcopy(arg1)')
    codigoPython.append(f'\tcp.sort(key=arg0)')
    codigoPython.append(f'\treturn cp\n')
    codigoPython.append(f'# arg0: Função a aplicar a cada elemento')
    codigoPython.append(f'# arg1: Caso da lista vazia')
    codigoPython.append(f'# arg2: Lista para aplicar o fold')
    codigoPython.append(f'def foldFun(arg0,arg1,arg2):')
    codigoPython.append(f'\tres = arg1')
    codigoPython.append(f'\tfor elem in arg2:')
    codigoPython.append(f'\t\tres = arg0(elem,res)')
    codigoPython.append(f'\treturn res\n')
    codigoPython.append(f'# arg0: Função a aplicar a cada elemento')
    codigoPython.append(f'# arg1: Caso da lista vazia')
    codigoPython.append(f'# arg2: Lista para aplicar o foldr')
    codigoPython.append(f'def foldrFun(arg0,arg1,arg2):')
    codigoPython.append(f'\treturn foldFun(arg0,arg1,copy.deepcopy(arg2))\n')
    codigoPython.append(f'# arg0: Função a aplicar a cada elemento')
    codigoPython.append(f'# arg1: Caso da lista vazia')
    codigoPython.append(f'# arg2: Lista para aplicar o foldl')
    codigoPython.append(f'def foldlFun(arg0,arg1,arg2):')
    codigoPython.append(f'\treturn foldFun(arg0,arg1,reverseFun(arg2))\n')
    return '\n'.join(codigoPython)
