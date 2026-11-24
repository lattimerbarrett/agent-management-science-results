import sympy as s
p,q,w,ws=s.symbols('p q w ws', commutative=False)
one=s.Integer(1)
relations={ws*w:p,w*ws:q,p*p:p,p*w:w,w*p:w,p*ws:ws,ws*p:ws}
def reduce(expr):
    old=None
    while expr != old:
        old=expr
        expr=s.expand(expr).subs(relations, simultaneous=True)
    return s.expand(expr)
v=one-p+w
vs=one-p+ws
print('v* v =',reduce(vs*v))
print('v v* =',reduce(v*vs))
assert reduce(vs*v)==1
assert s.expand(reduce(v*vs)-(1-p+q))==0
print('Thus a proper isometry in a projection corner extends to a proper isometry of the unit.')
print('The finiteness definition in the question therefore implies finiteness of every projection.')
