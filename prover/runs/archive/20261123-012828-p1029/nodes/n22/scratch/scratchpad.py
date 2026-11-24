import sympy as s
eta=s.symbols('eta', positive=True)
t=eta/2
bound=s.simplify((eta-t)/(1-t))
print('Take t=eta/2 and p_n=1_(t,1](d_n).')
print('From d_n <= t*1 + (1-t)*p_n: tau(p_n) >=',bound)
print('From t*p_n <= d_n: sum_(n<N) p_n <=',s.simplify(1/t),'*1 for every N.')
print('Consequently a witness would give an infinite projection Bessel family of uniformly positive quasitracial dimension.')
print('The supplied verified exhaustion theorem rules out the original witness; the spectral reduction identifies exactly the packing assertion needed for a projection-based proof.')