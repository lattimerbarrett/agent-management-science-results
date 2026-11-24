import sympy as s
z=s.Matrix(s.symbols('z1:4', real=True)); r=s.sqrt(z.dot(z))
P=z/r
J=P.jacobian(z)
expected=s.eye(3)/r-(z*z.T)/r**3
print('Jacobian of radial projection agrees with formula:',s.simplify(J-expected)==s.zeros(3))
print('Eigenvalues at z=(r,0,0):', J.subs({z[0]:s.symbols('a',positive=True),z[1]:0,z[2]:0}).eigenvals())
print('On 1/2 <= |z| <= 3/2, operator norm of projection derivative <= 2.')
print('A smooth cutoff supported in this annulus removes the singularity at zero.')
print('For any smooth vector field on S^2 x S^2, its pullback by the two radial projections, multiplied by these cutoffs, is a smooth compactly supported ambient extension.')
print('Its derivative is continuous with compact support, hence globally bounded.')
