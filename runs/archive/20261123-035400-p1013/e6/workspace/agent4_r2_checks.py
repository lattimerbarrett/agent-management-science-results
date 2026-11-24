import itertools, pickle, networkx as nx, sys, math
sys.path.insert(0,'workspace')
from agent1_cycles import *
H=nx.Graph();H.add_nodes_from(range(11))
H.add_edges_from([(0,1),(0,10),(1,8),(1,9),(2,3),(2,10),(3,8),(3,10),(4,5),(4,10),(5,8),(5,9),(6,7),(6,10),(7,9),(7,10)])

def match_maps(F,a):
 es=list(F.edges())
 if max(dict(F.degree()).values(),default=0)>1 or len(es)>a:return
 for dest in itertools.permutations(range(a),len(es)):
  for flips in itertools.product(range(2),repeat=len(es)):
   yield {v:2*d+(s^fl) for (u,w),d,fl in zip(es,dest,flips) for s,v in enumerate((u,w))}

def contains(a,b,missing=()):
 for mask in range(1<<len(H)):
  A=[v for v in H if mask>>v&1];B=[v for v in H if not(mask>>v&1)]
  FA=H.subgraph(A);FB=H.subgraph(B)
  for f in match_maps(FA,a):
   for g in match_maps(FB,b):
    if not any(H.has_edge(u,v) and (f[u],g[v]) in missing for u in f for v in g):return True
 return False

pairs=set();witness={};star=[]
for mask in range(1<<len(H)):
 A=[v for v in H if mask>>v&1];B=[v for v in H if not(mask>>v&1)]
 FA=H.subgraph(A);FB=H.subgraph(B)
 if max(dict(FA.degree()).values(),default=0)<=1 and max(dict(FB.degree()).values(),default=0)<=1:
  pairs.add((FA.number_of_edges(),FB.number_of_edges()))
  witness[(FA.number_of_edges(),FB.number_of_edges())]=(A,B)
 if FB.number_of_edges()==0 and FA.number_of_edges()==2 and max(dict(FA.degree()).values(),default=0)==2:star.append((A,B))
assert star
assert (4,0) in pairs and not any(a<=2 and b<=2 for a,b in pairs)
assert contains(3,1)
assert contains(3,3,((0,0),))
assert not contains(2,2)
assert not contains(3,0)
print('Hedges',list(H.edges()),'star',star[0], 'matching decomposition pairs',sorted(pairs),'witness13',witness[(1,3)],flush=True)

# Exact odd-n cycle inequalities clean rival lone3matching vs 2+2matching.
def qm(n,a):return mul(power([1,4,1],a),power([1,1],n-2*a))
for m in [10,20,50,100,200,500]:
 base=cycles_join_r2(qm(m+1,0),qm(m,0),m+1,m)
 rival=cycles_join_r2(qm(m+1,3),qm(m,0),m+1,m)
 ext=cycles_join_r2(qm(m+1,2),qm(m,2),m+1,m)
 if m>=100:assert rival>ext
 print('m',m,'n',2*m+1,'m*(rival/ext-1)',float((rival-ext)*m/ext),'rivalgain',float((rival-base)*m/base),'extgain',float((ext-base)*m/base),flush=True)
# rigorous interval for needed Bessel inequality: I0(2)>? I1(2).
# lone3 score - split2+2 = 2 I0/I1 -4 I2/I1 = (4 I1-2 I0)/I1 using I0-I2=I1.
# Positive iff 2 I1>I0, proved below by rational sums and geometric tail bounds.
from fractions import Fraction
I0=sum(Fraction(1,math.factorial(k)**2) for k in range(20));I1=sum(Fraction(1,math.factorial(k)*math.factorial(k+1)) for k in range(20))
tail0=Fraction(1,math.factorial(20)**2)/(1-Fraction(1,21**2))
tail1=Fraction(1,math.factorial(20)*math.factorial(21))/(1-Fraction(1,21*22))
assert Fraction(143,100)<I0/(I1+tail1)
assert (I0+tail0)/I1<Fraction(144,100)
assert 2*I1>I0+tail0
# Enumerate the resulting finite-template extremal surplus bound.
opt=[]
for a in range(4):
 for b in range(4):
  lower_missing=max(b if a==3 else 0,a if b==3 else 0)
  for ell in range(lower_missing,37):
   assert a+b-ell<=4
   if a+b-ell==4:opt.append((a,b,ell))
assert opt==[(2,2,0)]
print('unique finite-template extremal triple',opt,'Bessel ratio bounded1.43..1.44')
