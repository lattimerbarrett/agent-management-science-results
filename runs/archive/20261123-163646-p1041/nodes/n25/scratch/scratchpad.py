import os
for e in ['e1','e2']:
 p='experiments/'+e
 print(p,os.path.exists(p))
 if os.path.exists(p):
  print(os.listdir(p))
