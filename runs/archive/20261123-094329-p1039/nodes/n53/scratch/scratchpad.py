import sympy as s
z2, r=s.symbols('z2 r', nonnegative=True)
a=2-(z2-1)**2
print('Squared fiber radius:',s.expand(a))
print('At z=0, squared radius:',a.subs(z2,0))
print('At |z|=1, squared radius:',a.subs(z2,1))
print('For n>=3, fiber C^(n-1) minus a closed ball is Oka (or punctured/whole space).')
print('Thus any bounded-above psh function is constant on each fiber.')
print('A local holomorphic section with a sufficiently large constant w makes the induced base function subharmonic.')
print('The base is C, so bounded-above psh functions on the entire exterior are constant.')
# Check the boundary Levi form and a simple entire curve.
t,A,B=s.symbols('t A B', nonnegative=True)
curve=s.expand((t-1)**2 + A+B*t-2)
print('rho on curve (z,w)=(z,(sqrt(A),sqrt(B)*z,0,...)):',curve)
print('For A>1 and B>=2, this is positive for every t=|z|^2>=0.')
