import numpy as np,itertools
from scipy.integrate import solve_ivp
from scipy.special import expit
from pathlib import Path
Pbase=np.array([1.,-10.,26.,-4.,-5.]);crit=np.sort(np.roots(np.polyder(Pbase)).real);cc=crit[-1];H=-np.polyval(Pbase,cc);delta=H/np.sqrt(2);Corig=H*H/2
pa=Pbase.copy();pa[-1]-=H;pb=Pbase.copy();pb[-1]+=H;quo,rem=np.polydiv(pb,np.poly([cc,cc]));act_orig=np.sort(np.r_[np.roots(pa).real,np.roots(quo).real,cc]);mus_orig=np.sort(np.roots(Pbase).real)
rp=Pbase.copy();rp[-1]-=delta;rm=Pbase.copy();rm[-1]+=delta;rrplus=np.sort(np.roots(rp).real);rrminus=np.sort(np.roots(rm).real)
shift=2.5;sc=3.5;active=(act_orig-shift)/sc;allmu=(mus_orig-shift)/sc;C=Corig/sc**8;s=4;na=7;V=active[:,None]**np.arange(4);Dp=np.array([np.prod(a-np.delete(active,i)) for i,a in enumerate(active)])
print('GEOMETRY H',H,'active',active,'minus',allmu,flush=True)
rng=np.random.default_rng(782);bestcross=-1;longest=0
for bits in [(0,0,0,0),(0,0,0,1),(0,1,0,1),(0,1,1,0)]:
 rootsP=np.where(np.array(bits)==0,rrplus,rrminus);rootsQ=np.where(np.array(bits)==0,rrminus,rrplus);pco=np.poly((rootsP-shift)/sc);qco=np.poly((rootsQ-shift)/sc);p=np.polyval(pco,active);q=np.polyval(qco,active)
 pgaps=[sum((rootsP>act_orig[j])&(rootsP<act_orig[j+1])) for j in range(6)];gapids=np.flatnonzero(np.array(pgaps)==0)
 if len(gapids)!=2:print('BADGAPS',bits,pgaps);continue
 gaps=np.c_[active[gapids],active[gapids+1]];const=C/(Dp*p)
 def chart(u):
  sg=expit(u);dt=(gaps[:,1]-gaps[:,0])*sg*(1-sg);tt=gaps[:,0]+(gaps[:,1]-gaps[:,0])*sg;fac=active[:,None]-tt[None,:];B=np.empty((7,2))
  for j in range(2):
   fac[gapids[j],j]=-(gaps[j,1]-gaps[j,0])*sg[j];fac[gapids[j]+1,j]=(gaps[j,1]-gaps[j,0])*(1-sg[j]);B[:,j]=-dt[j]/fac[:,j];B[gapids[j],j]=1-sg[j];B[gapids[j]+1,j]=-sg[j]
  w=const*np.prod(fac,axis=1);return tt,w,B
 _,wref,_=chart(np.zeros(2));print('branch',bits,'gaps',gaps,'wmin',min(wref),'ortherr',np.max(abs(V.T@(wref*p))),flush=True)
 if min(wref)<0:continue
 S=V.T@((wref*p*p)[:,None]*V);ee,UU=np.linalg.eigh(S);invS=UU@np.diag(1/np.sqrt(ee))@UU.T
 for missing in range(4):
  mus=np.delete(allmu,missing);VM=mus[:,None]**np.arange(4);pm=np.polyval(pco,mus);qm=np.polyval(qco,mus)
  def calc(z):
   tt,w,B=chart(z[:2]);hc=z[2:6];A=z[6:];h=V@hc;u=w*p*h;M=V.T@(w[:,None]*V);zz=w*p*p/C;N=V.T@(zz[:,None]*V);ac=-C*np.linalg.solve(M,N@hc);aa=V@ac;F=np.dot(u,p*p);rat=2*(aa/p+C*h/q-F/C);b=w*rat;ud=np.linalg.lstsq(B,rat,rcond=None)[0]
   bb=-V@np.linalg.solve(M,V.T@(u*aa));e=np.dot(u,p*aa);z1=(u*p*p+2*w*p*aa-zz*F)/C;z2=(w*(aa*aa+2*p*bb)+2*u*p*aa-z1*F-zz*e)/C
   aaa=C*h;bbb=-V@np.linalg.solve(N,V.T@(z2*q+z1*aaa));eee=np.dot(z2,q*q)+np.dot(z1,q*aaa);f2=(z2*q*q+2*z1*q*aaa+zz*(aaa*aaa+2*q*bbb)-(u+b)*F-w*eee)/C
   hd=np.linalg.solve(C*N,V.T@(p*(f2-b*p*h)));hd+=np.linalg.solve(N,VM.T@(4*pm/C*A*A));ad=A*(-(pm*(C*(VM@hc))+qm*(VM@ac)+F)/C)
   r=(hc@S@hd+A@ad)/(hc@S@hc+A@A);return np.r_[ud,hd-r*hc,ad-r*A],-F/C
  def flow(t,z):return calc(z)[0]
  def ef(t,z):return calc(z)[1]
  ef.terminal=True;ef.direction=-1
  def eu(t,z):return 25-max(abs(z[:2]))
  eu.terminal=True;eu.direction=-1
  for j in range(25):
   h=invS@rng.normal(size=4);aa=10**rng.uniform(-4,0,size=3);z0=np.r_[np.zeros(2),h,aa]
   if calc(z0)[1]<0:z0[2:6]*=-1
   z0[2:]/=np.sqrt(z0[2:6]@S@z0[2:6]+aa@aa)
   try:sol=solve_ivp(flow,[0,100],z0,rtol=3e-6,atol=3e-8,max_step=.2,events=[ef,eu])
   except np.linalg.LinAlgError:continue
   cross=max(np.sum(sol.y[i,1:]*sol.y[i,:-1]<0) for i in range(2))
   if cross>bestcross or sol.t[-1]>longest:
    bestcross=max(bestcross,cross);longest=max(longest,sol.t[-1]);print('BEST',bits,missing,j,'cross',cross,'T',sol.t[-1],'ranges',[(min(a),max(a)) for a in sol.y[:2]],'E',calc(sol.y[:,-1])[1],flush=True);np.savez('workspace/agent4_sevencritical_best.npz',bits=bits,missing=missing,z0=z0,t=sol.t,y=sol.y,active=active,mus=mus,p=p,q=q,C=C)
