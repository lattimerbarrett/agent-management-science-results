import sys,json,time
from itertools import combinations
from pathlib import Path
sys.path.insert(0,'workspace')
from agent2_checker import *
from agent1_upper import complete as complete_upper

def union(fs):
 u=0
 for f in fs:u|=f
 return u

def complete_vd3(fs,c0):
 assert fs[0].bit_count()==4
 verify(fs,0,c0)
 if c0[0]=='simplex':return [],c0
 _,v,cd0,cl0=c0
 assert v.bit_count()==1
 D=deletion(fs,v);L=link(fs,v)
 dsteps,cd=complete_vd3(D,cd0)
 steps=[];cur=fs
 for F,cdi in dsteps:
  cur=tuple(sorted((*cur,F)));ci=('shed',v,cdi,cl0)
  verify(cur,1,ci);steps.append((F,ci))
 Dfull=tuple(sorted((*D,*(F for F,c in dsteps))))
 W=union(Dfull);cl=cl0
 for w in bits(W^union(L)):
  xy=next(s for f in L for s in subsets(f,2) if s.bit_count()==2)
  H=w|xy
  cl=('shed',w,cl,('simplex',xy))
  L=tuple(sorted((*L,H)));verify(L,1,cl)
  F=v|H;cur=tuple(sorted((*cur,F)));ci=('shed',v,cd,cl)
  verify(cur,1,ci);steps.append((F,ci))
 extra,cfinal=complete_upper(L,cl,1,[])
 for H in extra:
  L=tuple(sorted((*L,H)));cl=certificate(L,1);assert cl is not None
  F=v|H;cur=tuple(sorted((*cur,F)));ci=('shed',v,cd,cl)
  verify(cur,1,ci);steps.append((F,ci))
 if not steps:ci=('shed',v,cd,cl)
 assert set(cur)=={sum(z) for z in combinations(bits(union(fs)),4)}
 return steps,ci

if __name__=='__main__':
 Path('workspace/agent2_vd3_completion.py').write_text(Path(__file__).read_text())
 fs=tuple(json.load(open('workspace/agent3_bier_nonvd8.json'))[0]['facets'])
 c=certificate(fs,1);assert c is not None
 uv=(1<<0)|(1<<5)
 edges=[]
 for a,b in combinations([i for i in range(10) if i not in (0,5)],2):
  if any(f&((1<<0)|(1<<a)|(1<<b))==((1<<0)|(1<<a)|(1<<b)) for f in fs) and any(f&((1<<5)|(1<<a)|(1<<b))==((1<<5)|(1<<a)|(1<<b)) for f in fs):edges.append((1<<a)|(1<<b))
 prefix=[];cur=fs;out=[]
 while edges:
  if not prefix:e=edges[0]
  else:e=next(e for e in edges if e&union(prefix))
  edges.remove(e);prefix.append(e)
  cl=certificate(tuple(sorted(prefix)),1);assert cl is not None
  cur=tuple(sorted((*cur,uv|e)));ci=('shed',uv,c,cl);verify(cur,1,ci);out.append(uv|e)
 c0=certificate(cur,0);assert c0 is not None
 steps,final=complete_vd3(cur,c0);out.extend(F for F,c in steps)
 assert len(out)==180 and len(set(out))==180
 end=tuple(sorted((*fs,*out)));verify(end,1,final)
 assert set(end)=={sum(z) for z in combinations([1<<i for i in range(10)],4)}
 Path('workspace/agent2_bier_k1_completion.json').write_text(json.dumps(out))
 print('BiernonVDseed completedwith180facet additions; all180prefixk1certificatesindependentlyverified')
