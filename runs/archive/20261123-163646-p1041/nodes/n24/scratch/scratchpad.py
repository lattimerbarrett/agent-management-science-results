import os,json
for folder in ['experiments/e1','experiments/e2']:
 names=os.listdir(folder)
 print(folder, len(names))
 print('\n'.join(f for f in names if any(s in f.lower() for s in ['summary','conclusion','status','310','spectrum','readme','final'])))
for folder in ['experiments/e1','experiments/e2']:
 for f in os.listdir(folder):
  if f.endswith('.md'):
   t=open(folder+'/'+f).read()
   if '310' in t:
    print('\n',folder,f)
    lines=t.splitlines()
    for i,l in enumerate(lines):
     if '310' in l: print('\n'.join(lines[max(0,i-2):i+3]))
