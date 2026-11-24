import pickle,time
from sage.all import matrix,QQ,GF,vector
from fractions import Fraction
P,labs,sol,ri,ci=pickle.load(open('workspace/agent1_coupled_small_solution.pkl','rb'))
labsQ,rows,total=pickle.load(open('workspace/agent3_coupled_exact_sparse.pkl','rb'))
assert labs==labsQ
support=[i for i in ri if sol[i]%P]
print('support',len(support),'selected rows',len(ri),'columns',len(ci),'prime',P,flush=True)
q=support[-1]; rest=[i for i in support if i!=q]
# Reuse selected constraint columns, remove functional column; choose independent ones if coefficients vanished.
cc=[j for j in ci if j<total]
t=time.time()
if len(cc)!=len(rest):
 Z=matrix(GF(P),[[rows[i].get(j,0) for j in cc] for i in rest]);piv=Z.pivots();cc=[cc[j] for j in piv]
assert len(cc)==len(rest)
print('Building QQ square minor size',len(rest),'time',time.time()-t,flush=True)
A=matrix(QQ,[[rows[i].get(j,0) for j in cc] for i in rest]);b=vector(QQ,[rows[q].get(j,0) for j in cc])
print('Minor built; solving transpose at',time.time()-t,flush=True)
x=A.transpose().solve_right(b)
print('QQ solve complete at',time.time()-t,flush=True)
coeff={q:QQ(1)}
for i,c in zip(rest,x):
 if c:coeff[i]=-c
# All 1908 columns must vanish EXACTLY, not just selected minor.
M=matrix(QQ,[[rows[i].get(j,0) for j in range(total)] for i in coeff])
v=vector(QQ,list(coeff.values()))
assert not any(v*M)
print('ALL',total,'exact column identities VERIFIED at',time.time()-t,flush=True)
# Check residue against modular witness and functional.
P0,labs0,modrows,fl=pickle.load(open('workspace/agent1_coupled_small_matrix.pkl','rb'))
assert P0==P and labs0==labs
val=sum((int(c.numerator())*pow(int(c.denominator()),P-2,P)%P)*fl[i] for i,c in coeff.items())%P
assert val
print('Functional nonzero residue',val,'prime',P,flush=True)
print('max coefficient digits',max(len(str(c)) for c in coeff.values()),flush=True)
pickle.dump({'prime':P,'coefficients':coeff,'nonzero_residue':val,'q':q,'rows':list(coeff),'columns':cc},open('workspace/agent3_exact_dual_witness.pkl','wb'))
import json
json.dump({'prime':P,'coefficients':[[i,str(c)] for i,c in coeff.items()],'nonzero_residue':int(val),'q':q,'columns':cc},open('workspace/agent3_exact_dual_witness.json','w'))
src=open(__file__).read();open('workspace/agent3_lift.py','w').write(src)
