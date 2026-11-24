import sympy as s
eta,C=s.symbols('eta C', positive=True)
t=eta/2
print('Spectral reduction:')
print('D(p_n) >=',s.factor((eta-t)/(1-t)), 'for 0<eta<=1.')
print('Bound on projection partial sums C =',s.simplify(1/t))
print('\nAudit using the established sequential-exhaustion theorem:')
print('If sum_{n<N} p_n <= C*1, apply exhaustion to x_n=p_n/C.')
print('Then tau(x_n)=D(p_n)/C -> 0, hence D(p_n)->0.')
print('This excludes the proposed spectral family, but the justification')
print('is sequential exhaustion, not projection-lattice finiteness alone.')
print('\nDirect application is shorter:')
print('sum_{n<N}(a_{n+1}-a_n)=a_N-a_0 <= 1;')
print('exhaustion forces tau(a_{n+1}-a_n)->0, contradicting eta>0.')
