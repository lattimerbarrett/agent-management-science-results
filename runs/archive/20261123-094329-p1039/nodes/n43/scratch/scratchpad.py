import sympy as s
# Audit the dimension-raising candidate R(z,w)=rho(z)+||w||^2.
# At (q,0), its tangential Levi form is the original tangential
# Levi form direct sum the identity. Test an arbitrary mixed block.
a,b=s.symbols('a b', positive=True)
for k in range(1,5):
 H=s.diag(a,-b,*([1]*k))
 print('added dimensions',k,'tangential Levi eigenvalues',H.eigenvals())
print('Geometric facts: R<=0 => rho<=0 and ||w||^2<=-min_K rho, hence compact.')
print('Boundary: w!=0 gives dR!=0; w=0 gives rho=0 and drho!=0.')
print('Interior fibers over Omega are balls, and (z,w)->(z,tw) retracts onto Omega.')
print('These facts establish compactness, connectedness, smoothness and mixed Levi signature.')
print('They do NOT establish preservation of CAP. The projection of the exterior has changing fibers and is not an Oka fiber bundle.')