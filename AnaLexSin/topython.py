
from AnaLexSin.AuxFiles.liststructs import ListVar, ListStatic
import re
import numpy as np
exp = re.compile(r'((\+|\-)?\d+(\.\d+)?|True|False)')

# Argumentos (Argumento => string)
def takeout_lists_args(arg):
    if isinstance(arg,ListStatic) or isinstance(arg,ListVar):
        res = (arg.getName(),arg.toPythonArgs(),arg.toPythonIf())
    elif isinstance(arg,list):
        name = ''.join(arg)
        res = (name,'','')
    else:
        res = (arg,'','')
    return res

# Argumentos:
# Converter todos os argumentos em string e buscar pedaços de código em 
# relação ao pattern-matching e associação de variaives, ambos para listas
def get_args_ifs_codigo(implementacao):
    argumentos = implementacao['args']
    if(len(argumentos) == 0):
        args = []
        codigo = []
        ifs = []
    else:
        argsaux = list(map(lambda a: takeout_lists_args(a),argumentos))
        args = list(map(lambda a: a[0],argsaux))
        codigo = list(filter(lambda s: s != '',map(lambda a: a[1],argsaux)))
        ifs = list(filter(lambda s: s != '', map(lambda a: a[2],argsaux)))
    return (args,' and '.join(ifs),'\n'.join(codigo))

# Associação de variaveis + pattern matching
# Associação de variaveis e pattern matching para números e bools 
def trata_argumentos(argumentos,args):
    # criar condição
    condicoes = []
    codigo = []
    index = 0
    for a in args:
        if exp.match(a):
            condicoes.append(f'{argumentos[index]} == {a}')
        index += 1
    # associar variaveis
    aux = {}
    index = 0
    for a in args:
        if not exp.match(a):
            codigo.append(f'\t\t{a} = {argumentos[index]}')
            aux[a] = argumentos[index]
        index += 1
    return (' and '.join(condicoes), '\n'.join(codigo),aux)

# Argumentos: nomes dos argumentos
def geraArgs(argumentos):
    return list(map(lambda num: f'arg{num}',range(0,len(argumentos))))

# Pattern-Matching (pm) 
# juntar pm das listas (get_args_ifs_codigo) + números / bools (trata_argumentos)
def gera_if(implementacoes, ifsargs, ifs,aux):
    strif = ''
    if ifsargs != '':
        strif = ifsargs
    if ifs != '':
        if ifsargs != '':
            strif += ' and '
        strif += ifs
    if strif != '':
        res = f'\tif {strif}:'
    elif(len(implementacoes) > 1):
        res = f'\telse:'
    else:
        res = ''
    for a in aux.keys():
        res = re.sub(f'\({a}\)',f'({aux[a]})',res)
    return res

# Passar o else para última posição
def reorganiza_fun(codigofun):
    elseCorpo = []
    resto = []
    b = False
    haveIfs = re.match(r'(\tif|\telse)',codigofun[1])
    if haveIfs:
        haselse = False
        for s in codigofun:
            if '\telse:' == s:
                haselse = True
                b = True
                elseCorpo.append(s)
            elif b:
                if re.match(r'\tif',s):
                    b = False
                    resto.append(s)
                else:
                    elseCorpo.append(s)
            else:
                resto.append(s)
        if not haselse:
            resto.append('\telse:\n\t\tValueError')
    else:
        for e in codigofun[1:]:
            resto.extend(e.split('\n'))
        resto = list(map(lambda a: re.sub(r'^\t\t','\t',a),resto))
        resto.insert(0,codigofun[0])
    return resto + elseCorpo

# Corpo função: to python de 1 função
def toPythonFun(fun):
    name = fun['nome']
    implementacoes = fun['implementação']
    argumentos = geraArgs(implementacoes[0]['args'])
    aux = ','.join(argumentos)
    codigoFun = [f'def {name}({aux}):']
    for i in implementacoes:
        args, ifs,codigo = get_args_ifs_codigo(i)
        ifsargs, codigoargs, aux = trata_argumentos(argumentos,args)
        se = gera_if(implementacoes,ifsargs,ifs,aux)
        if se !=  '':
            codigoFun.append(se)
        if len(codigoargs) > 0:
            codigoFun.append(codigoargs)
        if len(codigo) > 0:
            codigoFun.append(codigo)
        resultado = str(i['res'])
        codigoFun.append(resultado)
    return reorganiza_fun(codigoFun)

def toPython(parser,namefileres):
    codigoPython = ['import copy']
    codigoPython.extend(parser.importspython)
    codigoPython.append('\n')
    codigoPython.append('#-------------------- Início Código Funcional --------------------')
    codigoPython.append('\n')
    for fun in parser.funcoes:
        codigoFun = toPythonFun(fun)
        codigoPython.append('\n'.join(codigoFun))
        codigoPython.append('')
    codigoPython.append('\n#-------------------- Fim do Código Funcional --------------------\n')
    codigoPython.extend(parser.codigopython)
    res = '\n'.join(codigoPython)
    with open(namefileres,'w') as f:
        f.write(res)