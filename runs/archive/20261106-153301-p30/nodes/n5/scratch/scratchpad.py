import sympy as sp

# Check the obstruction to a naive codimension-two reduction.
# E = R^n x {0,0}; original measures are smoothed by independent
# centered Gaussian coordinates u,v of variance eps^2.
# An auxiliary measure can use variance 1 in these coordinates.
u, eps = sp.symbols('u eps', positive=True)
phi = sp.exp(-u*u/(2*eps**2))/(sp.sqrt(2*sp.pi)*eps)
half_mass = sp.integrate(phi, (u, 0, sp.oo))
print('Gaussian half-space mass:', half_mass)
print('Each quadrant mass for every smoothed original measure:', half_mass**2)
print('Each quadrant mass for the auxiliary product measure:', (half_mass**2).subs(eps, 1))
n = 9
normal_u = sp.Matrix([0]*n + [1,0])
normal_v = sp.Matrix([0]*n + [0,1])
print('Restricted normal of H_u on E:', list(normal_u[:n]))
print('Restricted normal of H_v on E:', list(normal_v[:n]))
assert all(c == 0 for c in normal_u[:n])
assert all(c == 0 for c in normal_v[:n])
print('Both limiting hyperplanes contain E; neither restricts to a hyperplane of E.')
print('Thus this auxiliary-measure construction alone does not justify dimension reduction.')

for s in range(3,8):
    j = 2**s - 2
    lower = (3*j + 1)//2
    print(f's={s}: j={j}, moment-curve lower bound={lower}, supplied sharp value={3*2**(s-1)-3}')
