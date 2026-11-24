from sage.all import *
x=polygen(QQ)
for c,p in [(3,3),(5,5),(6,3),(9,3),(10,5),(12,3),(15,3)]:
 d=c//p; pol=sum((1+x**d)**j for j in range(p));K=NumberField(pol,'pi');pi=K.gen();zz=1+pi**d;a=1+pi;b=1+pi**(c-1)
 assert zz**p==1 and zz!=1
 fac={Q for Q,e in K.ideal(a).factor()}|{Q for Q,e in K.ideal(b).factor()}
 total=0;terms=[]
 for Q in fac:
  if Q.smallest_integer()==p:continue
  va=K.ideal(a).valuation(Q);vb=K.ideal(b).valuation(Q)
  unif=K.uniformizer(Q)
  F=K.residue_field(Q)
  aa=F(a/unif**va);bb=F(b/unif**vb)
  z=((-1)**(va*vb)*bb**va/aa**vb)**((F.cardinality()-1)//p)
  root=F(zz)
  js=[j for j in range(p) if root**j==z]
  assert len(js)==1,(c,p,Q,z,root)
  total+=js[0];terms.append((int(Q.norm()),js[0]))
 local=(-total)%p
 print(c,p,'odd Hilbert exponent=',local,'tame terms=',terms,flush=True)
 assert local!=0
from pathlib import Path
Path('workspace/agent2_odd_hilbert_checks.py').write_text(Path(__file__).read_text())
