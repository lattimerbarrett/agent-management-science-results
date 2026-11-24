import sympy as s
n,r,lam=s.symbols('n r lam',positive=True)
a=(n-2)/2
U=(lam/(lam**2+r**2))**a
# Boundary stress cancellation after two tangential integrations by parts.
D=n-1
DU2=s.diff(U**2,r,2)+(D-1)/r*s.diff(U**2,r)
c=(n-2)/(4*(n-1))
shape_density=-s.diff(U,r)**2/2+(n-2)**2*U**(2*n/(n-2))/2+c*DU2
# Positive symbols do not suffice for SymPy nested-power simplification;
# rewrite all critical powers with their exact rational form.
shape_density=shape_density.subs(U**(2*n/(n-2)),(lam/(lam**2+r**2))**n)
shape_density=s.powsimp(shape_density,force=True)
assert s.simplify(shape_density)==0
# Direct normalized stress formula avoids all nested powers.
stress=(n-2)**2*lam**(n-2)*(lam**2-r**2)/(2*(lam**2+r**2)**n)
assert s.simplify(stress+c*DU2)==0
# PDE for full radial bubble in n variables.
rho=s.symbols('rho',positive=True)
V=(lam/(lam**2+rho**2))**a
lap=s.diff(V,rho,2)+(n-1)/rho*s.diff(V,rho)
assert s.simplify(lap+n*(n-2)*lam**((n+2)/2)/(lam**2+rho**2)**((n+2)/2))==0
# Source for homogeneous harmonic degree l, multiplied by r^(2i).
i,l=s.symbols('i l',integer=True,nonnegative=True)
# In dimension d=n-1, Δ(r^(2i)H_l)=2i(2i+2l+n-3)r^(2i-2)H_l.
A=i*(2*i+2*l+n-3)/(n-1)
B=s.factor(A-(l+2*i-1))
print('Bubble PDE, first shape variation cancellation: exact PASS')
print('Normalized source for graph H_l*r^(2i): H_l*[A*r^(2i-2)+B*r^(2i)]')
print('A =',A,'B =',B)
print('For l=2,i=0: source/H_2 =',s.simplify(A.subs({l:2,i:0})),s.simplify(B.subs({l:2,i:0})))
print('For l=2,i=1: source/H_2 =',s.simplify(A.subs({l:2,i:1})),s.simplify(B.subs({l:2,i:1})))
