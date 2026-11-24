import sympy as s
n=s.symbols('n',integer=True,positive=True)
c=(n-2)/(4*(n-1)); u0=s.symbols('u0',positive=True)
# On the upper unit hemisphere z=x_{n+1}, dz/dnu=-1 on equator.
# A constant normal displacement rho=1 gives H'=-(n-1).
# Linearized Robin datum is -2*c*u0*H'.
b=s.simplify(2*c*u0*(n-1))
vcoef=-b  # v=vcoef*z gives outward normal derivative b
print('constant boundary displacement: Robin datum =',b)
print('Jacobi correction v = coefficient * x_(n+1), coefficient =',vcoef)
print('v|boundary=0, so the boundary pairing <source,v> is zero.')
print('But the negative Neumann mode (constant interior function) has Q(1,1)=-n*Vol, not zero.')
# General finite-dimensional coordinate-shift invariant for invertible A.
a,r,w,B=s.symbols('a r w B',nonzero=True)
newB=B+r*w+a*w*w/2
newr=r+a*w
print('Exact scalar Schur base-change defect:',s.simplify(newB-newr**2/(2*a)-(B-r*r/(2*a))))
# Need retain linear forcing as part of r if present.
f=s.symbols('f')
wrongnewB=B+r*w+a*w*w/2
correctnewr=r-f+a*w
old=B-(r-f)**2/(2*a)
print('Defect if base change omits the forcing contribution -f*w:',s.expand(wrongnewB-correctnewr**2/(2*a)-old))
