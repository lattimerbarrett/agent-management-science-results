from pathlib import Path
import json
# Every edge of length ell is either absent or carries integer current1/2.
a=10;budget=6*(a-1)
dp=[-10**6]*(budget+1);dp[0]=0
for ell in range(1,a):
 for _ in range(a-ell):
  nd=dp.copy()
  for c,v in enumerate(dp):
   if v<0:continue
   for j in [1,2]:
    if c+j*ell<=budget:nd[c+j*ell]=max(nd[c+j*ell],v+j*j)
  dp=nd
print('Exact knapsack max energy numerator',max(dp),'overbudget',budget)
assert max(dp)==69
Path('workspace/d5_tail10_knapsack_agent1.json').write_text(json.dumps({'a':a,'budget':budget,'max_energy_numerator':max(dp),'denominator':36}))
