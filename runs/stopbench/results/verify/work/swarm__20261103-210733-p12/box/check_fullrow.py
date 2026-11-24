import sys,json,runpy,os,pickle
sys.path.insert(0,'workspace')
from fractions import Fraction
from collections import Counter
from sage.all import GF,bernoulli
from math import factorial
import agent1_hodge_mod as H
import agent4_verify_lower as L
p=H.P;F=GF(p)
Pterms=[(tuple(a),H.Q(Fraction(c))) for a,c in json.load(open('workspace/agent2_Pgood.json'))['terms']]
basis=[tuple(a) for a in json.load(open('workspace/fz25_upper_data.json'))['basis']]
vals=L.roots();ps=list(L.partitions(24));idx={tuple(sorted(a)):i for i,a in enumerate(ps)}
# Build full bulk linear functional on degree-12 monomials from saved genus25 roots.
bulk=[]
for b in basis:
    W=Counter()
    for a,c in Pterms:
        for part,z in H.kappa_expansion(tuple(sorted(a+b))):W[part]=(W[part]+c*z)%p
    assert all(idx[a] in vals for a,c in W.items() if c),(b,[a for a,c in W.items() if c and idx[a] not in vals])
    bulk.append(sum(c*vals[idx[a]] for a,c in W.items() if c)%p)
print('bulk complete',flush=True)
# Use all twelve regenerated exact solutions.
L.factor.cache_clear()
origopen=open
L.factor=lambda h,d:pickle.load(origopen('scratch/agent2_exactfactor_%02d_%02d.pkl'%(h,d),'rb'))
# monkeypatch read of regenerated certificates
import builtins
def patched(path,*args,**kw):
    s=str(path)
    if s.startswith('workspace/agent2_exact_divisibility_'):path=s.replace('workspace/','scratch/')
    return origopen(path,*args,**kw)
builtins.open=patched
bnd=[]
for i,b in enumerate(basis):
    z,vs=L.boundary([(b,1)])
    bnd.append(z)
    if i%10==0:print('bnd done',i,flush=True)
row=[(x+y)%p for x,y in zip(bulk,bnd)]
rels=[[H.Q(Fraction(c)) for c in r] for r in json.load(origopen('workspace/fz25_upper_data.json'))['matrix']]
ann=[sum(x*y for x,y in zip(row,r))%p for r in rels]
print('annihilating FZ rows',sum(x==0 for x in ann),'of',len(ann));print(ann)
print('full row',row)
json.dump({'bulk':bulk,'boundary':bnd,'row':row,'annihilate_FZ':ann},origopen('fullrow.json','w'))
