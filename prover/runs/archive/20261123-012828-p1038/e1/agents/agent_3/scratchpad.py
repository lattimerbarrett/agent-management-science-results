import sympy as s
x,y,u,v,p,q=s.symbols('x y u v p q',nonzero=True)
a=x*(y*y+1)/(y*(x*x+1));b=(y*y-x*x)/(y*(x*x+1))
def trans(u,v):
 U=s.factor((v-a*u-b)/(a*v/u-1-b*v));return U,s.factor(v/u*U)
U,V=trans(u,v);P,Q=trans(p,q)
D=s.factor((Q-V)/(1+U*P)-(q-v)/(a*(1+u*p)))
print('D',D)
J=lambda t:t-1/t
curve=s.factor((J(u)-J(x))*(J(q)-J(y))-(J(p)-J(x))*(J(v)-J(y)))
print('ratio',s.factor(D/curve))
