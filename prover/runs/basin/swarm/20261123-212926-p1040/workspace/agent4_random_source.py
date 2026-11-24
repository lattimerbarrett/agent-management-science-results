import random,time,pickle,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
from agent2_source_defect import load,defect
from agent2_source_relations import cat,inv,cm
G=[('C',i,j) for i in range(3) for j in range(3) if i!=j]+[('M',i,j,k) for i,j,k in [(0,1,2),(1,0,2),(2,0,1)]]
U=((1,),(2,),(3,))
def endpoint(w):
 A=U
 for x in w:
  typ,i,*args=G[abs(x)-1];B=list(A)
  if typ=='C':
   j=args[0];v=A[j] if x>0 else inv(A[j]);B[i]=cat(v,A[i],inv(v))
  else:
   j,k=args;v=cm(A[j],A[k]);B[i]=cat(v if x>0 else inv(v),A[i])
  A=tuple(B)
 return A
if __name__=='__main__':
 random.seed(71325);base=Path(__file__).parent;B=load();seen={};hits=[];coll=0;t=time.time()
 for trial in range(500000):
  w=[]
  for i in range(6):
   x=random.randrange(1,19);x=x if x<10 else -(x-9)
   while w and x==-w[-1]:
    x=random.randrange(1,19);x=x if x<10 else -(x-9)
   w.append(x)
  w=tuple(w);A=endpoint(w)
  if A in seen:
   v=seen[A]
   if v==w:continue
   coll+=1;r=cat(w,inv(v));d=defect(r,B)
   if any(d.values()):
    assert endpoint(r)==U
    hits.append(r);print('NEW ACTUAL RELATION',r,{p:len(v) for p,v in d.items()},flush=True)
    (base/'agent4_random_source_hits.json').write_text(json.dumps(hits))
    for p,v in d.items():
     from agent2_source_defect import insert
     insert(B[p],v,p)
  else:seen[A]=w
  if trial%50000==0:print('trial',trial,'seen',len(seen),'coll',coll,'hits',len(hits),'sec',time.time()-t,flush=True)
 print('FINAL',len(seen),coll,len(hits),time.time()-t,flush=True)
 (base/'agent4_random_source_status.json').write_text(json.dumps({'seen':len(seen),'collisions':coll,'hits':len(hits),'seconds':time.time()-t}))
