import z3,time,json
n=14;N=1<<n;start=time.time()
f=[z3.Bool('x'+str(i)) for i in range(N)];anf=f.copy()
for j in range(n):
 for x in range(N):
  if x>>j&1:anf[x]=z3.Xor(anf[x],anf[x^(1<<j)])
s=z3.SolverFor('QF_FD');s.set(timeout=3600000)
s.add(*[z3.Not(anf[x]) for x in range(N) if x.bit_count()>7])
s.add(f[0],*[f[1<<j] for j in range(n)])
s.add(anf[127],anf[127<<7]);s.add(z3.Or(f[3],f[129]))
allowed=[128,192,224,240,248,252]+list(range(256,333,4))
def pop(vs):
 vs=[z3.If(v,z3.BitVecVal(1,1),z3.BitVecVal(0,1)) for v in vs]
 while len(vs)>1:vs=[z3.ZeroExt(1,vs[i])+z3.ZeroExt(1,vs[i+1]) for i in range(0,len(vs),2)]
 return vs[0]
wt=pop(f);s.add(z3.Or(*[wt==w for w in [322,326,330,334]]))
for j in range(n):
 d=[z3.Xor(f[x],f[x^(1<<j)]) for x in range(N) if not(x>>j&1)];cnt=pop(d)
 s.add(z3.Or(*[cnt==w for w in allowed]));print('derivative',j,time.time()-start,flush=True)
print('built',time.time()-start,flush=True)
open('workspace/agent4_exact_all_four_sat.py','w').write(open('scratchpad.py').read())
ans=s.check();elapsed=time.time()-start;print(ans,elapsed,flush=True)
json.dump({'answer':str(ans),'seconds':elapsed},open('workspace/agent4_exact_all_four_sat_result.json','w'))
if ans==z3.sat:
 sol=s.model();S=[x for x,v in enumerate(f) if z3.is_true(sol.eval(v))];print('FOUND',len(S),S);json.dump(S,open('workspace/agent4_found_badweight.json','w'))
