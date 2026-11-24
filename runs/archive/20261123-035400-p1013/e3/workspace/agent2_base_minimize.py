import networkx as nx,numpy as np,json,itertools,time,os
F=nx.node_link_graph(json.load(open('workspace/agent2_b_vs_clique_counter_min.json')));ROOT=29
POP=np.array([i.bit_count() for i in range(256)],dtype=np.uint8)

def Sfree(F):
 V=set(F);r=ROOT;profiles=set()
 def add(B):
  A=V-set(B);a=F.subgraph(A);com=list(nx.connected_components(a));heavy=sum(len(c) for c in com if len(c)>=3);eb=F.subgraph(B).number_of_edges();assert eb<=1
  if r in A:
   rc=next(c for c in com if r in c);sz=len(rc);profiles.add(('A',sz,heavy-(sz if sz>=3 else 0),eb))
  else:profiles.add(('B',0,heavy,eb))
 # root A
 for I in nx.find_cliques(nx.complement(F.subgraph(V-{r}))):add(I)
 for a,b in F.edges():
  if r in [a,b]:continue
  U=V-{r,a,b}-set(F[a])-set(F[b])
  for I in nx.find_cliques(nx.complement(F.subgraph(U))):add(set(I)|{a,b})
 # root B, independent
 U=V-{r}-set(F[r])
 for I in nx.find_cliques(nx.complement(F.subgraph(U))):add(set(I)|{r})
 # root B, with one edge
 for a,b in F.edges():
  if r in [a,b]:
   U=V-{a,b}-set(F[a])-set(F[b])
   for I in nx.find_cliques(nx.complement(F.subgraph(U))):add(set(I)|{a,b})
  elif not F.has_edge(r,a) and not F.has_edge(r,b):
   U=V-{r,a,b}-set(F[a])-set(F[b])-set(F[r])
   for I in nx.find_cliques(nx.complement(F.subgraph(U))):add(set(I)|{r,a,b})
 for p,q in itertools.product(profiles,repeat=2):
  if p[0]!=q[0] or p[3]+q[3]>1:continue
  req=p[2]+q[2]
  if p[0]=='A':
   sz=p[1]+q[1]-1
   if sz>=3:req+=sz
  if req<=5:return False
 return True

def Tfree(F):
 vs=sorted(F);n=len(vs);ix={v:i for i,v in enumerate(vs)};root=ix[ROOT];nm=[sum(1<<ix[w] for w in F[v]) for v in vs];FULL=(1<<n)-1;profiles=set()
 def comps(mask):
  out=[]
  while mask:
   bit=mask&-mask;cc=bit;front=bit
   while front:
    j=(front&-front).bit_length()-1;front &=front-1;new=nm[j]&mask&~cc;cc|=new;front|=new
   mask &=~cc;out.append(cc)
  return out
 for lo in range(0,1<<n,1<<18):
  a=np.arange(lo,min(lo+(1<<18),1<<n),dtype=np.uint32);valid=np.ones(len(a),dtype=bool)
  for v in range(n):
   q=a&np.uint32(nm[v]);bad=((a>>v)&1)!=0;bad &= (q&(q-np.uint32(1)))!=0;valid &=~bad
  a=a[valid]
  if not len(a):continue
  b=np.uint32(FULL)^a;active=np.zeros(len(a),dtype=np.uint32)
  for v in range(n):active |= np.where((((b>>v)&1)!=0)&((b&np.uint32(nm[v]))!=0),np.uint32(1<<v),np.uint32(0))
  pc=POP[active.view(np.uint8).reshape(-1,4)].sum(axis=1);a=a[pc<=6]
  for aa in a:
   aa=int(aa);bb=FULL^aa;cs=comps(bb);big=[c.bit_count() for c in cs if c.bit_count()>=3];ne=sum(c.bit_count()==2 for c in cs)
   if sum(big)+2*max(0,ne-1)>4:continue
   if aa>>root&1:p=('A',(aa&nm[root]).bit_count(),0,tuple(sorted(big)),ne)
   else:
    rc=next(c for c in cs if c>>root&1);sz=rc.bit_count();obig=big.copy();one=ne
    if sz>=3:obig.remove(sz)
    elif sz==2:one-=1
    p=('B',0,sz,tuple(sorted(obig)),one)
   profiles.add(p)
 for p,q in itertools.product(profiles,repeat=2):
  if p[0]!=q[0]:continue
  if p[0]=='A':
   if p[1]+q[1]>1:continue
   big=list(p[3]+q[3]);ne=p[4]+q[4]
  else:
   rc=p[2]+q[2]-1;big=list(p[3]+q[3]);ne=p[4]+q[4]
   if rc>=3:big.append(rc)
   elif rc==2:ne+=1
  if sum(big)+2*max(0,ne-1)<=4:return False
 return True

assert Sfree(F) and Tfree(F)
t0=time.time();change=True;tested=0
while change:
 change=False
 for e in list(F.edges()):
  G=F.copy();G.remove_edge(*e);tested+=1
  if Sfree(G) and Tfree(G):F=G;change=True;print('deleteedge',e,'now',len(F),F.number_of_edges(),flush=True);json.dump(nx.node_link_data(F),open('workspace/agent2_base_min_checkpoint.json','w'))
 for v in list(F):
  if v==ROOT:continue
  G=F.copy();G.remove_node(v);tested+=1
  if Sfree(G) and Tfree(G):F=G;change=True;print('deletevertex',v,'now',len(F),F.number_of_edges(),flush=True);json.dump(nx.node_link_data(F),open('workspace/agent2_base_min_checkpoint.json','w'))
 print('round',len(F),F.number_of_edges(),'seconds',time.time()-t0,flush=True)
print('FINAL',len(F),F.number_of_edges(),list(F.edges()),'tested',tested,'sec',time.time()-t0)
json.dump(nx.node_link_data(F),open('workspace/agent2_base_min.json','w'))
