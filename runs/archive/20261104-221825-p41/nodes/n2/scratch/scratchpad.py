from functools import lru_cache
from itertools import combinations
import random,time,pickle

def bits(x):
 while x:
  b=x&-x; yield b; x-=b
@lru_cache(None)
def kd(fs,k):
 if len(fs)==1:return True
 if not fs:return False
 dim=fs[0].bit_count()
 if dim==1:return True
 faces=set()
 for f in fs:
  vs=list(bits(f))
  for s in range(1,min(k+1,dim)+1):
   for t in combinations(vs,s):faces.add(sum(t))
 for s in sorted(faces,key=int.bit_count):
  D=tuple(f for f in fs if f&s!=s)
  if not D:continue
  C=tuple(f for f in fs if f&s==s)
  if any(not any((f^v)&g==(f^v) for g in D) for f in C for v in bits(s)):continue
  L=tuple(sorted(f^s for f in C))
  if kd(L,k) and kd(D,k):return True
 return False

def allowed(fs,f):
 # intersection facets must all have codimension one
 I=set(g&f for g in fs)
 ridges=[x for x in I if x.bit_count()==f.bit_count()-1]
 return all(any(x&r==x for r in ridges) for x in I)

def trial(n,d,N):
 ALL=[sum(1<<i for i in t) for t in combinations(range(n),d+1)]
 best=len(ALL)
 for it in range(N):
  fs=[random.choice(ALL)]; left=set(ALL)-set(fs)
  while True:
   choices=[f for f in left if allowed(fs,f)]
   if not choices:break
   f=random.choice(choices);fs.append(f);left.remove(f)
  if left and len(fs)<best:
   best=len(fs);print('stuck',n,d,it,len(fs),'/',len(ALL),flush=True)
   with open('stuck.pkl','wb') as h:pickle.dump((n,d,fs),h)
   if n<=9:
    print('kd',[(k,kd(tuple(sorted(fs)),k)) for k in range(d+1)],flush=True)
  if it%100==0: print('iteration',it,'cache',kd.cache_info(),flush=True)
if __name__=='__main__':
 trial(8,3,1000)
