import numpy as np,itertools,pickle,time
from scipy.integrate import quad

def constrain(interval,row):
 lo,hi=interval;a,b=row; # row dot(-1,s)>0
 if abs(b)<1e-12:return None if a>=0 else interval
 if b>0:lo=max(lo,a/b)
 else:hi=min(hi,a/b)
 return (lo,hi) if lo<hi-1e-10 else None

def words(refs,side,depth=4):
 # side +1 left incoming C>0, -1 right incoming C<0
 incoming=(0,np.inf) if side==1 else (-np.inf,0);parts=[((),np.eye(2),incoming)];exits=[]
 for n in range(depth):
  nxt=[]
  for word,M,iv in parts:
   for j,(R,b,ell) in enumerate(refs):
    if word and j==word[-1]:continue
    ivn=constrain(iv,ell@M)
    if ivn is None:continue
    MM=R@M;ivn=constrain(ivn,-MM[0])
    if ivn is None:continue
    ivexit=constrain(ivn,-side*MM[1])
    if ivexit is not None:exits.append((word+(j,),MM,ivexit))
    ivcont=constrain(ivn,side*MM[1])
    if ivcont is not None:nxt.append((word+(j,),MM,ivcont))
  parts=nxt
 return exits

def data(a,L,H):
 v=a+L;d=a*L;Q=np.poly([0,a,1,L]);pc=Q.copy();pc[-1]=-H;co=np.sort(np.roots(pc));pe=Q.copy();pe[-1]=H;ex=np.sort(np.roots(pe));ml=1-co[2];mr=1-co[1]
 def RR(m):return m*(m-1)*(d+m*m+(v-2)*m-v+1)
 def integrand(m):return (d+2*m*m+(v-3)*m-v+1)/(2*np.sqrt(RR(m)))
 I=quad(integrand,ml,mr,epsabs=1e-8,epsrel=1e-8)[0];F=np.array([[1,I],[0,1.]])
 refs=[]
 for m,lam0 in [(ml,co[2]),(mr,co[1])]:
  mp=m+v-1;V=m-m*m;Vp=v*mp-d-mp*mp;th=-m/V+mp/Vp;tz=1/V-1/Vp
  BC=d+(v-1)*(m-1);T=np.array([[-d,v-1],[-d*m/np.sqrt(H),BC/np.sqrt(H)]]);Ti=np.linalg.inv(T);row=[]
  for x in ex:
   px=x*(x-1);b=T@np.array([4*px,4*x*px]);ell=-4*(np.array([-d,v-1])/H+np.array([th,tz])/(x-lam0))@Ti
   R=np.eye(2)-2*np.outer(b,ell)/(ell@b);row.append((R,b,ell))
  refs.append(row)
 return co,ex,ml,mr,F,refs
rng=np.random.default_rng(718);found=[];t=time.time()
for case in range(10000):
 a,L=np.sort(rng.uniform(.001,.999,2));v=a+L;d=a*L;Q=np.poly([0,a,1,L]);crit=np.sort(np.roots(np.polyder(Q)));lev=np.polyval(Q,crit);H=10**rng.uniform(-6,-.001)*min(-lev[0],lev[1],-lev[2])
 co,ex,ml,mr,F,refs=data(a,L,H);wl=words(refs[0],1);wr=words(refs[1],-1)
 for il,(wordl,ML,ivl) in enumerate(wl):
  for ir,(wordr,MR,ivr) in enumerate(wr):
   M=np.linalg.solve(F,MR@F@ML);vals,vecs=np.linalg.eig(M)
   for ei in range(2):
    val=vals[ei]
    if abs(val.imag)>1e-6 or not 1e-6<val.real<1-1e-6:continue
    x=vecs[:,ei].real;x*=-np.sign(x[0]);x/=abs(x[0]);sl=x[1]
    if not ivl[0]<sl<ivl[1]:continue
    xr=F@ML@x
    if xr[0]>=0:continue
    sr=xr[1]/(-xr[0])
    if not ivr[0]<sr<ivr[1]:continue
    print('FOUND',case,'a,L,H',a,L,H,'words',wordl,wordr,'eig',val,'x',x,'ivs',ivl,ivr,flush=True);found.append((a,L,H,wordl,wordr,val,x,co,ex,F,refs));pickle.dump(found,open('workspace/words_found_agent4.pkl','wb'))
 if case%50==0:print('progress',case,'wordcounts',len(wl),len(wr),'time',time.time()-t,flush=True)
print('DONE',len(found),time.time()-t)
from pathlib import Path
Path('workspace/word_search_agent4.py').write_text(Path('scratchpad.py').read_text())
