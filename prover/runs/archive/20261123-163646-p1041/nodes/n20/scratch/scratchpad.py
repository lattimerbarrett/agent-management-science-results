import os
for folder in ['experiments/e1','experiments/e2']:
 for f in os.listdir(folder):
  if f.endswith(('.py','.md','.txt')):
   txt=open(folder+'/'+f).read()
   if any(s in txt.lower() for s in ['kasami','azumi','canonical forms','kta']):
    lines=[l for l in txt.splitlines() if any(s in l.lower() for s in ['kasami','azumi','canonical forms','kta'])]
    print(f,'\n'.join(lines)[:1800])
