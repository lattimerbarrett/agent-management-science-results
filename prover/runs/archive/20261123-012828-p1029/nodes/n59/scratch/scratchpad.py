import sympy as s
eta=s.symbols('eta',positive=True)
for N in range(1,9):
 t=s.symbols('t0:'+str(N),positive=True)
 c=s.symbols('c0:'+str(N),commutative=False)
 scaled=sum(eta/t[i]*c[i] for i in range(N))
 slack=1-sum(c)+sum((1-eta/t[i])*c[i] for i in range(N))
 assert s.expand(1-scaled-slack)==0
print('Verified for N=1,...,8:')
print('1 - sum((eta/t_j)c_j) = (1-sum(c_j)) + sum((1-eta/t_j)c_j).')
print('Thus eta<=t_j implies every scaled partial sum is <=1.')
