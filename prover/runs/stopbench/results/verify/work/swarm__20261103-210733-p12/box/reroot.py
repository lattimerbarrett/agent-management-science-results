import sys,time,json,pickle
sys.path.insert(0,'workspace')
import agent1_Kpersist as K
import agent1_hodge_mod as H
import agent4_verify_lower as L
from collections import Counter
from fractions import Fraction
P=H.P
start=time.time()
# One genus25 next-to-top value from a cold recursion, not a stored value.
v=K.J(25,23,(25,))
print('cold J25,23(25)',v,'seconds',time.time()-start,flush=True)
assert v==69541072
# Recompute the complete decisive root layer, consulting only lower-level stored states.
K.load('workspace/agent3_Kall.pkl')
print('cache loaded',time.time()-start,flush=True)
removed=[key for key in K.KSTORE if key[0]==25 and key[1]==23]
for key in removed: del K.KSTORE[key]
K._K.cache_clear();K.node.cache_clear()
vals=L.roots();parts=list(L.partitions(24))
W=Counter()
Edata=json.load(open('workspace/fz25_exceptional.json'))
E=[(tuple(a),int(c)) for a,c in zip(Edata['basis'],Edata['vector'])]
for a,c in json.load(open('workspace/agent2_Pgood.json'))['terms']:
    c=H.Q(Fraction(c))
    for b,d in E:
        for t,z in H.kappa_expansion(tuple(sorted(tuple(a)+b))): W[t]=(W[t]+c*d*z)%P
W={t:z for t,z in W.items() if z}
idx={tuple(sorted(a)):i for i,a in enumerate(parts)}
total=0
for j,(a,c) in enumerate(W.items()):
    i=idx[a]
    value=K.J(25,23,tuple(x+1 for x in a))
    assert value==vals[i],(i,value,vals[i])
    total=(total+c*value)%P
    if j%200==0: print('roots recomputed',j,'seconds',time.time()-start,flush=True)
print('all root layer recomputed; bulk',total,'seconds',time.time()-start,flush=True)
assert total==799683810
