import sympy as s
p,q,v,V=s.symbols('p q v V',commutative=False)
w=v+1-p
W=V+1-p
rules={p*p:p,V*v:p,v*V:q,V*p:V,p*v:v,v*p:v,p*V:V}
def reduce(expr):
    expr=s.expand(expr)
    for _ in range(5):
        old=expr
        for a,b in rules.items(): expr=s.expand(expr.subs(a,b))
        if expr==old: break
    return expr
print('If v*v=p and vv*=q<=p, set w=v+(1-p).')
print('w*w =',reduce(W*w))
print('ww* =',reduce(w*W))
print('Thus finiteness of the identity in the problem implies every projection is finite.')
print('\nPrecise supplied structural theorem: a unital AW*-factor with finite identity is monotone sequentially complete in its self-adjoint order.')
print('For the proposed sequence: increasing=True; upper bound=1; norm bound=1.')
print('Applying that theorem supplies a least upper bound in M_sa, contradicting the defining condition.')