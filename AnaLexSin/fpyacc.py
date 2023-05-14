import ply.yacc as yacc
from AnaLexSin.lexer import lexer
from AnaLexSin.lexer import tokens
from AnaLexSin.AuxFiles.base import Base
from AnaLexSin.AuxFiles.condicoes import Condicoes
from AnaLexSin.AuxFiles.resultado import Resultado
from AnaLexSin.AuxFiles.liststructs import ListVar, ListStatic
from AnaLexSin.AuxFiles.auxfunctions import getNameList, chamadaFuncoes
from AnaLexSin.AuxFiles.funcao import Funcao

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
    p.parser.variaveisfun = []
    p.parser.errosvar = set()
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
    'Corpofun : RETURN CondInside PV'
    # print(f'Funcao {p[1]} {p[2]} {p[3]}')
    p[0] = Resultado(p[1], p[2], p[3])
    return p


def p_Corpofun_IF(p):
    'Corpofun : IF ABREP CondInside FECHAP Corpofun ELSE Corpofun'
    # print(f'Funcao {p[1]} {p[2]} {p[3]} {p[4]} {p[6]}')
    p[0] = Condicoes(p[3], p[5], p[7])
    return p

def p_CondInside_CONDNOT(p):
    'CondInside : NOT CondNOT'
    p[0] = [f'{p[1]} '] + p[2]
    return p

def p_CondInside_CD_AuxCondInside(p):
    'CondInside : CondInside ConjDisj AuxCondInside'
    if isinstance(p[1],str):
        p[1] = [p[1]]
    if isinstance(p[3],str):
        p[3] = [p[3]]
    p[0] =  p[1] + p[2] + p[3]
    return p

def p_CondInside_CD_Result(p):
    'CondInside : CondInside ConjDisj Result'
    if isinstance(p[1],str):
        p[1] = [p[1]]
    if isinstance(p[3],str):
        p[3] = [p[3]]
    p[0] =  p[1] + p[2] + p[3]
    return p

def p_AuxCondInside_NOT(p):
    'AuxCondInside : ABREP NOT CondNOT FECHAP'
    p[0] = [p[1],p[2]] + p[3] + [p[4]]
    return p

def p_CondNOT(p):
    '''
    CondNOT : AuxCondInside
            | Varoper
            | ABREP Result FECHAP
    '''
    if(len(p) > 2):
        p[0] = [p[1]] + p[2] + [p[3]]
    else:
        p[0] = p[1]
    return p

def p_ConjDisj(p):
    '''
    ConjDisj : CONDAND
             | CONDOR
    '''
    p[0] = [f' {p[1]} ']
    return p

def p_AuxCondInside(p):
    '''
    AuxCondInside : ABREP CondInside ConjDisj Result FECHAP
                  | ABREP CondInside ConjDisj AuxCondInside FECHAP
    '''
    if not isinstance(p[2],list):
        p[2] = [p[2]]
    p[0] = [p[1]] + p[2] + p[3] + p[4] + [p[5]]
    return p

def p_CondInside_Result(p):
    '''
    CondInside : Result
               | AuxCondInside
    '''
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


def p_Sinais_OpernVareper(p):
    'Sinais : Opern Varoper'
    if (isinstance(p[2], list)):
        p[2] = transforma(p[2])
        p[0] = [p[1] + ''.join(p[2])]
    else:
        p[0] = p[1] + p[2]
    return p


def p_Sinais_OpernRes(p):
    'Sinais : Opern ABREP Result FECHAP'
    if (isinstance(p[3], list)):
        p[3] = transforma(p[3])
        p[0] = [p[1] + p[2] + ''.join(p[3]) + p[4]]
    else:
        p[0] = p[1] + p[2] + p[3] + p[4]
    return p

def p_Result(p):
    '''
    Result : Varoper
           | Sinais
           | ABREP Result FECHAP
           | Result Oper Varoper
           | Result Oper Sinais
           | Result Oper ABREP Result FECHAP
    '''
    if (len(p) == 6):
        p[0] = p[1] + [p[2]] + [p[3]] + [p[4]] + [p[5]]
    elif (len(p) == 4):
        if (isinstance(p[2], list)):
            p[2] = transforma(p[2])
            p[0] = p[1] + ''.join(p[2]) + p[3]
        elif (p[2].replace(' ','') in ['+', '-', '*', '/', '<', '>', '!=', '>=', '<=', 'in','==','%']):
            p[0] = p[1] + [p[2]] + p[3]
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
    p[0] = f' {p[1]} '
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
    if (not p[1] in p.parser.variaveisfun) and (not p[1] in p.parser.errosvar):
        p.parser.errors.append(f'Variavel {p[1]} na linha {lexer.lineno}, não está definida')
        p.parser.errosvar.add(p[1])
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

def aux_gera_chamada_fun(funcoes,argumentos):
    funabrp = list(map(lambda nomefun: nomefun+'(',funcoes))
    funres = ''.join(funabrp)
    fechap = len(funcoes) * ')'
    return f'{funres}{argumentos}{fechap}'

def p_Chamadafun_NoArgs(p):
    'Chamadafun : ChamadaFunName ABREP FECHAP'
    p[0] = aux_gera_chamada_fun(p[1],'')
    return p

def p_Chamadafun(p):
    'Chamadafun : ChamadaFunName ABREP Conjunto FECHAP'
    p[3] = ''.join(p[3])
    p[0] = aux_gera_chamada_fun(p[1],p[3])
    return p

def funexiste(nome,p):
    nomes = list(map(lambda fun : fun['nome'],p.parser.funcoes))
    if not nome in nomes:
        p.parser.warnings.append(f'Função {nome} não foi definida até à linha {lexer.lineno}')

def p_ChamadaFunName_Single(p):
    'ChamadaFunName : WORD'
    funexiste(chamadaFuncoes(p[1]),p)
    p[0] = [chamadaFuncoes(p[1])]
    return p

def p_ChamadaFunName_Composicao(p):
    'ChamadaFunName : ABREC Composicao FECHAC'
    p[0] = p[2]
    return p

def p_Composicao_Single(p):
    'Composicao : WORD'
    funexiste(chamadaFuncoes(p[1]),p)
    p[0] = [chamadaFuncoes(p[1])]
    return p

def p_Composicao(p):
    'Composicao : Composicao WORD'
    funexiste(chamadaFuncoes(p[2]),p)
    p[0] =  p[1] + [chamadaFuncoes(p[2])]
    return p

def p_VarArgs_BOOL(p):
    'VarArgs : BOOL'
    p[0] = p[1].capitalize()
    return p

def p_VarArgs_WORD(p):
    'VarArgs : WORD'
    p.parser.variaveisfun.append(p[1])
    p[0] = p[1]
    return p

def p_VarArgs(p):
    '''
    VarArgs : NUMBER
            | Opern NUMBER
            | ListArg
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

def p_error(p):
    if p:
        p.lexer.errors.append(f'O token "{p.value}" de tipo "{p.type}", na linha {p.lineno} não respeita a sintaxe da linguagem')
    tok = parser.token()
    parser.errok()
    return tok

parser = yacc.yacc(debug=True,errorlog=yacc.NullLogger())
parser.nomeslistas = 0
parser.funcoes = []
parser.codigopython = []
parser.importspython = []
parser.warnings = []
parser.variaveisfun = []
parser.errosvar = set()
parser.errors = []