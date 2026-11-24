from pathlib import Path
s=Path('workspace/agent1_negative_spin25.py').read_text();s=s[:s.index('rows=[]')]
s=s.replace(" print('S',n,len(S[-1]),flush=True)",' pass')
exec(compile(s,'negspin','exec'),globals())
Qseries=[]
for n in range(NN+1):
 out={}
 for a,v in C.items():
  for b,w in S[n].items():
   if sum(a)+sum(b)<=D:
    key=tuple(sorted(a+b));out[key]=(out.get(key,0)+v*w)%p
 Qseries.append(out)
for r in range(1,10):
 for n in range((36+r)//2+1,NN+1):
  row=[0]*len(cols)
  for u in range(n):
   k=u+1
   for e in range(14-r):
    coeff=k*Ls[k][e+k-1]*(-1)**(k-1)%p
    if not coeff:continue
    m=e+r-1
    if m==0:coeff=coeff*48%p
    for part,v in Qseries[n-1-u].items():
     if sum(part)+m==D:
      key=tuple(sorted(part+((m,) if m else ())))
      row[ix[key]]=(row[ix[key]]+coeff*v*factorial(n-1))%p
  new=add(row)
  print('mark K^',r,'n',n,'new?',new,'rank',len(pivs))
if Path(__file__).name=='scratchpad.py':Path('workspace/agent1_negative_spin_marked25.py').write_text(Path(__file__).read_text())
