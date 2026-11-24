import sys,json,pickle,time
sys.path.insert(0,'workspace')
from agent2_source_relations import cat,inv
from agent2_cubic_source import compose
from agent2_source_defect import load,vector,reduce,insert
from collections import deque
D=json.load(open('workspace/agent4_gap_ia3_data.json'));N=json.load(open('workspace/agent1_neumann_relators.json'));unit=((1,),(2,),(3,));S=[]
for e in D['endomorphisms']:
    name=e['name']
    if name=='I1':A=((-1,),(2,),(3,))
    elif name[0]=='P':p=tuple(map(int,name[2:-1].split(',')));A=tuple((i,) for i in p)
    else:
        sa,sb=map(int,name[4:-1].split(','));alpha=1 if sa==0 else -1;beta=1 if sb==0 else -1
        w=(beta*2,alpha);w=w if alpha==1 else inv(w);A=(w,(2,),(3,))
    S.append(A)
Si=[]
for A in S:Si.append(next(B for B in S if compose(A,B)==unit and compose(B,A)==unit))
def matrix(A):return tuple(sum((1 if x==i else -1 if x==-i else 0) for x in A[j]) for i in range(1,4) for j in range(3))
def mm(A,B):return tuple(sum(A[3*i+k]*B[3*k+j] for k in range(3)) for i in range(3) for j in range(3))
SM=list(map(matrix,S));I=matrix(unit);words=[tuple(w[::-1]) for w in N['nielsen_relators']];targets={I}
for w in words:
    M=I;A=unit
    for j in w:M=mm(M,SM[j]);A=compose(A,S[j]);targets.add(M)
    assert A==unit and M==I
sections={I:(unit,unit,())};q=deque([I]);start=time.time()
while not targets<=sections.keys():
    M=q.popleft();A,Ai,w=sections[M]
    for j,B in enumerate(S):
        P=mm(M,SM[j])
        if P not in sections:sections[P]=(compose(A,B),compose(Si[j],Ai),w+(j,));q.append(P)
print('Neumann targets',len(targets),'GLsections',len(sections),'time',time.time()-start,flush=True)
ball=pickle.load(open('workspace/agent2_ia3_left_ball5.pkl','rb'));print('ball loaded',flush=True)
one={w[0]:A for A,w in ball.items() if len(w)==1}
def evaluate(w):
    A=unit
    for x in w:A=compose(A,one[x])
    return A
short=[]
for A,w in ball.items():
    if 1<=len(w)<=3:short.append((evaluate(inv(w)),w))
print('MITM prefixes',len(short),flush=True)
factors={};unknown={};new=[];allrels=[];bases=load()
for ridx,w in enumerate(words):
    M=I;out=();bad=[]
    for j in w:
        P=mm(M,SM[j]);key=M,j
        if key not in factors:
            h=compose(compose(sections[M][0],S[j]),sections[P][1]);word=ball.get(h)
            if word is None:
                for Ai,u in short:
                    B=compose(Ai,h)
                    if B in ball:word=cat(u,ball[B]);break
            factors[key]=word
            if word is None:unknown[key]=h
        u=factors[key]
        if u is None:bad.append(key)
        elif not bad:out=cat(out,u)
        M=P
    if bad:
        print('Relator',ridx,'FAILED missing',len(bad),'factors',flush=True);continue
    assert evaluate(out)==unit
    allrels.append(list(out));v=vector(out);rs={p:reduce(B,v,p) for p,B in bases.items()}
    if any(rs.values()):
        new.append(list(out))
        for p,B in bases.items():insert(B,v,p)
        print('NEWDIRECT',ridx,'IAwordlen',len(out),'modranks',{p:len(B) for p,B in bases.items()},flush=True)
    else:print('Olddirect',ridx,'IAwordlen',len(out),flush=True)
print('FINISHED NeumannRS','knownfactors',sum(u is not None for u in factors.values()),'unknown',len(unknown),'newrels',len(new),'time',time.time()-start,flush=True)
json.dump({'new_relators':new,'all_relators':allrels},open('workspace/agent2_neumann_RS_relators.json','w'))
pickle.dump(unknown,open('workspace/agent2_neumann_unknown_factors.pkl','wb'))
