from pathlib import Path
s=Path('workspace/agent3_fz25.py').read_text().split('cols=parts(N);')[0]
s=s.replace('range(1,11)','range(1,37)').replace('def H(sig):','def H(sig,k0):').replace('(2*g-2 if n==0 else 1)','(k0 if n==0 else 1)').replace('H(tuple(sorted(rest)))','H(tuple(sorted(rest)),k0)')
exec(s)
import time,json
prime=1000000007;start=time.time()
def mod(x):return int(x.numerator%prime)*pow(int(x.denominator%prime),prime-2,prime)%prime
records=[];failed=[]
for h in range(2,25):
 H.cache_clear()
 for d in range((h+1)//2,min(12,h-1)+1):
  cols=parts(d);ix={p:i for i,p in enumerate(cols)};E={};count=0
  def add(row):
   for p,r in E.items():
    if row[p]:
     c=row[p];row[:]=[(a-c*b)%prime for a,b in zip(row,r)]
   p=next((i for i,x in enumerate(row) if x),None)
   if p is not None:
    iv=pow(row[p],prime-2,prime);E[p]=[x*iv%prime for x in row]
  for r in range(1,d+1):
   for a in range(2):
    for wt in range(3*r-h-a):
     if (r+wt+a-h+1)%2:continue
     for sig in parts(wt):
      if any(x%3==2 for x in sig):continue
      rel={p:mod(x) for p,x in H(sig,2*h-1).items() if sum(p)==r}
      for extra in parts(d-r):
       row=[0]*len(cols)
       for p,x in rel.items():row[ix[tuple(sorted(p+extra))]]=x
       add(row);count+=1
       if len(E)==len(cols):break
      if len(E)==len(cols):break
     if len(E)==len(cols):break
    if len(E)==len(cols):break
   if len(E)==len(cols):break
  records.append((h,d,len(cols),len(E),count))
  if len(E)<len(cols):failed.append(records[-1])
  print('framed h,d',h,d,'rank',len(E),'/',len(cols),'rows',count,'sec',time.time()-start,flush=True)
print('FRAMED ACTUAL FZ VANISHING exceptions',failed,flush=True)
json.dump({'prime':prime,'records':records,'exceptions':failed},open('workspace/agent2_framed_actual_fz25.json','w'))
if Path(__file__).name=='scratchpad.py':Path('workspace/agent2_framed_actual_fz25.py').write_text(Path(__file__).read_text())
