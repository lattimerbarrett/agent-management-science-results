import itertools,json,pathlib,time,sys,numpy as np,collections,random
sys.path.insert(0,'workspace')
from agent3_lift_closure import veronese

def anf(S,m):
 a=np.zeros(1<<m,dtype=np.uint8);a[S]=1
 for j in range(m):
  b=a.reshape(-1,2<<(j));b[:,1<<j:]^=b[:,:1<<j]
 return [int(p) for p in np.where(a)[0]]

def kernel(cols):
 B={};K=[]
 for i,v in enumerate(cols):
  c=1<<i
  while v:
   k=v.bit_length()-1
   if k in B:v^=B[k][0];c^=B[k][1]
   else:B[k]=(v,c);break
  if not v:K.append(c)
 return K

def top_transvections(S,m,r=6,maxout=30):
 AA=anf(S,m);assert max(x.bit_count() for x in AA)==r
 top=[x for x in AA if x.bit_count()==r];masks=[sum(1<<j for j in I) for I in itertools.combinations(range(m),r)];ix={x:i for i,x in enumerate(masks)}
 D=[[0]*m for i in range(m)]
 for q in top:
  for i in range(m):
   if not q>>i&1:continue
   v=q^(1<<i)
   for j in range(m):
    if not v>>j&1:D[i][j]^=1<<ix[v|(1<<j)]
 cols=[0]*m;old=0;translates={sum(1<<(p^b) for p in S) for b in range(1<<m)};counts=collections.Counter();out=[];seen=set();start=time.time()
 for z in range(1,1<<m):
  u=z^(z>>1);flip=u^old;i=flip.bit_length()-1;old=u
  cols=[v^d for v,d in zip(cols,D[i])];KB=kernel(cols);counts['u_with_kernel'+str(len(KB))]+=1
  L=[0]
  for v in KB:L +=[l^v for l in L]
  for ell in L[1:]:
   if (u&ell).bit_count()%2:continue
   counts['transvections']+=1;H=sorted(p^(u if (p&ell).bit_count()%2 else 0) for p in S);hmask=sum(1<<p for p in H)
   if hmask in translates:counts['only_translate']+=1;continue
   if hmask in seen:continue
   seen.add(hmask);G=sorted(S+[p|(1<<m) for p in H]);counts['aperiodic_gluings']+=1
   if len(out)<maxout:
    GG=anf(G,m+1);assert max(x.bit_count() for x in GG)<=6
    Ksame=kernel([veronese(m+1,m-6)[p] for p in G])
    out.append({'m':m+1,'weight':len(G),'u':u,'ell':ell,'support':G,'samecodeK':len(Ksame) if Ksame else None})
 print('TOPGLUE',m,dict(counts),'time',time.time()-start,flush=True)
 return out,dict(counts)

if __name__=='__main__':
 S=json.load(open('workspace/agent4_triorthogonal40_walk.json'))['aperiodic'][0]['support'];out,stats=top_transvections(S,10)
 json.dump({'stats':stats,'seeds':out},open('workspace/agent1_topform_gluing80.json','w'));pathlib.Path('workspace/agent1_topform_gluing.py').write_text(pathlib.Path(__file__).read_text());print('SAVED',len(out))
