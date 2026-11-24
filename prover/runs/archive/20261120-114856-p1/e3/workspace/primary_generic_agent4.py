from pathlib import Path
import numpy as np,pickle,time
exec(Path('workspace/word_search_agent4.py').read_text().split('rng=np.random.default_rng')[0])
def field(Y,a,L,H,ex):
 m,A=Y[:2];WW=Y[2:];v=a+L;d=a*L;Z=(d*A-1)/(v-1);D=d+m*m+(v-2)*m-v+1;RR=m*(m-1)*D;B=d+(v-1)*(m-1);g=-d*m*A+B*Z;f=-2*g*(RR-H)/(H*RR)
 aa=(d+2*m*m+2*m*v-4*m-2*v+2)/(2*(m-1)*D);ab=-(d+2*m*m+m*v-3*m-v+1)/(2*m*(m-1)*D);ba=d/(2*D);bb=(d+2*m*m+m*v-3*m-v+1)/(2*m*D)
 pp=ex*(ex-1);qq=ex*ex-v*ex+d;Fh=(aa*A+ab*Z)*f+4*np.sum(pp*WW);Fz=(ba*A+bb*Z)*f+4*np.sum(pp*ex*WW);gam=d*Fh-(v-1)*Fz
 mm=m+v-1;V=m-m*m;Vp=v*mm-d-mm*mm;bet=(Z-m*A)/V;alp=(Z-mm*A)/Vp;dq=A*(pp-qq)+alp*pp*(ex-mm)-bet*qq*(ex-m);ell=-2*(dq-1)/H
 return np.r_[f,Fh-A*gam,WW*(ell-2*gam)]
def jac(Y,a,L,H,ex):
 J=np.empty((len(Y),len(Y)))
 for j in range(len(Y)):
  yy=np.asarray(Y,dtype=complex);yy[j]+=1e-26j;J[:,j]=field(yy,a,L,H,ex).imag/1e-26
 return J
rng=np.random.default_rng(458);eq=[];t=time.time()
for case in range(20000):
 if case%2:a=rng.uniform(.0001,.9999);L=1+10**rng.uniform(-4,2)
 else:a,L=np.sort(rng.uniform(.0001,.9999,2))
 v=a+L;d=a*L;Q=np.poly([0,a,1,L]);cr=np.sort(np.roots(np.polyder(Q)));lev=np.polyval(Q,cr);H=10**rng.uniform(-6,-.0001)*min(-lev[0],lev[1],-lev[2]);pc=Q.copy();pc[-1]=-H;co=np.sort(np.roots(pc));pc[-1]=H;ex=np.sort(np.roots(pc));ml=1-co[2];mr=1-co[1]
 for j,x in enumerate(ex):
  mm=x*(d-v+1)/(d-(v-1)*x)
  if not ml+1e-9<mm<mr-1e-9:continue
  px=x*(x-1);be=4*px*((v-1)*x-d);AA=-4*px/be;ZZ=-4*x*px/be;mp=mm+v-1;V=mm-mm*mm;Vp=v*mp-d-mp*mp;dq=AA*(px-(x*x-v*x+d))+(ZZ-mp*AA)/Vp*px*(x-mp)-(ZZ-mm*AA)/V*(x*x-v*x+d)*(x-mm);ll=-2*(dq-1)/H;gam=ll/2;ww=-gam/be
  if ww<=0:continue
  Y=np.array([mm,AA,ww]);J=jac(Y,a,L,H,np.array([x]));ee=np.linalg.eigvals(J);err=np.max(abs(field(Y,a,L,H,np.array([x]))));eq.append((a,L,H,j,x,Y,ee,err))
  if any(abs(e.imag)>1e-6 for e in ee) and max(ee.real)>1e-8:
   print('UNSTABLEFOCUS',a,L,H,j,x,'Y',Y,'eig',ee,'err',err,flush=True);pickle.dump(eq,open('workspace/primary_eq_agent4.pkl','wb'));raise SystemExit
 if case%2000==0:print('progress',case,'eq',len(eq),'time',time.time()-t,flush=True)
print('DONE',len(eq));print('EIGEX',[(e[6],e[7])for e in eq[:10]]);pickle.dump(eq,open('workspace/primary_eq_agent4.pkl','wb'))
Path('workspace/primary_generic_agent4.py').write_text(Path('scratchpad.py').read_text())
