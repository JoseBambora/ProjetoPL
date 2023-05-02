from ply.lex import lex

# Falar dos tokens: # : ; then
# Falar de word não começar com números
# Exemplos

tokens = (
    'ADD',  # +
    'MINUS',  # -
    'TIMES',  # *
    'DIVIDE',  # /
    'MOD',  # %
    'OR',  # |
    'AND',  # &
    'NUMBER',  # INT FLOAT
    'BOOL',  # true false
    'FUNABRE',  # deff
    'FUNFECHA',  # end
    'ABREP',  # (
    'FECHAP',  # )
    'VIR',  # , -> argumentos
    'WORD',  # palavra
    'IF',  # if
    'ELSE',  # else
    'ABREFP',  # """FPYTHON
    'FECHAFP',  # """
    'MENOR',  # <
    'MAIOR',  # >
    'IGUAL',  # ==
    'DIFERENTE',  # !=
    'MAIORIGUAL',  # >=
    'MENORIGUAL',  # <=
    'IN',  # in
    'NOT',  # not
    'CONDAND',  # and
    'CONDOR',  # or
    'RETURN',  # return
    'ABREL',  # [
    'FECHAL',  # ]
    'NEXT',  # :
    'PV',  # ;
    'REST'
)

states = (('FPYTHON', 'inclusive'),)

t_FPYTHON_ignore = ' \t\n'
t_ignore = '\n'

def t_FPYTHON_VIR(t):
    r','
    # print(',',end=' ')
    return t


def t_FPYTHON_ADD(t):
    r'\+'
    # print(t.value,end=' ')
    return t


def t_FPYTHON_MINUS(t):
    r'\-'
    # print(t.value,end=' ')
    return t


def t_FPYTHON_OR(t):
    r'\|'
    # print(t.value,end=' ')
    return t


def t_FPYTHON_AND(t):
    r'&'
    # print(t.value,end=' ')
    return t


def t_FPYTHON_DIVIDE(t):
    r'\/'
    # print(t.value,end=' ')
    return t


def t_FPYTHON_TIMES(t):
    r'\*'
    # print(t.value,end=' ')
    return t


def t_FPYTHON_MOD(t):
    r'%'
    # print(t.value,end=' ')
    return t


def t_INITIAL_ABREFP(t):
    r'"""(?i:FPYTHON)'
    t.lexer.begin('FPYTHON')
    # print('---------------------------Comeca FPYTHON-------------------------')
    # print('Inicializa FPYTHON')
    return t


def t_FPYTHON_FECHAFP(t):
    r'"""'
    t.lexer.begin('INITIAL')
    # print('---------------------------Acaba FPYTHON-------------------------')
    # print('Acaba FPYTHON')
    # print('==========================')
    return t


def t_FPYTHON_FUNABRE(t):
    r'deff'
    # print('----------------Abre função----------------------')
    return t


def t_FPYTHON_BOOL(t):
    r'(true|false)'
    # print(f'Booleano {t.value}',end=' ')
    return t


def t_FPYTHON_ABREL(t):
    r'\['
    # print('[',end=' ')
    return t


def t_FPYTHON_FECHAL(t):
    r'\]'
    # print(']',end=' ')
    return t


def t_FPYTHON_ABREP(t):
    r'\('
    # print('(',end=' ')
    return t


def t_FPYTHON_FECHAP(t):
    r'\)'
    # print(')')
    return t


def t_FPYTHON_FUNFECHA(t):
    r'end'
    # print('--------------Termina função---------------------')
    return t


def t_FPYTHON_IF(t):
    r'if'
    # print('if')
    return t


def t_FPYTHON_ELSE(t):
    r'else'
    # print('else')
    return t


def t_FPYTHON_MENOR(t):
    r'<'
    # print('<',end=' ')
    return t


def t_FPYTHON_MAIOR(t):
    r'>'
    # print('>',end=' ')
    return t


def t_FPYTHON_MENORIGUAL(t):
    r'<='
    # print('<=',end=' ')
    return t


def t_FPYTHON_MAIORIGUAL(t):
    r'>='
    # print('>=',end=' ')
    return t


def t_FPYTHON_IGUAL(t):
    r'=='
    # print('==',end=' ')
    return t


def t_FPYTHON_IN(t):
    r'in'
    # print('in',end=' ')
    return t


def t_FPYTHON_NOT(t):
    r'not'
    # print('not',end=' ')
    return t


def t_FPYTHON_DIFERENTE(t):
    r'!='
    # print('!=',end=' ')
    return t


def t_FPYTHON_CONDAND(t):
    r'and'
    # print('and',end=' ')
    return t


def t_FPYTHON_CONDOR(t):
    r'or'
    # print('or',end=' ')
    return t


def t_FPYTHON_RETURN(t):
    r'return'
    # print('Return' ,end=' ')
    return t


def t_FPYTHON_NEXT(t):
    r':'
    # print(':',end=' ')
    return t


def t_FPYTHON_PV(t):
    r';'
    # print(';')
    return t


# def t_COMMENT(t):
#     r'\#'
#     # print('Comentário')
#     return t

def t_FPYTHON_NUMBER(t):
    r'\d+(\.d+)?'
    # print(f'Argumento número {t.value}',end=' ')
    return t


def t_FPYTHON_WORD(t):
    r'[A-Za-z_]\w*'
    # print(f'Palavra {t.value}',end=' ')
    return t


def t_INITIAL_REST(t):
    r'(?:(?!""").)+'
    return t


def t_error(t):
    t.lexer.skip(1)
    return t


lexer = lex()
lexer.stack = []

inp2 = '''
"""FPYTHON
deff pertence([],_)
    return false;
end

deff pertence([h:t],num)
    if (h == num) 
        return true ;
    else 
        return pertence(t,num) ;
end

deff append([],num)
    return [num];
end

deff append([h:t],num)
    return [h:append(t,num)];
end

deff adiciona(l,num)
    if (not pertence(l,num))
        return append(l,num) ;
    else
        return l ;
end

deff eliminarepetidos([])
    return [];
end
deff eliminarepetidos([h:t])
    return adiciona(eliminarepetidos(t),h);
end
"""

lista = [1,2,3,4,5,6,3,4,51,243,13,53,32]
soma = f_eliminarepetidos_(lista)
# print(soma)
'''

inp = '''

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
        if (not con2(t,n))
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
# print(y)
l = [1,2,3,4,5]
sum_l = f_sum_(l)
# print(sum_l)
'''

lexer.input(inp2)
t = lexer.token()
while (t):
    # if t.type != 'error':
    #     print(t)
    t = lexer.token()
