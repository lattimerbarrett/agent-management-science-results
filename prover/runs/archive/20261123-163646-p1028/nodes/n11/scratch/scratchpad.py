import os
os.environ['OPENBLAS_NUM_THREADS']='1'
os.environ['OMP_NUM_THREADS']='1'
import numpy as np, scipy.linalg as la
import networkx as nx
import random, math, time, json, multiprocessing as mp

# Connectivity >=3 iff deleting any one vertex leaves a biconnected graph.
def no_small_separator(masks):
 n=len(masks)
 for blocked in range(n):
  disc=[-1]*n;low=[0]*n;clock=0;ok=True
  root=0 if blocked!=0 else 1
  def dfs(u,parent):
   nonlocal clock,ok
   disc[u]=low[u]=clock;clock+=1;children=0
   todo=masks[u]&~(1<<blocked)
   while todo and ok:
    bit=todo & -todo;todo^=bit;v=bit.bit_length()-1
    if disc[v]<0:
     children+=1;dfs(v,u);low[u]=min(low[u],low[v])
     if parent!=-1 and low[v]>=disc[u]:ok=False
    elif v!=parent:low[u]=min(low[u],disc[v])
   if parent==-1 and children>1:ok=False
  dfs(root,-1)
  if not ok or clock!=n-1:return False
 return True

# (p,delta) of the external three-terminal component; its m adds a constant.
contexts=[(p,f*p) for p in [.5,1.,2.,4.,8.,16.] for f in [0.,.2,-.2,.45,-.45]]
shunts=[.5,2.,10.]

def search(n):
 rng=random.Random(712345+n);start=time.time()
 a,b=n-2,n-1
 rhs=np.zeros((n-1,3));rhs[0,0]=rhs[1,1]=rhs[a,2]=1.
 pext=np.array([x[0] for x in contexts]);dext=np.array([x[1] for x in contexts])
 def features(L):
  try:Q=la.cho_solve(la.cho_factor(L,lower=True,check_finite=False),rhs,check_finite=False)[[0,1,a],:]
  except la.LinAlgError:return None,None
  p=Q[2,2]
  if p<=0 or p>n:return None,None
  delta=p/2-Q[0,2];m=Q[0,0]+p/4-Q[0,2]
  cross=m-(delta+dext)**2/(p+pext+2)
  r01=Q[0,0]+Q[1,1]-2*Q[0,1]
  transfer=Q[0,2]-Q[1,2]
  same=np.array([r01-transfer**2/(p+q) for q in shunts])
  return np.r_[cross,same],Q
 def update(L,x,y,change):
  if x!=b and y!=b:L[x,y]+=change;L[y,x]+=change
 best=np.full(len(contexts)+len(shunts),-np.inf);winners={}
 accepted=0;improvements=0
 for rep in range(8):
  while True:
   G=nx.random_regular_graph(4,n,seed=rng.randrange(10**9))
   x,y=rng.choice(list(G.edges()));G.remove_edge(x,y)
   others=[v for v in G if v not in (x,y)]
   mapping={v:i for i,v in enumerate(others)};mapping[x]=a;mapping[y]=b
   G=nx.relabel_nodes(G,mapping)
   masks=[sum(1<<v for v in G[u]) for u in range(n)]
   if no_small_separator(masks):break
  edges=list(G.edges());L=4*np.eye(n-1)-nx.to_numpy_array(G,nodelist=range(n))[:-1,:-1];L[a,a]=3
  score,Q=features(L);criterion=(rep*5)%len(best)
  def retain(score,Q):
   nonlocal improvements
   improved=np.nonzero(score>best+1e-10)[0]
   if len(improved):
    frozen=list(edges)
    for z in improved:
     best[z]=score[z];winners[int(z)]={'edges':frozen,'Q':Q.tolist()}
    improvements+=1
  retain(score,Q)
  for k in range(2500):
   i,j=rng.sample(range(len(edges)),2);u,v=edges[i];x,y=edges[j]
   if rng.randrange(2):x,y=y,x
   if len({u,v,x,y})<4 or (masks[u]>>x)&1 or (masks[v]>>y)&1:continue
   update(L,u,v,1);update(L,x,y,1);update(L,u,x,-1);update(L,v,y,-1)
   newscore,newQ=features(L)
   temp=.025*(1-k/2500)**3+.00005
   if newscore is not None and (newscore[criterion]>=score[criterion] or rng.random()<math.exp(max(-745,(newscore[criterion]-score[criterion])/temp))):
    masks[u]^=(1<<v)|(1<<x);masks[v]^=(1<<u)|(1<<y)
    masks[x]^=(1<<y)|(1<<u);masks[y]^=(1<<x)|(1<<v)
    if no_small_separator(masks):
     edges[i]=(u,x);edges[j]=(v,y);score,Q=newscore,newQ;accepted+=1
     retain(score,Q);continue
    masks[u]^=(1<<v)|(1<<x);masks[v]^=(1<<u)|(1<<y)
    masks[x]^=(1<<y)|(1<<u);masks[y]^=(1<<x)|(1<<v)
   update(L,u,v,-1);update(L,x,y,-1);update(L,u,x,1);update(L,v,y,1)
 # Deduplicate portfolios, preserving distinct matrices even if their R01 agrees.
 portfolio={}
 for ctx,w in winners.items():
  key=tuple(round(x,11) for row in w['Q'] for x in row)
  if key not in portfolio:portfolio[key]={'contexts':[],'edges':w['edges'],'Q':w['Q']}
  portfolio[key]['contexts'].append(ctx)
 out={'n':n,'portfolio':list(portfolio.values()),'best_scores':best.tolist(),'accepted':accepted,'seconds':time.time()-start}
 with open('irreducible_portfolio_%d.json'%n,'w') as f:json.dump(out,f)
 return {'n':n,'distinct_retained_matrices':len(portfolio),'accepted_3_connected_states':accepted,'seconds':out['seconds']}

