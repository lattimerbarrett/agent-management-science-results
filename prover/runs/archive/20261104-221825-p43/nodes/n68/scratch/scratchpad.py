import os
p='experiments/e3'
for root,dirs,files in os.walk(p):
 for f in files:
  if f.endswith(('.md','.txt')): print(os.path.join(root,f))
