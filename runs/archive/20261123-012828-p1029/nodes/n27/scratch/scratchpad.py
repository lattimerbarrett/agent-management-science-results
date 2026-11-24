import sympy as s
x,n=s.symbols('x n', real=True, positive=True)
# On [-1,1], f_n(x)=min(1,n*max(x,0)); normalized Lebesgue state.
I=s.simplify((s.integrate(n*x,(x,0,1/n))+1-1/n)/2)
print('Integral of f_n:', I)
print('Integral increment:',s.factor(I.subs(n,n+1)-I))
print('The bounded increasing functions converge pointwise to 1_(0,1].')
print('That function is in the Borel/monotone completion, not in C([-1,1]).')
print('No continuous least upper bound exists: any continuous upper bound')
print('is >=1 at 0, but can be decreased at each prescribed point x<0.')
