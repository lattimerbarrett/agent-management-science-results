import networkx as nx
from sage.all import QQ, PolynomialRing, NumberField
from itertools import combinations
import time

# Coefficient convention: c[k] is k! times the coefficient of u^k.
def canonical(G):
 def rooted(v,parent):
  return '('+''.join(sorted(rooted(w,v) for w in G[v] if w!=parent))+')'
 return min(rooted(v,None) for v in G)

def all_trees():
 levels=[[nx.empty_graph(1)]]
 for n in range(2,11):
  found={}
  for G in levels[-1]:
   for v in G:
    H=G.copy();H.add_edge(v,n-1)
    found.setdefault(canonical(H),H)
  levels.append([found[k] for k in sorted(found)])
 assert list(map(len,levels))==[1,1,1,2,3,6,11,23,47,106]
 return sum(levels,[])

def hilbert(G,c,K=QQ,track=False):
 edges=list(G.edges());N=1<<len(edges)
 gs=[]
 for v in G:
  inc=[(i,1 if v==a else -1) for i,(a,b) in enumerate(edges) if v in (a,b)]
  g={}
  for s in range(1,1<<len(inc)):
   k=s.bit_count()
   if k>=len(c) or not c[k]:continue
   mask=0;a=K(c[k])
   for j,(e,sign) in enumerate(inc):
    if s>>j&1:mask|=1<<e;a*=sign
   g[mask]=a
  gs.append(g)
 order=sorted(range(N),key=lambda s:(s.bit_count(),s));pos={s:i for i,s in enumerate(order)}
 B={0:{0:K(1)}};new=[{0:K(1)}];h=[1];factors=set()
 while new and len(B)<N:
  pending=[]
  for b in new:
   for g in gs:
    row={}
    for x,a in b.items():
     for y,d in g.items():
      if not x&y:row[x|y]=row.get(x|y,K(0))+a*d
    row={x:a for x,a in row.items() if a}
    pending.append(row)
  pending.sort(key=len)
  new=[]
  for original in pending:
   row=original.copy()
   for p,b in B.items():
    if p not in row:continue
    a=row[p]
    for x,d in b.items():
     val=row.get(x,K(0))-a*d
     if val:row[x]=val
     elif x in row:del row[x]
   if not row:continue
   p=min(row,key=pos.get);a=row[p]
   if track:
    for polynomial in (a.numerator(),a.denominator()):
     for fac,e in polynomial.factor():
      if fac not in QQ:factors.add(fac.monic())
   B[p]={x:d/a for x,d in row.items()};new.append(original)
   if len(B)==N:break
  if new:h.append(len(new))
 return tuple(h),factors

EA=[(1,0),(1,2),(1,5),(0,6),(0,9),(2,3),(2,4),(6,7),(7,8)]
EB=[(1,0),(1,2),(0,4),(0,7),(2,3),(4,5),(4,6),(7,8),(7,9)]
def representative(edges):
 G=nx.Graph();G.add_nodes_from([1,0]+list(range(2,10)));G.add_edges_from(edges)
 return G
A=representative(EA);B=representative(EB)

def exhaustive():
 ts=all_trees()
 # Different orders are separated by f=u, whose series is (1+t)^(n-1).
 groups=[[G for G in ts if len(G)==n] for n in range(1,11)]
 tests=[[0]*k+[1] for k in range(2,10)]
 tests += [[0,1,1],[0,1,0,1],[0,1,1,3]]
 for c in tests:
  refined=[]
  for group in groups:
   if len(group)<2:refined.append(group);continue
   d={}
   for G in group:
    h,_=hilbert(G,c)
    d.setdefault(h,[]).append(G)
   refined.extend(d.values())
  groups=refined
  print('test',c,'classes',len(groups),'unresolved sizes',[len(g) for g in groups if len(g)>1],flush=True)
 remaining=[g for g in groups if len(g)>1]
 assert len(remaining)==1 and len(remaining[0])==2
 assert {canonical(G) for G in remaining[0]}=={canonical(A),canonical(B)}
 assert canonical(A)!=canonical(B)
 print('EXHAUSTIVE EXCLUSION VERIFIED',flush=True)

def universal():
 R=PolynomialRing(QQ,'z');z=R.gen();K=R.fraction_field()
 h1,f1=hilbert(A,[0,1,1,z],K,True)
 h2,f2=hilbert(B,[0,1,1,z],K,True)
 assert h1==h2==(1,10,49,146,225,81)
 factors=f1|f2
 print('generic',h1,'exception factors',sorted(map(str,factors)),flush=True)
 for p in sorted(factors,key=str):
  if p.degree()==1:L=QQ;r=-p[0]/p[1]
  else:L=NumberField(p,'alpha');r=L.gen()
  a=hilbert(A,[0,1,1,r],L)[0];b=hilbert(B,[0,1,1,r],L)[0]
  assert a==b
  print('at',p,a,flush=True)
 for c in [[0,1,0,1],[0,1,0,0],[0,0,1,1],[0,0,1,0],[0,0,0,1],[0,0,0,0]]:
  a=hilbert(A,c)[0];b=hilbert(B,c)[0]
  assert a==b
  print('case',c,a,flush=True)
 print('UNIVERSAL EQUALITY VERIFIED',flush=True)

if __name__=='__main__':
 start=time.time();exhaustive();universal();print('seconds',time.time()-start)
