import re
from AnaLexSin.AuxFiles.liststructs import ListStatic, ListVar
from AnaLexSin.AuxFiles.resultado import Resultado
expNum = re.compile(r'(\+|\-)?\d+(\.\d+)?')
expBool = re.compile(r'(True|False)')

def nrArgs(fun):
    res = ''
    name = fun['nome']
    implementacoes = fun['implementação']
    nrArgs = len(implementacoes[0]['args'])
    impl = 1
    implerr = []
    for i in implementacoes:
        if len(i['args']) != nrArgs:
            implerr.append(impl)
        impl += 1
    if len(implerr) > 0:
        res = f'''Função {name} contém implementações cujos número de argumentos são diferentes.
        Implementações com número de argumentos diferentes em relação à primeira implementação:
        {implerr}
        '''
    return [res]

def argsTypeAux(elem,type,name):
    if elem != 'VAR' and elem != type:
        return f'Função {name} contém implementações cujos argumentos são de diferentes tipos. Deve receber {elem} e recebe {type}'
    else:
        return ''

def argsType(fun):
    errors = []
    name = fun['nome']
    implementacoes = fun['implementação']
    nrArgs = len(implementacoes[0]['args'])
    type = ['VAR'] * nrArgs
    for i in implementacoes:
        args = i['args']
        index = 0
        for argumento in args:
            elem = type[index]
            if isinstance(argumento,ListStatic) or isinstance(argumento,ListVar):
                aux = argsTypeAux(elem,'LIST',name)
                if len(aux) > 0:
                    errors.append(aux)
                else:
                    type[index] = 'LIST'
            else:
                if isinstance(argumento,list):
                    argumento = str(argumento)
                if expNum.match(argumento):
                    aux = argsTypeAux(elem,'NUM',name)
                    if len(aux) > 0:
                        errors.append(aux)
                    else:
                        type[index] = 'NUM'
                elif expBool.match(argumento):
                    aux = argsTypeAux(elem,'BOOL',name)
                    if len(aux) > 0:
                        errors.append(aux)
                    else:
                        type[index] = 'BOOL'
            index += 1
    return errors

def analyseFun(fun):
    nrargs = nrArgs(fun)
    typeargs = []
    if len(nrargs[0]) == 0:
        typeargs = argsType(fun)
    return (nrargs,typeargs)

def analyse(parser):
    errors = []
    for fun in parser.funcoes:
        e1,e2 = analyseFun(fun)
        if len(e1[0]) > 0:
            errors.extend(e1)
        errors.extend(e2)
    return errors