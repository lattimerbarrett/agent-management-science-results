import sympy as s
k,i,e=s.symbols('k i e',integer=True,nonnegative=True)
# Sym^k E0 twist detE+K: a=6i-k+2, b=(12e+5)k-(12e+6)i+(11e+2)
a=6*i-k+2;b=(12*e+5)*k-(12*e+6)*i+11*e+2
chi=s.expand((a+1)*(b+1)-e*a*(a+1)/2)
print(s.factor(s.summation(chi,(i,0,k))))
