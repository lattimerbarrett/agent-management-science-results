import sys,pickle,time
sys.path.insert(0,'workspace')
from agent2_source_relations import generators
from agent2_cubic_source import IntegralLattice
from agent2_source_defect import insert as insertfield,reduce as reducefield
from itertools import combinations
G=generators(4);N=len(G);P=list(combinations(range(N),2));H=pickle.load(open('workspace/agent2_ia4_GL_relations.pkl','rb'));start=time.time();L=IntegralLattice()
for col in range(H.cols):
    R={}
    for r,(i,j) in enumerate(P):
        c=int(H[r,col])
        if c:R[i,j]=c;R[j,i]=-c
    for k in range(N):
        v={}
        for (i,j),c in R.items():
            a=(i*N+j)*N+k;b=(k*N+i)*N+j
            v[a]=v.get(a,0)+c;v[b]=v.get(b,0)-c
        L.insert(v)
print('n4quadraticconsequence rank',len(L.b),'secs',time.time()-start,flush=True)
gi={g:i for i,g in enumerate(G)};a=gi['M',2,0,1];b=gi['M',0,1,2];c=gi['C',0,1]
W={}
for (i,j,k),v in [((a,b,c),1),((b,a,c),-1),((c,a,b),-1),((c,b,a),1)]:W[(i*N+j)*N+k]=v
v=W.copy()
while v:
    p=min(v);a=v[p]
    if p not in L.b or a%L.b[p][p]:break
    q=a//L.b[p][p]
    for j,c in L.b[p].items():
        b=v.get(j,0)-q*c
        if b:v[j]=b
        else:v.pop(j,None)
print('OLDW exactremainderterms',len(v),'leading',min(v) if v else None,flush=True)
for p in [2,3,1000003]:
    B={}
    for r in L.b.values():insertfield(B,r,p)
    res=reducefield(B,W,p)
    print('mod',p,'Qconsequence rank',len(B),'Wremainderterms',len(res),flush=True)
pickle.dump(L.b,open('workspace/agent2_rank4_quadratic_cubic.pkl','wb'))
