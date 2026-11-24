import os
for dp,ds,fs in os.walk('experiments/e2'):
 for fn in fs:
  if 'proper_Cstar2' in fn:
   print(os.path.join(dp,fn));print(open(os.path.join(dp,fn)).read())
