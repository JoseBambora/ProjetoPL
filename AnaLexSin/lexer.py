from ply.lex import lex

reserved = {
   'if' : 'IF',
   'else' : 'ELSE',
   'in' : 'IN',
   'not' : 'NOT',
   'deff' : 'FUNABRE',
   'end' : 'FUNFECHA',
   'return' : 'RETURN',
   'and' : 'CONDAND',
   'or' : 'CONDOR',
   'true' : 'BOOL',
   'false' : 'BOOL'
}

tokens = [
    'ADD',  # +
    'MINUS',  # -
    'TIMES',  # *
    'DIVIDE',  # /
    'MOD',  # %
    'OR',  # |
    'AND',  # &
    'NUMBER',  # INT FLOAT
    # 'BOOL',  # true false
    # 'FUNABRE',  # deff
    # 'FUNFECHA',  # end
    'ABREP',  # (
    'FECHAP',  # )
    'VIR',  # , -> argumentos
    'WORD',  # palavra
    # 'IF',  # if
    # 'ELSE',  # else
    'ABREFP',  # """FPYTHON
    'FECHAFP',  # """
    'MENOR',  # <
    'MAIOR',  # >
    'IGUAL',  # ==
    'DIFERENTE',  # !=
    'MAIORIGUAL',  # >=
    'MENORIGUAL',  # <=
    # 'IN',  # in
    # 'NOT',  # not
    # 'CONDAND',  # and
    # 'CONDOR',  # or
    # 'RETURN',  # return
    'ABREL',  # [
    'FECHAL',  # ]
    'NEXT',  # :
    'PV',  # ;
    'REST',
    'ABREC',
    'FECHAC'
] + list(set(reserved.values()))

states = (('FPYTHON', 'inclusive'),)

t_FPYTHON_ignore = ' \t'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_FPYTHON_VIR(t):
    r','
    # print(',',end=' ')
    return t

def t_FPYTHON_ABREC(t):
    r'\{'
    return t

def t_FPYTHON_FECHAC(t):
    r'\}'
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


def t_FPYTHON_MENORIGUAL(t):
    r'<='
    # print('<=',end=' ')
    return t


def t_FPYTHON_MAIORIGUAL(t):
    r'>='
    # print('>=',end=' ')
    return t

def t_FPYTHON_MENOR(t):
    r'<'
    # print('<',end=' ')
    return t


def t_FPYTHON_MAIOR(t):
    r'>'
    # print('>',end=' ')
    return t

def t_FPYTHON_IGUAL(t):
    r'=='
    # print('==',end=' ')
    return t


def t_FPYTHON_DIFERENTE(t):
    r'!='
    # print('!=',end=' ')
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
    t.type = reserved.get(t.value,'WORD')
    return t


def t_INITIAL_REST(t):
    # r'(?:(?!""").)+'
    r'.+'
    return t


def t_error(t):
    t.lexer.errors(f'Token "{t.value}" não está definido')
    t.lexer.skip(1)


lexer = lex()
lexer.errors = []