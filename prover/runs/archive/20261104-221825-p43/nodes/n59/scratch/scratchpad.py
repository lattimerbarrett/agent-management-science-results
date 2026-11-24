import os
for e in ['e1','e2','e3']:
 p='experiments/'+e
 print(e,os.path.exists(p))
 if os.path.exists(p):
  for root,ds,fs in os.walk(p):
   for f in fs:
    if f.endswith(('.md','.txt')): print(os.path.join(root,f))
