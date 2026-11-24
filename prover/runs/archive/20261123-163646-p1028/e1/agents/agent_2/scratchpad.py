from pathlib import Path
code='''from fractions import Fraction as Q
for q in range(100):
 r=q//2;g=r*(r+1) if q%2==0 else (r+1)**2
 assert Q(g)>=Q(q*q,4)+Q(q,2)
for a in range(1,1000):
 W=6*a-3
 assert Q(W*W,2*a)+W>24*(a-1)
for a in range(11,1000):assert Q(a,12)-Q(1,18)+Q(1,2)<=Q(a,8)
for n in range(17,1000):assert Q(3*n-4,36)<=Q(n,8)-Q(139,180)
assert Q(1,16)+Q(1,2)<1
assert Q(1,2)+Q(1,2)<Q(9,8)
for h in [2,4,6]:assert Q(h*h,32*(8-h))<=Q(10,8)-Q(h,32)-Q(1,4)
print('All d8 core DAG, budget, residual dense-case, full-connectivity exact checks passed.')
'''
Path('workspace/check_d8_core_agent2.py').write_text(code)
code='''import itertools,json,networkx as nx,sympy as S
out={}
for n in [5,7]:
 valid=0;mx=S.Rational(0);best=None
 poss=list(itertools.combinations(range(1,n),2))
 for es in itertools.combinations(poss,(3*n-1)//2-2):
  edges=[(0,1),(0,2)]+list(es);deg=[0]*n
  for u,v in edges:deg[u]+=1;deg[v]+=1
  if deg!=[2]+[3]*(n-1):continue
  G=nx.Graph(edges)
  if not nx.is_connected(G) or list(nx.bridges(G)):continue
  valid+=1;L=S.zeros(n)
  for u,v in edges:L[u,u]+=1;L[v,v]+=1;L[u,v]-=1;L[v,u]-=1
  rs=L[1:,1:].inv().diagonal();r=max(rs)
  if r>mx:mx=r;best=edges
 assert valid=={5:1,7:54}[n]
 assert mx=={5:S.Rational(7,8),7:S.Rational(11,8)}[n]
 out[n]=best
 print('terminal order',n,'all labelings',valid,'exact max',mx)
def cubic_extremizer(n):
 sizes=[5]+[4]*((n-10)//4 if n%4==2 else (n-12)//4)+[5 if n%4==2 else 7]
 G=nx.Graph();off=0;ports=[]
 for i,size in enumerate(sizes):
  if i==0:edges=out[5];left=right=0
  elif i==len(sizes)-1:edges=out[size];left=right=0
  else:edges=[(0,2),(0,3),(1,2),(1,3),(2,3)];left=0;right=1
  G.add_edges_from((u+off,v+off)for u,v in edges);ports.append((off+left,off+right));off+=size
 for i in range(len(ports)-1):G.add_edge(ports[i][1],ports[i+1][0])
 return G,3,n-sizes[-1]+(3 if sizes[-1]==5 else 5)
for n in range(10,42,2):
 G,s,t=cubic_extremizer(n)
 assert len(G)==n and nx.is_connected(G) and set(dict(G.degree()).values())=={3}
 L=S.zeros(n)
 for u,v in G.edges():L[u,u]+=1;L[v,v]+=1;L[u,v]-=1;L[v,u]-=1
 keep=[i for i in range(n)if i!=t];e=S.zeros(n-1,1);e[keep.index(s)]=1
 sol=L.extract(keep,keep).inv()*e
 assert sol[keep.index(s)]==S.Rational(2*n-(9 if n%4==2 else 11),4)
print('All full cubic constructions n=10,...,40 passed exact resistance checks.')
'''
Path('workspace/check_even_terminals.py').write_text(code)
assert Path('workspace/even_cubic_proof.md').stat().st_size>1000
assert Path('workspace/odd_degree8_core_agent2.md').stat().st_size>3000
# The unused auxiliary d5 strip certificate is not needed by the main proof;
# retain a self-contained arithmetic/flow check without self-modification.
code='''from fractions import Fraction as F
n=16;pending=[0,0,0];edges=[]
for v,q in [(1,1)]+[(i,2)for i in range(2,14)]+[(14,1)]:
 if q==1:chosen=[next(x for x in pending if pending.count(x)>1)]
 else:chosen=list(dict.fromkeys(pending));assert len(chosen)==2
 for u in chosen:pending.remove(u);edges.append((u,v))
 pending += [v]*q
edges += [(u,15)for u in pending];assert len(set(edges))==len(edges)==29
curr={e:F(1,3)for e in edges}
for a,b,c in [(0,1,2),(2,3,4)]:
 for e in [(a,b),(b,c)]:curr[e]-=F(1,9)
 curr[(a,c)]+=F(1,9)
assert sum(i*i for i in curr.values())==F(85,27)<F(63,20)
for v in range(n):assert sum(i for(a,b),i in curr.items()if a==v)-sum(i for(a,b),i in curr.items()if b==v)==(1 if v==0 else -1 if v==15 else 0)
print('Auxiliary d5 double-triangle exact flow passed.')
'''
Path('workspace/check_d5_highconnect_agent2.py').write_text(code)
import importlib.util
for name in ['check_even_terminals','check_d8_core_agent2','check_d5_highconnect_agent2']:
 p='workspace/'+name+'.py';before=Path(p).read_text();sp=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);assert Path(p).read_text()==before
print('All owned certificates restored, passed, and confirmed non-self-modifying.')
