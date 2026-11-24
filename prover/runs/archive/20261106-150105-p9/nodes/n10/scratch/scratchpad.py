import sympy as s
p=s.symbols('p', positive=True)
U=1+1/(p-1)-1/p
print('If A_p = R_p^p, an exponent a on R_p becomes a/p on A_p.')
print('Claimed expression U:',s.factor(U))
print('If U were an exponent on R_p, converted exponent:',s.factor(U/p))
print('For p>2, converted exponent minus scalar lower bound 1:',s.factor(U/p-1))
q=p/(p-1)
print('Dual consistency U(q)/(p-1)-U(p):',s.simplify(U.subs(p,q)/(p-1)-U))
print('Root-characteristic exponent corresponding to U:',s.simplify(p*U))
for v in [s.Rational(3,2),2,3,4]:
    print('p=',v,'U=',U.subs(p,v),'U/p=',(U/p).subs(p,v),'scalar lower=',max(1,1/(v-1)))
