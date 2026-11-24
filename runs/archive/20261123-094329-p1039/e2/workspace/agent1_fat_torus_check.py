import sympy as s
t,e=s.symbols("t e",real=True)
P=(4*t-2)*(e**2-(t-1)**2)+4*t*(t-1)**2
assert s.expand(P-(2*(t-(1-e**2))**2+2*e**2*(1-e**2)))==0
print("PASS: solid torus boundary strongly pseudoconvex for all 0<epsilon<1")
