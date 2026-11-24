import json,mpmath as m,numpy as np
m.mp.dps=65;D=json.load(open('workspace/zpart_highdegree_agent3.json'));s=D['s'];a=m.mpf(D['a']);b=m.mpf(D['b']);B=m.mpf(D['B'])
def lev(t):return sorted(m.cos((m.acos(t)+2*m.pi*k)/s) for k in range(s))
u,v=(a+b+m.sqrt((a-b)**2+4*B*B))/2,(a+b-m.sqrt((a-b)**2+4*B*B))/2;lam=sorted(lev(u)+lev(v));nu,nl=(a+b+m.sqrt((a-b)**2-4*B*B))/2,(a+b-m.sqrt((a-b)**2-4*B*B))/2;z=sorted(lev(nu)+lev(nl));raw=lambda x:m.chebyt(s,x);Q=[(raw(t)-a)/B for t in lam];P=[1/x for x in Q];xi=[lam[2*j+1]+m.mpf(t)*(lam[2*j+2]-lam[2*j+1]) for j,t in enumerate(D['tt'])];pd=[s*m.sin(s*m.acos(t))/m.sqrt(1-t*t)*(2*raw(t)-a-b) for t in lam];w=[P[i]*m.fprod(t-r for r in xi)/pd[i] for i,t in enumerate(lam)];w=[x/sum(w) for x in w];assert min(w)>0
V=m.matrix([[m.chebyt(j,t) for j in range(s+1)] for t in lam]);Z=m.matrix([[m.chebyt(j,t) for j in range(s+1)] for t in z]);G=V.T*m.diag(w)*V;H=V.T*m.diag([w[i]*Q[i]**2 for i in range(2*s)])*V;d=[(raw(t)-a)/B for t in z];KG=Z*G**-1*Z.T;KH=Z*H**-1*Z.T;C=m.diag([1/x for x in d])*KG*m.diag(d)+m.diag(d)*KH*m.diag(d);N=m.matrix(2*s)
for i in range(2*s):
 for j in range(2*s):N[i,j]=max(0,-C[i,j])/C[i,i] if i!=j else 0
vec=m.matrix([1]*(2*s))
for it in range(500):
 vec=N*vec;vec/=max(vec)
rat=[(N*vec)[i]/vec[i] for i in range(2*s)];print('COLLATZ',m.nstr(min(rat),30),m.nstr(max(rat),30));assert min(rat)>1
# Check actualC semipositivity by double LP (not a proof).
from scipy.optimize import linprog
CC=np.array(C.tolist(),float);r=linprog(np.zeros(2*s),A_ub=-CC.T,b_ub=-np.ones(2*s),bounds=[(1e-8,None)]*(2*s),method='highs');print('semipositive LP',r.success)
