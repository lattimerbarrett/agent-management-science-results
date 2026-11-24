import sympy as s
n,v,Delta,grad2,Sgg,S2=s.symbols('n v Delta grad2 Sgg S2', nonzero=True)
# The flat scalar-curvature equation for v=u^(-2/(n-2)) is
# v*Delta(v)-n/2*|grad(v)|^2=2*n.
# Differentiating it gives grad(Delta(v)).grad(v)=n*S(grad(v),grad(v))/v,
# where S=Hess(v)-Delta(v)*I/n.
gradDelta_dot_grad=n*Sgg/v
expression=v**(1-n)*S2+(n-1)/n*v**(1-n)*gradDelta_dot_grad+(1-n)*v**(-n)*Sgg
print('div(v^(1-n) S(grad v)) =',s.simplify(expression))
print('The integrated identity is a nonnegative bulk integral equal to the full boundary flux.')
print('For nonumbilic boundary the flux includes -II^0(grad_boundary v,grad_boundary v); its sign is not automatic.')
