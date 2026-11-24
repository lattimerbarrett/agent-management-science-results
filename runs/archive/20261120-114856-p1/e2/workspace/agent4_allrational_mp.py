import mpmath as mp,pickle,json
from pathlib import Path
mp.mp.dps=65
co=json.load(open('workspace/agent4_allrational_coeffs.json'))
def rational_mp(z):
 a=z.split('/');return mp.mpf(a[0])/(mp.mpf(a[1]) if len(a)>1 else 1)
pc=[rational_mp(z) for z in co['pc']];qc=[rational_mp(z) for z in co['qc']];h=mp.mpf(1)/15000
chi=lambda x:mp.polyval(pc,x)*mp.polyval(qc,x)-h
core6=[mp.findroot(chi,z) for z in [-1,mp.mpf('-.94'),mp.mpf('-.70'),mp.mpf('.47'),mp.mpf('.71'),1]]
extra=[mp.findroot(lambda z:chi(z)+2*h,z) for z in [mp.mpf('-.9421'),mp.mpf('.71048')]]
p=lambda x:mp.polyval(pc,x);q=lambda x:mp.polyval(qc,x);core=[z for i,z in enumerate(core6) if i!=4];left=core6[1];right=core6[2]
X=mp.matrix([[1,z,z*z] for z in core]);aa=[1/mp.fprod(z-y for y in core if y!=z) for z in core];pp=mp.matrix([p(z) for z in core]);qq=mp.matrix([q(z) for z in core]);wt=mp.matrix([-aa[i]*qq[i] for i in range(5)])
def data(t):
 w=mp.matrix([aa[i]*qq[i]*(core[i]-t) for i in range(5)]);H=X.T*mp.diag(w)*X;Hp=X.T*mp.diag([w[i]*pp[i]**2/h for i in range(5)])*X;Bmap=-Hp**-1*H;ER=mp.matrix([[sum(w[i]*X[i,j]*(pp[i]-qq[i]) for i in range(5)) for j in range(3)]])
 RC=mp.diag(qq)*X+mp.diag(pp)*X*Bmap+mp.ones(5,1)*ER
 VR=2*w[0]/h/wt[0]*RC[0,:]
 return w,H,Bmap,ER,VR
ell=data((left+right)/2)[4];ell/=mp.sqrt(sum(z*z for z in ell))
def bv(t):
 w,H,_,_,vr=data(t);cv=H**-1*X.T*mp.matrix([wt[i]**2/w[i]*pp[i]/4 for i in range(5)]);return -cv*sum(vr[j]*ell[j] for j in range(3))
sf=lambda t:mp.sqrt(q(t)/p(t)/(q(left)/p(left)))
u=mp.matrix([mp.quad(lambda t:bv(t)[j]*sf(t),[left,(2*left+right)/3,(left+2*right)/3,right]) for j in range(3)])
U=mp.eye(3)+u*ell
print('ell',mp.nstr(ell,25));print('U',mp.nstr(U,25));print('detcheck',mp.nstr(mp.det(U)-abs(p(left)/p(right)),15),flush=True)
def end(t):
 w,H,Bmap,E,vr=data(t);DD=[];FF=[];SS=[]
 for z in extra:
  lx=mp.matrix([[1,z,z*z]]);R=q(z)*lx+p(z)*lx*Bmap+E;D=(4*E-2*R)/h;F=4*p(z)*H**-1*lx.T;DD.append(D);FF.append(F);SS.append(mp.eye(3)-2*F*D/(D*F)[0])
 return E,DD,FF,SS
EL,DL,FL,SL=end(left);ER,DR,FR,SR=end(right);C=SL[1]*SL[0]*U**-1*SR[1]*U;ev,evec=mp.eig(C)
print('extra',[mp.nstr(x,45) for x in extra]);print('eig',[mp.nstr(x,45) for x in ev],flush=True)
for j,rr in enumerate(ev):
 if abs(mp.im(rr))>mp.mpf('1e-45') or not(0<mp.re(rr)<.1):continue
 a=evec[:,j];a=a/(EL*a)[0];ar=U*a;aro=SR[1]*ar;al=U**-1*aro;al0=SL[0]*al;af=SL[1]*al0
 print('a',[mp.nstr(x,45) for x in a]);print('energies',*[mp.nstr(z,35) for z in [ER*ar,ER*aro,EL*al,EL*al0,EL*af]]);print('right growth',*[mp.nstr(z,35) for z in [DR[0]*ar,DR[1]*ar,DR[0]*aro,DR[1]*aro]]);print('left growth',*[mp.nstr(z,35) for z in [DL[0]*al,DL[1]*al,DL[0]*al0,DL[1]*al0,DL[0]*af,DL[1]*af]],flush=True)
 def convert(v):
  if isinstance(v,mp.matrix):return [[mp.nstr(v[i,j],65) for j in range(v.cols)] for i in range(v.rows)]
  if isinstance(v,list):return [convert(z) for z in v]
  return mp.nstr(v,65)
 with open('workspace/agent4_allrational_mp.json','w') as out:json.dump({k:convert(v) for k,v in dict(core6=core6,h=h,extra=extra,pc=pc,qc=qc,U=U,EL=EL,ER=ER,DL=DL,DR=DR,SL=SL,SR=SR,ell=ell,rho=rr,a=a).items()},out)
