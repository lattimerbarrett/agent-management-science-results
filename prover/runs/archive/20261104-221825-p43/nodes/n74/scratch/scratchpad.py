import os
for root,ds,fs in os.walk('experiments/e3'):
 for f in fs:
  print(os.path.join(root,f))
