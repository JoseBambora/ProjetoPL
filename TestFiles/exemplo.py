
"""FPYTHON
deff pertence([],_)
    return false;
end

deff pertence([h:t],num)
    if (h == num) 
        return true;
    else 
        return pertence(t,num);
end

deff append([],num)
    return [num];
end

deff append([h:t],num)
    return [h:append(t,num)];
end

deff adiciona(l,num)
    if (not pertence(l,num))
        return append(l,num);
    else
        return l;
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
print(soma)