import json,sys,itertools,pathlib,time,random,numpy as np
import z3
sys.path.insert(0,'workspace')
from agent3_lift_closure import veronese,closure

def ker(S,vs):
 B={};K=[]
 for i,p in enumerate(S):
  v=vs[p];c=1<<i
  while v:
   k=v.bit_length()-1
   if k in B:v^=B[k][0];c^=B[k][1]
   else:B[k]=(v,c);break
  if not v:K.append(c)
 return K
D=json.load(open('workspace/agent1_new320_quadratic_K14_closure_results.json'));S=sorted(D['results'][0]['support']);SS=set(S);random.seed(32064)
for it in range(10000):
 a,b,c=random.sample(S,3);d=a^b^c
 if d in SS and len({p&127 for p in [a,b,c,d]})==4:R=[a,b,c,d];break
print('R',R,flush=True)
fib={x:[] for x in range(128)}
for p in S:fib[p&127].append(p>>7)
A=[z3.BitVec('a'+str(j),6) for j in range(8)];sol=z3.Solver();sol.set(timeout=90000,random_seed=3214);Y=[]
for x in range(128):
 y=A[7]
 for j in range(7):
  if x>>j&1:y=y^A[j]
 Y.append(y)
M=[z3.Or([Y[x]==a for a in ys]) for x,ys in fib.items()];sol.add(z3.PbEq([(p,1) for p in M],64));rlist=[Y[p&127]==(p>>7) for p in R];sol.add(z3.Xor(z3.Xor(rlist[0],rlist[1]),z3.Xor(rlist[2],rlist[3])));st=time.time();result=sol.check();print('SAT',result,'time',time.time()-st,flush=True);ans={'status':str(result),'time':time.time()-st,'R':R}
if result==z3.sat:
 model=sol.model();aa=[model.eval(a).as_long() for a in A];H=[]
 for x in range(128):
  y=aa[7]
  for j in range(7):
   if x>>j&1:y^=aa[j]
  H.append(x|(y<<7))
 assert len(SS.intersection(H))==64 and len(set(R).intersection(H))%2==1
 G=sorted(SS^set(H));assert len(G)==320;K5=ker(G,veronese(13,5));K6=ker(G,veronese(13,6));gram=sum((u&v).bit_count()%2 for u in K5 for v in K5);cl,r=closure(set(G),veronese(13,5));ans.update(support=G,flat=H,K5=len(K5),K6=len(K6),Gram_nonzero=gram,cl5extra=len(cl));print({k:v for k,v in ans.items() if k not in ['support','flat']},flush=True)
json.dump(ans,open('workspace/agent1_indecomp320_neutralSAT.json','w'));pathlib.Path('workspace/agent1_indecomp320_neutralSAT.py').write_text(pathlib.Path(__file__).read_text())
