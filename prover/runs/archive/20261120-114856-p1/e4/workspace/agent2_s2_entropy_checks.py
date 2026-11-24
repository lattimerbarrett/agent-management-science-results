import sympy as S
from pathlib import Path
a,b,c,d,u,v,z=S.symbols('a b c d u v z')
nodes=[a,b,c,d]
L=[S.prod((z-nodes[j])/(nodes[i]-nodes[j]) for j in range(4) if j!=i) for i in range(4)]
A=L[2].subs(z,v);B=-L[2].subs(z,u)
cs=[S.factor(A*li.subs(z,u)+B*li.subs(z,v)) for li in L]
assert cs[2]==0
print('c0=',cs[0]);print('c1=',cs[1]);print('c3=',cs[3])
# Linear terms of the external-log identity cancel by interpolation.
co=S.symbols('g0:4');g=sum(co[j]*z**j for j in range(4))
assert S.factor(sum(li.subs(z,u)*g.subs(z,nd) for li,nd in zip(L,nodes))-g.subs(z,u))==0
# Rational witness positivity and exact interpolation for all cubic monomials.
vals={a:-3,b:-1,c:1,d:3,u:-2,v:2}
assert A.subs(vals)>0 and B.subs(vals)>0
assert all(ci.subs(vals)>=0 for ci in cs)
for j in range(4): assert S.factor(sum(cs[i]*nodes[i]**j for i in range(4))-A*u**j-B*v**j)==0
print('s2 entropy-cone/interpolation certificates: PASS')

# Single-negative-contact facet signs, certified symbolically using positive gaps.
g1,g2,g3,g4=S.symbols('g1 g2 g3 g4',positive=True)
left={a:0,u:g1,b:g1+g2,c:g1+g2+g3,d:g1+g2+g3+g4}
ls=[S.factor(li.subs(z,u).subs(left,simultaneous=True)) for li in L]
assert all(ls[j].is_positive for j in [0,1,3]) and (-ls[2]).is_positive
# Reflection exchanges the negative coefficient index 2 with index 1.
right={a:0,b:g1,c:g1+g2,u:g1+g2+g3,d:g1+g2+g3+g4}
rs=[S.factor(li.subs(z,u).subs(right,simultaneous=True)) for li in L]
assert all(rs[j].is_positive for j in [0,2,3]) and (-rs[1]).is_positive
# Generic R_next=R+R^2 A cancellation used by the exponential perturbation proof.
H,C0,R,zz,trace,const=S.symbols('H C0 R zz trace const')
Q=lambda t:t*t-trace*t+const
hp=H+R*R*C0
Rdiff=S.factor(R*C0*(Q(zz-R)/H-Q(zz)/hp))
Aval=-C0*(2*zz-R-trace)/H+Q(zz)*R*C0*C0/(H*hp)
assert S.factor(Rdiff-R*R*Aval)==0
print('Single-contact facet signs and generic quadratic residue drift: PASS')
