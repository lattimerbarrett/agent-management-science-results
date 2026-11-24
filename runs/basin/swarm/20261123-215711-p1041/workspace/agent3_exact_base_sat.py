import z3,time,json
n=14;N=1<<n;start=time.time()
f=[z3.Bool('x'+str(i)) for i in range(N)];anf=f.copy()
for j in range(n):
 for x in range(N):
  if x>>j&1:anf[x]=z3.Xor(anf[x],anf[x^(1<<j)])
s=z3.SolverFor('QF_FD');s.set(timeout=3600000)
s.add(*[z3.Not(anf[x]) for x in range(N) if x.bit_count()>7]);s.add(z3.PbEq([(x,1) for x in f],322))
# Valid symmetry: full affine span14, affine plane exists since choose(322,2)>16383.
# Full affine basis plus parallelogram may be normalized; then coordinate permutation
# can normalize a complementary degree7 ANF pair. The two plane directions lie
# either in the same half or opposite halves.
s.add(f[0],*[f[1<<j] for j in range(n)])
s.add(anf[127],anf[127<<7]);s.add(z3.Or(f[3],f[129]))
allowed=[128,192,224,240,248,252,256,272,288,296,304,308,312,316,320]
def pop(vs):
 vs=[z3.If(v,z3.BitVecVal(1,1),z3.BitVecVal(0,1)) for v in vs]
 while len(vs)>1:vs=[z3.ZeroExt(1,vs[i])+z3.ZeroExt(1,vs[i+1]) for i in range(0,len(vs),2)]
 return vs[0]
for j in range(n):
 d=[z3.Xor(f[x],f[x^(1<<j)]) for x in range(N) if not(x>>j&1)];cnt=pop(d)
 s.add(z3.Or(*[cnt==w for w in allowed]));print('derivative',j,time.time()-start,flush=True)
print('built',time.time()-start,flush=True);ans=s.check();print(ans,time.time()-start,flush=True)
if ans==z3.sat:
 sol=s.model();S=[x for x,v in enumerate(f) if z3.is_true(sol.eval(v))];print('FOUND',S);json.dump(S,open('workspace/agent3_found322.json','w'))
