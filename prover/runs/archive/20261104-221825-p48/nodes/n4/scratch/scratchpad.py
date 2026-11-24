import sympy as s
m,i,e=s.symbols('m i e', integer=True, nonnegative=True)
a=6*i-m+2
b=-(12*e+6)*i+(12*e+5)*m+11*e+2
# summands Sym^m E0 tensor detE tensor K
chi=s.expand((a+1)*(b+1)-e*a*(a+1)/2)
print(s.factor(s.summation(chi,(i,0,m))))
