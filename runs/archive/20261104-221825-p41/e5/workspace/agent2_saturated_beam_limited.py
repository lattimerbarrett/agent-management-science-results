import itertools,random,time,json,sys,signal
from pathlib import Path
sys.path.insert(0,'workspace')
from a3_fastkd import kd

def run(n=8,width=20,seconds=100):
 random.seed(892)
 def handler(signum,frame):raise TimeoutError
 signal.signal(signal.SIGALRM,handler)
 unknown=0
 def test(fs,k):
  nonlocal unknown
  signal.setitimer(signal.ITIMER_REAL,.03)
  try:return kd(fs,k)
  except TimeoutError:unknown+=1;return None
  finally:signal.setitimer(signal.ITIMER_REAL,0)
 Fs=[sum(1<<v for v in c) for c in itertools.combinations(range(n),4)]
 Ts=[sum(1<<v for v in c) for c in itertools.combinations(range(n),3)]
 Es=[sum(1<<v for v in c) for c in itertools.combinations(range(n),2)]
 ti={t:i for i,t in enumerate(Ts)};ei={e:i for i,e in enumerate(Es)}
 fb=[sum(1<<ti[f^(1<<v)] for v in range(n) if f>>v&1) for f in Fs]
 fe=[sum(1<<ei[e] for e in Es if e&f==e) for f in Fs]
 def state(tm):
  inds=[j for j,b in enumerate(fb) if tm&b==b]
  fs=tuple(Fs[j] for j in inds);canon=edge=0
  for j in inds:canon|=fb[j];edge|=fe[j]
  return canon,edge,fs
 start=time.time();beam=[(1<<len(Ts))-1];seen=set(beam);checked=nonVD=0;best=10000;records=[]
 for depth in range(len(Ts)):
  children=[]
  for tm in beam:
   for j in range(len(Ts)):
    if not(tm>>j&1):continue
    can,edge,fs=state(tm&~(1<<j))
    if can in seen:continue
    seen.add(can)
    if edge!=(1<<len(Es))-1 or not fs or test(fs,1) is not True:continue
    checked+=1
    vd=test(fs,0)
    if vd is None:continue
    nonVD+=not vd
    good=0;bad=0;fm=set(fs)
    for f,b in zip(Fs,fb):
     if f in fm or (can&b).bit_count()!=3:continue
     result=test(tuple(sorted(fs+(f,))),1)
     if result is None:break
     if result:good+=1
     else:bad+=1
    else:result=True
    if result is None:continue
    if not vd and good<best:
     best=good;rec=dict(depth=depth,facets=fs,good=good,bad=bad)
     records.append(rec);print('bestnonVD',rec,flush=True)
    if good==0:
     print('FOUND TERMINAL',fs,flush=True);Path('workspace/agent2_edge_terminal_found.json').write_text(json.dumps(fs));return
    children.append((vd,good,len(fs),random.random(),can))
    if time.time()-start>seconds:break
   if time.time()-start>seconds:break
  children.sort();beam=[x[-1] for x in children[:width]]
  print('depth',depth,'checked',checked,'nonVD',nonVD,'beam',len(beam),'seconds',time.time()-start,flush=True)
  if not beam or time.time()-start>seconds:break
 report=dict(n=n,width=width,checked=checked,nonVD=nonVD,bestnonVD=best,seconds=time.time()-start,records=records,unknown_calls=unknown)
 Path('workspace/agent2_saturated_beam_limited_report.json').write_text(json.dumps(report));return report
if __name__=='__main__':run()
