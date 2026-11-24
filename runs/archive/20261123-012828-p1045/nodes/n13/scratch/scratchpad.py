import sympy as s
# Audit the random-colouring argument independently of any upper-bound theorem.
a,e,n=s.symbols('alpha epsilon n', positive=True)
p=s.sqrt(a)/(1+s.sqrt(a))
N=(1-e)*(1+s.sqrt(a))**2*n
red_mean_bound=s.simplify(N*p**2)
blue_mean_bound=s.simplify(N*(1-p)**2)
print('red probability:',p)
print('upper bound on expected red common neighbours:',red_mean_bound)
print('upper bound on expected blue common neighbours:',blue_mean_bound)
print('red mean / (alpha*n):',s.simplify(red_mean_bound/(a*n)))
print('blue mean / n:',s.simplify(blue_mean_bound/n))
print('Logical consequence: a lower bound on liminf, not an upper bound.')
print('No matching upper-bound theorem or parameter range is verified by this computation.')
