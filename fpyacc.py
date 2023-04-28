import ply.yacc as yacc
from lexer import lexer
from lexer import tokens
from base import Base
from condicoes import Condicoes
from resultado import Resultado
from liststructs import ListVar,ListStatic
from imutable import getImut,getNameList
import re

exp = re.compile(r'((\+|\-)?\d+(\.\d+)?|True|False)')

def transforma(lista):
    index = 0
    for e in lista:
        if isinstance(e,ListVar) or isinstance(e,ListStatic):
            lista[index] = e.toPythonRes()
        elif isinstance(e,list):
            lista[index] = ''.join(e)
        index +=1
    return lista

# Python produção de código
# produção nova sinais (muito simular a varoper)
# argumentos (+|-) NUMBER

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
    # if p[1] != None:
    #     print(f'Código Python {p[1]}')
    # else:
    #     print(f'Código Python {p[2]}')
    return p


# deff uminho([h:t:t2:t3]):
#       return 0;
# end

# def uminho(l):
#   h = l[0]
#   t = l[1]
#   t2 = l[2]
#   t3 = l[3:]
#   return 0
#

# h:t
# cabeca = lista[0]
# cauda = lista[1:]
# h:h2:t
# cabeca = lista[0]
# cabeca2 = lista[1]
# cauda = lista[2:]
def p_Fpython(p):
    '''
    Fpython : Fpython Funcao
            | Funcao
    '''
    # funcao = p[2]
    # p.yacc.funcoes = []
    # b = False
    # i = 0
    # for f in p.yacc.funcoes:
    #     if f['nome'] == funcao['nome']:
    #         b = True
    #         break
    #     i+=1
    # if not b:
    #     p.yacc.funcoes.append(funcao)
    # else:
    #     dec = p.yacc.funcoes[i]
    print('=============================')
    return p


def trata_funcao(p):
    # p.parser.listasnomes = {}
    p.parser.nomeslistas = 0


def p_Funcao_Args(p):
    'Funcao : FUNABRE WORD ABREP Args FECHAP Corpofun FUNFECHA'
    print(f'def {p[2]}({Base(p[4]).toPythonBase()}):')
    print(f'Meter ifs para pattern matching')
    print(f'Invocar função toPythonArgs das listas caso temos listas')
    print(f'Função resultado:\n{p[6].toPython()}')  # meter toPython
    trata_funcao(p)
    return p


def p_Funcao(p):
    'Funcao : FUNABRE WORD ABREP FECHAP Corpofun FUNFECHA'
    print(f'def {p[2]}():')
    print(f'Meter ifs para pattern matching')
    print(f'Invocar função toPythonArgs das listas caso temos listas')
    print(f'Função resultado:\n{p[5].toPython()}')  # meter toPython
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
    p[0] = p[1] + [p[2],p[3]]
    if len(p) == 5:
        p[0] += p[4]
    return p


def p_Conjunto_Result(p):
    'Conjunto : Result'
    if isinstance(p[1],list):
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
    # print(f'Condicao operador {p[1]}')
    p[0] = p[1]
    return p


