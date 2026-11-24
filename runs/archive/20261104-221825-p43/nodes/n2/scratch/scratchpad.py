import sympy as s
x,y,u,v=s.symbols('x y u v',real=True)
print('Lefschetz number on S2 x S2:',1+2+1)
for k in (2,3,5):
    # Re(z^k+w^2): the z-gradient has local degree -(k-1),
    # while the w-gradient has degree -1.
    F=s.re(s.expand((x+s.I*y)**k+(u+s.I*v)**2))
    print('k =',k,' F =',F,' local gradient degree =',k-1)
