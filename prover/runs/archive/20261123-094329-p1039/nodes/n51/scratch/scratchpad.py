import sympy as s
x,y,u,v,r=s.symbols('x y u v r', real=True)
norm2=x*x+y*y+u*u+v*v
sphere2=(x-1)**2+y*y+u*u+v*v
h=x-1
print('Identity |z|^2 - 1 - |z-q|^2 - 2h =',s.expand(norm2-1-sphere2-2*h))
print('On |z|<=1 and |z-q|=r, h <= -r^2/2.')
print('With c=-r^2/4, bound h-c <=',s.simplify(-r*r/2+r*r/4))
print('Thus max(h,c)=c near the artificial boundary; gluing to c is valid.')
