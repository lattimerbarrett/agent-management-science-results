from fractions import Fraction
from sage.all import matrix,QQ
import json,sys,math
s=open('workspace/agent2_fz.py').read().split('base={}; pivots=[]')[0]
s=s.replace('k0=48','k0=46').replace('range(1,11)','range(1,D+1)').replace('range(9,13)','range(1,D+1)').replace('3*r-26+1','3*r-25+1').replace('(size-r)%2','(24-r-size-1)%2')
s=s.replace('def inv(x):return pow(x,P-2,P)','def inv(x):return Fraction(1,x)').replace('pow(-logA[n],j,P)','(-logA[n])**j').replace('%P','')
S={'Fraction':Fraction};exec(s,S)
R=matrix(QQ,S['rows']);piv=R.pivots();mons=[m for i,m in enumerate(S['cols']) if i not in piv]
print('Genus24 survivors',len(mons))
sys.path.insert(0,'workspace');import agent3_lower as L
from functools import lru_cache
@lru_cache(None)
def I(mu):
 n=len(mu);return sum((-1)**(n-k)*math.factorial(45+k)*v for k,v in enumerate(L.exact_bell(mu)))
A=matrix(QQ,[[I(tuple(sorted(a+b,reverse=True))) for b in L.partitions(10)] for a in mons])
K=A.left_kernel();assert K.dimension()==1
v=K.basis()[0]
json.dump({'monomials':mons,'coefficients':list(map(str,v))},open('workspace/agent3_radical_g24.json','w'))
print('Genus24 radical saved; nonzero coefficients',sum(bool(x) for x in v))
