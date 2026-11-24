import sys,itertools as it,time
sys.path.insert(0,'workspace')
from agent2_compute import reduce_units

def make_deletion(m):
 q=m-4
 cells=[];ids=[]
 for k in range(5):
  cc=[]
  for cols in it.combinations(range(m+1),k):
   for rows in it.product(range(3),repeat=k):
    if any(rows.count(i)>2 for i in range(3)):continue
    f=tuple(zip(cols,rows));rem=tuple(j for j in range(m) if j not in cols)
    if len(rem)<=q:continue
    for s in it.combinations(rem[:-1],q):cc.append((f,s))
  cells.append(cc);ids.append({x:i for i,x in enumerate(cc)})
 ds=[None]
 for k in range(1,5):
  D={}
  for c,(f,s) in enumerate(cells[k]):
   olda=max(set(range(m))-{x for x,y in f})
   for p,(x,y) in enumerate(f):
    ff=f[:p]+f[p+1:]
    if (ff,s) not in ids[k-1]: continue
    newa=max(set(range(m))-{xx for xx,yy in ff});sgn=(-1)**p
    terms={s:1}
    if newa!=olda:
     for h in range(q):
      raw=s[:h]+(olda,)+s[h+1:];inv=sum(raw[i]>raw[j] for i in range(q) for j in range(i+1,q));ss=tuple(sorted(raw));terms[ss]=terms.get(ss,0)-(-1)**inv
    for ss,coef in terms.items():
     if coef:D[(ids[k-1][ff,ss],c)]=sgn*coef
  ds.append(D)
 return cells,ds

def deletion(m):
 from agent2_compute import check
 cells,ds=make_deletion(m);check(ds)
 print('DELETION',m,'sizes',list(map(len,cells)),flush=True)
 active=None
 for k in range(1,5):
  R,C=reduce_units(ds[k],len(cells[k-1]),len(cells[k]),active);active=set(C)
  print('H',k-1,'free rows',len(R),'nnz',sum(map(len,R.values())),flush=True)
  if any(R.values()):break
if __name__=='__main__':
 for m in (7,8,9):deletion(m)
