import networkx as nx, itertools, time, pickle, os

def regular_graphs(n,d,verbose=True):
 states=[tuple([0]*n)]
 for k in range(n):
  table={}; count=0
  for masks in states:
   masks=list(masks)
   v=max(range(k,n),key=lambda x:masks[x].bit_count())
   if v!=k:
    perm=list(range(n));perm[k],perm[v]=v,k
    masks=[sum(1<<b for b in range(n) if (masks[perm[a]]>>perm[b])&1) for a in range(n)]
   r=d-masks[k].bit_count()
   groups={}
   for j in range(k+1,n):groups.setdefault(masks[j],[]).append(j)
   groups=list(groups.values())
   def subsets(g,needed,chosen):
    if g==len(groups):
     if needed==0:yield chosen
     return
    vs=groups[g]
    for c in range(min(len(vs),needed)+1):
     yield from subsets(g+1,needed-c,chosen+vs[:c])
   for neighbors in subsets(0,r,[]):
    new=masks.copy()
    for j in neighbors:new[k]|=1<<j;new[j]|=1<<k
    if any(not (d-(n-k-2)<=new[j].bit_count()<=d) for j in range(k+1,n)):continue
    G=nx.Graph();G.add_nodes_from((i,{'p':int(i<=k)}) for i in range(n))
    G.add_edges_from((i,j) for i in range(n) for j in range(i+1,n) if (new[i]>>j)&1)
    h=nx.weisfeiler_lehman_graph_hash(G,node_attr='p',iterations=3)
    bucket=table.setdefault(h,[])
    if not any(nx.is_isomorphic(G,H,node_match=lambda a,b:a['p']==b['p']) for H,_ in bucket):bucket.append((G,tuple(new)))
    count+=1
  states=[masks for bucket in table.values() for G,masks in bucket]
  if verbose:print(n,d,k+1,len(states),count,round(time.time()-start,2),flush=True)
 out=[]
 for masks in states:
  G=nx.Graph();G.add_nodes_from(range(n));G.add_edges_from((i,j) for i in range(n) for j in range(i+1,n) if masks[i]>>j&1)
  out.append(G)
 return out

start=time.time()
for d in [0,1,2,3,4]:
 f=f'graphs_10_{d}.pkl'
 if os.path.exists(f):Gs=pickle.load(open(f,'rb'))
 else:
  Gs=regular_graphs(10,d);pickle.dump(Gs,open(f,'wb'))
 print('DONE',d,len(Gs),sum(nx.is_connected(g) for g in Gs),time.time()-start,flush=True)

import sympy as sp

def exact_tau(G):
 n=len(G);L=sp.zeros(n)
 for i,j in G.edges():L[i,i]+=1;L[j,j]+=1;L[i,j]-=1;L[j,i]-=1
 A=L[:n-1,:n-1].inv()
 def ent(i,j):return A[i,j] if i<n-1 and j<n-1 else sp.S.Zero
 R=max(ent(i,i)+ent(j,j)-2*ent(i,j) for i in range(n) for j in range(i+1,n))
 return 2*G.number_of_edges()*R

best=0
for d in range(10):
 Gs=pickle.load(open(f'graphs_10_{min(d,9-d)}.pkl','rb'))
 if d>=5:Gs=[nx.complement(G) for G in Gs]
 vals=[exact_tau(G) for G in Gs if nx.is_connected(G)]
 b=max(vals) if vals else None
 if b is not None:best=max(best,b)
 print('n=10 degree',d,'count connected',len(vals),'maximum',b,flush=True)
print('t_10=',best,flush=True)

from math import lcm, comb, log2

def lap(G):
 n=len(G);L=sp.zeros(n)
 for i,j in G.edges():L[i,i]+=1;L[j,j]+=1;L[i,j]-=1;L[j,i]-=1
 return L

def hitting(G):
 n=len(G);L=lap(G);H=sp.zeros(n)
 for t in range(n):
  ix=[i for i in range(n) if i!=t]
  h=L.extract(ix,ix).inv()*sp.Matrix([G.degree(i) for i in ix])
  for i,x in zip(ix,h):H[i,t]=x
 return H

def ilog(x,b):
 k=int((x.bit_length()-1)/log2(b))
 while b**k>x:k-=1
 while b**(k+1)<=x:k+=1
 return k

def check_formula(n,literal=False):
 N=comb(n,2);B=2**N+1;M=n**(n-2);Q=1
 for x in range(1,M+1):Q=lcm(Q,x)
 edges=list(itertools.combinations(range(n),2));s=n-2;t=n-1
 S=0;Emax=0;independent=0;valid=0
 for mask in range(2**N):
  G=nx.Graph();G.add_nodes_from(range(n));G.add_edges_from(e for j,e in enumerate(edges) if mask>>j&1)
  L=lap(G);T=int(L[:n-1,:n-1].det());F=int(L[:n-2,:n-2].det())
  z=1//(1+T);rho=1
  ds=[G.degree(i) for i in range(n)]
  for d in ds[:-1]:rho*=1//(1+(d-ds[-1])**2)
  assert bool(1-z)==nx.is_connected(G)
  assert bool(rho)==(len(set(ds))==1)
  # Directly count spanning trees, independently of the determinant.
  Tc=0
  for es in itertools.combinations(G.edges(),n-1):
   H=nx.Graph();H.add_nodes_from(range(n));H.add_edges_from(es)
   Tc+=nx.is_tree(H)
  assert T==Tc and 0<=T<=M
  assert (Q*sum(ds)*F)%(T+z)==0
  E=Q*sum(ds)*F//(T+z)
  if T:
   H=hitting(G);A=L[:n-1,:n-1].inv();vol=sum(ds)
   for u,v in itertools.combinations(range(n),2):
    a=A[u,u] if u<n-1 else 0;b=A[v,v] if v<n-1 else 0;c=A[u,v] if v<n-1 else 0
    assert H[u,v]+H[v,u]==vol*(a+b-2*c)
   assert H[s,t]+H[t,s]==sp.Rational(sum(ds)*F,T)
   if rho:independent=max(independent,H[s,t]+H[t,s])
  if rho and not z:
   valid+=1;Emax=max(Emax,E)
   if literal:S+=B**E
 assert sp.Rational(Emax,Q)==independent
 if literal:assert ilog(S,B)==Emax
 print('formula check',n,'t=',independent,'valid labeled graphs=',valid,'literal=',literal,flush=True)

for n in [2,3,4]:check_formula(n,literal=True)
# Independent hitting-equation verification on every connected regular graph on ten vertices.
checks=0
for d in range(10):
 Gs=pickle.load(open(f'graphs_10_{min(d,9-d)}.pkl','rb'))
 for G in Gs:
  if d>=5:G=nx.complement(G)
  if nx.is_connected(G):
   H=hitting(G)
   assert max(H[i,j]+H[j,i] for i,j in itertools.combinations(range(10),2))==exact_tau(G)
   checks+=1
print('independent n=10 hitting checks:',checks,flush=True)
for d in [2,4,6,8,10,12,14]:
 G=nx.cycle_graph(15) if d==2 else nx.random_regular_graph(d,15,seed=123+d)
 assert nx.is_connected(G)
 L=lap(G);T=int(L[:14,:14].det());F=int(L[:13,:13].det())
 assert 0<T<=15**13
 H=hitting(G)
 assert H[13,14]+H[14,13]==sp.Rational(15*d*F,T)
 assert max(H[i,j]+H[j,i] for i,j in itertools.combinations(range(15),2))==exact_tau(G)
 print('n=15 identity checks: degree',d,'passed',flush=True)
