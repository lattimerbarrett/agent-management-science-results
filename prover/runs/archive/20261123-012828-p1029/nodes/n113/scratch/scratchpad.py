import sympy as sp
# Audit the coefficients in repeated convex interpolation. No operator
# commutativity is used: every coefficient here is scalar and nonnegative.
for r in range(1,9):
    t=sp.symbols('t0:'+str(r))
    P=sp.prod(1-u for u in t)
    weights=[t[j]*sp.prod(1-t[l] for l in range(j+1,r)) for j in range(r)]
    assert sp.expand(P+sum(weights)-1)==0
print('Verified convex-interpolation coefficient identity for r=1,...,8.')
print('Audit conclusion: preservation of all upper bounds is valid when')
print('uniform tail gaps provide interpolation parameters bounded away from zero.')
print('Mere absence of a least upper bound does not supply that gap hypothesis.')
