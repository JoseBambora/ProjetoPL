import ply.yacc as yacc
import re
from AnaLexSin.lexer import lexer
from AnaLexSin.lexer import tokens
from AnaLexSin.AuxFiles.base import Base
from AnaLexSin.AuxFiles.condicoes import Condicoes
from AnaLexSin.AuxFiles.resultado import Resultado
from AnaLexSin.AuxFiles.liststructs import ListVar, ListStatic
from AnaLexSin.AuxFiles.auxfunctions import getImut, getNameList, chamadaFuncoes
from AnaLexSin.AuxFiles.funcao import Funcao
from AnaLexSin.topython import toPython

def transforma(lista):
    index = 0
    for e in lista:
        if isinstance(e, ListVar) or isinstance(e, ListStatic):
            lista[index] = e.toPythonRes()
        elif isinstance(e, list):
            e = transforma(e)
            lista[index] = ''.join(e)
        index += 1
    return lista

def p_Codigo(p):
    '''Codigo : Codigo Python
              | Codigo CodigoFun
              | Python
              | CodigoFun'''
    return p

def p_CodigoFun(p):
    'CodigoFun : ABREFP Fpython FECHAFP'
    return p

def p_Python(p):
    '''
    Python : REST
    '''
    if(p[1].__contains__('import')):
        p.parser.importspython.append(p[1])
    else:
        p.parser.codigopython.append(p[1])
    return p

def p_Fpython(p):
    '''
    Fpython : Fpython Funcao
            | Funcao
    '''
    return p

def trata_funcao(p):
    p.parser.nomeslistas = 0
    nome = chamadaFuncoes(p[2])
    b = False
    index = 0
    lista = p.parser.funcoes

    if len(p) == 8:
        fun = Funcao(nome, p[4], p[6]).nova_funcao()
    else:
        fun = Funcao(nome, [], p[5]).nova_funcao()

    for i in lista:
        if nome in i.values():
            b = True
            break
        index += 1
    if b:
        nova_implementacao = fun["implementação"]
        lista[index]["implementação"].extend(nova_implementacao)
        # adicionar dentro do dicionário da funcao: nova implementação
    else:
        lista.append(fun)
        # Adicionar novo dicionário à lista com a nova função

    # print('!!!!!!!!!!!!!!!!!!')
    # print(lista)
    # print('!!!!!!!!!!!!!!!!!!')

    return p


def p_Funcao_Args(p):
    'Funcao : FUNABRE WORD ABREP Args FECHAP Corpofun FUNFECHA'
    # print(f'def {p[2]}({Base(p[4]).toPythonBase()}):')
    # print(f'Meter ifs para pattern matching')
    # print(f'Invocar função toPythonArgs das listas caso temos listas')
    # print(f'Função resultado:\n{p[6].toPython()}')
    trata_funcao(p)
    return p


def p_Funcao(p):
    'Funcao : FUNABRE WORD ABREP FECHAP Corpofun FUNFECHA'
    # print(f'def {p[2]}():')
    # print(f'Meter ifs para pattern matching')
    # print(f'Invocar função toPythonArgs das listas caso temos listas')
    # print(f'Função resultado:\n{p[5].toPython()}')
    trata_funcao(p)
    return p


def p_Args_Var(p):
    'Args : VarArgs'
    p[0] = [p[1]]
    return p


def p_Args(p):
    'Args : Args VIR VarArgs'
    p[0] = p[1]
    p[0] += [p[3]]
    return p


def p_Conjunto(p):
    'Conjunto : Conjunto VIR Result'
    if (isinstance(p[3], list)):
        p[3] = transforma(p[3])
        p[3] = ''.join(p[3])
    p[0] = p[1] + [p[2], p[3]]
    if len(p) == 5:
        p[0] += p[4]
    return p


def p_Conjunto_Result(p):
    'Conjunto : Result'
    if isinstance(p[1], list):
        p[1] = transforma(p[1])
        p[1] = ''.join(p[1])
    p[0] = [p[1]]
    return p


