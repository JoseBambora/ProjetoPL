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

