from z3 import *
from pathlib import Path
import itertools,time,json,sys
sys.path.insert(0,'workspace')
from agent2_five_affine_model import triple_weights
n=6;H=1<<n;count=H*2
D={0:BitVecVal(15,8)}|{S:BitVec('d'+str(S),8) for S in range(1,count)};V={S:BitVec('v'+str(S),16) for S in range(1,H)}
s=SolverFor("QF_BV");s.set(timeout=120000)
singles=[1<<i for i in range(n)]
for S in range(1,count):
 upper=14 if S==H else (7 if S&H else 8);s.add(D[S]>=0,D[S]<=upper)
for S in singles:s.add(D[S]==8,D[S|H]==7)
s.add(D[H]==14,D[3]==1,D[3|H]==0)
for A in range(count):
 for B in range(count):
  if A&B==A:s.add(D[B]<=D[A])
  s.add(D[A|B]+D[A&B]>=D[A]+D[B])
for A,B,C,E in itertools.permutations(singles+[H],4):s.add(D[A|B]+D[A|C]+D[A|E]+D[B|C]+D[B|E]<=D[A]+D[B]+D[C|E]+D[A|B|C]+D[A|B|E])
for S in range(1,H):s.add(Or(And(V[S]==0,D[S]==D[S|H]),*[And(V[S]==(1<<j),D[S]==j+1,D[S|H]==j) for j in range(8)]))
def wt(T):return Sum([(-2)**(S.bit_count()-1)*V[S] for S in range(1,H) if S&T==S])
W3=triple_weights();targets=[322,326,330,334]
for T in range(1,H-1):
 k=T.bit_count();z=wt(T)
 if k==2:s.add(z>=192)
 elif k==3:s.add(Or(*[z==w for w in W3 if w>=224]))
 elif k>=4:s.add(z>=({4:240,5:256}[k]),*[z!=w for w in targets])
pairs=[S for S in range(1,H) if S.bit_count()==2]
p=BoolVal(False)
for S in pairs:p=Xor(p,V[S]==1)
s.add(p,Sum([V[S] for S in pairs])>=217)
s.add(V[5]>=4,V[5]>=V[9],V[9]>=V[17],V[17]>=V[33],*[V[5]>=V[S] for S in (6,10,18,34)])
w=wt(H-1);s.add(Or(*[w==t for t in targets]))

s.add(V[5]>=16,Or(*[V[S]==32 for S in pairs]),Or(*[V[S]==0 for S in [7,11,19,35]]))
t=time.time();r=s.check();print(r,time.time()-t,flush=True)
if r==sat:
 m=s.model();dims={S:m.eval(D[S]).as_long() for S in range(count)}
 print('WEIGHT',m.eval(w),dims,flush=True)
 json.dump({'weight':m.eval(w).as_long(),'dims':dims},open('workspace/agent2_six_affine_new_candidate.json','w'))
