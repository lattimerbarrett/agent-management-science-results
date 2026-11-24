import itertools,math,networkx as nx
from fractions import Fraction

def conv(a,b):
 c=[0]*(len(a)+len(b)-1)
 for i,x in enumerate(a):
  for j,y in enumerate(b):c[i+j]+=x*y
 return c

def forest_poly(G):
 es=list(G.edges);n=len(G);out=[0]*(n+1)
 for mask in range(1<<len(es)):
  H=nx.Graph();H.add_edges_from(es[j] for j in range(len(es)) if mask>>j&1)
  if H and (max(dict(H.degree()).values())>2 or not nx.is_forest(H)):continue
  cc=nx.number_connected_components(H);u=len(H);base=2**cc
  for j in range(n-u+1):out[cc+j]+=base*math.comb(n-u,j)
 return out

def star_poly(n):
 out=[math.comb(n,j) for j in range(n+1)]
 if n>=2:
  for j in range(n-1):out[j+1]+=2*(n-1)*math.comb(n-2,j)
 if n>=3:
  for j in range(n-2):out[j+1]+=(n-1)*(n-2)*math.comb(n-3,j)
 return out

def cyc(parts,W,internalcycles=0):
 R=len(parts);stride=[math.prod(x+1 for x in parts[i+1:]) for i in range(R)];size=math.prod(x+1 for x in parts);Q=[0]*size;Q[0]=1
 transitions={mask:[(sum(stride[j] for j in range(R) if sub>>j&1),sub.bit_count()-1,sub.bit_count()*(sub.bit_count()-1)) for sub in range(1,1<<R) if sub&mask==sub and sub.bit_count()>=2] for mask in range(1<<R)}
 fac=[math.factorial(i) for i in range(max(parts)+1)]
 ws=[[W[i]*fac[i] for i in range(parts[0]+1)]]+[[fac[b]//fac[b-i] for i in range(b+1)] for b in parts[1:]]
 ans=0
 for inds in itertools.product(*(range(b+1) for b in parts)):
  S=sum(inds)
  if not S:continue
  idx=sum(a*b for a,b in zip(inds,stride));mask=sum((1<<j) for j,a in enumerate(inds) if a)
  q=N=0
  for delta,c,d in transitions[mask]:
   old=Q[idx-delta];q+=c*old;N+=d*old
  Q[idx]=q
  if N:
   wt=math.prod(ws[j][a] for j,a in enumerate(inds));z=N*wt
   assert z%S==0,(inds,z%S)
   ans+=z//S
 cross=sum(parts[i]*parts[j] for i in range(R) for j in range(i))
 assert (ans-cross)%2==0
 return (ans-cross)//2+internalcycles
