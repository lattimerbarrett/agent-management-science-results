import sympy as s
T,c,x0,x1,y0,y1=s.symbols('T c x0 x1 y0 y1')
P=[(1-x0*T)*(1-y0*T),T*(1-x1*T)*(1-y1*T),(1-c*T)*(T+x0)*(T+x1),(T+c)*(T+y0)*(T+y1)]
M=s.Matrix([[s.expand(p).coeff(T,j) for j in range(4)] for p in P])
D=s.expand(M.det())
print('D=',D)
base=(1+c*c)*(1+x0*y0)**2*(1+x1*y1)**2
print('residual factor=',s.factor(D-base))
# Exact geometric divided-difference relation.
r,R,d,xi,xj,yi,yj=s.symbols('r R d xi xj yi yj',positive=True)
F=lambda z:z-1/z
E=lambda x,y:r*F(x)-R*F(y)-2*d
Delta=(yj-yi)*(1+1/(yi*yj))-(r/R)*(xj-xi)*(1+1/(xi*xj))
print('difference identity residual:',s.factor(Delta+(E(xj,yj)-E(xi,yi))/R))
# Under y between x and c, this factor is nonnegative.
x,y,U,V=s.symbols('x y U V')
print('confluent positive factor:',(y-c)*(x-y)*(1+c*x))
