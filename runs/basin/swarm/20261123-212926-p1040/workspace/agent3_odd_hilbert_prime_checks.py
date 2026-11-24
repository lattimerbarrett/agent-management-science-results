import sys,time
sys.path.insert(0,'workspace')
from agent3_arithmetic_fields import data,X
import sympy as S
from pathlib import Path
for p in list(S.primerange(3,32)):
 _,ell,r,e,P=data(p)
 # Resultant reduce v modulo P first for efficiency.
 V=S.rem(1-X**(p-1)+X**(2*p-2),P.as_expr(),X)
 norm=int(S.resultant(P.as_expr(),V,X))
 print('p',p,'Norm(v)modp2',norm%(p*p),'Artinexponent',((norm-1)//p)%p,flush=True)
 assert (norm-1)%p==0 and ((norm-1)//p)%p!=0
