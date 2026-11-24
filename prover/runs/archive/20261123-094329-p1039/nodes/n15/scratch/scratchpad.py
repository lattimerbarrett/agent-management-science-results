import sympy as s
x,y,u,v,a,b=s.symbols('x y u v a b', real=True)
# A smooth compact obstacle with a locally indented boundary.
rho=(x*x+y*y-a)**2+u*u+v*v-b
L1=s.simplify((s.diff(rho,x,2)+s.diff(rho,y,2))/4)
L2=s.simplify((s.diff(rho,u,2)+s.diff(rho,v,2))/4)
print('Full complex Levi entries:',L1,L2,'and 1 in each further coordinate')
print('At q=(0,sqrt(b-a^2),0,...), b>a^2:')
print('complex tangency excludes the z2 normal; tangent Levi eigenvalues are',L1.subs({x:0,y:0}),'and 1 with multiplicity n-2')
# This is only a differential-geometric check, not an Oka proof.
print('n=2: exterior is strictly pseudoconvex at q, ruling out Oka.')
print('n>=3: the exterior Levi form is mixed; the peak-function obstruction does not apply.')
# Critical values determine boundary regularity.
print('rho at critical points:',-b,a*a-b)
print('For a>0,b>a^2, neither critical value is zero; boundary is smooth and obstacle is bounded, connected.')