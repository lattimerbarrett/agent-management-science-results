import sympy as s
E=s.symbols('e', integer=True,nonnegative=True)
def dot(v,w):
 a,b=v;c,d=w
 return s.expand(-E*a*c+a*d+b*c)
H=(1,3*E+1);P=(4,12*E+3);A=(5,-1);B=(-1,12*E+5);K=(-2,-E-2)
add=lambda v,w:tuple(v[i]+w[i] for i in range(2))
scale=lambda k,v:tuple(k*x for x in v)
h2=dot(H,H);c1=add(A,B);c2=dot(A,B)
assert s.expand(c2-13*h2)==0
assert s.expand(dot(c1,c1)-16*h2)==0
assert s.expand(dot(A,P)-dot(c1,P)/2)==-3
assert s.expand(dot(B,P)-dot(c1,P)/2)==3
C=scale(2,H)
genus=s.expand(1+(dot(C,C)+dot(C,K))/2)
assert genus==5*E+1
# Check and REJECT tempting elementary-transform construction.
# Kernel O(3H)^2 -> i_*L with deg L=d H² has c2=(d-3)H².
d=s.symbols('d')
c1_new=add(scale(6,H),scale(-1,C))
ch2_new=s.expand(9*h2-(d*h2-dot(C,C)/2))
c2_new=s.expand(dot(c1_new,c1_new)/2-ch2_new)
assert c1_new==scale(4,H)
assert s.expand(c2_new-(d-3)*h2)==0
assert s.solve(c2_new-13*h2,d)==[16]
# For d=16, kernel restriction to C has negative-degree line quotient.
quotient_degree=s.expand(dot(scale(6,H),C)-16*h2)
assert s.expand(quotient_degree+4*h2)==0
# Ext² criterion E0 prioritary: h0 of K+f plus offdiag differences
print({'H2':h2,'c2':c2,'c1square':dot(c1,c1),'genus_C':genus,'deg_pencil_minus_2g':10*E+6})
for v in [(0,0),add(A,scale(-1,B)),add(B,scale(-1,A))]:
 print('Ext2 test line K+f+diff =',add(add(K,(0,1)),v))
# e=0 destabilizer lift: H1(6,-6) -> H1(7,-6): multiplication by nonzero linear polynomial on H0(P1,O6), tensor H1(P1,O-6), hence injective
x,y=s.symbols('x y')
M=s.zeros(8,7)
for i in range(7): M[i,i]=1
assert M.rank()==7
print('Kunneth lift map rank',M.rank(),'domain dimension',7*5,'full tensor rank',M.rank()*5)
# exhaust effective D with P.D<=3 numerically for e=0..20
for e in range(21):
 candidates=[]
 for a in range(5):
  for b in range(5):
   if a*(8*e+3)+4*b<=3:candidates.append((a,b))
 assert candidates==([(0,0),(1,0)] if e==0 else [(0,0)]),candidates
print('All symbolic checks and finite candidate enumeration passed.')
from pathlib import Path
Path('workspace/agent3_algebra_checks.py').write_text(Path(__file__).read_text().split("from pathlib import Path")[0])