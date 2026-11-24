import os,re
for e in os.listdir('experiments'):
 p='experiments/'+e
 print('\n###',e)
 for root,ds,fs in os.walk(p,followlinks=True):
  if root != p: ds[:]=[];continue
  for f in fs:
   if not f.endswith(('.md','.txt')):continue
   text=open(root+'/'+f,errors='replace').read()
   for i,line in enumerate(text.splitlines()):
    if re.search(r'Li.{0,12}Zhu|Druet|Marques|Disconzi|Khuri|known.*compactness|established.*compactness|literature',line,re.I):
     print(f'{f}:{i+1}: {line[:400]}')
