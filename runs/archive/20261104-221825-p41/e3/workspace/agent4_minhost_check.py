import json,sys,itertools,random,time,functools
from collections import Counter
sys.path.insert(0,'workspace');from agent4_fastcert import fastcert

def maximal(fs):
 ans=[]
 for f in sorted(set(fs),key=int.bit_count,reverse=True):
  if not any(f&g==f for g in ans):ans.append(f)
 return tuple(sorted(ans))
def hdel(H,s):
 return maximal(g for f in H for g in ([f]if f&s!=s else[f^(1<<v)for v in range(s.bit_length())if s>>v&1]))
def hlk(H,s):return maximal(f^s for f in H if f&s==s)
@functools.lru_cache(None)
def minfaces(fs,k):
 q=fs[0].bit_count();rs=Counter(f^(1<<v)for f in fs for v in range(f.bit_length())if f>>v&1)
 for size in range(1,min(k+1,q)+1):
  cand={sum(1<<v for v in vs)for f in fs for vs in itertools.combinations([v for v in range(f.bit_length())if f>>v&1],size)};good=[]
  for s in cand:
   co=[f for f in fs if f&s==s];de=tuple(f for f in fs if f&s!=s)
   if not de or any(rs[f^(1<<v)]==1 for f in co for v in range(s.bit_length())if s>>v&1):continue
   lk=tuple(sorted(f^s for f in co))
   if fastcert(de,k)and fastcert(lk,k):good.append((s,de,lk))
  if good:return good
 return []
seen=set();nodes=0;worst=100

def visit(fs,H,path):
 global nodes,worst
 key=(fs,H)
 if key in seen:return
 seen.add(key);nodes+=1;q=fs[0].bit_count();slack=min(map(int.bit_count,H))-q
 if slack<worst:worst=slack;print('newslack',slack,'nodes',nodes,'q',q,'facets',len(fs),flush=True)
 if slack< -1:
  print('COUNTER',fs,H,path,flush=True);json.dump({'facets':fs,'host':H,'path':path},open('workspace/agent4_minhost_counter.json','w'));raise SystemExit
 if len(fs)==1:return
 choices=minfaces(fs,1)
 assert choices
 for s,de,lk in choices:
  visit(de,hdel(H,s),path+[('del',s)])
  visit(lk,hlk(H,s),path+[('link',s)])
G=tuple(sorted(json.load(open('workspace/agent2_gluecounter.json'))['G']))
for name,fs in [('G',G),('OPS',tuple(sorted({f|128 for f in G}|{f|1 for f in G if not(f&1)})))]:
 V=0
 for f in fs:V|=f
 print('start',name,len(fs),flush=True);visit(fs,(V,),[]);print('done',name,nodes,worst,flush=True)
open('workspace/agent4_minhost_check.py','w').write(open(__file__).read())
