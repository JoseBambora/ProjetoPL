"""FPYTHON
deff insert(e,[])
    return [e];
end

deff insert(e,[h:t])
    if (e >= h) 
        return [h:insert(e,t)];
    else
        return [e:h:t];
end

deff insertionSort([])
    return [];
end

deff insertionSort([h:t])
    return insert(h,insertionSort(t));
end
"""

lista = [-10,-8,4,2,1,-34,50]
aux = f_insertionSort_(lista)
print(lista)
print(f'isort: {aux}')

"""FPYTHON
deff junta(l0,l1,elem)
    return l0+[elem]+l1;
end

deff menores(e,[])
    return [];
end

deff maiores(e,[])
    return [];
end

deff menores(e,[h:t])
    if(h < e)
        return [h:menores(e,t)];
    else
        return menores(e,t);
end
    
deff maiores(e,[h:t])
    if(h > e)
        return [h:maiores(e,t)];
    else
        return maiores(e,t);
end

deff qsort([])
    return [];
end

deff qsort([h:t])
    return junta(qsort(menores(h,t)),qsort(maiores(h,t)),h);
end
"""

aux2 = f_qsort_(lista)
print(f'qsort: {aux2}')