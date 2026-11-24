import itertools,math,time,json,pickle
from sage.all import GF,matrix
from sage.coding.binary_code import weight_dist
cache={}
def block(n,cyclic):
 key=(n,cyclic)
 if key in cache:return cache[key]
 keys={};ids=[];orbs=[]
 for x in range(1<<n):
  k=min(((x>>s)|(x<<(n-s)))&((1<<n)-1) for s in range(n)) if cyclic else x.bit_count()
  if k not in keys:keys[k]=len(keys);orbs.append([])
  idx=keys[k];ids.append(idx);orbs[idx].append(x)
 H=[]
 for o in orbs:
  row=set();t=o[0]
  while True:
   z=ids[t]
   if z in row:row.remove(z)
   else:row.add(z)
   if not t:break
   t=(t-1)&o[0]
  H.append(sorted(row))
 result=(list(map(len,orbs)),[o[0].bit_count() for o in orbs],H,ids)
 cache[key]=result;return result

def run(P,flags,cut):
 data=[block(n,c) for n,c in zip(P,flags)];inds=list(itertools.product(*[range(len(d[0])) for d in data]));N=len(inds);lookup={i:k for k,i in enumerate(inds)}
 W=[math.prod(d[0][a] for d,a in zip(data,i)) for i in inds];R=[]
 for i in inds:
  if sum(d[1][a] for d,a in zip(data,i))>7:R.append(sum(1<<lookup[j] for j in itertools.product(*[d[2][a] for d,a in zip(data,i)])))
 piv={}
 for row in R+[1<<i for i,w in enumerate(W) if w>cut]:
  while row:
   p=row.bit_length()-1
   if p in piv:row^=piv[p]
   else:piv[p]=row;break
 free=[i for i in range(N) if i not in piv];basis=[]
 for i in free:
  b=1<<i
  for p in sorted(piv):
   if(piv[p]&b).bit_count()%2:b|=1<<p
  basis.append(b)
 pts=[];ids=[]
 for x in range(16384):
  t=x;key=[]
  for n,d in zip(P,data):key.append(d[3][t&((1<<n)-1)]);t>>=n
  idx=lookup[tuple(key)]
  if W[idx]<=cut:pts.append(x);ids.append(idx)
 print('START',P,flags,cut,'dim',len(basis),'length',len(pts),flush=True)
 name=''.join(map(str,P))+'_'+''.join(map(str,flags))+'_'+str(cut)
 pickle.dump((P,flags,cut,basis,pts,ids),open('workspace/agent2_mixed_'+name+'.pkl','wb'))
 if len(basis)<=31:subspaces=[basis]
 elif len(basis)==32:subspaces=[basis[:31],basis[:30]+[basis[31]],basis[:30]+[basis[30]^basis[31]]]
 else:raise ValueError('dimension')
 for B in subspaces:
  G=matrix(GF(2),[[(b>>i)&1 for i in ids] for b in B]);t=time.time();D=weight_dist(G);counts={w:D[w] if w<len(D) else 0 for w in [322,326,330,334]};print('RESULT',name,time.time()-t,counts,flush=True)
  if any(counts.values()):pickle.dump((P,flags,cut,B,pts,ids,counts),open('workspace/agent2_POSITIVE_'+name+'.pkl','wb'));return True
 return False
if __name__=='__main__':
 open('workspace/agent2_mixed_search.py','w').write(open(__file__).read())
 for P,F,C in [((6,6,1,1),(1,1,0,0),6),((6,5,3),(1,1,0),15),((6,5,2,1),(0,1,0,0),20),((6,5,3),(1,0,0),20),((6,5,3),(0,1,0),45)]:
  if run(P,F,C):break
