import json,sys,pathlib,itertools
sys.path.insert(0,'workspace')
from agent4_checker import maximal,subsets
order=json.load(open('workspace/agent2_blowup_best_shelling.json'))['order']
nodes=[];facs=[]
def simplex(F):
 i=len(nodes);nodes.append(['s',F]);facs.append((F,));return i
def make(s,D,L):
 assert s and s.bit_count()<=3
 F=maximal(list(facs[D])+[s|g for g in facs[L]])
 rank=F[0].bit_count();assert all(g.bit_count()==rank for g in F)
 actualD=maximal([g for g in F if g&s!=s]+[g^v for g in F if g&s==s for v in subsets(s) if v.bit_count()==1])
 actualL=tuple(sorted(g^s for g in F if g&s==s))
 assert actualD==facs[D],(s,actualD,facs[D])
 assert actualL==facs[L],(s,actualL,facs[L])
 assert all(g.bit_count()==rank for g in facs[D])
 i=len(nodes);nodes.append(['n',s,D,L]);facs.append(F);return i

def oldface(t,G):return any(G&H==G for H in facs[t])
def full_add(t,F):
 rank=F.bit_count();assert not oldface(t,F)
 assert all(oldface(t,F^v) for v in subsets(F) if v.bit_count()==1)
 if rank==1:return make(F,t,simplex(0))
 node=nodes[t];assert node[0]=='n',('impossible_simplex',facs[t],F)
 _,s,D,L=node
 if s&F==s:return make(s,D,full_add(L,F^s))
 return make(s,full_add(D,F),L)

t=simplex(order[0])
for i,F in enumerate(order[1:],1):
 R=sum(v for v in subsets(F) if v.bit_count()==1 and oldface(t,F^v))
 assert not oldface(t,R)
 if R==F:t=full_add(t,F)
 else:t=make(R,t,simplex(F^R))
 assert set(facs[t])==set(order[:i+1])
print('VERIFIED EXPLICIT 2-DECOMPOSITION','facets',len(facs[t]),'nodes',len(nodes),'root',t,flush=True)
json.dump({'k':2,'nodes':nodes,'root':t,'facets':facs[t]},open('workspace/agent4_base_2decomposition.json','w'))
