import sys,json,pathlib,time,collections,z3
sys.path.insert(0,'workspace');from agent3_lift_closure import veronese
vs=veronese(12,3)
def act(p):
 out=p&3
 for j in range(2,12,2):
  a=p>>j&1;b=p>>(j+1)&1;out|=b<<j;out|=(a^b)<<(j+1)
 return out
seen=set();orbs=[]
for p in range(4096):
 if p in seen:continue
 O=sorted({p,act(p),act(act(p))});seen.update(O)
 if len(O)==3:orbs.append(O)
assert len(orbs)==1364
cols=[vs[O[0]]^vs[O[1]]^vs[O[2]] for O in orbs];target=vs[0]^vs[1];B={}
for bit in range(299):
 row=sum(1<<i for i,c in enumerate(cols) if c>>bit&1);rhs=target>>bit&1
 while row:
  k=row.bit_length()-1
  if k not in B:B[k]=(row,rhs);break
  row^=B[k][0];rhs^=B[k][1]
 if not row:assert not rhs
print('rank',len(B),'orbits',len(orbs),flush=True)
X=[z3.Bool('x%d'%i) for i in range(len(orbs))];sol=z3.Solver();sol.set(timeout=180000)
for row,rhs in B.values():
 args=[X[i] for i in range(len(X)) if row>>i&1]
 while len(args)>1:args=[z3.Xor(args[i],args[i+1]) if i+1<len(args) else args[i] for i in range(0,len(args),2)]
 sol.add(args[0]==bool(rhs))
sol.add(z3.PbEq([(x,1) for x in X],12));t=time.time();result=sol.check();print('result',result,'sec',time.time()-t,flush=True)
D={'moment_rank':len(B),'result':str(result),'seconds':time.time()-t}
if result==z3.sat:
 M=sol.model();S=[0,1]+[p for i,O in enumerate(orbs) if z3.is_true(M.eval(X[i])) for p in O];assert len(S)==38
 syn=0
 for p in S:syn^=vs[p]
 assert syn==0
 BB={}
 for p in S:
  r=p^S[0]
  while r:
   j=r.bit_length()-1
   if j in BB:r^=BB[j]
   else:BB[j]=r;break
 D.update(support=S,affine_rank=len(BB));print(D,flush=True)
json.dump(D,open('workspace/agent2_T38_C3.json','w'));pathlib.Path('workspace/agent2_T38_C3.py').write_text(pathlib.Path(__file__).read_text())
