import sys,pickle,time
sys.path.insert(0,'workspace')
from agent3_exact_pointed import smooth,tail,S48
from fractions import Fraction
from collections import defaultdict
parts=S48['parts']
def mons(d,n):
 if n==2:return [(p,a,d-k-a) for k in range(d+1) for p in parts(k) for a in range(d-k+1)]
 return [(p,d-k) for k in range(d+1) for p in parts(k)]
c2=mons(13,2);c12=mons(12,1);c13=mons(13,1)
i2={m:i for i,m in enumerate(c2)};i12={m:i for i,m in enumerate(c12)};i13={m:i for i,m in enumerate(c13)}
N=len(c2);U=len(c12);V=len(c13);total=N+U+V

def row_exact(lab):
 out=defaultdict(Fraction)
 if lab[0]=='rel':
  r,ab,sig,mul=lab[1]
  for (p,aps),c in smooth(r,sig,ab).items():
   key=(tuple(sorted(p+mul[0])),)+tuple(x+y for x,y in zip(aps,mul[1:]))
   out[i2[key]]+=c
  if mul[1:]==(0,0):
   for (p,a),c in tail(r,sig,*ab).items():out[N+i12[(tuple(sorted(p+mul[0])),a)]]+=c
 elif lab[0]=='beta':
  p,a,b=lab[1]
  for aa,bb in [(a,b)]+([] if a==b else [(b,a)]):
   for key in [(p,aa+1,bb),(p,aa,bb+1)]:out[i2[key]]-=1
 elif lab[0]=='gamma':
  p,a=lab[1];out[N+i12[(p,a+1)]]=-1;out[N+U+i13[(p,a+2)]]=1
 elif lab[0]=='single':
  d,lab1=lab[1:];r,ab,sig,mul=lab1;offset=N if d==12 else N+U;idx=i12 if d==12 else i13
  for (p,aps),c in smooth(r,sig,ab).items():out[offset+idx[(tuple(sorted(p+mul[0])),aps[0]+mul[1])]]+=c
 else:raise ValueError(lab)
 return {j:c for j,c in out.items() if c}

if __name__=='__main__':
 t=time.time();P,labs,rows,fl=pickle.load(open('workspace/agent2_coupled_matrix.pkl','rb'));exact=[]
 assert total==len(rows[0])
 for i,(lab,row) in enumerate(zip(labs,rows)):
  d=row_exact(lab);exact.append(d)
  mod={j:c.numerator*pow(c.denominator,P-2,P)%P for j,c in d.items()}
  mod={j:c for j,c in mod.items() if c}
  assert mod=={j:c%P for j,c in enumerate(row) if c%P},(i,lab)
 print('ALL',len(exact),'coupled rows independently constructed EXACTLY and matchmod; time',time.time()-t)
 pickle.dump((labs,exact,total),open('workspace/agent3_coupled_exact_sparse.pkl','wb'))
 src=open(__file__).read();open('workspace/agent3_coupled_exact.py','w').write(src)
