from itertools import combinations
from pathlib import Path
# Count upsets in T3 x T3 via central rank orientations (equiv split selfdual families).
groups=[{0,1},{2,3,4},{5,6,7}]
full=(1<<8)-1
def safe(a):
 return all(a & sum(1<<i for i in g) and ((full^a)&sum(1<<i for i in g)) for g in groups)
safe_sets=[a for a in range(256) if safe(a)]
low=[a for a in safe_sets if a.bit_count()==3]
pairs=[(a,full^a) for a in safe_sets if a.bit_count()==4 and a<(full^a)]
assert len(low)==18 and len(pairs)==18
# A low triple can be chosen iff every safe4-superset is chosen. Encode forced orientations.
requirements=[]
for a in low:
 ones=zeros=0
 for i,(b,c) in enumerate(pairs):
  if a&b==a: ones|=1<<i
  if a&c==a: zeros|=1<<i
 assert not ones&zeros
 requirements.append((ones,zeros))
count=0
for mask in range(1<<18):
 elig=[a for a,(one,zero) in zip(low,requirements) if mask&one==one and mask&zero==0]
 assert all(a&b for a,b in combinations(elig,2))
 count+=1<<len(elig)
print('fixed capacity',count,'double',2*count)
# Root label meets every safe set, is rainbow for group coloring.
A=sum(1<<i for i in [0,1,2,5])
assert all(A&a for a in safe_sets)
assert all(A&sum(1<<i for i in g) for g in groups)
print('root compatibility verified on all',len(safe_sets),'safe sets')
