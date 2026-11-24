import sys,itertools,time
sys.path.insert(0,'workspace')
from agent2_checker import certificate,verify,deletion,link,subsets
from agent1_upper import skeleton,skeleton_cert,uniform_cert

def acyclic_euler(fs):
 allfaces={g for f in fs for g in subsets(f)}
 return sum((-1)**g.bit_count() for g in allfaces)==0

def join_cert(c,B):
 if c[0]=='simplex':return ('simplex',c[1]|B)
 return ('shed',c[1],join_cert(c[2],B),join_cert(c[3],B))

def expansion(fs,q,m):
 out=set()
 for f in fs:
  U=[1<<(v*m+j) for v in range(f.bit_length()) if f>>v&1 for j in range(m)]
  for c in itertools.combinations(U,q):out.add(sum(c))
 return tuple(sorted(out))

def lift(fs,c,q,m,k,phase_check=True):
 if q==0:return (0,),('simplex',0)
 assert acyclic_euler(fs)
 if c[0]=='simplex':
  U=sum(1<<(v*m+j) for v in range(c[1].bit_length()) if c[1]>>v&1 for j in range(m))
  return expansion(fs,q,m),uniform_cert(U,q)
 sigma=c[1];s=sigma.bit_count();D=deletion(fs,sigma);L=link(fs,sigma)
 ef,ec=lift(D,c[2],q,m,k,phase_check)
 if s>q:return ef,ec
 lf,lc=lift(L,c[3],q-s,m,k,phase_check)
 vv=[i for i in range(sigma.bit_length()) if sigma>>i&1]
 for inds in sorted(itertools.product(range(m),repeat=s),reverse=True):
  sig=sum(1<<(v*m+i) for v,i in zip(vv,inds))
  B=sum(1<<(v*m+j) for v,i in zip(vv,inds) for j in range(i+1,m))
  jf=tuple(f|B for f in lf);jc=join_cert(lc,B)
  pf=skeleton(jf,q-s);pc=skeleton_cert(jf,jc,q-s)
  nf=tuple(sorted(set(ef)|{sig|f for f in pf}));nc=('shed',sig,ec,pc)
  if phase_check:assert deletion(nf,sig)==ef and link(nf,sig)==pf
  ef,ec=nf,nc
 assert ef==expansion(fs,q,m)
 return ef,ec

def acyclicize(fs,c,k):
 if c[0]=='simplex':
  assert fs!=(0,)
  return fs,c
 sigma=c[1];q=fs[0].bit_count()
 df,dc=acyclicize(deletion(fs,sigma),c[2],k)
 if sigma.bit_count()==q:
  out,cc=df,dc
 else:
  lf,lc=acyclicize(link(fs,sigma),c[3],k)
  out=tuple(sorted(set(df)|{sigma|f for f in lf}));cc=('shed',sigma,dc,lc)
 assert skeleton(out,q-1)==skeleton(fs,q-1)
 assert acyclic_euler(out)
 return out,cc

if __name__=='__main__':
 cases=[((3,6),0,3,3),((7,14),0,4,4),((7,11,13),1,4,4),((7,11,19,25,28,37,38,49,70,73,76,82,84,97),1,4,4)]
 for fs,k,q,m in cases:
  c=certificate(fs,k);assert c and acyclic_euler(fs)
  tm=time.time();ef,ec=lift(fs,c,q,m,k);verify(ef,k,ec)
  print('PASS',fs,k,q,m,'expandedfacets',len(ef),'time',time.time()-tm,flush=True)
