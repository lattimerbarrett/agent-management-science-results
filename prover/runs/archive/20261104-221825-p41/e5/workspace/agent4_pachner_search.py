import sys,random,time,signal,json
from pathlib import Path
from itertools import combinations
from collections import Counter
sys.path.insert(0,'workspace');from a3_fastkd import kd
random.seed(31415)
class Limit(Exception):pass
def handler(a,b):raise Limit
signal.signal(signal.SIGALRM,handler)
def test(fs,k,seconds=.2):
 signal.setitimer(signal.ITIMER_REAL,seconds)
 try:return kd(tuple(sorted(fs)),k)
 except Limit:return None
 finally:signal.setitimer(signal.ITIMER_REAL,0)
def submasks(f,k):return [sum(1<<v for v in cc) for cc in combinations([v for v in range(f.bit_length()) if f>>v&1],k)]
def moves(fs):
 out=[];tri=Counter(h for f in fs for h in submasks(f,3));edges=Counter(h for f in fs for h in submasks(f,2))
 for h,c in tri.items():
  if c!=2:continue
  old=[f for f in fs if f&h==h];ab=(old[0]^h)|(old[1]^h)
  if ab in edges:continue
  out.append((old,[ab|g for g in submasks(h,2)]))
 for h,c in edges.items():
  if c!=3:continue
  old=[f for f in fs if f&h==h];tau=0
  for f in old:tau|=f^h
  if tau.bit_count()!=3 or tau in tri:continue
  out.append((old,[tau|(1<<v) for v in range(h.bit_length()) if h>>v&1]))
 return out
n=12;universe=[sum(1<<v for v in cc) for cc in combinations(range(n),4)]
start=time.time();scanned=0;accepted=0;unknown=0;best=999
for trial in range(10000):
 fs={31^(1<<v) for v in range(5)}
 for v in range(5,n):
  f=random.choice(tuple(fs));fs.remove(f);fs.update((1<<v)|h for h in submasks(f,3))
 for step in range(500):
  choices=moves(fs)
  if not choices:break
  old,new=random.choice(choices);gs=(fs-set(old))|set(new);yes=test(gs,1)
  if yes:fs=gs;accepted+=1
  elif yes is None:unknown+=1
  if step%20==0:
   scanned+=1;tri=set(h for f in fs for h in submasks(f,3));edges=set(h for f in fs for h in submasks(f,2))
   sat={g for g in universe if all(h in tri for h in submasks(g,3))}
   legal=[];safe=False
   for g in universe:
    if g in sat:continue
    rr=[h for h in submasks(g,3) if h in tri]
    allfaces=[h for h in submasks(g,2) if h in edges]+[1<<v for v in range(n) if g>>v&1]
    if rr and all(any(h&r==h for r in rr) for h in allfaces):
     legal.append(g)
     if len(rr)<=2:safe=True;break
   if not safe and len(legal)<best:best=len(legal);print('best',best,'spherefacets',len(fs),'sat',len(sat),'scanned',scanned,'time',time.time()-start,flush=True)
   if not safe and test(sat,0) is False:
    good=False;known=True
    for g in legal:
     yes=test(sat|{g},1,.5)
     if yes:good=True;break
     if yes is None:known=False;break
    if known and not good:
     print('FOUND',sat,flush=True);Path('workspace/a4_pachner_trap.json').write_text(json.dumps(sorted(sat)));raise SystemExit
  if time.time()-start>100:break
 if time.time()-start>100:break
print('done accepted',accepted,'scanned',scanned,'unknown',unknown,'best',best,'time',time.time()-start,flush=True)
Path('workspace/agent4_pachner_search.py').write_text(Path(__file__).read_text())
