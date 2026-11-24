import sympy as s
a,b=s.symbols('a b')
G=s.groebner([a*a-1,b*b-1],a,b)
E={ (i,j):s.expand((1+i*a)*(1+j*b)/4) for i in [-1,1] for j in [-1,1] }
reduce=lambda p:s.expand(G.reduce(s.expand(p))[1])
# Use rational-coefficient Groebner basis for the idempotents.
G=s.groebner([a*a-1,b*b-1],a,b,domain=s.QQ)
print('Quantum specialization: a^2=b^2=1; basis 1,a,b,ab.')
print('Four orthogonal idempotents:')
for k,e in E.items():
 print(k,e,'; e^2-e =',reduce(e*e-e))
assert all(reduce(e*f)==0 for k,e in E.items() for l,f in E.items() if k!=l)
print('Sum:',s.expand(sum(E.values())))
print('This algebra calculation does not identify distinct geometric fixed points: a local Floer group may have rank greater than one.')
