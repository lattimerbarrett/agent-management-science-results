import sympy as S
n=S.symbols("n",positive=True)
p=(n+2)/(n-2);q=p+1;r=q/p
assert S.simplify(1/r-(p-2)/q-2/q)==0
assert S.simplify(q-2*n/(n-2))==0
assert S.simplify(1/r-p/q)==0
print("All reverse-LS exponent checks passed.")
