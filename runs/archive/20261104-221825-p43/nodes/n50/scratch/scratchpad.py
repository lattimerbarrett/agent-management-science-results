import sympy as s
lam,L,T=s.symbols('lambda L T', positive=True)
# For a nonconstant T-periodic solution, let D be its positive diameter.
# Mean(X(x))=0 gives |X(x(t))| <= L D.
# The shorter time arc between diametral points has duration <=T/2.
# Hence D <= lambda*L*D*T/2.
print('Diameter estimate implies T >=',s.solve(s.Eq(1,lam*L*T/2),T)[0])
print('For T=1, lambda*L < 2 excludes every nonconstant periodic trajectory.')
# The sharper variance + Wirtinger estimate is also available.
print('Variance/Wirtinger estimate implies T >=', 2*s.pi/(lam*L))
