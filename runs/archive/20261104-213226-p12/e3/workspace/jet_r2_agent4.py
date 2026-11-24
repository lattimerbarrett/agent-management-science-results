import itertools,math,functools,time,json
from collections import Counter,defaultdict
P=1000003;G=25;R=2;MAX=12
@functools.lru_cache(None)
def local(s):
 out={(0,0):1}
 for a in range(s):
  new=defaultdict(int)
  for (u,v),c in out.items():
   new[u,v]+=c;new[u+1,v]+=c*(R+a);new[u,v+1]-=c
  out=dict(new)
 return out
@functools.lru_cache(None)
def mergecoef(weights,b):
 # positive multiplicities, sign from diagonal self intersection
 return (-1)**(b-len(weights))*sum((-1)**(len(weights)-len(J))*sum(J)**b for n in range(len(weights)+1) for J in itertools.combinations(weights,n))%P
calls=0;start=time.time()
@functools.lru_cache(None)
def push(state):
 global calls
 calls+=1
 if calls%10000==0:print('states',calls,'cache',push.cache_info(),'sec',time.time()-start,flush=True)
 if not state:return {():1}
 if sum(max(e-1,0) for s,e in state)>MAX:return {}
 # remove maximal jet length to leave smaller jets
 s,e=state[-1];rest=state[:-1];group=Counter(rest);types=list(group);counts=[group[t] for t in types]
 transitions=defaultdict(int)
 # tuple state, optional kappa index (None for merges)
 for (a,b),c in local(s).items():
  if b==0:
   k=e+a-1
   if 0<=k<=MAX:transitions[rest,k]+=c
 for sel in itertools.product(*[range(min(c,s)+1) for c in counts]):
  l=sum(sel)
  if l==0 or l>s:continue
  weights=tuple(w for (w,h),n in zip(types,sel) for _ in range(n));exp=sum(h*n for (w,h),n in zip(types,sel))
  mult=math.prod(math.comb(c,n) for c,n in zip(counts,sel))
  left=[t for t,c,n in zip(types,counts,sel) for _ in range(c-n)]
  for (a,b),c in local(s).items():
   if b<l:continue
   newe=exp+e+a+b-l
   if newe>MAX+1:continue
   newstate=tuple(sorted(left+[(sum(weights),newe)]))
   transitions[newstate,None]+=c*mult*mergecoef(weights,b)
 out=defaultdict(int)
 for (sub,k),c in transitions.items():
  c%=P
  if not c:continue
  for mon,v in push(sub).items():
   if k==None:dest=mon;factor=1
   elif k==0:dest=mon;factor=48
   elif sum(mon)+k<=MAX:dest=tuple(sorted(mon+(k,)));factor=1
   else:continue
   out[dest]=(out[dest]+c*v*factor)%P
 return dict(out)
initial=tuple(sorted([(7,0)]*13+[(6,0)]))
out=push(initial)
print('DONE',calls,time.time()-start,len(out),flush=True)
json.dump({','.join(map(str,k)):v for k,v in out.items()},open('workspace/jet_r2_97_agent4.json','w'))
