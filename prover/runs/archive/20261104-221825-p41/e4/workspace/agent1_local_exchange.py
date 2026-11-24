import sys,random
sys.path.insert(0,'workspace')
from agent3_checker import subsets
from agent1_shellability import restriction,faces
from functools import lru_cache
from itertools import combinations

def addable(C,F):
 # Efficient unique-minimal-nonface test via covered-ridge labels.
 R=sum(v for v in subsets(F,1) if (F^v) in C[1])
 return R not in C[1]
def state(fs):return (frozenset(fs),frozenset(faces(fs)))

def local_search(fs,A,B,U,m):
 target=tuple(subsets(U,m))
 @lru_cache(None)
 def go(current):
  if B in current:return ()
  C=state(current)
  for f in target:
   if f in current or not addable(C,f):continue
   ans=go(frozenset(current|{f}))
   if ans is not None:return (f,)+ans
  return None
 return go(frozenset(fs|{A}))

from pathlib import Path
source=Path('scratchpad.py').read_text().split('