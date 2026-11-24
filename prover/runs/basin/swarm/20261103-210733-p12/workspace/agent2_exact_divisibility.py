import sys,json,pickle,time,os
sys.path.insert(0,'workspace')
import agent2_pointed_fz as T
from functools import lru_cache
from collections import Counter
from itertools import product
from math import comb
from sage.all import matrix,QQ,vector
P=T.P;start=time.time()

def qrows(h,d):
 idx={x:i for i,x in enumerate(T.basis(d))}
 for r in range(1,d+1):
  for a in (0,1):
   for sz in range(min(12,3*r-h-a-1)+1):
    if (3*r-h-1-a-sz)%2:continue
    for sig in T.F.partitions(sz):
     if any(s%3==2 for s in sig):continue
     rr={}
     for t in range(r+1):
      for q,c in T.unrel(h,r-t,sig).items():rr[(q,t)]=c*(T.F.A if a==0 else T.F.B)[t]
     for ex,ps in T.basis(d-r):
      row=[QQ(0)]*len(idx)
      for (kp,t),c in rr.items():row[idx[(tuple(sorted(kp+ex,reverse=True)),t+ps)]]=QQ(str(c))
      yield row
@lru_cache(None)
def factor(h,d):
 path='workspace/agent2_exactfactor_%02d_%02d.pkl'%(h,d)
 if False and os.path.exists(path):return pickle.load(open(path,'rb'))
 n=len(T.basis(d))
 if d>h-1:out={'basis':T.basis(d),'free':[],'red':[[] for _ in range(n)],'dim':0}
 else:
  piv={};selected=[]
  for qr in qrows(h,d):
   row=[int(x.numerator()%P)*pow(int(x.denominator()%P),-1,P)%P for x in qr]
   for j in range(n):
    v=row[j]
    if not v:continue
    if j in piv:row=[(x-v*y)%P for x,y in zip(row,piv[j])]
    else:
     inv=pow(v,-1,P);piv[j]=[x*inv%P for x in row];selected.append(qr);break
  E=matrix(QQ,selected,ncols=n).echelon_form() if selected else matrix(QQ,0,n)
  pc=E.pivots();assert len(pc)==len(piv)
  free=[j for j in range(n) if j not in pc];red=[]
  for j in range(n):
   if j in pc:
    i=pc.index(j);red.append([-E[i,k] for k in free])
   else:red.append([QQ(int(j==k)) for k in free])
  out={'basis':T.basis(d),'free':free,'red':red,'dim':len(free)}
 pickle.dump(out,open(path,'wb'));return out
@lru_cache(None)
def psi(h,d):
 a=factor(h,d);b=factor(h,d+1);idx={v:i for i,v in enumerate(b['basis'])}
 return [b['red'][idx[(a['basis'][j][0],a['basis'][j][1]+1)]] for j in a['free']]
@lru_cache(None)
def splits(a):
 c=Counter(a);ks=tuple(c);cs=tuple(c[k] for k in ks);out=[]
 for vv in product(*(range(v+1) for v in cs)):
  x=tuple(k for k,v in zip(ks,vv) for _ in range(v));y=tuple(k for k,c0,v in zip(ks,cs,vv) for _ in range(c0-v));z=1
  for c0,v in zip(cs,vv):z*=comb(c0,v)
  out.append((x,y,z))
 return out

def layout(a,b,d):
 keys=[]
 for i in range(d+1):
  for x in range(factor(a,i)['dim']):
   for y in range(factor(b,d-i)['dim']):keys.append((i,x,y))
 return keys,{k:i for i,k in enumerate(keys)}
def run(a):
 b=25-a;dom,di=layout(a,b,11);cod,ci=layout(a,b,12)
 print('factors',a,len(dom),len(cod),time.time()-start,flush=True)
 M=matrix(QQ,len(cod),len(dom),sparse=False)
 for j,(d,x,y) in enumerate(dom):
  for i,c in enumerate(psi(a,d)[x]):
   if c:M[ci[(d+1,i,y)],j]+=c
  for i,c in enumerate(psi(b,11-d)[y]):
   if c:M[ci[(d,x,i)],j]+=c
 V=vector(QQ,len(cod));p=json.load(open('workspace/agent2_Pgood.json'))
 for part,coeff in p['terms']:
  c0=QQ(coeff)
  for x,y,mult in splits(tuple(part)):
   d=sum(x)
   if d>a-1 or 12-d>b-1:continue
   fa=factor(a,d);fb=factor(b,12-d)
   ra=fa['red'][fa['basis'].index((x,0))];rb=fb['red'][fb['basis'].index((y,0))]
   for i,c in enumerate(ra):
    if c:
     for j,e in enumerate(rb):
      if e:V[ci[(d,i,j)]]+=c0*mult*c*e
 print('solving',a,time.time()-start,flush=True)
 sol=M.solve_right(V);assert M*sol==V
 pickle.dump({'M':M,'target':V,'solution':sol,'domain':dom,'codomain':cod},open('workspace/agent2_exact_divisibility_%02d.pkl'%a,'wb'))
 print('EXACT SUCCESS',a,time.time()-start,flush=True)
 return {'split':a,'shape':M.dimensions(),'exact_solution':True}
if __name__=='__main__':
 out=[]
 for a in range(1,13):
  out.append(run(a));json.dump(out,open('workspace/agent2_exact_divisibility.json','w'))
