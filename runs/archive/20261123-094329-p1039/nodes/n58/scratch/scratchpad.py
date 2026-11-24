import sympy as s
z,zb,w,wb=s.symbols('z zb w wb')
rho=z*zb+(w*wb)**2-w*wb-1
vars=[z,w]; bars=[zb,wb]
H=s.Matrix([[s.diff(rho,a,b) for b in bars] for a in vars])
print('Levi matrix of rho in a horizontal/vertical pair:',H)
p=-s.log(-rho)
Hp=s.Matrix([[s.diff(p,a,b) for b in bars] for a in vars])
g=s.Matrix([s.diff(rho,a) for a in vars])
gb=s.Matrix([[s.diff(rho,b) for b in bars]])
assert (Hp-(-H/rho+g*gb/rho**2)).applyfunc(s.simplify)==s.zeros(2)
print('Verified H(-log(-rho)) = H(rho)/(-rho) + partial(rho) tensor barpartial(rho)/rho^2.')
print('At z=1,w=0: rho=',rho.subs({z:1,zb:1,w:0,wb:0}),'; vertical Levi=',H[1,1].subs({w:0,wb:0}))
t=s.symbols('t',real=True)
print('Critical values (all horizontal coordinates zero):', [s.simplify((t*t-t-1).subs(t,a)) for a in [0,s.Rational(1,2)]])
print('Thus level rho=0 is regular, and horizontal restriction gives n-1 positive eigenvalues of the exhaustion.')
