import json,mpmath as m
from pathlib import Path
m.mp.dps=80;D0=json.loads(Path('workspace/general_constant_counter_agent4.json').read_text());aa=m.matrix(D0['aa']);az=m.matrix(D0['az']);w=list(map(m.mpf,D0['w']));w=[t/sum(w) for t in w];Q=list(map(m.mpf,D0['Q']));mean=sum(wi*qi for wi,qi in zip(w,Q));Q=[qi-mean for qi in Q];norm=m.sqrt(sum(wi*qi*qi for wi,qi in zip(w,Q)));Q=[qi/norm for qi in Q];DD=list(map(m.mpf,D0['D']));v=m.matrix(D0['v'])
for i in range(len(w)):aa[i,0]=1;aa[i,1]=Q[i];aa[i,2]=1/Q[i]
for i in range(len(DD)):az[i,0]=1;az[i,1]=DD[i];az[i,2]=-1/DD[i]
G=aa.T*m.diag(w)*aa;H=aa.T*m.diag([w[i]*Q[i]**2 for i in range(len(w))])*aa;KG=az*G**-1*az.T;KH=az*H**-1*az.T;C=m.diag([1/t for t in DD])*KG*m.diag(DD)+m.diag(DD)*KH*m.diag(DD);out=C*v
print('meanQ',sum(wi*qi for wi,qi in zip(w,Q)),'normQ²',sum(wi*qi*qi for wi,qi in zip(w,Q)));print('maxCv',m.nstr(max(out),30));print('Cv',list(map(lambda t:m.nstr(t,18),out)));assert max(out)<0
