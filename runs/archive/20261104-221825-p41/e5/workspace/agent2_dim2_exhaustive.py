import itertools,numpy as np,time,json

def run(n=6):
 T=list(itertools.combinations(range(n),3));E=list(itertools.combinations(range(n),2));N=1<<len(T)
 te=[sum(1<<j for j,e in enumerate(E) if set(e)<=set(t)) for t in T]
 incE=[sum(1<<j for j,t in enumerate(T) if set(e)<=set(t)) for e in E]
 incV=[sum(1<<j for j,t in enumerate(T) if v in t) for v in range(n)]
 keepV=[sum(1<<j for j,e in enumerate(E) if v not in e) for v in range(n)]
 union=np.zeros(N,dtype=np.uint32)
 # vectorized subset-union table
 for j,b in enumerate(te):union[1<<j:1<<(j+1)]=union[:1<<j]|b
 # all vertex-link connected flags for each global triangle mask
 inds=np.arange(N,dtype=np.uint32)
 conn=[]
 for v in range(n):
  js=[j for j,t in enumerate(T) if v in t]
  ledges=[set(T[j])-{v} for j in js]
  table=[]
  for mask in range(1<<len(js)):
   edges=[e for j,e in enumerate(ledges) if mask>>j&1]
   if not edges:table.append(False);continue
   vertices=set().union(*edges);seen={next(iter(vertices))}
   while True:
    new=seen|set().union(*(e for e in edges if e&seen))
    if new==seen:break
    seen=new
   table.append(seen==vertices)
  compressed=np.zeros(N,dtype=np.uint16)
  for b,j in enumerate(js):compressed|=(((inds>>j)&1)<<b).astype(np.uint16)
  conn.append(np.array(table,dtype=np.bool_)[compressed])
 kd=np.zeros(N,dtype=np.bool_)
 started=time.time()
 for mask in range(1,N):
  if mask&(mask-1)==0:kd[mask]=True;continue
  orig=int(union[mask])
  for e,inc in enumerate(incE):
   rem=mask&~inc
   if rem!=mask and kd[rem] and int(union[rem])==(orig&~(1<<e)):
    kd[mask]=True;break
  if not kd[mask]:
   for v,inc in enumerate(incV):
    rem=mask&~inc
    if rem!=mask and kd[rem] and int(union[rem])==(orig&keepV[v]) and conn[v][mask]:
     kd[mask]=True;break
  if mask%200000==0:print('kd',mask,time.time()-started,flush=True)
 reachable=np.zeros(N,dtype=np.bool_);reachable[-1]=True
 bad=[]
 for mask in range(N-2,0,-1):
  if not kd[mask]:continue
  missing=(N-1)^mask
  while missing:
   bit=missing&-missing;missing^=bit
   if reachable[mask|bit]:reachable[mask]=True;break
  if not reachable[mask]:bad.append(mask)
 result=dict(n=n,kd=int(kd.sum()),reachable=int(reachable.sum()),bad=len(bad),seconds=time.time()-started)
 print(result,flush=True)
 if bad: print('first_bad',[T[j] for j in range(len(T)) if bad[-1]>>j&1],flush=True)
 np.savez_compressed('workspace/agent2_dim2_n%d.npz'%n,kd=kd,reachable=reachable)
 open('workspace/agent2_dim2_n%d.json'%n,'w').write(json.dumps(result))
 return result
if __name__=='__main__':run()
