import sys,json,pickle
sys.path.insert(0,'workspace')
import agent2_direct_lpres_cubic as d
from agent2_source_relations import generators,extend,cat,inv
from agent2_cubic_source import magnus3
from agent2_sparse_closure import apply
import sympy as S
from sympy.matrices.normalforms import smith_normal_form
from sympy.polys.domains import ZZ
from collections import Counter
G=generators(3);gi={g:i+1 for i,g in enumerate(G)};unit=((1,),(2,),(3,));conv={}
for k,g in enumerate(d.data['names'],1):
    typ,*a=g;a=[x-1 for x in a]
    if typ=='C':conv[k]=(gi[(typ,*a)],)
    else:
        i,j,l=a;b=gi['C',i,j];c=gi['C',i,l];m=gi['M',i,j,l];conv[k]=(-c,-b,c,b,m)
def evaluate(w):
    word=cat(*(conv[x] if x>0 else inv(conv[-x]) for x in w));A=unit
    for x in word:A=extend(A,G[abs(x)-1],1 if x>0 else -1)
    return A
thetas={e['name']:[tuple(w[::-1]) for w in e['images']] for e in d.data['endomorphisms']}
def substitute(theta,w):return cat(*(theta[x-1] if x>0 else inv(theta[-x-1]) for x in w))
rels=[]
for a,b in [('I1','I1'),('M12(0, 0)','M12(0, 3)'),('M12(0, 3)','M12(0, 0)'),('M12(3, 0)','M12(3, 3)'),('M12(3, 3)','M12(3, 0)')]:
    for k in range(9):
        word=cat(substitute(thetas[a],thetas[b][k]),(-k-1,))
        assert evaluate(word)==unit,(a,b,k)
        rels.append(word);p=magnus3(word,9);assert not any(len(u)==1 for u in p);d.L.insert(d.vector(p))
print('Verified consistency identities',len(rels),'maxlen',max(map(len,rels)),flush=True)
idx=0
while idx<len(d.L.queue):
    v=d.L.queue[idx];idx+=1
    for k in range(9):d.L.insert(d.comm(v,k))
    for act in d.acts:d.L.insert(apply(act,v))
C={p-81:{i-81:c for i,c in v.items()} for p,v in d.L.b.items() if p>=81};M=S.zeros(729,len(C))
for j,v in enumerate(C.values()):
    for i,c in v.items():M[i,j]=c
D=smith_normal_form(M,domain=ZZ);ds=[abs(D[i,i]) for i in range(len(C))]
print('CONSISTENCY SOURCE cubic rank',len(C),'SNF',dict(Counter(ds)),flush=True)
pickle.dump(C,open('workspace/agent2_consistency_cubic.pkl','wb'))
