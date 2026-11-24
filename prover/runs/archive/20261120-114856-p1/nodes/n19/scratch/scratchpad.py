import sympy as S
x=S.symbols('x');lam=[1,2,4];w=[S.Rational(1,6),S.Rational(2,6),S.Rational(3,6)]
def step(w):
 M=S.Matrix([[sum(wi*t**(i+j) for wi,t in zip(w,lam)) for j in range(2)] for i in range(2)])
 c=M.inv()*-S.Matrix([sum(wi*t**(i+2) for wi,t in zip(w,lam)) for i in range(2)])
 p=x*x+c[1]*x+c[0];h=sum(wi*p.subs(x,t)**2 for wi,t in zip(w,lam));ww=[wi*p.subs(x,t)**2/h for wi,t in zip(w,lam)]
 return p,h,ww
p,h,ww=step(w);q,_,_=step(ww)
print(p,q,h,S.factor(p*q-h));print('p',S.nroots(p),'q',S.nroots(q))
