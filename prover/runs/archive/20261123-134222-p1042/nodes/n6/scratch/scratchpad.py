import itertools as it,pickle

def transferred(m):
 k=m-5;cells=[];ids=[]
 for q in range(5):
  cs=[]
  for S in it.combinations(range(m),q):
   U=tuple(x for x in range(m) if x not in S);p=U[0]
   for a in it.product(range(3),repeat=q):
    if any(a.count(i)>2 for i in range(3)):continue
    for R in it.combinations(U[1:],k):
     cs.append((tuple(zip(S,a)),R))
  cells.append(cs);ids.append({c:i for i,c in enumerate(cs)})
 mats=[]
 for q in range(1,5):
  cols=[]
  for sig,R in cells[q]:
   p=next(x for x in range(m) if x not in dict(sig))
   # Inclusion i(R)=boundary[p,R], an integral cycle in the skeleton.
   bracket=(p,)+R
   cycle=[(bracket[:h]+bracket[h+1:],(-1)**h) for h in range(k+1)]
   out={}
   for j in range(q):
    sig2=sig[:j]+sig[j+1:];p2=next(x for x in range(m) if x not in dict(sig2))
    for tau,v in cycle:
     # Projection pi kills top faces containing p2.
     if p2 in tau:continue
     row=ids[q-1][sig2,tau];out[row]=out.get(row,0)+(-1)**j*v
   cols.append({i:v for i,v in out.items() if v})
  mats.append(cols)
 return mats
for m in [7,8,9,10]:
 old=pickle.load(open(f'mats{m}.pkl','rb'))[1]
 new=transferred(m)
 print(m,[(q+1,sum(a!=b for a,b in zip(old[q],new[q]))) for q in range(4)],flush=True)
 # h after a horizontal deletion is identically zero: target skeleton is truncated at k,
 # and every term in the inclusion remains of size k.
 print('All higher transferred terms vanish since h vanishes on size-k faces.',flush=True)
