import itertools,collections,random,time,json,pathlib
n=19;res={i*i%19 for i in range(1,19)};assert len(res)==9
G=[(1<<i)|sum(1<<(19+(j+i)%19) for j in res) for i in range(19)]
assert all((a&b).bit_count()%2==0 for a in G for b in G)
D=[0]*(1<<19)
for i in range(1,1<<19):D[i]=D[i^(i&-i)]^G[(i&-i).bit_length()-1]
print('Dweightenum',dict(sorted(collections.Counter(x.bit_count() for x in D).items())),flush=True)
def basis(rows):
 B={}
 for z in rows:
  while z:
   h=z.bit_length()-1
   if h in B:z^=B[h]
   else:B[h]=z;break
 return B
def null(rows):
 B=basis(rows);out=[]
 for i in range(19):
  if i in B:continue
  z=1<<i
  for h in sorted(B):
   if (B[h]&z).bit_count()%2:z^=1<<h
  out.append(z)
 return out
def independent(C,z):
 B=basis(C)
 while z:
  h=z.bit_length()-1
  if h in B:z^=B[h]
  else:return True
 return False
cache={}
def contraction(a,b):
 z=D[a]&D[b]
 if z not in cache:cache[z]=sum(((z&g).bit_count()%2)<<j for j,g in enumerate(G))
 return cache[z]
def ker(C):return null([contraction(a,b) for i,a in enumerate(C) for b in C[:i]])
rng=random.Random(3813);one=(1<<19)-1;assert D[one]==(1<<38)-1
hist=collections.Counter();best=[];start=time.time();trials=0
while time.time()-start<25:
 trials+=1;C=[one]
 while True:
  K=ker(C);r=0
  for b in K:
   if rng.getrandbits(1):r^=b
  if not independent(C,r):
   r=next((b for b in K if independent(C,b)),0)
  if not r:break
  C.append(r)
 hist[len(C)]+=1
 if len(C)>len(best):best=C;print('NEW',len(C),'trial',trials,flush=True)
 if len(C)>=13:break
print('trials',trials,'hist',hist,'best',len(best),'cache',len(cache),'secs',time.time()-start)
pathlib.Path('workspace/agent3_Paley38_triorthogonal.json').write_text(json.dumps({'G':G,'best_coeff_rows':best,'best_word_rows':[D[a] for a in best],'histogram':dict(hist),'trials':trials},indent=2))
pathlib.Path('workspace/agent3_Paley38_triorthogonal.py').write_text(pathlib.Path(__file__).read_text())
