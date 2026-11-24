"""Exact certificate for rank7 P4 three-step composition (3,1,3).
Run agent3_ch313_reduce.py first to regenerate the additive incidence system.
The Groebner solve is over QQ (about one minute); no modular conclusions.
"""
import pickle,sympy as S,time
D=pickle.load(open('workspace/agent3_ch313_reduced.pkl','rb'))
us=D['vars']; b,a,c,d=us
es=[S.Poly(e,*us).clear_denoms()[1].as_expr() for e in D['equations']]
start=time.time()
gb=S.groebner(es,*reversed(us),order='grevlex',domain=S.QQ).fglm('lex')
print('Rational Groebner elapsed:',time.time()-start,flush=True)
sol=S.solve([p.as_expr() for p in gb.polys],us,dict=True)
expected={(-1,0,0,0),(1,-1,-S.Rational(1,2),-S.Rational(1,6)),(0,0,0,0),(0,-2,2,-S.Rational(4,3)),(0,-2,-2,-S.Rational(4,3)),(0,-4,0,S.Rational(16,3))}
assert {tuple(v[u] for u in us) for v in sol}==expected
for v in sol:assert all(S.expand(e.subs(v))==0 for e in es)
# Coordinate-power identities and finite grid certify all complex roots.
import itertools
vals=[sorted({v[u] for v in sol}) for u in us]
for u,vs in zip(us,vals):
 f=S.prod(u-v for v in vs)
 assert any(gb.reduce(S.expand(f**k))[1]==0 for k in range(1,9))
good=[]
for tup in itertools.product(*vals):
 v=dict(zip(us,tup))
 if all(S.expand(z.subs(v))==0 for z in es):good.append(tup)
assert set(good)==expected
# Explicit elimination certifies root list exhaustion independently of solve.
assert gb.reduce(b*(b-1)*(b+1))[1]==0
assert gb.reduce(b*(b+2*a+1))[1]==0
assert gb.reduce(b*(b+4*c+1))[1]==0
assert gb.reduce(3*b*b+3*b+2*a*(a+2)*(a+4))[1]==0
assert gb.reduce(11*b*b+11*b+8*a*a+32*a+8*c*c)[1]==0
print('Six exact numerical candidates; explicit b/a/c eliminants checked.')
# Fiber Chern numbers in exceptional finite-map case:
h,x=S.symbols('h x')
v=dict(zip(us,(0,-4,0,S.Rational(16,3))))
C=[S.expand(z.subs(v).subs(h,0)) for z in D['chern'][0][:4]]
assert C==[1,-4*x,8*x*x,0]
# c1 Hom(A,B)=4 equals c1(TP3)=4, but c2 differs.
assert S.binomial(4,1)==4 and S.binomial(4,2)==6!=8
print('Hard case: determinant differential degree0, but c2 target8 != c2 tangent6.')