def p_Result(p):
    '''
    Result : Varoper
           | Opern Sinais
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
            p[0] = p[1] + str(p[2]) + p[3]
        else:
            p[0] = p[1] + p[2] + p[3]
    elif (len(p) == 3):
        if (isinstance(p[2], list)):
            p[0] = [p[1]+''.join(p[2])]
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
    # print(p[1])
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
    # print(f'Operacao {p[1]}')
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
    # print(f'Número {p[1]}')
    p[0] = p[1]
    return p


def p_Var_BOOL(p):
    'Var : BOOL'
    # print(f'Booleano: {p[1]}')
    p[0] = p[1].capitalize()
    return p


def p_Var_List(p):
    'Var : List'
    # print(f'Lista')
    p[0] = p[1]
    return p


def p_VAR_WORD(p):
    'Var : WORD'
    # print(f'Variável: {p[1]}')
    p[0] = p[1]
    return p


def p_List_Vazia(p):
    'List : ABREL FECHAL'
    name = getNameList(p.parser.nomeslistas)
    lista = ListStatic([], name)
    p[0] = lista
    p.parser.nomeslistas +=1
    # p.parser.listasnomes[name] = lista
    return p


def p_List_Estatica(p):
    'List : ABREL Conjunto FECHAL'
    name = getNameList(p.parser.nomeslistas)
    lista = ListStatic(p[2], name)
    p[0] = lista
    p.parser.nomeslistas +=1
    # p.parser.listasnomes[name] = lista
    return p


def p_List(p):
    'List : ABREL Result NEXT Conjunto2 FECHAL'
    name = getNameList(p.parser.nomeslistas)
    lista = ListVar(p[2], p[4], name)
    p[0] = lista
    p.parser.nomeslistas +=1
    # p.parser.listasnomes[name] = lista
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
    p[0] = [p[1], p[2], p[3]]
    return p


def p_Chamadafun(p):
    'Chamadafun : WORD ABREP Conjunto FECHAP'
    print(p[3])
    for e in range(0, len(p[3]), 2):
        p[3][e] = getImut(p[3][e])
    p[0] = [p[1], p[2]] + p[3] + [p[4]]
    return p


def p_error(p):
    print('Erro ' + str(p))
    return p


def p_Sinais(p):
    '''
    Sinais : Chamadafun
           | WORD
           | NUMBER
    '''
    if p[1] != None:
        p[0] = p[1]
    if not isinstance(p[0], list):
        p[0] = [p[0]]
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
    if(len(p) == 2):
        p[0] = p[1]
    else:
        p[0] = [p[1],p[2]]
    return p

def p_ListArg(p):
    '''
    ListArg : ABREL FECHAL
            | ABREL ConjuntoListaArgs FECHAL
            | ABREL VarArgs NEXT Conjunto2ListaArgs FECHAL
    '''
    name = getNameList(p.parser.nomeslistas)
    if len(p) == 3:
        lista = ListStatic([],name)
    elif len(p) == 4:
        lista = ListStatic(p[2],name)
    else:
        lista = ListVar(p[2], p[4], name)
    p[0] = lista
    p.parser.nomeslistas += 1
    # p.parser.listasnomes[name] = lista
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

inp2 = '''
"""FPYTHON 

deff con2(h,k)
    return seila(t) + seila(t2) + seila(t3);
end

deff con2([h:t:t2:t3:t4],n)
    if (n == h)
        if (not (con2(t,n) and con2(t,n)))
            if(true)
                return [h:t:t2:t3:con2(t4,4)];
            else
                return [h,t,t2];
        else
            return false;
    else 
        if (con2(t,n))
            if(true)
                return true;
            else
                return false;
        else
            return false;
end
"""
'''

inp = '''
print('Boas')
"""FPYTHON
deff mais_um(x)
    return x + 1;
end

deff sum([])
    return 0;
end

deff div(n,0)
    return 0;
end

deff div(0,n)
    return 0;
end

deff div(n,-1)
    return n*(-1);
end

deff sum([h : t])
    return h + sum(t);
end

deff cond(x)
    if (x < 1)
        return 2;
    else
        return 3;
end

deff con2([],_)
    return false;
end

deff con2([h:t],n)
    if (n == h)
        if (not (con2(t,n) and con2(t,n)))
            if(true)
                return true;
            else
                return false;
        else
            return false;
    else 
        if (con2(t,n))
            if(true)
                return true;
            else
                return false;
        else
            return false;
end

deff seila([1,2],0,true)
    return 4;
end

deff seila([],num,true)
    return num+1;
end

deff seila([],num,false)
    return num;
end

deff seila([h:t],num,true)
    return h + seila(t) + num + 1;
end

deff seila([h:t],num,false)
    return h + seila3(seila(t)) + num;
end

deff seila3(d)
    return seila4(5+(3*d)); 
end
"""

x = 4
y = f_mais_um_(x)
print(y)
l = [1,2,3,4,5]
sum_l = f_sum_(l)
print(sum_l)

"""FPYTHON

deff uminho()
    return 1+2;
end

deff uminho(n,t)
    return [n:t];
end
"""

print(f_uminho_())
'''

inp3 = '''
"""FPYTHON

deff con2([1,2,3,4,false],k)
    return 0;
end

deff con2([[2:t]:t2],k)
   return 0;
end


deff con3([[h1:2:h2:3:t]:t2],k)
    if ((k in t) and (k in t2))
        if (k != seila(2,3,4))
            return con2([[2:3:t]:t2],k,3);
        else
            return False;
    else 
        return seila(1,3*1*(-40)+43,2,kkk(1,2,3));
end

"""
'''
# deff con2([[h:t]:t2],k)
#    return 0;
# end
parser = yacc.yacc(debug=True)
# parser.listasnomes = {}
parser.nomeslistas = 0
parser.parse(inp3)
