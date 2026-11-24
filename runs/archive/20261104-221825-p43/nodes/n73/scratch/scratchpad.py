import os
for root,dirs,files in os.walk('experiments/e3'):
 for f in files:
  if f.endswith(('.md','.py','.txt')): print(os.path.join(root,f))