def p_Corpofun_RETURN(p):
    'Corpofun : RETURN Result PV'
    # print(f'Funcao {p[1]} {p[2]} {p[3]}')
    p[0] = Resultado(p[1], p[2], p[3])
    return p


def p_Corpofun_IF(p):
    'Corpofun : IF ABREP Cond FECHAP Corpofun ELSE Corpofun'
    # print(f'Funcao {p[1]} {p[2]} {p[3]} {p[4]} {p[6]}')
    p[0] = Condicoes(p[3], p[5], p[7])
    return p


def p_Cond_CondSimple(p):
    'Cond : CondSimple'
    p[0] = p[1]
    return p


def p_Cond_CONDAND(p):
    'Cond : Cond CONDAND CondSimple'
    p[0] = p[1] + ['and'] + p[3]
    return p


def p_Cond_CONDOR(p):
    'Cond : Cond CONDOR CondSimple'
    p[0] = p[1] + ['or'] + p[3]
    return p


def p_Cond_NOT(p):
    'Cond : NOT CondSimple'
    p[2].insert(0, p[1])
    p[0] = p[2]
    return p


def p_CondSimple_ABREP(p):
    'CondSimple : ABREP Cond FECHAP'
    p[2].insert(0, p[1])
    p[2].append(p[3])
    p[0] = p[2]
    return p


def p_CondSimple(p):
    '''
    CondSimple : ABREP Cond FECHAP Conds Varoper
               | Varoper Conds ABREP Cond FECHAP
               | ABREP Cond FECHAP Conds ABREP Cond FECHAP
               | Varoper Conds Varoper
               | Varoper
    '''
    if (len(p) > 2):
        p[0] = p[1] + [p[2]] + p[3]
    else:
        p[0] = p[1]
    return p


def p_Conds(p):
    '''
    Conds : MENOR
          | MAIOR
          | IGUAL
          | DIFERENTE
          | MAIORIGUAL
          | MENORIGUAL
          | IN
    '''
    p[0] = p[1]
    return p


def p_Result_OpernVareper(p):
    'Result : Opern Varoper'
    if (isinstance(p[2], list)):
        p[2] = transforma(p[2])
        p[0] = [p[1] + ''.join(p[2])]
    else:
        p[0] = p[1] + p[2]
    return p


def p_Result_OpernRes(p):
    'Result : Opern ABREP Result FECHAP'
    if (isinstance(p[3], list)):
        p[3] = transforma(p[3])
        p[0] = [p[1] + p[2] + ''.join(p[3]) + p[4]]
    else:
        p[0] = p[1] + p[2] + p[3] + p[4]
    return p

def p_Result(p):
    '''
    Result : Varoper
           | Result Oper Varoper
           | ABREP Result FECHAP
           | Result Oper ABREP Result FECHAP
    '''
    if (len(p) == 6):
        p[0] = p[1] + [p[2]] + [p[3]] + [p[4]] + [p[5]]
    elif (len(p) == 4):
        if (p[2] in ['+', '-', '*', '/', '$', 'and', 'or', '<', '>', '=', '!=', '>=', '<=', 'in']):
            p[0] = p[1] + [p[2]] + p[3]
        elif (isinstance(p[2], list)):
            p[2] = transforma(p[2])
            p[0] = p[1] + ''.join(p[2]) + p[3]
        else:
            p[0] = p[1] + p[2] + p[3]
    elif (len(p) == 3):
        if (isinstance(p[2], list)):
            p[2] = transforma(p[2])
            p[0] = [p[1] + ''.join(p[2])]
        else:
            p[0] = p[1] + p[2]
    else:
        p[0] = p[1]
    return p


def p_Opern(p):
    '''
    Opern : ADD
          | MINUS
    '''
    p[0] = p[1]
    return p


def p_Oper(p):
    '''
    Oper : Opern
         | TIMES
         | DIVIDE
         | MOD
         | OR
         | AND
         | Conds
    '''
    p[0] = p[1]
    return p


