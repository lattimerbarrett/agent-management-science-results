import os
os.environ['OPENBLAS_NUM_THREADS']='1'
os.environ['OMP_NUM_THREADS']='1'
import numpy as np, scipy.linalg as la
import networkx as nx
import random, math, time, json, multiprocessing as mp

def seed_graph(n,d):
    base=({0:12,2:10}[n%4] if d==3 else {0:15,1:21,2:17,3:23,4:19}[n%5])
    with open('best_%s_%s.json'%(base,d)) as f:out=json.load(f)
    G=nx.Graph();G.add_nodes_from(range(base));G.add_edges_from(out['edges'])
    while len(G)<n:
        m=len(G);oldtarget=m-1
        if d==3:
            for a,b in nx.bridges(G):
                H=G.copy();H.remove_edge(a,b)
                if not nx.has_path(H,0,oldtarget):break
            G.remove_edge(a,b)
            G.add_nodes_from(range(m,m+4))
            G.add_edges_from((x,y) for x in range(m,m+4) for y in range(x+1,m+4) if (x,y)!=(m,m+3))
            G.add_edges_from([(a,m),(b,m+3)])
            newtarget=m+3
        else:
            for c in nx.articulation_points(G):
                H=G.copy();H.remove_node(c)
                comps=list(nx.connected_components(H))
                if len(comps)!=2 or c in (0,oldtarget):continue
                sinkcomp=next(C for C in comps if oldtarget in C)
                if 0 not in sinkcomp:
                    ns=[x for x in G[c] if x in sinkcomp]
                    if len(ns)==2:break
            G.add_nodes_from(range(m,m+5))
            for x in ns:G.remove_edge(c,x);G.add_edge(m,x)
            G.add_edges_from((x,y) for x in range(m+1,m+5) for y in range(x+1,m+5))
            G.add_edges_from([(c,m+1),(c,m+2),(m,m+3),(m,m+4)])
            newtarget=m+4
        G=nx.relabel_nodes(G,{oldtarget:newtarget,newtarget:oldtarget},copy=True)
    assert len(G)==n and nx.is_connected(G) and set(dict(G.degree()).values())=={d}
    return G

def search(args):
 n,d,restarts,steps=args
 rng=random.Random(82123+n*100+d);start=time.time()
 seed=seed_graph(n,d)
 ground=n-1;rhs=np.zeros(n-1);rhs[0]=1.
 def value(L):
  try:
   x=la.cho_solve(la.cho_factor(L,lower=True,check_finite=False),rhs,check_finite=False)
   r=x[0]
   return r if 0<r<n-1+1e-5 else -1.
  except la.LinAlgError:return -1.
 def lap(G):return d*np.eye(n-1)-nx.to_numpy_array(G,nodelist=range(n))[:-1,:-1]
 def update(L,a,b,change):
  if a!=ground and b!=ground:L[a,b]+=change;L[b,a]+=change
 best=value(lap(seed));baseline=best;bestedges=list(seed.edges());finals=[]
 for rep in range(restarts):
  G=seed.copy() if rep%2==0 else nx.random_regular_graph(d,n,seed=rng.randrange(10**9))
  edges=list(G.edges());masks=[sum(1<<v for v in G[u]) for u in range(n)]
  L=lap(G);val=value(L)
  for k in range(steps):
   i,j=rng.sample(range(len(edges)),2)
   a,b=edges[i];c,e=edges[j]
   if rng.randrange(2):c,e=e,c
   if len({a,b,c,e})<4 or (masks[a]>>c)&1 or (masks[b]>>e)&1:continue
   update(L,a,b,1);update(L,c,e,1);update(L,a,c,-1);update(L,b,e,-1)
   newval=value(L)
   temp=(.025 if rep%2==0 else .2)*(1-k/steps)**3+.00005
   if newval>0 and (newval>=val or rng.random()<math.exp(max(-745,(newval-val)/temp))):
    masks[a]^=(1<<b)|(1<<c);masks[b]^=(1<<a)|(1<<e)
    masks[c]^=(1<<e)|(1<<a);masks[e]^=(1<<c)|(1<<b)
    seen=1;todo=1
    while todo:
     bit=todo & -todo;todo^=bit;u=bit.bit_length()-1
     more=masks[u]&~seen;seen|=more;todo|=more
    if seen==(1<<n)-1:
     edges[i]=(a,c);edges[j]=(b,e);val=newval
     if val>best+1e-11:best=val;bestedges=list(edges)
     continue
    masks[a]^=(1<<b)|(1<<c);masks[b]^=(1<<a)|(1<<e)
    masks[c]^=(1<<e)|(1<<a);masks[e]^=(1<<c)|(1<<b)
   update(L,a,b,-1);update(L,c,e,-1);update(L,a,c,1);update(L,b,e,1)
  if val>=best-1e-6:finals.append(list(edges))
 out={'n':n,'d':d,'R':best,'baseline':baseline,'edges':bestedges,'finals':finals,'seconds':time.time()-start}
 with open('extended_%s_%s.json'%(n,d),'w') as f:json.dump(out,f)
 return {k:v for k,v in out.items() if k not in ('edges','finals')}

def exactR(edges,n):
 from sage.all import matrix,vector,QQ
 G=nx.Graph();G.add_nodes_from(range(n));G.add_edges_from(edges)
 assert nx.is_connected(G)
 L=matrix(QQ,n-1)
 for u in range(n-1):
  L[u,u]=G.degree(u)
  for v in G[u]:
   if v!=n-1:L[u,v]=-1
 rhs=vector(QQ,[1]+[0]*(n-2))
 return L.solve_right(rhs)[0]

if __name__=='__main__':
 cases=[(n,4,6,12000) for start in [40,90,140] for n in range(start,start+10)]
 cases += [(n,3,6,12000) for n in [50,52,54,56,98,100,102,104,146,148,150,152]]
 with mp.Pool(2) as pool:
  for out in pool.imap_unordered(search,cases):print(out,flush=True)
 print('EXACT VERIFICATION',flush=True)
 exacts={}
 for n,d,_,_ in cases:
  with open('extended_%s_%s.json'%(n,d)) as f:r=json.load(f)
  candidate_edges=[r['edges']]+r['finals']
  seed=seed_graph(n,d)
  base=exactR(list(seed.edges()),n)
  vals=[exactR(es,n) for es in candidate_edges]
  val=max(vals+[base]);exacts[n,d]=val
  print('n',n,'d',d,'best exact candidate',val,'improvement over repeated-block seed',val-base,'close candidates',len(vals),flush=True)
 print('SUCCESSIVE EXACT CANDIDATE INCREMENTS',flush=True)
 for n,d in sorted(exacts,key=lambda x:(x[1],x[0])):
  step=4 if d==3 else 5
  if (n-step,d) in exacts:
   print('d',d,'n',n-step,'->',n,'increment',exacts[n,d]-exacts[n-step,d],flush=True)
 with open('extended_exact_results.json','w') as f:json.dump({f'{n},{d}':str(v) for (n,d),v in exacts.items()},f)
