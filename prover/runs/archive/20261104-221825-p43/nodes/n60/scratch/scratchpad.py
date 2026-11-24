import os
root='experiments/e3'
for p,ds,fs in os.walk(root):
 for f in fs:
  if f.endswith(('.md','.txt','.py')):
   print(os.path.join(p,f))
