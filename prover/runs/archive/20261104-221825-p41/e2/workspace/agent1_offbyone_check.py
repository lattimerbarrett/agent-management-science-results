from functools import lru_cache
from itertools import combinations
from pathlib import Path

def subsets(f):
 s=f
 while s:
  yield s;s=(s-1)&f

@lru_cache(None)
def kd(F,k):
 if len(F)==1:return True
 if not F:return False
 D=F[0].bit_count()
 if any(f.bit_count()!=D for f in F):return False
 candidates={s for f in F for s in subsets(f) if s.bit_count()<=k+1}
 for s in sorted(candidates,key=lambda s:(s.bit_count(),s)):
  de=tuple(f for f in F if f&s!=s)
  co=tuple(f for f in F if f&s==s)
  if not de:continue
  if any(not any((f^v)&g==f^v for g in de) for f in co for v in subsets(s) if v.bit_count()==1):continue
  li=tuple(sorted(f^s for f in co))
  if kd(li,k) and kd(de,k):return True
 return False

def run():
 allF=[sum(1<<v for v in c) for c in combinations(range(6),4)]
 positive=0;boundary_checks=0
 for flags in range(1,1<<len(allF)):
  F=tuple(f for i,f in enumerate(allF) if flags>>i&1)
  a=kd(F,2);b=kd(F,3)
  assert a==b,(F,a,b)
  if not a:continue
  positive+=1
  ridges={f^v for f in F for v in subsets(f) if v.bit_count()==1}
  for f in allF:
   if f in F:continue
   if all((f^v) in ridges for v in subsets(f) if v.bit_count()==1):
    assert kd(tuple(sorted(F+(f,))),2)
    boundary_checks+=1
 print('Checked all',2**len(allF)-1,'nonempty pure 3-complexes on subsets of six vertices.')
 print('2-decomposable = 3-decomposable in all cases;',positive,'positive cases.')
 print('Verified',boundary_checks,'full-boundary additions preserve 2-decomposability.')
if __name__=='__main__':
 Path('workspace/agent1_offbyone_check.py').write_text(Path(__file__).read_text())
 run()
