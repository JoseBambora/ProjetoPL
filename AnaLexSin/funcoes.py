def getReservadas():
    reservadas = set()
    reservadas.add('map')
    reservadas.add('filter')
    return reservadas

def mapAux(arg0,arg1):
    return list(map(arg0,arg1))

def filterAux(arg0,arg1):
    return list(filter(arg0,arg1))

def getName(name):
    return name + 'Aux'

def getFun(name):
    codigoPython = []
    codigoPython.append(f'def {name}Aux(arg0,arg1):')
    codigoPython.append(f'\treturn list({name}(arg0,arg1))\n')
    return '\n'.join(codigoPython)
        