import itertools,networkx as nx,json
# Internal host types: empty, K2, K3, K3+K2, 3K2, K1,3, 2P3.
def flags(adj,mask):
    deg=[(x&mask).bit_count() if mask>>i&1 else 0 for i,x in enumerate(adj)]
    E=sum(deg)//2
    if not E:return 127
    non=sum(1<<i for i,d in enumerate(deg) if d)
    comps=[];todo=non;tri=False
    while todo:
        front=todo&-todo;comp=0
        while front:
            comp|=front;new=0
            ff=front
            while ff:
                bit=ff&-ff;ff-=bit;new|=adj[bit.bit_length()-1]
            front=new&mask&~comp
        todo&=~comp
        size=comp.bit_count();edges=sum(deg[i] for i in range(len(adj)) if comp>>i&1)//2
        comps.append((size,edges))
    sizes=sorted([a for a,b in comps],reverse=True)
    out=0
    if E==1:out|=2
    if len(sizes)==1 and sizes[0]<=3:out|=4
    if sizes in [[2],[3],[2,2],[3,2]]:out|=8
    if max(deg)<=1 and E<=3:out|=16
    if len(comps)==1 and max(deg)==E and E<=3:out|=32
    if len(comps)<=2 and all(a<=3 and b==a-1 for a,b in comps):out|=64
    return out
pairs=list(itertools.combinations(range(3),2))+[(0,1,2)]
for ca in range(16):
 for cb in range(16):
  H=nx.Graph();H.add_nodes_from(range(7))
  for i in range(3):H.add_edges_from([(0,1+i),(0,4+i),(1+i,4+i)])
  for offset,code in [(1,ca),(4,cb)]:
   for k,subset in enumerate(pairs):
    if code>>k&1:
     w=len(H);H.add_edges_from((w,offset+i) for i in subset)
  n=len(H);full=(1<<n)-1;adj=[sum(1<<w for w in H[i]) for i in range(n)]
  fs=[flags(adj,m) for m in range(1<<n)]
  def contains(a,b):return any(f&a and fs[full^m]&b for m,f in enumerate(fs))
  if contains(4,4) or contains(8,1):continue
  print('candidate',ca,cb,n,'star',contains(32,1),'matching',contains(16,1),'2P3',contains(64,1),'mixed',contains(8,2),flush=True)
  print(list(H.edges()),flush=True)
  if contains(32,1) and contains(16,1) and contains(64,1) and contains(8,2):
   json.dump({'n':n,'edges':list(H.edges())},open('candidate.json','w'));raise SystemExit
print('no candidate')