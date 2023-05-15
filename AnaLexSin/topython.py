
from AnaLexSin.AuxFiles.liststructs import ListVar, ListStatic
import re
import numpy as np
from AnaLexSin.AuxFiles.auxfunctions import getImut
from AnaLexSin.funcoes import getFun
exp = re.compile(r'((\+|\-)?\d+(\.\d+)?|True|False)')

# Argumentos: nomes dos argumentos
def geraArgs(argumentos):
    return list(map(lambda num: f'arg{num}',range(0,len(argumentos))))

# Passar o else para última posição
# tirar 1 tab se a função não tiver pattern-matching
def reorganiza_fun(codigofun):
    elseCorpo = []
    resto = []
    insideelse = False
    haveIfs = re.match(r'(\tif|\telse)',codigofun[1])
    if haveIfs:
        haselse = False
        for s in codigofun:
            if '\telse:' == s:
                haselse = True
                insideelse = True
                elseCorpo.append(s)
            elif insideelse:
                if re.match(r'\t(if|elif)',s):
                    insideelse = False
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


def pattern_matching_elem(arg,word):
    if isinstance(arg,ListStatic) or isinstance(arg,ListVar):
        arg.setName(word)
        res = arg.toPythonIf()
    else:
        if isinstance(arg,list):
            arg = ''.join(arg)
        if exp.match(arg):
            res = f'{word} == {arg}'
        else:
            res = ''
    return res

def associacao_vars_elem(arg,word):
    if isinstance(arg,ListStatic) or isinstance(arg,ListVar):
        arg.setName(word)
        res = arg.toPythonArgs()
    else:
        if isinstance(arg,list):
            arg = ''.join(arg)
        if not exp.match(arg) and arg != '_':
            aux = getImut(word)
            res = f'\t\t{arg} = {aux}'
        else:
            res = ''
    return res

def aux_pm_av(argumentos,args,funcao):
    res = []
    for index in range(0,len(args)):
        resaux = funcao(args[index],argumentos[index])
        if len(resaux) > 0:
            res.append(resaux)
    return res

def pattern_matching(argumentos,args,fst):
    condicoes = aux_pm_av(argumentos,args,pattern_matching_elem)
    strfinal = ''
    if(len(condicoes) > 0):
        strfinal = ' and '.join(condicoes)
        ifstr = 'elif'
        if fst:
            ifstr = 'if'
        strfinal = f'\t{ifstr} {strfinal}:'
    return strfinal

def associacao_vars(argumentos,args):
    associacao = aux_pm_av(argumentos,args,associacao_vars_elem)
    strfinal = ''
    if(len(associacao) > 0):
        strfinal = '\n'.join(associacao)
    return strfinal

def gera_codigo(resultado):
    return str(resultado)

# Corpo função: to python de 1 função
def toPythonFun(fun):
    name = fun['nome']
    implementacoes = fun['implementação']
    argumentos = geraArgs(implementacoes[0]['args'])
    aux = ','.join(argumentos)
    codigoFun = [f'def {name}({aux}):']
    fst = True
    for i in implementacoes:
        pm = pattern_matching(argumentos,i['args'],fst)
        av = associacao_vars(argumentos,i['args'])
        gc = gera_codigo(i['res'])
        if len(pm) > 0:
            codigoFun.append(pm)
            fst = False
        elif len(implementacoes) > 1:
            codigoFun.append('\telse:')
        if len(av) > 0:
            codigoFun.append(av)
        codigoFun.append(gc)
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
    codigoPython.append('\n#--------------------- Funções pré definidas ---------------------\n')
    codigoPython.append(getFun('map'))
    codigoPython.append(getFun('filter'))
    codigoPython.append('\n#-------------------- Fim do Código Funcional --------------------\n')
    codigoPython.extend(parser.codigopython)
    res = '\n'.join(codigoPython)
    with open(namefileres,'w') as f:
        f.write(res)