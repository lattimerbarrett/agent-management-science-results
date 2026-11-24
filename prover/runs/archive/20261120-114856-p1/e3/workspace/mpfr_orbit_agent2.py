import gmpy2 as g, numpy as np,pickle,time,os
from pathlib import Path
g.get_context().precision=384;g.get_context().emin=-1000000000;g.get_context().emax=1000000000
D=np.load('workspace/subset_best_agent2.npz');pars=D['pars'];base=D['logw0'];lam0=D['lam'];inds=[0,1,2,3,5,6]
M=lambda x:g.mpfr(str(x))
a,L,H=map(M,pars);zero=M(0);one=M(1)
def Q(x):return x*(x-one)*(x-a)*(x-L)
def dQ(x):return (x-one)*(x-a)*(x-L)+x*(x-a)*(x-L)+x*(x-one)*(x-L)+x*(x-one)*(x-a)
lam=[]
for j in inds:
 x=M(lam0[j]);sg=1 if j<4 else-1
 for _ in range(20):x-= (Q(x)-sg*H)/dQ(x)
 lam.append(x)
w=[g.exp(M(base[j]))for j in inds];ss=sum(w);w=[x/ss for x in w]
l2=[x*x for x in lam];l3=[x*x*x for x in lam];ml=one-lam[2];mr=one-lam[1]
def T(w):
 m=sum(v*x for v,x in zip(w,lam));m2=sum(v*x for v,x in zip(w,l2));m3=sum(v*x for v,x in zip(w,l3));aa=(m*m2-m3)/(m2-m*m);bb=-m2-aa*m
 qs=[x2+aa*x+bb for x,x2 in zip(lam,l2)];ww=[v*q*q for v,q in zip(w,qs)];hh=sum(ww);return [v/hh for v in ww],m,hh
statefile='workspace/mpfr384_orbit_agent2.pkl'
if os.path.exists(statefile):
 dat=pickle.load(open(statefile,'rb'));w=dat['w'];k0=dat['k'];visits=dat['visits'];side=dat['side'];hist=dat['hist'];prevH=dat['Hlast']
else:k0=0;visits=[];side=0;hist=[];prevH=zero
start=time.time();N=2000000
for k in range(k0,k0+N):
 w,m,hh=T(w);w,_,_=T(w)
 if hh<prevH*(one-M('1e-80')):raise Exception(('H DECREASE',k,hh,prevH))
 prevH=hh
 if k%10==0:
  ns=-1 if m<ml+(mr-ml)/10 else(1 if m>ml+9*(mr-ml)/10 else 0)
  if ns and ns!=side:
   side=ns;visits.append((k,float(m),float(hh/H),float(g.log(abs(H-hh)))))
   print('VISIT',len(visits),k,'normmean',float((m-ml)/(mr-ml)),'Hratio',g.digits(hh/H,10,30),flush=True)
 if k%1000==0:hist.append((k,float(m),str(hh/H),*[float(g.log(v))for v in w]))
 if k%100000==0:
  print('iter',k,'time',time.time()-start,flush=True)
  pickle.dump(dict(w=w,k=k+1,visits=visits,side=side,hist=hist,Hlast=hh,lam=lam,pars=(a,L,H)),open(statefile,'wb'))
pickle.dump(dict(w=w,k=k0+N,visits=visits,side=side,hist=hist,Hlast=hh,lam=lam,pars=(a,L,H)),open(statefile,'wb'))
Path('workspace/mpfr_orbit_agent2.py').write_text(Path(__file__).read_text())
