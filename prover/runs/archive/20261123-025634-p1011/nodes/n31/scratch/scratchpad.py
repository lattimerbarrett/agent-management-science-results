import os,re
for base in ['experiments/e1','experiments/e2','experiments/e3']:
 for root,ds,fs in os.walk(base):
  if 'boundary_yamabe_verified' in root:continue
  for f in fs:
   if f.endswith(('.md','.txt')):
    p=os.path.join(root,f);s=open(p,errors='replace').read()
    for line in s.splitlines():
     if re.search(r'(compactness|theorem)',line,re.I) and re.search(r'(20|21|22|23|24)',line):print(p,line[:1200])
