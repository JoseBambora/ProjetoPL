"""FPYTHON
deff fib(0) return 0; end
deff fib(1) return 1; end
deff fib(n) return fib(n-1) + fib(n-2); end
"""
print([f_fib_(n) for n in range(12)])

"""FPYTHON
deff soma_impares([]) return 0; end
deff soma_impares([h:t])
    if(h % 2 == 1)
        return h + soma_impares(t);
    else
        return soma_impares(t);
end
"""

print(f_soma_impares_([1,2,5,7,2,3]))

"""FPYTHON
deff mais_um(x) return x+1; end
deff sum([]) return 0; end
deff sum([h:t]) return h + sum(t); end
"""

x = 4
y = f_mais_um_(x)

print(y)
l = [1,2,3,4,5]
sum_l = f_sum_(l)
print(sum_l)

"""FPYTHON
deff complicado(x,y,z)
    if (not (x < z and x > y))
        return 0;
    else
        if (x == z or x == y)
            return 1;
        else
            if(z == y and (not (z < z) and z != 1))
                return 2;
            else
                if(z <= y or z <= x)
                    return 3;
                else
                    return 4;
end

deff complicado(0,y,z)
    if (y == z)
        return 0;
    else
        if (y < z)
            return 1;
        else
            if (y+z < -1)
                return 2;
            else
                return 3;
end


deff complicado2([],[])
    return true;
end

deff complicado2(_,[])
    return false;
end

deff complicado2([],_)
    return false;
end

deff complicado2([h:t],[h2:t2])
    return h == h2 and complicado2(t,t2);
end

deff getindexAux([h],_)
    return h;
end

deff getindexAux([h:t],index)
    if(index == 0)
        return h;
    else
        return getindexAux(t,index-1);
end
        
deff getindex([],_)
    return [];
end

deff getindex([[h:t2]:t],index)
    return [getindexAux([h:t2],index):getindex(t,index)];
end

deff abs(x)
    if (x >= 0)
        return x;
    else
        return x*-1;
end

deff inverso(true)
    return false;
end

deff inverso(false)
    return true;
end

deff all_zero([0])
    return true;
end

deff all_zero([0:t])
    return all_zero(t);
end

deff all_zero(_)
    return false;
end
"""

print(f_complicado2_([1,2,3],[1,2,3]))
print(f_complicado2_([1,2,3],[1,2,3,4]))

print(f_getindex_([[1,2],[3,4],[5,6,7,4]],3))

print(f_abs_(-1))
print(f_abs_(0))
print(f_abs_(30))
print(f_inverso_(False))
print(f_inverso_(True))

"""
"""

def seila():
    print(f_all_zero_([0,0,0,0,0]))
    print(f_all_zero_([0,0,0,3,0]))
    print(f_all_zero_([1,0,0,-3,0])) 

seila()
