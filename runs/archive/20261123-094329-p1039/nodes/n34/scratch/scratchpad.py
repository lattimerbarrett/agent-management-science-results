import sympy as s
r=s.symbols('r', nonnegative=True)
R2=4-(r-1)**2
# Fubini/Hartogs fiber ball radius R(w) with r=|w|^2.
phi=-s.log(R2)/2
levi=s.factor(s.diff(phi,r)+r*s.diff(phi,r,2))
print('Ball-fiber radius squared:',s.factor(R2))
print('Levi coefficient of -log R(w):',levi)
print('At w=0:',levi.subs(r,0))
print('K: ||z||^2+(|w|^2-1)^2 <= 4')
print('At (sqrt(3),0,...;0), tangent Levi signature of K: n-2 positive and one negative.')
print('For n>=3, nonempty nontrivial fibers of the exterior are complements of closed balls in C^(n-1), hence Oka.')
print('But the fiber over |w|^2>3 is all C^(n-1), so fiber topology changes; this projection is not an Oka fiber bundle.')
print('The negative curvature at w=0 rules out applying holomorphic convexity of the total obstacle in a Stein neighborhood.')