def p_Varoper(p):
    '''
    Varoper : Chamadafun
            | Var
    '''
    if p[1] != None:
        p[0] = p[1]
    if not isinstance(p[0], list):
        p[0] = [p[0]]
    return p


def p_Var_NUMBER(p):
    'Var : NUMBER'
    p[0] = p[1]
    return p


def p_Var_BOOL(p):
    'Var : BOOL'
    p[0] = p[1].capitalize()
    return p

def p_Var_List(p):
    'Var : List'
    p[0] = p[1]
    return p

def p_VAR_WORD(p):
    'Var : WORD'
    p[0] = p[1]
    return p

def criaListaStatic(p,l):
    name = getNameList(p.parser.nomeslistas)
    lista = ListStatic(l, name)
    p[0] = lista
    p.parser.nomeslistas += 1
    return p

def p_List_Vazia(p):
    'List : ABREL FECHAL'
    return criaListaStatic(p,[])

def p_List_Estatica(p):
    'List : ABREL Conjunto FECHAL'
    return criaListaStatic(p,p[2])


def p_List(p):
    'List : ABREL Result NEXT Conjunto2 FECHAL'
    name = getNameList(p.parser.nomeslistas)
    lista = ListVar(p[2], p[4], name)
    p[0] = lista
    p.parser.nomeslistas += 1
    return p


def p_Conjunto2_Word(p):
    'Conjunto2 : Result'
    p[0] = [p[1]]
    return p


def p_Conjunto2(p):
    'Conjunto2 : Conjunto2 NEXT Result'
    p[0] = p[1] + [p[2], p[3]]
    return p


def p_Chamadafun_NoArgs(p):
    'Chamadafun : WORD ABREP FECHAP'
    p[0] = [chamadaFuncoes(p[1]), p[2], p[3]]
    return p


def p_Chamadafun(p):
    'Chamadafun : WORD ABREP Conjunto FECHAP'
    for e in range(0, len(p[3]), 2):
        p[3][e] = getImut(p[3][e])
    p[0] = [chamadaFuncoes(p[1]), p[2]] + p[3] + [p[4]]
    return p


def p_error(p):
    print('Erro ' + str(p))
    return p


def p_VarArgs_BOOL(p):
    'VarArgs : BOOL'
    p[0] = p[1].capitalize()
    return p


def p_VarArgs(p):
    '''
    VarArgs : NUMBER
            | Opern NUMBER
            | ListArg
            | WORD
    '''
    if (len(p) == 2):
        p[0] = p[1]
    else:
        p[0] = [p[1], p[2]]
    return p


def p_ListArg(p):
    '''
    ListArg : ABREL FECHAL
            | ABREL ConjuntoListaArgs FECHAL
            | ABREL VarArgs NEXT Conjunto2ListaArgs FECHAL
    '''
    name = getNameList(p.parser.nomeslistas)
    if len(p) == 3:
        lista = ListStatic([], name)
    elif len(p) == 4:
        lista = ListStatic(p[2], name)
    else:
        lista = ListVar(p[2], p[4], name)
    p[0] = lista
    p.parser.nomeslistas += 1
    return p


def p_ConjuntoListaArgs_Single(p):
    'ConjuntoListaArgs : VarArgs'
    p[0] = [p[1]]
    return p


def p_ConjuntoListaArgs(p):
    'ConjuntoListaArgs : ConjuntoListaArgs VIR VarArgs'
    p[0] = p[1] + [p[3]]
    return p


def p_Conjunto2ListaArgs_Single(p):
    'Conjunto2ListaArgs : VarArgs'
    p[0] = [p[1]]
    return p


def p_Conjunto2ListaArgs(p):
    'Conjunto2ListaArgs : Conjunto2ListaArgs NEXT VarArgs'
    p[0] = p[1] + [p[3]]
    return p

parser = yacc.yacc()
parser.nomeslistas = 0
parser.funcoes = []
parser.codigopython = []
parser.importspython = []
# toPython(parser)
# codigopython
# importspython
# mudar estrutura (relativamente ao argumentos)