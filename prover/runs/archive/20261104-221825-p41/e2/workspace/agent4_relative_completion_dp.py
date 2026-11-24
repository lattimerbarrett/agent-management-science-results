import sys,itertools,time,json,pathlib
sys.path.insert(0,'workspace')
from agent4_checker import dec

def check(n,rank,k,sz):
 sigma=(1<<sz)-1
 target=[sum(1<<v for v in c) for c in itertools.combinations(range(n),rank) if not set(range(sz))<=set(c)]
 N=len(target);allmask=(1<<N)-1
 good=bytearray(1<<N);kd=bytearray(1<<N);start=time.time();bad=[];positive=0
 for m in sorted(range(1,1<<N),key=int.bit_count,reverse=True):
  fs=tuple(sorted(target[i] for i in range(N) if m>>i&1))
  if not dec(fs,k):continue
  positive+=1;kd[m]=1
  if m==allmask or any(good[m|(1<<i)] for i in range(N) if not(m>>i&1)):good[m]=1
  else:bad.append(m)
 print(n,rank,k,sz,'N',N,'kdec',positive,'bad',len(bad),'time',time.time()-start,flush=True)
 if bad:
  m=bad[-1];print('BADFACETS',[target[i] for i in range(N) if m>>i&1],flush=True)
 return {'n':n,'rank':rank,'k':k,'sigma_size':sz,'target_facets':N,'kdec':positive,'bad':len(bad)}
results=[check(6,4,1,2),check(6,4,2,3),check(6,4,2,2),check(6,4,1,3)]
json.dump(results,open('workspace/agent4_relative_completion_dp.json','w'))
