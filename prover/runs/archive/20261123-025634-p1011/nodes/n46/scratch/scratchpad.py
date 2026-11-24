import sympy as s
n=s.symbols('n', positive=True)
# On S^n_+, z=x_{n+1}. Surface latitude density is
# |S^(n-1)|*(1-z*z)^((n-2)/2) dz, 0<z<1.
# Normalize all integrals by |S^(n-1)|.
I_z=s.Rational(1,2)*s.beta(1,n/2)
print('Integral z / |S^(n-1)| =',s.simplify(s.expand_func(I_z)))
print('Jacobi pairing J(z,1)/|S^(n-1)| =',s.simplify(-n*s.expand_func(I_z)))
# Since |grad z|^2=1-z^2, J(z,z) has integrand 1-(n+1)z^2.
I_0=s.beta(s.Rational(1,2),n/2)/2
I_z2=s.beta(s.Rational(3,2),n/2)/2
print('Jacobi pairing J(z,z)/|S^(n-1)| =',s.simplify(s.expand_func(I_0-(n+1)*I_z2)))
# Stereographic boundary normal displacements for graph gauge functions.
z=s.symbols('z')
r2=(1+z)/(1-z)
print('graph constant -> displacement:',s.simplify(2/(1+r2)))
print('graph radial quadratic -> displacement:',s.simplify(2*r2/(1+r2)))
print('radial quadratic minus constant -> displacement:',s.simplify(2*(r2-1)/(1+r2)))
