import itertools,math,time,json
TARGETS={322,326,330,334};FOUND={}
def search(parts,cutoff):
 inds=list(itertools.product(*[range(n+1) for n in parts]));N=len(inds);idx={i:k for k,i in enumerate(inds)};W=[math.prod(math.comb(n,a) for n,a in zip(parts,i)) for i in inds];R=[]
 for i in inds:
  if sum(i)>7:R.append(sum(1<<idx[j] for j in inds if all(a&b==b for a,b in zip(i,j))))
 piv={}
 for row in R+[1<<k for k,w in enumerate(W) if w>cutoff]:
  while row:
   p=row.bit_length()-1
   if p in piv:row^=piv[p]
   else:piv[p]=row;break
 free=[i for i in range(N) if i not in piv];print(parts,cutoff,'dimension',len(free),flush=True)
 def solve(v):
  for i in sorted(piv):
   if (piv[i]&v).bit_count()&1:v|=1<<i
  return v
 basis=[solve(1<<i) for i in free];orbitmasks=[0]*N
 for x in range(16384):
  vals=[];shift=0
  for n in parts:vals.append((x>>shift&((1<<n)-1)).bit_count());shift+=n
  k=idx[tuple(vals)];orbitmasks[k]|=1<<x
 def expand(v):
  out=0
  for i in range(N):
   if v>>i&1:out^=orbitmasks[i]
  return out
 v=0;bs=[expand(b) for b in basis];ov=0;start=time.time();small=set()
 for it in range(1<<len(free)):
  if it:
   bit=(it&-it).bit_length()-1;v^=bs[bit];ov^=basis[bit]
  w=v.bit_count()
  if w<=450:small.add(w)
  if w in TARGETS:
   FOUND[w]={'parts':parts,'ones':[inds[i] for i in range(N) if ov>>i&1],'weight':w};TARGETS.remove(w);print('FOUND',w,FOUND[w],flush=True);json.dump(FOUND,open('workspace/agent2_cutoff_seeds.json','w'))
   if not TARGETS:break
 print('done',it+1,'time',time.time()-start,'remain',TARGETS,'small',sorted(small),flush=True)
if __name__=='__main__':
 open('workspace/agent2_cutoff_search.py','w').write(open(__file__).read())
 search((6,5,2,1),20)
