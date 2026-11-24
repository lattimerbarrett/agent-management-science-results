import sympy as s
from pathlib import Path
e=s.symbols('e',integer=True,nonnegative=True)
b1,b2=s.symbols('b1 b2',integer=True)
N=45*e+18
bsum=-33*e-14
# ch(O(2S+bf))=1+(2S+bf)+(-2e+2b)[pt].
c1f=(4,b1+b2)
ch2f=-4*e+2*(b1+b2)
c1e=(4,s.expand(bsum+N))
ch2e=s.expand(ch2f.subs(b2,bsum-b1)+N)
c1square=-16*e+8*c1e[1]
c2=s.expand(c1square/2-ch2e)
assert c1e==(4,12*e+4)
assert ch2e==-25*e-10
assert c2==65*e+26
# Local freeness of the fibre extension follows two linear forms have no common zero.
a,b,c,d,x,y=s.symbols('a b c d x y')
f=a*x+b*y;g=c*x+d*y
res=s.resultant(f.subs(y,1),g.subs(y,1),x)
assert s.expand(res-(a*d-b*c))==0
print('Hecke Chern checks passed:',c1e,ch2e,c2)
