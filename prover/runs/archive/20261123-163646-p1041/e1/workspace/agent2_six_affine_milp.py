import itertools,time,json
import numpy as np
from scipy.optimize import milp,Bounds,LinearConstraint
from scipy.sparse import coo_matrix
from pathlib import Path
import sys;sys.path.insert(0,'workspace')
from agent2_five_affine_model import triple_weights
n=6;H=64;count=128
lb=[];ub=[];integ=[]
def var(lo,hi,integer=1):
 i=len(lb);lb.append(lo);ub.append(hi);integ.append(integer);return i
D={S:var(0,15) for S in range(count)}
P={S:[var(0,1) for j in range(9)] for S in range(1,H)} # j0..7=2^j, j8empty
ri=[];ci=[];vv=[];cl=[];cu=[]
def add(expr,lo=-np.inf,hi=np.inf):
 r=len(cl);cl.append(lo);cu.append(hi)
 for i,a in expr.items():
  if a:ri.append(r);ci.append(i);vv.append(a)
def exprsum(*items):
 out={}
 for E,k in items:
  for i,a in E.items():out[i]=out.get(i,0)+k*a
 return out
def dim(S):return {D[S]:1}
def card(S):return {P[S][j]:2**j for j in range(8)}
def eq(E,v):add(E,v,v)
def wtex(T):
 E={}
 for S in range(1,H):
  if S&T==S:
   k=(-2)**(S.bit_count()-1)
   for i,a in card(S).items():E[i]=E.get(i,0)+k*a
 return E
eq(dim(0),15);eq(dim(H),14)
singles=[1<<i for i in range(n)]
for S in range(1,count):
 add(dim(S),0,14 if S==H else (7 if S&H else 8))
for S in singles:eq(dim(S),8);eq(dim(S|H),7)
eq(dim(3),1);eq(dim(3|H),0)
for A in range(count):
 for B in range(count):
  if A&B==A:add(exprsum((dim(B),1),(dim(A),-1)),hi=0)
  add(exprsum((dim(A|B),1),(dim(A&B),1),(dim(A),-1),(dim(B),-1)),lo=0)
for A,B,C,E in itertools.permutations(singles+[H],4):
 out={}
 for S,k in [(A|B,1),(A|C,1),(A|E,1),(B|C,1),(B|E,1),(A,-1),(B,-1),(C|E,-1),(A|B|C,-1),(A|B|E,-1)]:out=exprsum((out,1),(dim(S),k))
 add(out,hi=0)
for S in range(1,H):
 eq({i:1 for i in P[S]},1)
 eq(exprsum((dim(S),1),(dim(S|H),-1),({P[S][j]:1 for j in range(8)},-1)),0)
 z={P[S][j]:j for j in range(8)}
 add(exprsum((dim(S|H),1),(z,-1)),lo=0)
 add(exprsum((dim(S|H),1),(z,-1),({P[S][8]:7},-1)),hi=0)
for T in range(1,H-1):
 k=T.bit_count();z=wtex(T)
 if k==2:add(z,lo=192)
 elif k==3:
  allowed=sorted(w for w in triple_weights() if w>=224);b=[var(0,1) for w in allowed]
  eq({i:1 for i in b},1);eq(exprsum((z,1),({i:w for i,w in zip(b,allowed)},-1)),0)
 elif k in [4,5]:add(z,lo={4:240,5:248}[k])
eq(card(5),32);eq(card(7),1)
for A,B in [(5,9),(9,17),(17,33),(5,6),(5,10),(5,18),(5,34)]:add(exprsum((card(A),1),(card(B),-1)),lo=0)
eq(wtex(H-1),334)
print('variables',len(lb),'constraints',len(cl),flush=True)
A=coo_matrix((vv,(ri,ci)),shape=(len(cl),len(lb))).tocsc();t=time.time()
r=milp(np.zeros(len(lb)),integrality=np.array(integ),bounds=Bounds(lb,ub),constraints=LinearConstraint(A,cl,cu),options={'time_limit':115})
print('RESULT',r.message,'sec',time.time()-t,flush=True)
if r.x is not None:
 x=np.rint(r.x).astype(np.int64);assert np.max(np.abs(r.x-x))<1e-5
 assert all(l-1e-5<=z<=u+1e-5 for z,l,u in zip(A@x,cl,cu))
 dims={S:int(x[i]) for S,i in D.items()};cards={S:sum((2**j)*int(x[i]) for j,i in enumerate(P[S][:8])) for S in P}
 weights={T:sum(a*int(x[i]) for i,a in wtex(T).items()) for T in range(1,H)}
 print('WEIGHTS',weights,flush=True)
 json.dump({'dims':dims,'cards':cards,'weights':weights},open('workspace/agent2_six_affine_milp_candidate.json','w'))
Path('workspace/agent2_six_affine_milp.py').write_text(Path('scratchpad.py').read_text())
