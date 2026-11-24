import itertools,z3,json,time
n=9;d=3
fs=[sum(1<<i for i in c) for c in itertools.combinations(range(n),d+1)]
s=z3.Solver();s.set(timeout=900000)
r=[z3.Int('r%d'%i) for i in range(len(fs))]
for x in r:s.add(x>=0,x<=len(fs))
s.add(r[0]==1,r[1]==2)
count=z3.Sum([z3.If(x>0,1,0) for x in r])
for x in r:s.add(x<=count)
s.add(z3.Or([x==0 for x in r]))
for i in range(len(fs)):
 for j in range(i):s.add(z3.Or(r[i]==0,r[j]==0,r[i]!=r[j]))
for v in range(n):s.add(z3.Or([r[i]>0 for i,f in enumerate(fs) if f>>v&1]))
for i,f in enumerate(fs):
 vs=[v for v in range(n) if f>>v&1]
 B={v:z3.Or([z3.And(r[j]>0,r[j]<r[i]) for j,h in enumerate(fs) if j!=i and (f^(1<<v))&h==(f^(1<<v))]) for v in vs}
 for j,h in enumerate(fs):
  if j==i:continue
  s.add(z3.Implies(z3.And(r[i]>1,r[j]>0,r[j]<r[i]),z3.Or([B[v] for v in vs if not h>>v&1])))
 BF={v:z3.Or([r[j]>0 for j,h in enumerate(fs) if j!=i and (f^(1<<v))&h==(f^(1<<v))]) for v in vs}
 blocked=z3.Or([z3.And(r[j]>0,*[z3.Not(BF[v]) for v in vs if not h>>v&1]) for j,h in enumerate(fs) if j!=i])
 s.add(z3.Implies(r[i]==0,blocked))
print('built',len(fs),flush=True);t=time.time();res=s.check();print(res,time.time()-t,flush=True)
with open('scratchpad.py') as src,open('workspace/agent3_terminal_sat_n9.py','w') as dst:dst.write(src.read())
with open('workspace/agent3_terminal_sat_n9_result.json','w') as out:json.dump({'n':n,'d':d,'result':str(res),'time':time.time()-t},out)
if res==z3.sat:
 m=s.model();order=[f for rank,f in sorted([(m.eval(r[i]).as_long(),f) for i,f in enumerate(fs)]) if rank]
 print(order,flush=True)
 json.dump({'n':n,'d':d,'order':order},open('workspace/agent3_sat_obstruction.json','w'))
