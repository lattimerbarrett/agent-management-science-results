from functools import lru_cache
import time
n=7;N=1<<n
DOWN=[sum(1<<y for y in range(N) if y&x==y) for x in range(N)]
UP=[sum(1<<y for y in range(N) if y&x==x) for x in range(N)]
ADJ=[(DOWN[x]|UP[x])^(1<<x) for x in range(N)]
calls=0
@lru_cache(maxsize=2000000)
def rec(S):
 global calls
 calls+=1
 if not S:return 1
 T=S;isol=0;best=None;score=0
 while T:
  b=T&-T;x=b.bit_length()-1;T-=b
  a=(ADJ[x]&S)
  if not a:isol|=b;continue
  sc=(DOWN[x]&S).bit_count()*(UP[x]&S).bit_count()
  if sc>score:score=sc;best=x
 if isol:return (1<<isol.bit_count())*rec(S^isol)
 # component
 C=S&-S;front=C
 while front:
  b=front&-front;front-=b;x=b.bit_length()-1
  more=ADJ[x]&S&~C
  C|=more;front|=more
 if C!=S:return rec(C)*rec(S^C)
 return rec(S&~DOWN[best])+rec(S&~UP[best])
t=time.time();ans=rec((1<<N)-1)
print(ans,calls,time.time()-t,rec.cache_info(),flush=True)
