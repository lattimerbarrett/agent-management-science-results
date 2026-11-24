from fractions import Fraction as Q
from pathlib import Path
import json
cap=[(6,Q(7,10)),(7,Q(389,460)),(8,Q(34,35)),(9,Q(197,180)),(10,Q(19,20))]
mid=[(6,Q(0)),(7,Q(1,6)),(8,Q(1,4)),(9,Q(5,12)),(10,Q(1,4))]
# Dijkstra on 5 residue classes; loops may have zero weight but no negative weights.
d=[None]*5;d[0]=Q(0);paths=[None]*5;paths[0]=[]
for _ in range(5):
 for r in range(5):
  if d[r] is None:continue
  for b,c in mid:
   t=(r+b-1)%5;z=d[r]+c
   if d[t] is None or z<d[t]:d[t]=z;paths[t]=paths[r]+[b]
best=[None]*5;witness=[None]*5
for a,ca in cap:
 for b,cb in cap:
  for r in range(5):
   t=(a+b-1+r)%5;z=ca+cb-Q(1,4)+d[r]
   if best[t] is None or z<best[t]:best[t]=z;witness[t]=[a,b,paths[r]]
expected=[Q(7,5),Q(23,20),Q(149,115),Q(7,5),Q(139,90)]
assert best==expected,(best,expected)
# A generic cap eps>=6/5 cannot beat any target, nor generic middle delta>=1/2.
assert Q(6,5)+min(c for b,c in cap)-Q(1,4)>max(expected)
assert 2*min(c for b,c in cap)-Q(1,4)+Q(1,2)>max(expected)
print('residue defect minima',best,'witnesses',witness)
Path('workspace/odd_minplus_agent1.json').write_text(json.dumps({'defects':list(map(str,best)),'witnesses':witness},indent=2))
