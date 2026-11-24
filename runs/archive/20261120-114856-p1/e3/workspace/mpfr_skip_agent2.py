import gmpy2 as g,pickle,time,os,numpy as np
from pathlib import Path
g.get_context().precision=384;g.get_context().emin=g.get_emin_min();g.get_context().emax=g.get_emax_max()
old='workspace/mpfr384_orbit_agent2.pkl';save='workspace/mpfr_skip_agent2.pkl'
D=pickle.load(open(save if os.path.exists(save) else old,'rb'));w=D['w'];lam=D['lam'];a,L,H=D['pars'];k=D['k'];vis=D['visits'];side=D['side'];hist=D['hist'];M=lambda x:g.mpfr(str(x));one=M(1);zero=M(0);l2=[x*x for x in lam];l3=[x*x*x for x in lam];ml=one-lam[2];mr=one-lam[1]
def jac(w,dw=None):
 mu=[sum(v*x for v,x in zip(w,xx))for xx in[lam,l2,l3]];m,m2,m3=mu;var=m2-m*m;N=m*m2-m3;aa=N/var;bb=-m2-aa*m;pp=[x2+aa*x+bb for x,x2 in zip(lam,l2)];ww=[v*p*p for v,p in zip(w,pp)];hh=sum(ww);nw=[v/hh for v in ww]
 if dw is None:return nw,m,hh
 dm,dm2,dm3=[sum(v*x for v,x in zip(dw,xx))for xx in[lam,l2,l3]];dvar=dm2-2*m*dm;dN=dm*m2+m*dm2-dm3;da=(dN*var-N*dvar)/(var*var);db=-dm2-da*m-aa*dm;dh=sum(v*p*p for v,p in zip(dw,pp));ndw=[(v*p*p+2*ww0*p*(da*x+db))/hh-nv*dh/hh for v,ww0,p,x,nv in zip(dw,w,pp,lam,nw)]
 return nw,ndw
EPS=M('1e-35');start=time.time();exact=0;jumps=D.get('jumps',[]);maxvis=len(vis)+100
while exact<3000000 and len(vis)<maxvis:
 active=sorted(range(6),key=lambda i:w[i],reverse=True)[:3];missing=[i for i in range(6)if i not in active]
 if max(w[i]for i in missing)<EPS:
  mass=sum(w[i]for i in active);wa=[w[i]/mass if i in active else zero for i in range(6)];wa1,_,_=jac(wa)
  data=[];Nskip=None
  for j in missing:
   dw=[-v for v in wa];dw[j]=one;_,dw1=jac(wa,dw);_,dw2=jac(wa1,dw1);mult=dw2[j];bvec=[dw2[i]+mult*wa[i]for i in range(6)];lg=g.log(mult)
   data.append((j,mult,bvec,lg))
   if lg>0:
    ns=int(g.floor((g.log(EPS)-g.log(w[j]))/lg));Nskip=ns if Nskip is None else min(Nskip,ns)
  if Nskip is None:
   print('STABLE FACE all missingmultipliers<1 at',k,'vis',len(vis),flush=True);D['stable']=True;break
  if Nskip>20:
   neww=w.copy();an=wa.copy()
   for j,mult,bvec,lg in data:
    fac=g.exp(Nskip*lg);geom=g.expm1(Nskip*lg)/g.expm1(lg) if mult!=1 else M(Nskip)
    for i in active:an[i]+=w[j]*geom*bvec[i]
    neww[j]=w[j]*fac
   mmass=sum(neww[j]for j in missing)
   for i in active:neww[i]=an[i]*(one-mmass)
   w=neww;k+=Nskip;jumps.append((k,Nskip,[float(x[1])for x in data]));
   print('SKIP to',k,'N',Nskip,'vis',len(vis),flush=True)
   continue
 w,m,hh=jac(w);w,_,_=jac(w);k+=1;exact+=1
 if exact%10==0:
  ns=-1 if m<ml+(mr-ml)/10 else(1 if m>ml+9*(mr-ml)/10 else 0)
  if ns and ns!=side:
   side=ns;vis.append((k,float(m),float(hh/H),float(g.log(abs(H-hh)))))
   print('VISIT',len(vis),k,'Hratio',g.digits(hh/H,10,25),'time',time.time()-start,flush=True)
 if exact%10000==0:
  hist.append((k,float(m),str(hh/H),*[float(g.log(v))for v in w]));D.update(w=w,k=k,visits=vis,side=side,hist=hist,jumps=jumps);pickle.dump(D,open(save,'wb'))
D.update(w=w,k=k,visits=vis,side=side,hist=hist,jumps=jumps);pickle.dump(D,open(save,'wb'))
Path('workspace/mpfr_skip_agent2.py').write_text(Path(__file__).read_text())
