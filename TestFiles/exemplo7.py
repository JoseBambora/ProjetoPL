"""FPYTHON
deff soma(x,y)
    return seila(x,y);
end

deff seila(x,y)
    return 0;
end

deff soma_1(x)
    return x + 1;
end

deff soma1(l)
    return map(soma_1,l);
end

deff eq_zero(x) return x != 0; end
deff eq_zero2(x) return not (x == 0); end
deff pos(x) return x > 0; end
deff sem_zeros2(l) return filter(eq_zero2,l); end
deff sem_zeros(l)
    return map(sem_zeros2,l); 
end

deff soma_1_positivos(l)
    return { soma1 filter }(pos,l);
end

deff soma_1_10vezes(l)
    return { soma1 soma1 soma1 soma1 soma1 soma1 soma1 soma1 soma1 soma1}(l);
end

deff cmp(x)
    return -x;
end

deff sort_reverse(l)
    return { reverse sort }(cmp,l);
end


deff my_sort(l)
    return { sort }(cmp,l);
end

deff soma_2(elem,res)
    return elem + res;
end

deff somalista1(l)
    return foldr(soma_2,0,l);
end

deff somalista2(l)
    return foldl(soma_2,0,l);
end


deff soma_3(elem,res)
    if (elem > 0)
        return elem + res;
    else
        return res;
end

deff somalista_positivos(l)
    return foldr(soma_3,0,l);
end
    
"""

print(f_seila_(0,0))
l = [1,2,3,4]
aux = f_soma1_(l)
print(aux)

l[0] = 30
print(aux)
print(l)

aux = [[1,2,3,0,0,4,2],[3,4,0,0,0,3,4],[0,0,0,0,0]]
aux2 = f_sem_zeros_(aux)

aux[0][0] = 3
aux[2][1] = 1
print(aux)
print(aux2)

print(f_soma_1_positivos_([0,0,1,2,3,4,-4,-50,-40,210,0,320]))
print(f_soma_1_10vezes_([1,2,3,4,5,6,7,8,9,10]))
print(f_sort_reverse_([-10,-15,3,10,1,5,-20,3]))
print(f_my_sort_([-10,-15,3,10,1,5,-20,3]))
print(f_somalista1_([1,2,3,4,5,6,7,8,9,10]))
print(f_somalista2_([1,2,3,4,5,6,7,8,9,10]))
print(f_somalista_positivos_([1,2,3,4,5,6,7,8,9,10]))
print(f_somalista_positivos_([1,2,3,4,5,6,7,8,9,10,-50,0]))