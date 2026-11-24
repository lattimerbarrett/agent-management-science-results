import itertools,time,collections,json
from pathlib import Path
f24={x for x in range(64) if ((x&3)==3)^((x&12)==12)}
mons=[sum(1<<i for i in I) for k in range(4) for I in itertools.combinations(range(8),k)];cols=[sum((x&m==m)<<j for j,m in enumerate(mons)) for x in range(256)]
def span(bs,sh=0):
 out=[sh]
 for b in bs:out +=[x^b for x in out]
 return out
stats=collections.Counter();bad=[];count=0;t=time.time()
for pivs in itertools.combinations(range(6),2):
 free=[(i,j) for i in range(2) for j in range(pivs[i]+1,6) if j not in pivs]
 for bits in range(1<<len(free)):
  bs=[1<<p for p in pivs]
  for k,(i,j) in enumerate(free):
   if bits>>k&1:bs[i]^=1<<j
  V=span(bs);covered=set()
  for sh in range(64):
   if sh in covered:continue
   W={x^sh for x in V};covered|=W;I=len(W&f24);count+=1
   if I%2==0:continue
   A={x^y for x in W for y in (0,64,128,192)};U=A|f24;bas={};K=[]
   for x in U:
    v=cols[x]
    while v:
     p=v.bit_length()-1
     if p not in bas:bas[p]=v;break
     v^=bas[p]
    if not v:K.append(x)
   order=sorted(bas,reverse=True);classes=collections.Counter()
   for x in range(256):
    if x in U:continue
    v=cols[x]
    for p in order:
     if v>>p&1:v^=bas[p]
    classes[v]+=1
   key=(I,len(K),classes[0],max(classes.values()));stats[key]+=1
   good=(len(K)==2 and classes[0]==0 and (len(U)==39 or max(classes.values())==1))
   if not good:bad.append({'W':sorted(W),'I':I,'dim':len(K),'zero':classes[0],'maxclass':max(classes.values())})
print('COUNT',count,'stats',dict(stats),'bad',len(bad),'seconds',time.time()-t,flush=True)
json.dump(bad,open('workspace/agent2_oldD_f24_bad.json','w'))
Path('workspace/agent2_oldD_f24_check.py').write_text(Path('scratchpad.py').read_text())
