import os
for id in ['e2','e3']:
 root='experiments/'+id
 print(root,os.path.exists(root))
 if os.path.exists(root):
  for dp,ds,fs in os.walk(root):
   for f in fs:
    if 'standalone' in f or 'selfcontained' in f or 'lower_universal' in f:print(os.path.join(dp,f))
