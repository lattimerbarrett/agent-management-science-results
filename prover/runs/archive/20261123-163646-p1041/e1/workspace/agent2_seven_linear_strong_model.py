from z3 import *
from pathlib import Path
import itertools,time,json,sys
sys.path.insert(0,'workspace')
from agent2_five_affine_model import triple_weights
n=7;H=1<<n
D={0:IntVal(14)}|{S:Int('d'+str(S)) for S in range(1,H)}
V={S:Int('v'+str(S)) for S in range(1,H)}
s=Solver();s.set(timeout=120000)
singles=[1<<i for i in range(n)]
for S in range(1,H):
 s.add(D[S]>=0,D[S]<=7)
 s.add(Or(*[And(D[S]==j,V[S]==(1<<j)) for j in range(8)]))
for S in singles:s.add(D[S]==7)
s.add(D[3]==0)
for A in range(H):
 for B in range(H):
  if A&B==A:s.add(D[B]<=D[A])
  s.add(D[A|B]+D[A&B]>=D[A]+D[B])
for A,B,C,E in itertools.permutations(singles,4):s.add(D[A|B]+D[A|C]+D[A|E]+D[B|C]+D[B|E]<=D[A]+D[B]+D[C|E]+D[A|B|C]+D[A|B|E])
def wt(T):return Sum([(-2)**(S.bit_count()-1)*V[S] for S in range(1,H) if S&T==S])
W3=triple_weights();low=[128,192,224,240,248,252,254,256,272,288,296,304,308,312,314,316,318];targets=[322,326,330,334]
for T in range(1,H-1):
 k=T.bit_count();z=wt(T)
 if k==2:s.add(z>=192)
 elif k==3:s.add(Or(*[z==w for w in W3 if w>=224]))
 elif k>=4:s.add(z>=({4:240,5:248,6:252}[k]),*[z!=w for w in targets])
pairs=[S for S in range(1,H) if S.bit_count()==2]
s.add(Or(*[D[S]==5 for S in pairs]))
s.add(Xor(*[D[S]==0 for S in pairs[:2]])) if False else None
# z3 Xor accepts only binary; iterate parity explicitly.
p=BoolVal(False)
for S in pairs:p=Xor(p,D[S]==0)
s.add(p)
s.add(D[5]>=D[9],D[9]>=D[17],D[17]>=D[33],D[33]>=D[65],*[D[5]>=D[S] for S in (6,10,18,34,66)])
s.add(Sum([V[S] for S in pairs])>=299)
w=wt(H-1);s.add(Or(*[w==t for t in targets]))
t=time.time();r=s.check();print(r,time.time()-t,flush=True)
if r==sat:
 m=s.model();dims={S:m.eval(D[S]).as_long() for S in range(H)}
 print('WEIGHT',m.eval(w),dims,flush=True)
 json.dump({'weight':m.eval(w).as_long(),'dims':dims},open('workspace/agent2_seven_linear_strong_dimensions.json','w'))

