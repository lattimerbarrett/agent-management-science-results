import networkx as nx,itertools,functools,json,time
# All bounded internal graphs with Delta<=2 and matching number<=3.
types=[(s,False) for s in range(2,8)]+[(s,True) for s in range(3,8)]
hosts=[]
def gen(start,rem,parts):
 hosts.append(tuple(parts))
 for j in range(start,len(types)):
  t=types[j]
  if t[0]//2<=rem:gen(j,rem-t[0]//2,parts+[t])
gen(0,3,[])
def ee(F):return sum(s if cyc else s-1 for s,cyc in F)
@functools.lru_cache(None)
def sub(pat,host):
 bins=[s for s,c in host];tri=[i for i,(s,c) in enumerate(host) if s==3 and c]
 # A triangle consumes an entire triangular host component.
 p=list(pat)
 for _ in range(p.count(-3)):
  if not tri:return False
  i=tri.pop();bins[i]=0
 p=sorted([x for x in p if x>0],reverse=True)
 def pack(j):
  if j==len(p):return True
  tried=set()
  for i,b in enumerate(bins):
   if b>=p[j] and b not in tried:
    tried.add(b);bins[i]-=p[j]
    if pack(j+1):return True
    bins[i]+=p[j]
  return False
 return pack(0)

coreedges=[(0,i) for i in [1,2,3,5,6,8]]+[(i,4+i) for i in range(1,5)]
colorinfos=[]
for mask in range(256):
 col=[0]+[(mask>>(i-1))&1 for i in range(1,9)]
 adj=[[] for _ in range(9)]
 for u,v in coreedges:
  if col[u]==col[v]:adj[u].append(v);adj[v].append(u)
 if max(map(len,adj))>2:continue
 comps=[];ci=[-1]*9
 for u in range(9):
  if ci[u]>=0:continue
  stack=[u];vs=[];idx=len(comps);ci[u]=idx
  while stack:
   v=stack.pop();vs.append(v)
   for w in adj[v]:
    if ci[w]<0:ci[w]=idx;stack.append(w)
  comps.append((len(vs),col[u],sum(len(adj[v]) for v in vs)//2==len(vs)))
 colorinfos.append((col,[2-len(a) for a in adj],comps,ci))
print('hosts',len(hosts),'core colorings',len(colorinfos),flush=True)

def patterns(conn):
 result=set()
 for col,cap,comps,ci in colorinfos:
  cross=[(u,v) for u,v in conn if col[u]!=col[v]]
  counts=[0]*len(comps);used=[0]*9
  def rec(k):
   if k==len(cross):
    pats=[[],[]];nu=[0,0]
    for j,(size,c,cyc) in enumerate(comps):
     s=size+counts[j]
     if s>1:pats[c].append(-3 if cyc else s);nu[c]+=s//2
    if max(nu)<=3:
     a=tuple(sorted(pats[0]));b=tuple(sorted(pats[1]));result.add((a,b));result.add((b,a))
    return
   for v in cross[k]:
    if used[v]<cap[v]:
     used[v]+=1;counts[ci[v]]+=1;rec(k+1);counts[ci[v]]-=1;used[v]-=1
  rec(0)
 return result

import random
ps=list(itertools.combinations(range(4),2))
trees=[[p for i,p in enumerate(ps) if mask>>i&1] for mask in range(64)]
random.Random(123).shuffle(trees)
seen=set();start=time.time()
for it,(ta,tb) in enumerate(itertools.product(trees,repeat=2)):
 conn=[(u+1,v+1) for u,v in ta]+[(u+5,v+5) for u,v in tb]
 pats=patterns(conn)
 frozen=frozenset(pats)
 if frozen in seen:continue
 seen.add(frozen)
 ok=[F for F in hosts if not any(not b and sub(a,F) for a,b in pats)]
 am=[sum(1<<j for j,(a,b) in enumerate(pats) if sub(a,F)) for F in ok]
 bm=[sum(1<<j for j,(a,b) in enumerate(pats) if sub(b,F)) for F in ok]
 pairs=[(i,j) for i in range(len(ok)) for j in range(i,len(ok)) if not am[i]&bm[j]]
 if not pairs:continue
 me=max(ee(ok[i])+ee(ok[j]) for i,j in pairs)
 score=lambda i,j:3.3088*max(ee(ok[i]),ee(ok[j]))+min(ee(ok[i]),ee(ok[j]))
 mw=max(score(i,j) for i,j in pairs)
 if all(score(i,j)<mw-1e-7 for i,j in pairs if ee(ok[i])+ee(ok[j])==me):
  print('FOUND',it,conn,'maxe',me,'mw',mw,flush=True)
  for i,j in pairs:
   if ee(ok[i])+ee(ok[j])==me or abs(score(i,j)-mw)<1e-7:print(' templates',ok[i],ok[j],ee(ok[i]),ee(ok[j]),flush=True)
  print('patterns',pats)
  H=nx.Graph();H.add_edges_from(coreedges)
  for u,v in conn:
   w=len(H);H.add_edges_from([(u,w),(w,v)])
  json.dump({'n':len(H),'edges':list(H.edges())},open('candidate.json','w'));break
else:print('none')
print('unique pattern sets',len(seen),'time',time.time()-start)
