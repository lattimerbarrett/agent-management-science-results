import sympy as s
x,y,X,Y,eta=s.symbols('x y X Y eta', real=True)
# Lift w=exp(x+iy), t=2x; set z=Z*exp(2i*(x+iy)), Z=X+iY.
# Then |z-exp(2ix)|^2 = exp(-4y)*|Z-exp(2y)|^2.
expr=s.expand(s.exp(-4*y)*((X-s.exp(2*y))**2+Y**2)-1+eta)
print('Lifted worm defining function:',s.simplify(expr))
print('Equivalent inequality:', 'X^2+Y^2 - 2 exp(2y) X + eta exp(4y) <= 0')
print('For eta>=0 it implies Re Z=X>=0.')
print('Deck shift xi -> xi+2*pi*i sends Z -> exp(4*pi)*Z.')
print('Thus the lift has half-plane supporting geometry but nontrivial expanding monodromy; it is not a compact holomorphically convex obstacle.')