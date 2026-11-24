import z3,time,json,itertools
n=15;N=1<<n;start=time.time()
f=[z3.Bool('x'+str(i)) for i in range(N)];anf=f.copy()
for j in range(n):
 for x in range(N):
  if x>>j&1:anf[x]=z3.Xor(anf[x],anf[x^(1<<j)])
s=z3.SolverFor('QF_FD');s.set(timeout=3600000)
s.add(*[z3.Not(anf[x]) for x in range(N) if x.bit_count()>8])
# Full affine span follows Q=0, wt=2mod4: every shift intersects support.
# Normalize full affine frame and then complementary degree7/8 top pair.
s.add(f[0],*[f[1<<j] for j in range(n)])
s.add(anf[127],anf[(N-1)^127]);s.add(z3.Or(f[3],f[384],f[129]))
def pop(vs):
 vs=[z3.If(v,z3.BitVecVal(1,1),z3.BitVecVal(0,1)) for v in vs]
 while len(vs)>1:vs=[z3.ZeroExt(1,vs[i])+z3.ZeroExt(1,vs[i+1]) for i in range(0,len(vs),2)]
 return vs[0]
def xorall(vs):
 while len(vs)>1:vs=[z3.Xor(vs[i],vs[i+1]) if i+1<len(vs) else vs[i] for i in range(0,len(vs),2)]
 return vs[0] if vs else z3.BoolVal(False)
wt=pop(f);s.add(z3.Or(*[wt==w for w in [322,326,330,334]]))
for i in range(n):
 others=[j for j in range(n) if j!=i];mask=(N-1)^(1<<i)
 T=[sum(1<<j for j in S) for S in itertools.combinations(others,7)]
 pairs=[z3.And(anf[t|(1<<i)],anf[(t^mask)|(1<<i)]) for t in T if t<(t^mask)]
 assert len(pairs)==1716
 s.add(z3.Not(xorall(pairs)));print('Qzero',i,time.time()-start,flush=True)
# Redundant odd-half constraint: Qzero removes 8+8 covers, leaving 7+8 complementary pairs.
pairs=[z3.And(anf[t],anf[(N-1)^t]) for t in range(N) if t.bit_count()==7]
s.add(xorall(pairs))
print('built',time.time()-start,flush=True)
open('workspace/agent4_m15_qzero_sat.py','w').write(open('scratchpad.py').read())
ans=s.check();elapsed=time.time()-start;print(ans,elapsed,flush=True)
json.dump({'answer':str(ans),'seconds':elapsed},open('workspace/agent4_m15_qzero_sat_result.json','w'))
if ans==z3.sat:
 sol=s.model();S=[x for x,v in enumerate(f) if z3.is_true(sol.eval(v))];print('FOUND',len(S),S);json.dump(S,open('workspace/agent4_m15_qzero_found.json','w'))
