import sys,itertools,json,pathlib
sys.path.insert(0,'workspace')
from agent4_checker import dec
count=0
for n in range(4,10):
 for rank in range(2,min(n,5)+1):
  old=[sum(1<<v for v in c) for c in itertools.combinations(range(n),rank)]
  cone=[(1<<n)|sum(1<<v for v in c) for c in itertools.combinations(range(n),rank-1)]
  fs=tuple(sorted(old));assert dec(fs,0);count+=1
  for f in cone:
   fs=tuple(sorted(fs+(f,)));assert dec(fs,0);count+=1
print('auxiliary-monotonicity extension stages verified',count)
