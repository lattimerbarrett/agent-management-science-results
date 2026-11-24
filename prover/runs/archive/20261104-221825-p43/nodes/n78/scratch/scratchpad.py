import sympy as s
x,y,u,v=s.symbols('x y u v', real=True)
F=x**5-10*x**3*y**2+5*x*y**4+u**2-v**2
print('Hamiltonian germ:',F)
print('gradient:',[s.diff(F,t) for t in (x,y,u,v)])
print('Local degree: degree of grad Re(z^5) is -4; degree of grad Re(w^2) is -1; product =',(-4)*(-1))
print('Global Lefschetz number = Euler characteristic =',1+2+1)
print('Floer total rank (over a suitable Novikov field) =',1+2+1)
print('Sphere action periods: omega(mA+nB)=4*pi*(m+n); group = 4*pi*Z')
print('Thus index and ungraded rank both allow four units of local data at a single fixed point. The germ alone does not establish compatibility of graded local Floer data or provide the global construction.')
