"""FPYTHON 

deff len([]) return 0; end
deff len([h:t]) return 1 + len(t); end

deff kkk(_,_,_) return false; end

deff con2(h,k)
    return seila(h) + seila(h) + seila(k);
end


deff con2([h:t:t2:t3:t4],n)
    if (n == h)
        if (not (con2(t,n) and con2(t,n)))
            if(true)
                return [h:t:t2:t3:con2(t4,4)];
            else
                return [h,t,t2];
        else
            return funcaonaodefinda(1,2,3);
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
import ply.yacc as yacc
import ply.lex
from AnaLexSin.lexer import tokens

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
    return seila3(5+(3*d)); 
end
"""

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

"""FPYTHON

deff uminho(1,2)
    return [0+2];
end

deff uminho(n,t)
    return [n:t];
end
"""


"""FPYTHON

deff con2([1,2,3,4,false],k)
    return 0;
end

deff con2([[2:t]:t2],k)
   return 0;
end

deff con3([[3]],k)
    return 0;
end

deff con3([[[h1:k]:[h2:k2]:3:t]:t2],k)
    if ((k in t) and (k in t2))
        if (k != seila(2,3,4))
            return con2([[2:3:t]:t2],k,3);
        else
            return false;
    else 
        return seila(3*(-(1)),1,3*1*(-(40*50*len([h1:t])))+43-([h1:t]),2,kkk(1,2,3));
end

deff semargs()
    return 0;
end

deff soma(x,y)
    return x + y;
end

deff soma(x,-1)
    return x - 1;
end

"""

print(f_uminho_(1,2))
print(f_uminho_(4,[4,5,6,8]))

"""FPYTHON

deff con2([1,2,3,4,false],k)
    return 0;
end

deff con2([[2:t]:t2],k)
   return 0;
end

deff con3([[3]],k)
    return 0;
end

deff con3([[h1:2:h2:3:t]:t2],k)
    if ((k in t) and (k in t2))
        if (k != seila(2,3,4))
            return con2([[2:3:t]:t2],k,3);
        else
            return false;
    else 
        return seila(3*(-(1)),1,3*1*(-(40*50*len([h1:t])))+43-([h2:t]),2,kkk(1,2,3));
end
"""