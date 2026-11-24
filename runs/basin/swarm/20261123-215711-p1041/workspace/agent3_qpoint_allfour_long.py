import z3,time,json
from pathlib import Path
n=14;N=1<<n;start=time.time();f=[z3.Bool('x'+str(i)) for i in range(N)];anf=f.copy()
for j in range(n):
 for x in range(N):
  if x>>j&1:anf[x]=z3.Xor(anf[x],anf[x^(1<<j)])
s=z3.SolverFor('QF_FD');s.set(timeout=3600000)
s.add(*[z3.Not(anf[x]) for x in range(N) if x.bit_count()>7])
def pop(vs):
 vs=[z3.If(v,z3.BitVecVal(1,1),z3.BitVecVal(0,1)) for v in vs]
 while len(vs)>1:vs=[z3.ZeroExt(1,vs[i])+z3.ZeroExt(1,vs[i+1]) for i in range(0,len(vs),2)]
 return vs[0]
W=pop(f);s.add(z3.Or(*[W==w for w in [322,326,330,334]]));s.add(*[f[1<<j] for j in range(n)]);s.add(anf[127],anf[16256])
for j in range(n):
 # qpoint translated to0: every linear-coordinate section has weight divisible4.
 vs=[z3.If(f[x],z3.BitVecVal(1,2),z3.BitVecVal(0,2)) for x in range(N) if x>>j&1]
 while len(vs)>1:vs=[vs[i]+vs[i+1] for i in range(0,len(vs),2)]
 s.add(vs[0]==0)
 d=[z3.Xor(f[x],f[x^(1<<j)]) for x in range(N) if not(x>>j&1)];cnt=pop(d)
 # Conservative, established Kasami-Tokura weights strictly below2d only.
 s.add(z3.Extract(1,0,cnt)==0,z3.ULE(z3.ZeroExt(1,cnt),W-2))
 s.add(z3.Or(*[cnt==v for v in [128,192,224,240,248,252]],z3.UGE(cnt,256)))
 print('coordinate',j,time.time()-start,flush=True)
print('built',time.time()-start,flush=True)
Path('workspace/agent3_qpoint_allfour_long.py').write_text(Path(__file__).read_text())
ans=s.check();print(ans,time.time()-start,flush=True)
out={'result':str(ans),'seconds':time.time()-start}
if ans==z3.sat:
 sol=s.model();S=[x for x,v in enumerate(f) if z3.is_true(sol.eval(v))];vals=[int(x in set(S)) for x in range(N)];aa=vals.copy()
 for j in range(n):
  for x in range(N):
   if x>>j&1:aa[x]^=aa[x^(1<<j)]
 assert len(S) in [322,326,330,334] and max(i.bit_count() for i,a in enumerate(aa) if a)<=7
 out['support']=S;print('FOUND',len(S),S,flush=True)
json.dump(out,open('workspace/agent3_qpoint_allfour_result.json','w'))