def verify(n):
 from sage.all import matrix,QQ
 with open('irreducible_portfolio_%d.json'%n) as f:r=json.load(f)
 records=[]
 for j,w in enumerate(r['portfolio']):
  G=nx.Graph();G.add_nodes_from(range(n));G.add_edges_from(w['edges'])
  assert no_small_separator([sum(1<<v for v in G[u]) for u in range(n)])
  assert sorted(dict(G.degree()).values())==[3,3]+[4]*(n-2)
  a,b=n-2,n-1;L=matrix(QQ,n-1)
  for u in range(n-1):
   L[u,u]=G.degree(u)
   for v in G[u]:
    if v!=b:L[u,v]=-1
  rhs=matrix(QQ,n-1,3)
  for col,u in enumerate([0,1,a]):rhs[u,col]=1
  invcols=L.solve_right(rhs);Q=invcols.matrix_from_rows([0,1,a])
  # Grounded response on {0,1,a} is the inverse of Q (b is grounded).
  response_grounded=Q.inverse()
  p=Q[2,2];delta=p/2-Q[0,2];m=Q[0,0]+p/4-Q[0,2]
  r01=Q[0,0]+Q[1,1]-2*Q[0,1]
  records.append({'contexts':w['contexts'],'p':str(p),'m':str(m),'delta':str(delta),'R01':str(r01),'grounded_response':[[str(x) for x in row] for row in response_grounded.rows()]})
 with open('irreducible_exact_%d.json'%n,'w') as f:json.dump(records,f)
 print('EXACT portfolio n',n,'matrices',len(records),'cross profiles (p,m,delta):',[(x['p'],x['m'],x['delta']) for x in records],flush=True)

if __name__=='__main__':
 ns=[8,12,20,32,48,72]
 with mp.Pool(2) as pool:
  for out in pool.imap_unordered(search,ns):print(out,flush=True)
 for n in ns:verify(n)
