
from liststructs import ListVar, ListStatic
import re
exp = re.compile(r'((\+|\-)?\d+(\.\d+)?|True|False)')

def takeout_lists_args(arg):
    if isinstance(arg,ListStatic) or isinstance(arg,ListVar):
        res = (arg.getName(),arg.toPythonArgs(),arg.toPythonIf())
    elif isinstance(arg,list):
        res = (''.join(arg),'','')
    else:
        res = (arg,'','')
    return res

def get_args_ifs_codigo(implementacao):
    argumentos = implementacao['args']
    if(len(argumentos) == 0):
        argsaux = [('','','')]
    else:
        argsaux = list(map(lambda a: takeout_lists_args(a),argumentos))
    args = list(map(lambda a: a[0],argsaux))
    codigo = list(map(lambda a: a[1],argsaux))[0]
    ifs = list(map(lambda a: a[2],argsaux))[0]
    return (args,ifs,codigo)

def trata_argumentos(argumentos,args):
    if(len(argumentos) == 0):
        argumentos = args
    else:
        i = 0
        for var in args:
            if not exp.match(var):
                argumentos[i] = var
            i+=1
    return argumentos
            
def toPythonFun(fun):
    name = fun['nome']
    implementacoes = fun['implementação']
    codigoFun = []
    codigoFun.append(f'def {name}')
    pos = len(codigoFun)-1
    argumentos = []
    for i in implementacoes:
        resultado = str(i['res'])
        args, ifs,codigo = get_args_ifs_codigo(i)
        argumentos = trata_argumentos(argumentos,args)
        codigoFun.append(f'\tif {ifs}:')
        if(len(codigo) > 0):
            codigoFun.append(codigo)
        codigoFun.append(resultado)
    argumentosfinal = ','.join(argumentos)
    codigoFun[pos] += f'({argumentosfinal}):'
    return codigoFun

def toPython(parser):
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
    with open('Result.py','w') as f:
        f.write(res)
    print('====================')
    print('Escreveu ficheiro')