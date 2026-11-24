import itertools,time,pickle,os,functools
D=6;L=D+1;n=3
powers=[3**i for i in range(L+1)];off=[(3**i-1)//2 for i in range(L+2)]
N=off[L+1];mask=[(1<<powers[i])-1 for i in range(L+1)]
letters=[1<<(off[1]+i) for i in range(3)]
wordinfo=[None]*N
for d in range(L+1):
 for w in range(powers[d]):wordinfo[off[d]+w]=(d,w)

def bits(a):
 while a:
  x=a&-a;a^=x;yield x.bit_length()-1

def pmul(p,q):
 if not p or not q:return 0
 ans=0
 qparts=[(q>>off[d])&mask[d] for d in range(L+1)]
 for i in bits(p):
  d,w=wordinfo[i]
  for e in range(L+1-d):
   if qparts[e]:ans^=qparts[e]<<(off[d+e]+w*powers[e])
 return ans

def suball(ps,gs):
 ys=[letters[i]^gs[i] for i in range(3)]
 @functools.lru_cache(None)
 def sw(d,w):
  if d==0:return 1
  if d==1:return ys[w]
  return pmul(ys[w//powers[d-1]],sw(d-1,w%powers[d-1]))
 out=[]
 for p in ps:
  a=0
  for i in bits(p):a^=sw(*wordinfo[i])
  out.append(a)
 return tuple(out)
zero=(0,0,0)
def degree(g):
 return min([wordinfo[(a&-a).bit_length()-1][0]-1 for a in g if a] or [D+1])
def mul(g,h):
 if not any(g):return h
 if not any(h):return g
 if degree(g)+degree(h)>D:return tuple(a^b for a,b in zip(g,h))
 hs=suball(h,g)
 return tuple(a^b for a,b in zip(g,hs))

def inv(g):
 d=degree(g)
 if 2*d>D:return g
 # g^-1 = product of g^(2^j) up to exponent guaranteed to vanish
 ans=g;p=g
 for j in range(3):
  p=mul(p,p)
  if not any(p):break
  ans=mul(ans,p)
 assert not any(mul(g,ans))
 return ans

def comm(g,h):
 if degree(g)+degree(h)>D:return zero
 return mul(mul(mul(g,h),inv(g)),inv(h))

def polyword(word):
 ans=1
 for i in word:ans=pmul(ans,1^letters[i])
 return ans

def pinv(p):
 a=p^1;out=1;z=1
 for i in range(L):z=pmul(z,a);out^=z
 return out

# exact Magnus series of conjugating xi by xj and multiplying xi by [xj,xk]
gens=[]
for i in range(3):
 for j in range(3):
  if i==j:continue
  out=[0,0,0];out[i]=pmul(pmul(1^letters[j],1^letters[i]),pinv(1^letters[j]))^1^letters[i]
  gens.append(tuple(out))
for i in range(3):
 j,k=[a for a in range(3) if a!=i]
 w=pmul(pmul(pmul(1^letters[j],1^letters[k]),pinv(1^letters[j])),pinv(1^letters[k]))
 out=[0,0,0];out[i]=pmul(w,1^letters[i])^1^letters[i];gens.append(tuple(out))

def pivot(g):
 # polynomial positions ordered by length, then component then word
 opts=[(wordinfo[(a&-a).bit_length()-1][0],i,(a&-a).bit_length()-1) for i,a in enumerate(g) if a]
 _,i,p=min(opts);return i,p

def closure(seeds,label='',normal=True):
 basis={};degrees={};queue=list(seeds);head=0;t=time.time()
 while head<len(queue):
  a=queue[head];head+=1
  while any(a):
   p=pivot(a)
   if p not in basis:break
   a=mul(a,basis[p])
  if not any(a):continue
  p=pivot(a);d=degree(a);basis[p]=a;degrees[p]=d
  if 2*d<=D:queue.append(mul(a,a))
  if normal:
   for b in gens:
    if d+degree(b)<=D:queue.append(comm(a,b))
  for q,b in list(basis.items()):
   if q!=p and d+degrees[q]<=D:queue.append(comm(a,b))
  if len(basis)%25==0:print(label,len(basis),'queue',head,len(queue),'secs',round(time.time()-t,2),flush=True)
 return basis

if __name__=='__main__':
 os.makedirs('workspace',exist_ok=True)
 with open('workspace/agent3_noncomm_pc.py','w') as f:f.write(open(__file__).read())
 # directly generate gamma4 by normal closure all left-nested 4-brackets (6561)
 b={pivot(g):g for g in gens};allb=[]
 for c in range(1,6):
  if c==1:seeds=gens
  else:seeds=[comm(x,y) for x in b.values() for y in gens if degree(x)+degree(y)<=D]
  b=closure(seeds,label='g%d'%c);allb.append(b)
  print('GAMMA',c,'ORDER_LOG2',len(b),'degrees',{d:sum(degree(x)==d for x in b.values()) for d in range(1,D+1)},flush=True)
  with open('workspace/agent3_noncomm_pc_D%d.pkl'%D,'wb') as f:pickle.dump((gens,allb),f)
