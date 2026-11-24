from sage.all import *
import json,pickle,time
q=json.load(open('workspace/agent3_fz25.json'));p=json.load(open('workspace/pairing25_agent2.json'))
M=matrix(QQ,pickle.load(open('workspace/agent2_exact_pairing.pkl','rb')))
F=matrix(QQ,[[QQ(x) for x in row] for row in q['rows']])
K=M.left_kernel().basis_matrix();print('F rank',F.rank(),'kernel',K.nrows())
W=F.row_space()
v=next(v for v in K if v not in W)
E=F.echelon_form();v=vector(QQ,v)
for row in E:
 if row:
  j=next(j for j,x in enumerate(row) if x)
  v-=v[j]/row[j]*row
assert not v.is_zero() and v*M==0
z=vector(ZZ,v.denominator()*v);z=z/gcd(list(z));z=vector(ZZ,z)
if next(x for x in z if x)<0:z=-z
print('support',sum(bool(x) for x in z),'max digits',max(len(str(abs(x))) for x in z))
for i,x in enumerate(z):
 if x:print(tuple(q['columns'][i]),x)
json.dump({'monomials':q['columns'],'coefficients':[str(x) for x in z]},open('workspace/agent2_anomaly25.json','w'))
print('verified anomaly nonzero modulo FZ, zero against all degree11 monomials')
for bound in range(2,9):
 ids=[i for i,part in enumerate(q['columns']) if max(part)<=bound]
 S=M.matrix_from_rows(ids);KS=S.left_kernel().basis_matrix();found=[]
 for u in KS:
  full=vector(QQ,77)
  for i,x in zip(ids,u):full[i]=x
  if full not in W:found.append(full)
 print('maxpart',bound,'variables',len(ids),'nullity',KS.nrows(),'anomaly found',bool(found))
 if found:
  vv=found[0];zz=vector(ZZ,vv.denominator()*vv);zz=vector(ZZ,zz/gcd(list(zz)))
  json.dump({'monomials':q['columns'],'coefficients':[str(x) for x in zz]},open('workspace/agent2_anomaly25_maxpart'+str(bound)+'.json','w'))
  if bound==5:
   Z=matrix(ZZ,[list(v.denominator()*v) for v in KS]).LLL()
   for zv in Z:
    full=vector(QQ,77)
    for i,x in zip(ids,zv):full[i]=x
    if full not in W:
     zz=vector(ZZ,full);zz=vector(ZZ,zz/gcd(list(zz)))
     print('LLL representative support',sum(bool(x) for x in zz),'maxdigits',max(len(str(abs(x))) for x in zz))
     json.dump({'monomials':q['columns'],'coefficients':[str(x) for x in zz]},open('workspace/agent2_anomaly25_small.json','w'))
     break
from pathlib import Path
if Path(__file__).name=='scratchpad.py':Path('workspace/agent2_anomaly25.py').write_text(Path(__file__).read_text())
