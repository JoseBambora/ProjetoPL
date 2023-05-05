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