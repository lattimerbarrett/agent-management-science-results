import sympy as s
x,y,t=s.symbols('x y t', real=True)
# Levi signature of the compact quartic family mentioned by the other solvers.
# At z_1=0, |z'|^2=3, the complex tangent excludes one z' direction.
for n in range(2,7):
 tangent_levi=[-2]+[1]*(n-2)
 print(n, tangent_levi)
