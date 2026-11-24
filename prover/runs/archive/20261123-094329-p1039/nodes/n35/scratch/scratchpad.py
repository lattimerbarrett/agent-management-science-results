import sympy as s
pi=s.pi
eps=1/(32*pi)
r=s.Rational(1,1000)
# Graph-ball candidate: rho=|w-h(z)|^2+eps^2|z|^2/4-eps^2.
# On the radius-r ball about (1/2,0), |h(z)-h(1/2)| <= (pi+1)r,
# and |w|<=r, using |h_z|<=pi on |z|<=1, |h_barz|=1.
lower=s.sqrt(2)/pi-(pi+2)*r
print('epsilon =',s.N(eps,16))
print('Lower bound for |w-h(z)| on local ball =',s.N(lower,16))
print('Certified exterior margin, lower^2 - eps^2 =',s.N(lower**2-eps**2,16))
assert float(lower**2-eps**2)>0.19
print('Circle |z|=1, |w|<sqrt(3)*eps/2 lies in int(K).')
print('For any entire g nonzero on K: winding of g along such a circle is zero')
print('(the circle is nullhomotopic in the graph ball K).')
print('Argument principle then excludes zeros throughout each flat disk.')
print('Thus no ambient-closed analytic hypersurface in the exterior meets')
print('{|z|<1, |w|<sqrt(3)*eps/2}. This does NOT exclude nonproper entire maps.')
