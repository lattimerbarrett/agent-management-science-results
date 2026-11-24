from math import comb, factorial
from itertools import product, combinations
import networkx as nx

def mul(a,b):
 c=[0]*(len(a)+len(b)-1)
 for i,x in enumerate(a):
  for j,y in enumerate(b):c[i+j]+=x*y
 return c

def forest_paths(G):
 assert nx.is_forest(G)
 es=list(G.edges()); n=len(G); ans=[0]*(n+1)
 for mask in range(1<<len(es)):
  d={}; m=0
  for i,(u,v) in enumerate(es):
   if mask>>i&1:d[u]=d.get(u,0)+1;d[v]=d.get(v,0)+1;m+=1
  if max(d.values(),default=0)>2:continue
  q=len(d)-m; rem=n-len(d)
  for j in range(rem+1):ans[q+j]+=2**q*comb(rem,j)
 return ans

def exact_cycles_forests(forests):
 polys=[forest_paths(f) for f in forests]
 trans=[]
 for p in polys:
  q=[0]*len(p);q[0]=1
  for k in range(1,len(p)):
   for l in range(1,k+1):q[l]+=p[k]*(-1)**(k-l)*comb(k-1,l-1)*factorial(k)//factorial(l)
  trans.append(q)
 Q=[1]
 for q in trans:Q=mul(Q,q)
 for q in trans:
  for l in range(1,len(q)):Q[l]-=q[l]
 twice=sum(factorial(k-1)*Q[k] for k in range(2,len(Q)))
 twice-=sum(len(f)*len(g) for f,g in combinations(forests,2))
 assert twice%2==0
 return twice//2

def brute(G):
 ans=0
 for k in range(3,len(G)+1):
  for subset in combinations(G,k):
   v=min(subset); rest=set(subset)-{v}
   def rec(path,avail):
    if not avail:return int(G.has_edge(path[-1],v))
    return sum(rec(path+[x],avail-{x}) for x in avail if G.has_edge(path[-1],x))
   ans+=rec([v],rest)//2
 return ans

def join_forests(fs):
 G=nx.Graph();parts=[]
 for f in fs:
  off=len(G); mp={u:off+i for i,u in enumerate(f)};g=nx.relabel_nodes(f,mp);G.update(g);parts.append(set(g))
 for a,b in combinations(parts,2):G.add_edges_from(product(a,b))
 return G

if __name__=='__main__':
 from fractions import Fraction as F
 from math import ceil
 for r in range(3,9):
  found=[]
  for s in range(3,2*r+5):
   a=F(s-1,s);bs=F((s-1)*(s-2),2*s);bp=F(s-2,s)
   wins=[];ties=[]
   for n0 in range(r*s):
    n=100*r*s+n0;rows=[]
    for m in range(n//r-4,n//r+5):
     q,z=divmod(n-m,r-1);sizes=[m]+[q+1]*z+[q]*(r-1-z)
     xs=[F(v)-F(n,r) for v in sizes];Q=sum(x*x for x in xs)
     cross=(n*n-sum(v*v for v in sizes))//2
     for branch,beta,offset in [('P',bp,0),('S',bs,3)]:
      E=m-ceil(F(m-offset,s));e=cross+E
      phi=E-F(r-1,2*(r-2))*Q+F(2,r-2)*a*xs[0]-beta/F(r-1)
      rows.append((e,phi,branch,m))
    em=max(x[0] for x in rows);cm=max(x[1] for x in rows)
    if all(x[0]<em for x in rows if x[1]==cm):wins.append(n0)
    elif any(x[0]<em for x in rows if x[1]==cm):ties.append(n0)
   if wins or ties:found.append((s,wins,ties))
  print('r',r,'first cases',found[:2])
 import pathlib
 cnt=0
 for n in range(3,9):
  for r in range(2,min(n,4)+1):
   for sizes in product(range(1,n),repeat=r):
    if sum(sizes)!=n or tuple(sorted(sizes))!=sizes:continue
    for choices in product(range(2),repeat=r):
     fs=[nx.path_graph(s) if c else nx.empty_graph(s) for s,c in zip(sizes,choices)]
     x=exact_cycles_forests(fs);y=brute(join_forests(fs))
     assert x==y,(sizes,choices,x,y)
     cnt+=1
 print('Verified exact cycle formula against brute-force enumeration:',cnt,'graphs')
