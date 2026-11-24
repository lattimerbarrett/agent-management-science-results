import os
for e in ['e2','e3','e4']:
 p='experiments/'+e+'/workspace'
 print(e,os.path.exists(p))
 if os.path.exists(p): print(os.listdir(p)[:25])
