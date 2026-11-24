import sys
sys.path.insert(0,'workspace')
from agent2_decomp import witness
from agent2_completion import complete_facets,masks
from functools import reduce

def check():
 count=steps=0
 for n in range(3,6):
  for r in range(3,n+1):
   vertices=[1<<v for v in range(n)]
   ff=masks(vertices,r)
   for bits in range(1,1<<len(ff)):
    fs=frozenset(f for j,f in enumerate(ff) if bits>>j&1)
    if sum(vertices)!=reduce(int.__or__,fs):continue
    for k in [1,2]:
     if witness(fs,k) is None:continue
     buffs=[1<<v for v in range(n,n+r-3)]
     order=complete_facets(fs,k,vertices,buffs)
     current=fs
     for f in order:
      assert f not in current
      current=current|{f}
      assert witness(current,k) is not None
      steps+=1
     assert current==frozenset(masks(vertices+buffs,r))
     count+=1
 return count,steps

if __name__=='__main__':print(check())
