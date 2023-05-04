from AnaLexSin.fpyacc import parser
from AnaLexSin.topython import toPython


def havepy(namefile):
    if not namefile.__contains__('.py'):
        namefile += '.py'
    return namefile

def getLinesfile():
    namefile = input('Qual o ficheiro que quer converter (não é preciso meter o .py)?\n')
    namefile = havepy(namefile)
    with open(namefile) as f:
        lines = f.readlines()
    return (namefile,lines)

def parseficheiro(namefile,lines):
    print(f'A fazer parsing do ficheiro {namefile}')
    parser.parse('\n'.join(lines))

def escreveRes():
    namefile = input('Qual o nome do ficheiro resultante (não é preciso meter o .py | default.py => ficheiro pré definido)?\n')
    if namefile == '':
        namefile = 'default'
    namefile = havepy(namefile)
    print('A escrever ficheiro resultante')
    toPython(parser,namefile)
    print(f'Escreveu ficheiro {namefile}')

namefile,lines = getLinesfile()
parseficheiro(namefile,lines)
escreveRes()