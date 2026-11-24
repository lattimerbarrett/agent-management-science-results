import sympy as s
r=s.symbols('r', positive=True)
a=s.exp(-1/r**2)
print('radial derivative:',s.diff(a,r))
print('second radial derivative:',s.diff(a,r,2))
for k in [2,3,4,6,8]:
    print('limit r^(-%d) exp(-1/r^2) ='%k,s.limit(a/r**k,r,0,dir='+'))
# A local Lipschitz constant L bounds periods of any nonconstant orbit
# contained in that neighborhood: D <= (T/2) * L*D.
T,L,D=s.symbols('T L D',positive=True)
print('Diameter estimate gives T >=',s.solve(s.Eq(D,T*L*D/2),T)[0])
