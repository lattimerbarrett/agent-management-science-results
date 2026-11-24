import sympy as s
u,v,a,b=s.symbols('u v a b', real=True)
h=s.sqrt(1-a*a)*s.cos(u+v)-s.sqrt(1-b*b)*s.cos(u-v)
coords=[u,v,a,b]
H=s.hessian(h,coords)
print('Hessian at left endpoint:')
print(H.subs({u:0,v:0,a:0,b:0}))
print('Hessian at right endpoint:')
print(H.subs({u:s.pi,v:0,a:0,b:0}))
print('Transverse Hessian on regular arc:')
print(s.hessian(h,[a,b]).subs({a:0,b:0,v:0}))
print('Coefficient of v along arc:',s.diff(h,v).subs({a:0,b:0,v:0}))
