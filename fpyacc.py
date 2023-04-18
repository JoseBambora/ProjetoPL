import ply.yacc as yacc
from lexer import lexer
from lexer import tokens
from condicoes import Condicoes
from resultado import Resultado

def p_Codigo(p):
    '''Codigo : Codigo CodigoFun Python
              | Codigo CodigoFun
              | Python CodigoFun Python
              | Python CodigoFun
              | CodigoFun Python
              | CodigoFun'''
    return p

def p_CodigoFun(p):
    'CodigoFun : ABREFP Fpython FECHAFP'
    return p

def p_Python(p):
    '''
    Python : Python REST 
           | REST
    '''
    if p[1] != None:
        print(f'Código Python {p[1]}')
    else:
        print(f'Código Python {p[2]}')
    return p

def p_Fpython(p):
    '''
    Fpython : Fpython Funcao
            | Funcao
    '''
    print('=============================')
    return p

def p_Funcao(p):
    '''
    Funcao : FUNABRE WORD ABREP Args FECHAP Corpofun FUNFECHA
           | FUNABRE WORD ABREP FECHAP Corpofun FUNFECHA'''
    print(f'Funçao nome: {p[2]}')
    if p[6] == ']':
        print(f'Função resultado:\n{p[5]}') #meter toPython
    else:
        print(f'Função resultado:\n{p[6]}') #meter toPython
    return p

def p_Args(p):
    '''
    Args : Var
         | Opern Var
         | Args VIR Var
         | Args VIR Opern Var
    '''
    return p

def p_Conjunto(p):
    '''
    Conjunto : Conjunto VIR Var
             | Conjunto VIR Opern Var
             | Result
    '''
    return p

def p_Corpofun_RETURN(p):
    'Corpofun : RETURN Result PV'
    #print(f'Funcao {p[1]} {p[2]} {p[3]}')
    p[0] = Resultado(p[1],p[2],p[3]).pp()
    return p


def p_Corpofun_IF(p):
    'Corpofun : IF ABREP Cond FECHAP Corpofun ELSE Corpofun'
    # print(f'Funcao {p[1]} {p[2]} {p[3]} {p[4]} {p[6]}')
    p[0] = Condicoes(p[3],p[5],p[7])
    return p


def p_Cond(p):
    '''
    Cond : Varoper Conds Varoper
         | Varoper
    '''
    if (len(p) > 2):
        p[0] = p[1] + [p[2]] + p[3]
    else:
        p[0] = p[1]
    return p

def p_Cond_CONDAND(p):
    'Cond : Cond CONDAND Cond'
    p[0] = p[1] + ['and'] + p[3]
    return p


def p_Cond_CONDOR(p):
    'Cond : Cond CONDOR Cond'
    p[0] = p[1] + ['or'] + p[2]
    return p

def p_Cond_NOT(p):
    'Cond : NOT Cond'
    p[2].insert(0,p[1])
    p[0] = p[2]
    return p

def p_Cond_ABREP(p):
    'Cond : ABREP Cond FECHAP'
    p[2].insert(0,p[1])
    p[2].append(p[3])
    p[0] = p[2]
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
# n*(-1)
def p_Result(p):
    '''
    Result : Varoper
           | Opern Varoper
           | Result Oper Result
           | ABREP Result FECHAP
    '''
    if (len(p) == 4):
        if (p[2] in ['+','-','*','/','$','and','or','<','>','=','!=','>=','<=','in']):
            p[0] = p[1] + [p[2]] + [p[3]]
        elif(isinstance(p[2],list)):
                p[0] = p[1] + str(p[2]) +p[3]
        else:
            p[0] = p[1] + p[2] + p[3]
    elif (len(p) == 3):
            if(isinstance(p[2],list)):
                p[0] = p[1] + str(p[2])
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
    print(p[1])
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
    if p[1] != None:
        print(f'Operacao {p[1]}')
    p[0]=p[1]
    return p

def p_Varoper(p):
    '''
    Varoper : Chamadafun
            | Var
    '''
    if p[1] != None:
        p[0] = p[1]
    if not isinstance(p[0],list):
        p[0] = [p[0]]
    return p

def p_Var_NUMBER(p):
    'Var : NUMBER'
    print(f'Número {p[1]}')
    p[0] = p[1]
    return p

def p_Var_BOOL(p):
    'Var : BOOL'
    print(f'Booleano: {p[1]}')
    p[0] = p[1]
    return p

def p_Var_List(p):
    'Var : List'
    print(f'Lista')
    p[0] = p[1]
    return p

def p_VAR_WORD(p):
    'Var : WORD'
    print(f'Variável: {p[1]}')
    p[0] = p[1]
    return p


def p_List(p):
    '''
    List : ABREL FECHAL
         | ABREL WORD NEXT Conjunto2 FECHAL
         | ABREL Conjunto FECHAL
    '''
    return p

def p_Conjunto2(p):
    '''
    Conjunto2 : Conjunto2 NEXT WORD
              | WORD
    '''
    return p

def p_Chamadafun(p):
    '''
    Chamadafun : WORD ABREP Conjunto FECHAP
               | WORD ABREP FECHAP
    '''
    p[0] = [p[1]] + [p[2]] + [')']
    return p

def p_error(p):
    print('Erro ' + str(p))
    return p

inp2 = '''
"""FPYTHON 

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
end"""
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
"""

print(f_uminho_())
'''

parser = yacc.yacc()
parser.parse(inp2)