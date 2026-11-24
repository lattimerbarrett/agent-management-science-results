import numpy as np,pickle,sympy as sy,time
from scipy.integrate import solve_ivp
Mat=pickle.load(open('workspace/generic_connection_agent4.pkl','rb'));sm,sv,sd=sy.symbols('m v d');mf=sy.lambdify((sm,sv,sd),Mat,'numpy')
N=3
class J:
 def __init__(self,x):self.a=np.asarray(x,float) if isinstance(x,(list,np.ndarray)) else np.array([x,0,0,0.])
 def __add__(s,t):return J(s.a+j(t).a)
 __radd__=__add__
 def __neg__(s):return J(-s.a)
 def __sub__(s,t):return s+-j(t)
 def __rsub__(s,t):return j(t)+-s
 def __mul__(s,t):return J(np.convolve(s.a,j(t).a)[:4])
 __rmul__=__mul__
 def __truediv__(s,t):
  t=j(t).a;o=np.empty(4)
  for k in range(4):o[k]=(s.a[k]-sum(t[r]*o[k-r]for r in range(1,k+1)))/t[0]
  return J(o)
 def __pow__(s,n):
  o=J(1)
  for k in range(n):o=o*s
  return o

def j(t):return t if isinstance(t,J) else J(t)
def op(state,bu,b0,bv,b1,v,d,H,xi):
 mm,hh,zz,ww=state;M=[J(1),mm,bu*mm-b0+hh];M.append(bu*M[2]-b0*mm+zz)
 for k in range(4,8):M.append((1+v)*M[-1]-(v+d)*M[-2]+d*M[-3]+H*M[-4]-2*H*xi**(k-4)*ww)
 a=(M[3]-mm*M[2])/(M[2]-mm*mm);b=M[2]-a*mm;Q=[b*b,2*a*b,a*a-2*b,-2*a,J(1)]
 nums=[sum((Q[r]*M[k+r]for r in range(5)),J(0))for k in range(4)];norm=nums[0];ms=[nums[k]/norm for k in range(1,4)]
 return [ms[0],ms[1]-bv*ms[0]+b1,ms[2]-bv*ms[1]+b1*ms[0],ww*(xi*xi-a*xi-b)**2/norm]
def jet(mm,A,B,W,v,d,H,xi):
 e=J([0,1,0,0]);st=[J(mm),A*e,B*e,W*e**2]
 return op(op(st,1,0,v,d,v,d,H,xi),v,d,1,0,v,d,H,xi)
def reflection(mm,xi,v,d,H):
 o=jet(mm,0,0,1,v,d,H,xi);b=np.array([o[1].a[2],o[2].a[2]])
 ell=np.array([jet(mm,1,0,1,v,d,H,xi)[3].a[3],jet(mm,0,1,1,v,d,H,xi)[3].a[3]])
 R=np.eye(2)-2*np.outer(b,ell)/(ell@b);return R,b,ell
rng=np.random.default_rng(581);t=time.time();found=[]
for case in range(700):
 a=rng.uniform(.05,.95);L=1+10**rng.uniform(-.6,1.3);v=a+L;d=a*L;Q=np.poly([0,a,1,L]);crit=np.sort(np.roots(np.polyder(Q)));levels=np.polyval(Q,crit);H=rng.uniform(.02,.95)*min(-levels[0],levels[1],-levels[2]);pc=Q.copy();pc[-1]=-H;core=np.sort(np.roots(pc));pe=Q.copy();pe[-1]=H;ext=np.sort(np.roots(pe));left=1-core[2];right=1-core[1]
 if left<=0 or right>=1:continue
 sol=solve_ivp(lambda m,z:(mf(m,v,d)@z.reshape(2,2)).ravel(),[left,right],np.eye(2).ravel(),rtol=1e-8,atol=1e-10,dense_output=True)
 P=sol.y[:,-1].reshape(2,2);mid=(left+right)/2;Pm=sol.sol(mid).reshape(2,2)
 refs=[[reflection(m,xi,v,d,H)for xi in ext]for m in[left,right]]
 vel=np.array([jet(mid,1,0,0,v,d,H,0)[0].a[1],jet(mid,0,1,0,v,d,H,0)[0].a[1]])
 E=np.array([-d,v-1])
 for i in range(4):
  for k in range(4):
   if i==k:continue
   RL,bl,ll=refs[0][i];RR,br,lr=refs[1][k];prod=np.linalg.solve(P,RR@P@RL);vals,vecs=np.linalg.eig(prod)
   for eigidx in range(2):
    if abs(vals[eigidx].imag)>1e-6 or not .0001<vals[eigidx].real<.9999:continue
    x=vecs[:,eigidx].real;x*=np.sign(-(E@x));xa=RL@x;xb=P@xa;xc=RR@xb
    valid=all(E@z<0 for z in[x,xa,xb,xc])and ll@x>0 and lr@xb>0 and vel@Pm@x<0 and vel@Pm@xa>0 and vel@Pm@np.linalg.solve(P,xc)<0
    if valid:
     print('FOUND',case,'a,L,H',a,L,H,'mends',left,right,'pair',i,k,'eig',vals[eigidx],'x',x,'E',[E@z for z in[x,xa,xb,xc]],flush=True);found.append((a,L,H,core,ext,i,k,vals[eigidx],x,P,refs));pickle.dump(found,open('workspace/billiard_found_agent4.pkl','wb'))
 if case%100==0:print('progress',case,time.time()-t,flush=True)
print('DONE',len(found),time.time()-t)
from pathlib import Path
Path('workspace/billiard_search_agent4.py').write_text(Path('scratchpad.py').read_text())
