import os
for e in ['e2','e3','e4']:
 p='experiments/'+e+'/workspace'
 if not os.path.isdir(p):p='experiments/'+e
 print(e,p,os.listdir(p)[:100])
