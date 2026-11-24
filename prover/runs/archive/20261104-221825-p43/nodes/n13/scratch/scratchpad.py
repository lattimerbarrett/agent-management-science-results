import os
for team in ('e1','e2'):
 p='experiments/'+team
 print(p, os.path.isdir(p))
 if os.path.isdir(p):
  for root,dirs,files in os.walk(p):
   for f in files:
    if f.endswith('.py'):print(os.path.join(root,f))
