import itertools,time,pickle,json,os
D=int(os.environ.get('DEG','7')); n=3
mons=[]
for d in range(D+1):
 mons += [a for a in itertools.product(range(d+1), repeat=n) if sum(a)==d]
idx={a:i for i,a in enumerate(mons)}; N=len(mons); mask=(1<<N)-1
# multiplication by monomial maps bits to shifted bits
mult=[[(j,idx[tuple(a[k]+b[k] for k in range(n))]) for j,b in enumerate(mons) if sum(a)+sum(b)<=D] for a in mons]
def pmul(a,b):
 if not a or not b:return 0
 if a.bit_count()>b.bit_count():a,b=b,a
 ans=0
 while a:
  x=a&-a;i=x.bit_length()-1;a^=x
  for j,k in mult[i]:
   if (b>>j)&1:ans^=1<<k
 return ans
sh=[N*i for i in range(9)]
def chunks(a):return [(a>>s)&mask for s in sh]
def prod(a,b):
 if not a or not b:return 0
 aa=chunks(a);bb=chunks(b);ans=0
 for i in range(3):
  for j in range(3):
   p=0
   for k in range(3):p^=pmul(aa[3*i+k],bb[3*k+j])
   ans|=p<<sh[3*i+j]
 return ans
def mul(a,b):return a^b^prod(a,b)
def inv(a):
 ans=0;p=a
 for _ in range(D):
  ans^=p;p=prod(p,a)
 return ans
def comm(a,b):return mul(mul(mul(a,b),inv(a)),inv(b))
def degree(a):
 if not a:return D+1
 return min(sum(mons[i%N]) for i in range(9*N) if (a>>i)&1)
# reorder pivot preference by polynomial degree then matrix position
order=sorted(range(9*N), key=lambda i:(sum(mons[i%N]),i//N,i%N))
pivorder={i:k for k,i in enumerate(order)}
def pivot(a):
 best=None;key=9*N
 while a:
  x=a&-a;i=x.bit_length()-1;a^=x
  if pivorder[i]<key:best=i;key=pivorder[i]
 return best
us=[1<<idx[tuple(int(k==j) for k in range(3))] for j in range(3)]
gens=[]
for i in range(3):
 for j in range(3):
  if i!=j:gens.append((us[j]<<sh[3*i+i])^(us[i]<<sh[3*i+j]))
for i in range(3):
 j,k=[v for v in range(3) if v!=i]
 gens.append((us[k]<<sh[3*i+j])^(us[j]<<sh[3*i+k]))

def closure(seeds,normalgens=gens,label=''):
 basis={};degrees={};queue=list(seeds);head=0;t=time.time()
 while head<len(queue):
  a=queue[head];head+=1
  while a:
   p=pivot(a)
   if p not in basis:break
   a=mul(a,basis[p])
  if not a:continue
  p=pivot(a);d=degree(a)
  # Normal closure also squares. Since every basis word lies normal closure of seeds,
  # conjugations by original generators plus squares enforce group closure.
  basis[p]=a;degrees[p]=d
  if 2*d<=D:queue.append(prod(a,a))
  for b in normalgens:
   if d+degree(b)<=D:queue.append(comm(a,b))
  # Pair commutators guarantee closure of collected span.
  for q,b in list(basis.items()):
   if q!=p and d+degrees[q]<=D:queue.append(comm(a,b))
  if len(basis)%20==0: print(label,'basis',len(basis),'queue',head,len(queue),'time',round(time.time()-t,2),flush=True)
 return basis
if __name__=='__main__':
 with open('workspace/agent3_magnus_pc.py','w') as f:
  f.write(open(__file__).read())
 b=closure(gens,label='g1');allb=[b]
 print('gamma 1',len(b),flush=True)
 for c in range(2,D+1):
  seeds=[comm(x,y) for x in b.values() for y in gens if degree(x)+degree(y)<=D]
  b=closure(seeds,label='g'+str(c));allb.append(b)
  print('gamma',c,len(b), 'pivots by matrix degree',{d:sum(degree(x)==d for x in b.values()) for d in range(1,D+1)},flush=True)
 os.makedirs('workspace',exist_ok=True)
 with open('workspace/agent3_magnus_pc_D%d.pkl'%D,'wb') as f:pickle.dump((mons,gens,allb),f)
