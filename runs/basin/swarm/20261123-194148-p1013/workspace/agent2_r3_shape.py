import itertools,math,time
from fractions import Fraction

def htable(mx):
 shape=tuple(x+1 for x in mx);vs=list(itertools.product(*(range(x) for x in shape)));hs={v:0 for v in vs}
 for start in range(3):
  init=tuple(int(i==start) for i in range(3));dp={init:[int(i==start) for i in range(3)]}
  for v in vs:
   x=dp.get(v,[0]*3)
   hs[v]+=sum(x[i] for i in range(3) if i!=start)
   for end in range(3):
    if v[end]==mx[end]:continue
    nv=list(v);nv[end]+=1;nv=tuple(nv)
    if nv not in dp:dp[nv]=[0]*3
    dp[nv][end]+=sum(x[i] for i in range(3) if i!=end)
 for v,w in hs.items():
  N=sum(v);hs[v]=w*math.prod(math.factorial(t) for t in v)//(2*N) if N>=3 else 0
 return hs

def compopts(k,kind):
 if kind=='star':return [(0,0,1),(1,1,k-1),(2,1,math.comb(k-1,2))]
 opts=[(0,0,1)]
 for j in range(1,k):
  for p in range(1,min(j,k-j)+1):opts.append((j,p,math.comb(j-1,p-1)*math.comb(k-j,p)))
 return opts

def cycles(a,b,c,k,kind,hs):
 assert a%k==0
 coeff={(0,0):1}
 for _ in range(a//k):
  ne={}
  for (j,p),v in coeff.items():
   for dj,dp,mul in compopts(k,kind):
    key=j+dj,p+dp;ne[key]=ne.get(key,0)+v*mul
  coeff=ne
 ans=(b+c)*sum(v for (j,p),v in coeff.items() if j>=1 and p==1)
 for (j,p),v in coeff.items():
  for ka in range(p,a-j+1):
   ac=math.comb(a-j-p,ka-p)
   for kb in range(b+1):
    bc=math.comb(b,kb)
    for kc in range(c+1):ans+=v*2**p*ac*bc*math.comb(c,kc)*hs[ka,kb,kc]
 return ans
if __name__=='__main__':
 import sys
 sys.path.insert(0,'workspace')
 from agent2_cycles import brute
 for kind in ['star','path']:
  a,b,c=4,1,1;n=6
  ed=[(i,j) for i in range(n) for j in range(i+1,n) if (i<a)!=(j<a) or(i>=a and j>=a)]
  ed += ([(0,i) for i in range(1,a)] if kind=='star' else [(i,i+1) for i in range(a-1)])
  assert brute(n,ed)==cycles(a,b,c,4,kind,htable((a,b,c)))
 print('Exact tripartite formulas passed independent brute-cycle checks.')
 for k in [4,6]:
  D=Fraction((k-2)*(k-3),2*k);pred=Fraction(3,2)*D
  for a in [2*k,3*k,4*k]:
   st=time.time();hs=htable((a,a,a));pa=cycles(a,a,a,k,'path',hs);sa=cycles(a,a,a,k,'star',hs)
   print('k',k,'n',3*a,'n*(path/star-1)',float(Fraction(3*a*(pa-sa),sa)),'predictedlimit',float(pred),'seconds',time.time()-st,flush=True)
