import sys,json,pickle,time
sys.path.insert(0,'workspace')
from agent2_source_relations import cat,inv
from agent2_cubic_source import compose
from agent2_source_defect import load,defect,insert,vector,reduce
from collections import deque,Counter
D=json.load(open('workspace/agent4_gap_ia3_data.json'));unit=((1,),(2,),(3,));S=[]
for e in D['endomorphisms']:
    name=e['name']
    if name=='I1':A=((-1,),(2,),(3,))
    elif name[0]=='P':p=tuple(map(int,name[2:-1].split(',')));A=tuple((i,) for i in p)
    else:
        sa,sb=map(int,name[4:-1].split(','));alpha=1 if sa==0 else -1;beta=1 if sb==0 else -1
        w=(beta*2,alpha);w=w if alpha==1 else inv(w);A=(w,(2,),(3,))
    S.append(A)
Si=[]
for A in S:
    candidates=[B for B in S if compose(A,B)==unit and compose(B,A)==unit];assert candidates;Si.append(candidates[0])
def matrix(A):return tuple(sum((1 if x==i else -1 if x==-i else 0) for x in A[j]) for i in range(1,4) for j in range(3))
def mm(A,B):return tuple(sum(A[3*i+k]*B[3*k+j] for k in range(3)) for i in range(3) for j in range(3))
SM=list(map(matrix,S));I=matrix(unit);nodes=[(unit,unit,I,())];seen={unit:0};sections={I:0};edges=[];layer=[0];start=time.time()
for dep in range(1,8):
    nxt=[]
    for idx in layer:
        A,Ai,M,w=nodes[idx]
        for j,B in enumerate(S):
            C=compose(A,B);P=mm(M,SM[j])
            if C in seen:k=seen[C]
            else:
                k=len(nodes);seen[C]=k;nodes.append((C,compose(Si[j],Ai),P,w+(j,)));nxt.append(k)
                if P not in sections:sections[P]=k
            edges.append((idx,j,k))
    layer=nxt;print('AutRSdepth',dep,'nodes',len(nodes),'sections',len(sections),'edges',len(edges),'time',time.time()-start,flush=True)
# Extra closing edges from boundary, without new endpoints.
for idx in layer:
    A,Ai,M,w=nodes[idx]
    for j,B in enumerate(S):
        C=compose(A,B)
        if C in seen:edges.append((idx,j,seen[C]))
print('Loading IA ball5',flush=True)
ball=pickle.load(open('workspace/agent2_ia3_left_ball5.pkl','rb'));print('Loaded',len(ball),flush=True)
cache={};adj=[[] for n in nodes];available=0;missing=0
for ia,j,ib in edges:
    Ma=nodes[ia][2];Mb=nodes[ib][2];key=(Ma,j)
    if key not in cache:
        Ta=nodes[sections[Ma]][0];Tbi=nodes[sections[Mb]][1];h=compose(compose(Ta,S[j]),Tbi)
        cache[key]=ball.get(h)
    w=cache[key]
    if w is None:missing+=1;continue
    available+=1;adj[ia].append((ib,w));adj[ib].append((ia,inv(w)))
print('RSavailable',available,'missing',missing,'unique factors',len(cache),flush=True)
RW={i:() for i in sections.values()};q=deque(RW);bases=load();new=[];tested=0
while q:
    a=q.popleft();u=RW[a]
    for b,w in adj[a]:
        cand=cat(u,w)
        if b not in RW:RW[b]=cand;q.append(b);continue
        rel=cat(cand,inv(RW[b]))
        if not rel:continue
        tested+=1;v=vector(rel);res={p:reduce(B,v,p) for p,B in bases.items()}
        if any(res.values()):
            new.append(list(rel))
            for p,B in bases.items():insert(B,v,p)
            print('NEWactualRSrel',len(new),'length',len(rel),'modranks',{p:len(B) for p,B in bases.items()},flush=True)
print('RSFINAL','rewritten nodes',len(RW),'tested',tested,'new',len(new),'time',time.time()-start,flush=True)
json.dump({'relators':new,'source_order':D['names'],'composition':'RTL','left_M':True},open('workspace/agent2_RS_new_relators.json','w'))
