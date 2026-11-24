"""Generate exact degree-five moment Taylor jet for the n7 critical candidate."""
from sage.all import *
import pickle
R=PowerSeriesRing(QQ,names=['z'+str(i) for i in range(6)],default_prec=6);z=R.gens()
base=[QQ(1),QQ(1)/10,QQ(51)/100,QQ(51)/1000,QQ(5051)/10000,QQ(5051)/100000,QQ(515051)/1000000]
def step(ms):
 m=list(ms)
 for j in range(7,13):m.append(QQ(201)/100*m[j-2]-QQ(51)/50*m[j-4]+QQ(1)/50*m[j-6])
 M=matrix(R,[[m[i+j] for j in range(3)] for i in range(3)])
 Mi=M.adjugate()*(1/M.det());c=-Mi*vector(R,m[3:6]);qp=list(c)+[R(1)]
 coeff=[sum(qp[i]*qp[j] for i in range(4) for j in range(4) if i+j==k) for k in range(7)]
 numer=[sum(coeff[j]*m[k+j] for j in range(7)) for k in range(7)];F=numer[0]
 return [v/F for v in numer],qp,F
m=[R(base[0])]+[R(base[j+1])+z[j] for j in range(6)]
mp,p,F=step(m);mpp,q,Fp=step(mp)
G=[(mpp[j+1]-base[j+1]).truncate(6) for j in range(6)]
for j in range(6):assert G[j].constant_coefficient()==0
with open('workspace/agent3_n7_jet5.pkl','wb') as f:pickle.dump(dict(R=R,G=G,base=base,p=p,q=q,F=F,Fp=Fp),f)
print('Exact degree5 jet saved; monomial counts:',[len(g.monomials()) for g in G])
