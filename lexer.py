from ply.lex import lex
import re

tokens = (
    'ADD',          # +
    'MINUS',        # -
    'TIMES',        # *
    'DIVIDE',       # /
    'MOD',          # %
    'OR',           # |
    'AND',          # &
    'NUMBER',       # INT FLOAT
    'BOOL',         # true false
    'LIST',         # [(...)] 
    'FUNABRE',      # deff
    'FUNFECHA',     # end
    'ARGSABRE',     # (
    'ARGSFECHA',    # )
    'VIR',          # , -> argumentos
    'ABRECORPOFUN', # :
    'VAR',          # palavra
    'IF',           # if
    'THEN',         # then
    'ELSE',         # else
    'CHAMADAFUN',   # palavra(
    'ABREFP',       # """FPYTHON
    'FECHAFP',      # """
    'MENOR',        # <
    'MAIOR',        # > 
    'IGUAL',        # ==
    'DIFERENTE',    # != 
    'MAIORIGUAL',   # >=
    'MENORIGUAL',   # <=
    'IN',           # in
    'NOT'           # not
    'CONDAND',      # and
    'CONDOR',       # or
    'RETURN'        # return
)

states = (
    ('FPYTHON','inclusive'),
    ('CORPOFUN','inclusive'),
    ('FUNCAO','inclusive'),
    ('IFTHENELSE','inclusive'),
    ('COND','inclusive')
)

t_VIR = r','

def t_INITIAL_ABREFP(t):
    r'"""(?i:FPYTHON)'
    t.lexer.begin('FPYTHON')
    print('INICIALIZA FPYTHON')
    return t

def t_FPYTHON_FECHAFP(t):
    r'"""'
    t.lexer.begin('INITIAL')
    print('Acaba FPYTHON')
    return t

def t_FPYTHON_FUNABRE(t):
    r'deff\s+([\w-]+)\('
    t.lexer.begin('FUNCAO')
    print('Nome funcão: ' + re.search('deff\s+(\w+)',t.value).group(1))
    return t

def t_FUNCAO_VAR(t):
    r'(\w+|\[\w+\s*\|\s*\w+\s*\])'
    print('Argumento ' + re.search('(\w+|\[\w+\s*\|\s*\w+\s*\])',t.value).group())
    return t

def t_FUNCAO_NUMBER(t):
    r'\d+'
    print('Argumento número ' + re.search('\d+',t.value).group())
    return t

def t_FUNCAO_LIST(t):
    r'(\[\s*\]|\[\s*((\w+|\d+)\s*,\s*)*(\w+|\d+)\s*\])'
    print('Argumento lista ' + re.search('(\[\s*\]|\[\s*((\w+|\d+)\s*,\s*)*(\w+|\d+)\s*\])',t.value).group())
    return t

def t_FUNCAO_BOOL(t):
    r'(true|false)'
    print('Argumento booleano ' + re.search('\w+',t.value).group())
    return t

def t_FUNCAO_ARGSFECHA(t):
    r'\)\s*:'
    t.lexer.begin('CORPOFUN')
    print('comeca corpo fun')
    return t

def t_CORPOFUN_FUNFECHA(t):
    r'end'
    state = 'FPYTHON'
    if len(t.lexer.stack) > 0:
        state = t.lexer.stack.pop()
    print('fecha funcao ' + state)
    if state == 'FPYTHON':
        print('========================')
    t.lexer.begin(state)
    return t

def t_CORPOFUN_IF(t):
    r'if\s*\('
    print('Inicializa if')
    t.lexer.begin('COND')
    t.lexer.stack.append('IFTHENELSE')
    return t

def t_COND_NUMBER(t):
    r'\d+'
    print('cond number')
    return t

def t_COND_BOOL(t):
    r'(true|false)'
    print('bool cond')
    return t

def t_COND_LISTA(t):
    r'(\[\s*\]|\[\s*((\w+|\d+)\s*,\s*)*(\w+|\d+)\s*\])'
    print('condicao lista')
    return t

def t_COND_VAR(t):
    r'(\w+|\[\w+\s*\|\s*\w+\s*\])'
    print('Condicao variável')
    return t

def t_COND_MENOR(t):
    r'<'
    print('menor')
    return t

def t_COND_MAIOR(t):
    r'>'
    print('maior')
    return t

def t_COND_MENORIGUAL(t):
    r'<='
    print('menor igual')
    return t

def t_COND_MAIORIGUAL(t):
    r'>='
    print('maior igual')
    return t

def t_COND_IGUAL(t):
    r'=='
    print('igual')
    return t

def t_COND_IN(t):
    r'in'
    print('in')
    return t

def t_COND_NOT(t):
    r'not'
    print('not')
    return t

def t_COND_DIFERENTE(t):
    r'!='
    print('diferente')
    return t

def t_COND_AND(t):
    r'and'
    print('and')
    return t

def t_COND_OR(t):
    r'or'
    print('or')
    return t

def t_COND_ARGSFECHA(t):
    r'\)'
    state = t.lexer.stack.pop(-1)
    t.lexer.begin(state)
    print('Fecha Condição. Estado: ' + state)
    return t

def t_COND_ARGSABRE(t):
    r'\('
    print('Condição aninhada')
    t.lexer.stack.append('COND')
    return t

def t_IFTHENELSE_THEN(t):
    r'then\s*:'
    print('then')
    t.lexer.stack.append('IFTHENELSE')
    t.lexer.begin('CORPOFUN')
    return t

def t_IFTHENELSE_ELSE(t):
    r'else\s*:'
    print('else')
    t.lexer.begin('CORPOFUN')
    return t

def t_CORPOFUN_RETURN(t):
    r'return'
    print('Return função')
    return t

def t_error(t):
    t.lexer.skip(1)
    return t


lexer = lex()
lexer.stack = []

inp = '''

"""FPYTHON
deff mais_um(x):
    return x + 1
end

deff sum([]):
    return 0
end

deff sum([h | t]):
    return h + sum(t)
end

deff cond(x):
    if (x < 1) then:
           return 2
        end
    else:
            return 3
        end
"""

x = 4
y = f_mais_um_(x)
print(y)
l = [1,2,3,4,5]
sum_l = f_sum_(l)
print(sum_l)
'''
lexer.input(inp)
t = lexer.token()
while(t):
    t = lexer.token()