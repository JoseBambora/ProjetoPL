import copy
import ply.yacc as yacc
import ply.lex
from AnaLexSin.lexer import tokens


#-------------------- Início Código Funcional --------------------


def f_mais_um_(arg0):
	x = arg0
	return copy.deepcopy(x+1)

def f_sum_(arg0):
	if len(list_0) == 0:
		list_0 = arg0
		return copy.deepcopy(0)
	if len(list_0) >= 1:
		list_0 = arg0
		h = list_0[0]
		t = list_0[1:]
		return copy.deepcopy(h+f_sum_(copy.deepcopy(t)))

def f_div_(arg0,arg1):
	if arg1 == 0:
		n = arg0
		return copy.deepcopy(0)
	if arg0 == 0:
		n = arg1
		return copy.deepcopy(0)
	if arg1 == -1:
		n = arg0
		return copy.deepcopy(n*(copy.deepcopy(-1)))

def f_cond_(arg0):
	x = arg0
	if x < 1:
		return copy.deepcopy(2)
	else:
		return copy.deepcopy(3)

def f_con2_(arg0,arg1):
	if len(list_0) == 0:
		list_0 = arg0
		_ = arg1
		return copy.deepcopy(False)
	if len(list_0) >= 1:
		list_0 = arg0
		n = arg1
		h = list_0[0]
		t = list_0[1:]
		if n == h:
			if not ( f_con2_ ( copy.deepcopy(t) , copy.deepcopy(n) ) and f_con2_ ( copy.deepcopy(t) , copy.deepcopy(n) ) ):
				if True:
					return copy.deepcopy(True)
				else:
					return copy.deepcopy(False)
			else:
				return copy.deepcopy(False)
		else:
			if f_con2_ ( copy.deepcopy(t) , copy.deepcopy(n) ):
				if True:
					return copy.deepcopy(True)
				else:
					return copy.deepcopy(False)
			else:
				return copy.deepcopy(False)
	if len(list_0) == 5 and list_0[0] == 1 and list_0[1] == 2 and list_0[2] == 3 and list_0[3] == 4 and list_0[4] == False:
		list_0 = arg0
		k = arg1
		return copy.deepcopy(0)
	if len(list_1) >= 1 and (len(list_1[0]) >= 1 and list_1[0][0] == 2):
		list_1 = arg0
		k = arg1
		list_0 = list_1[0]
		t = list_0[1:]
		t2 = list_1[1:]
		return copy.deepcopy(0)

def f_seila_(arg0,arg1,arg2):
	if arg1 == 0 and arg2 == True and len(list_0) == 2 and list_0[0] == 1 and list_0[1] == 2:
		list_0 = arg0
		return copy.deepcopy(4)
	if arg2 == True and len(list_0) == 0:
		list_0 = arg0
		num = arg1
		return copy.deepcopy(num+1)
	if arg2 == False and len(list_0) == 0:
		list_0 = arg0
		num = arg1
		return copy.deepcopy(num)
	if arg2 == True and len(list_0) >= 1:
		list_0 = arg0
		num = arg1
		h = list_0[0]
		t = list_0[1:]
		return copy.deepcopy(h+f_seila_(copy.deepcopy(t))+num+1)
	if arg2 == False and len(list_0) >= 1:
		list_0 = arg0
		num = arg1
		h = list_0[0]
		t = list_0[1:]
		return copy.deepcopy(h+f_seila3_(copy.deepcopy(f_seila_(copy.deepcopy(t))))+num)

def f_seila3_(arg0):
	d = arg0
	return copy.deepcopy(f_seila3_(copy.deepcopy(5+(3*d))))

def f_uminho_(arg0,arg1):
	if arg0 == 1 and arg1 == 2:
		return copy.deepcopy([copy.deepcopy(0+2)])
	else:
		n = arg0
		t = arg1
		return copy.deepcopy([copy.deepcopy(n)] + copy.deepcopy(t))

def f_con3_(arg0,arg1):
	if len(list_1) == 1 and (len(list_1[0]) == 1 and list_1[0][0] == 3):
		list_1 = arg0
		k = arg1
		return copy.deepcopy(0)
	if len(list_3) >= 1 and (len(list_3[0]) >= 3 and (len(list_3[0][0]) >= 1) and (len(list_3[0][1]) >= 1) and list_3[0][2] == 3):
		list_3 = arg0
		k = arg1
		list_2 = list_3[0]
		list_0 = list_2[0]
		list_1 = list_2[1]
		h1 = list_0[0]
		k = list_0[1:]
		h2 = list_1[0]
		k2 = list_1[1:]
		t = list_2[3:]
		t2 = list_3[1:]
		if ( k in t ) and ( k in t2 ):
			if k != f_seila_ ( copy.deepcopy(2) , copy.deepcopy(3) , copy.deepcopy(4) ):
				return copy.deepcopy(f_con2_(copy.deepcopy([copy.deepcopy([copy.deepcopy(2),copy.deepcopy(3)] + copy.deepcopy(t))] + copy.deepcopy(t2)),copy.deepcopy(k),copy.deepcopy(3)))
			else:
				return copy.deepcopy(False)
		else:
			return copy.deepcopy(f_seila_(copy.deepcopy(3*(-(1))),copy.deepcopy(1),copy.deepcopy(3*1*(-(40*50*f_len_(copy.deepcopy([copy.deepcopy(h1)] + copy.deepcopy(t)))))+43-([copy.deepcopy(h)] + copy.deepcopy(t))),copy.deepcopy(2),copy.deepcopy(f_kkk_(copy.deepcopy(1),copy.deepcopy(2),copy.deepcopy(3)))))

def f_semargs_():
	return copy.deepcopy(0)

def f_soma_(arg0,arg1):
	if arg1 == -1:
		x = arg0
		return copy.deepcopy(x-1)
	else:
		x = arg0
		y = arg1
		return copy.deepcopy(x+y)


#-------------------- Fim do Código Funcional --------------------

print('Boas')
x = 4
y = f_mais_um_(x)
print(y)
l = [1,2,3,4,5]
sum_l = f_sum_(l)
print(sum_l)
def seila():
    print('boas')
    i = 3 + 5
    print(i)
print(f_uminho_())