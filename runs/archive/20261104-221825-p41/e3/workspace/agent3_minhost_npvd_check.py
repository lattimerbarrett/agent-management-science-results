import json,collections,sys,functools,time,signal,itertools
from sage.all import SimplicialComplex,GF
sys.path.insert(0,'workspace')
from agent3_check import maximal
from agent4_fastcert import fastcert
class TimedOut(Exception):pass
def alarm(sig,frame):raise TimedOut()
signal.signal(signal.SIGALRM,alarm)
@functools.lru_cache(None)
def npvd(H):
 if len(H)<=1:return True
 V=0
 for h in H:V|=h
 for v in range(V.bit_length()):
  b=1<<v
  if not V&b:continue
  dh=maximal(h&~b for h in H);lh=maximal(h&~b for h in H if h&b)
  if not set(dh)&set(lh) and npvd(dh) and npvd(lh):return True
 return False
@functools.lru_cache(None)
def notcm(fs):
 r=fs[0].bit_count()
 if r<=1:return False
 K=SimplicialComplex([[v for v in range(20) if f>>v&1] for f in fs])
 # Reisner test all links, stopping as soon as obstruction appears.
 for z in range(r-1):
  faces=set(tuple(c) for f in fs for c in itertools.combinations([v for v in range(20) if f>>v&1],z))
  for face in faces:
   L=K if not face else K.link(face)
   h=L.homology(base_ring=GF(2))
   if any(h[i].dimension()>0 for i in range(r-z-1)):return True
 return False

def convert(c):return ('simplex',c[1]) if c[0]=='s' else ('shed',c[1],convert(c[2]),convert(c[3]))
visited=stops=prunes=0

def walk(fs,H,c,path=()):
 global visited,stops,prunes
 visited+=1
 r=fs[0].bit_count()
 common=H[0]
 for h in H:common &= h
 if common.bit_count()<r-2:return {'path':path,'facets':fs,'host':H,'kind':'fewcones','conevertices':common}
 if min(h.bit_count() for h in H)<r-1:return {'path':path,'facets':fs,'host':H,'kind':'smallfacet'}
 if c[0]=='simplex':return None
 s=c[1]
 if s.bit_count()>1:
  ridges=collections.Counter(f^(1<<v) for f in fs for v in range(f.bit_length()) if f>>v&1)
  pure=[v for v in range(20) if any(f>>v&1 for f in fs) and all(ridges[f^(1<<v)]>1 for f in fs if f>>v&1)]
  unknown=False
  for v in pure:
   vs=1<<v;ds=tuple(sorted(f for f in fs if not f&vs));ls=tuple(sorted(f^vs for f in fs if f&vs))
   if notcm(ds):prunes+=1;continue
   try:
    signal.setitimer(signal.ITIMER_REAL,2);dc=fastcert(ds,1);lc=fastcert(ls,1) if dc is not None else None
   except TimedOut:unknown=True;continue
   finally:signal.setitimer(signal.ITIMER_REAL,0)
   if dc is not None and lc is not None:s=vs;c=('shed',vs,convert(dc),convert(lc));break
  else:
   if unknown:stops+=1;return None
 dh=maximal([h for h in H if h&s!=s]+[h^(1<<v) for h in H if h&s==s for v in range(s.bit_length()) if s>>v&1]);lh=maximal(h^s for h in H if h&s==s)
 ds=tuple(f for f in fs if f&s!=s);ls=tuple(sorted(f^s for f in fs if f&s==s))
 return walk(ds,dh,c[2],path+(('d',s),)) or walk(ls,lh,c[3],path+(('l',s),))
D=json.load(open('workspace/agent2_corridor_trap_K1_certified.json'));start=time.time();ans=walk(tuple(D['facets']),((1<<20)-1,),D['k1certificate'])
print('RESULT',ans,'visited',visited,'stops',stops,'CMprunes',prunes,'seconds',time.time()-start,'cache',npvd.cache_info(),flush=True)
if ans:json.dump(ans,open('workspace/agent3_minhost_npvd_bad.json','w'))
open('workspace/agent3_minhost_npvd_check.py','w').write(open(__file__).read())
