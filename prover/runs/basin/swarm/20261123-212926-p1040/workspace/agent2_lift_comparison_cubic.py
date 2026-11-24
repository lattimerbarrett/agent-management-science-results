import sys,pickle,json,time
sys.path.insert(0,'workspace')
from agent2_source_relations import generators,extend,cat,inv
from agent2_cubic_source import magnus3,IntegralLattice
from agent2_cubic_nonlinear_closure import actions
from agent2_sparse_closure import apply
import sympy as S
from sympy.matrices.normalforms import smith_normal_form
from sympy.polys.domains import ZZ
from collections import Counter
D=json.load(open('workspace/agent4_gap_ia3_data.json'));G=generators(3);gi={g:i+1 for i,g in enumerate(G)};unit=((1,),(2,),(3,));conv={}
for k,g in enumerate(D['names'],1):
    typ,*a=g;a=[x-1 for x in a]
    if typ=='C':conv[k]=(gi[(typ,*a)],)
    else:
        i,j,l=a;b=gi['C',i,j];c=gi['C',i,l];m=gi['M',i,j,l];conv[k]=(-c,-b,c,b,m)
def evaluate(w):
    A=unit
    for x in w:A=extend(A,G[abs(x)-1],1 if x>0 else -1)
    return A
def convert(w):return cat(*(conv[x] if x>0 else inv(conv[-x]) for x in w[::-1]))
N=9;off=81;L=IntegralLattice()
for v in pickle.load(open('workspace/agent2_ia3_mixed_relations.pkl','rb')).values():L.insert(v)
for v in pickle.load(open('workspace/agent2_ia3_cubic_relations.pkl','rb')).values():L.insert({i+off:c for i,c in v.items()})
short=pickle.load(open('workspace/agent2_nielsen_lifts_complete.pkl','rb'));inverse=pickle.load(open('workspace/agent2_inversion_lifts.pkl','rb'));rels=[]
for e in D['endomorphisms']:
    if e['name']=='I1':lift=inverse
    elif e['name']=='M12(3, 3)':lift={k:short[1,0,k] for k in range(9)}
    else:continue
    for k in range(1,10):
        A=convert(e['images'][k-1]);B=cat(*(lift[x-1] if x>0 else inv(lift[-x-1]) for x in conv[k]))
        assert evaluate(A)==evaluate(B)
        word=cat(A,inv(B));rels.append(word)
        p=magnus3(word,N);v={}
        for w,c in p.items():
            if len(w)==2:v[w[0]*N+w[1]]=c
            if len(w)==3:v[off+(w[0]*N+w[1])*N+w[2]]=c
        L.insert(v)
print('Verified lift comparison relators',len(rels),'maxlen',max(map(len,rels)),flush=True)
Js=[tuple(gi['C',i,j] for i in range(3) if i!=j) for j in range(3)]
for k,g in enumerate(G):
    A=extend(unit,g,1)
    for a in range(3):
        rhs=cat(*(Js[x-1] if x>0 else inv(Js[-x-1]) for x in A[a]))
        word=cat((k+1,),Js[a],(-k-1,),inv(rhs))
        assert evaluate(word)==unit
        p=magnus3(word,N);v={}
        for w,c in p.items():
            if len(w)==2:v[w[0]*N+w[1]]=c
            if len(w)==3:v[off+(w[0]*N+w[1])*N+w[2]]=c
        L.insert(v)
print('Added27 exact inner naturality identities',flush=True)
acts=actions();idx=0
while idx<len(L.queue):
    v=L.queue[idx];idx+=1
    for act in acts:L.insert(apply(act,v))
C={p-off:{i-off:c for i,c in v.items()} for p,v in L.b.items() if p>=off};M=S.zeros(729,len(C))
for j,v in enumerate(C.values()):
    for i,c in v.items():M[i,j]=c
Diag=smith_normal_form(M,domain=ZZ);ds=[abs(Diag[i,i]) for i in range(len(C))]
print('CUBIC rank',len(C),'SNF',dict(Counter(ds)),flush=True)
pickle.dump(C,open('workspace/agent2_ia3_comparison_cubic.pkl','wb'))
