import sys,pickle
sys.path.insert(0,'workspace')
from agent2_cubic_source import compose
from agent2_source_relations import generators,extend,inv
n=3;G=generators(n);unit=tuple((i+1,) for i in range(n));U=list(unit);U[0]=(-1,);U=tuple(U)
targets={k:compose(compose(U,extend(unit,g,1)),U) for k,g in enumerate(G)};found={}
seen={unit:()};layer=[(unit,())]
for d in range(1,5):
    nxt=[]
    for A,w in layer:
        for a,g in enumerate(G):
            for s in (1,-1):
                letter=s*(a+1)
                if w and w[-1]==-letter:continue
                B=extend(A,g,s);ww=w+(letter,)
                if B not in seen:
                    seen[B]=ww;nxt.append((B,ww))
                    for key,target in list(targets.items()):
                        if B==target:found[key]=ww;targets.pop(key)
    layer=nxt
print('ball',len(seen),'targets',len(targets),flush=True)
def evaluate(w):
    A=unit
    for x in w:A=extend(A,G[abs(x)-1],1 if x>0 else -1)
    return A
for A,w in seen.items():
    if not targets:break
    Ai=evaluate(inv(w))
    for key,target in list(targets.items()):
        B=compose(Ai,target)
        if B in seen:
            word=w+seen[B];assert evaluate(word)==target
            found[key]=word;targets.pop(key);print('FOUND',key,'length',len(word),flush=True)
print('remaining',len(targets),'lifts',found,flush=True)
pickle.dump(found,open('workspace/agent2_inversion_lifts.pkl','wb'))
