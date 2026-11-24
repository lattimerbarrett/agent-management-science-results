import sympy as s
eta=s.symbols('eta', positive=True)
t=eta/2
lower=s.simplify((eta-t)/(1-t))
print('If tau(x)=eta and p=1_(eta/2,1](x), D(p) >=', lower)
print('Because x >= (eta/2)*p, bounded partial sums of x imply:')
print('sum_{n<N} p_n <= (2/eta)*1 for every N.')
print('Thus the proposed sequence yields an infinite bounded-sum sequence')
print('of projections whose dimensions are all >= eta/(2-eta).')
