import sys,pickle
sys.path.insert(0,'workspace')
from agent2_cubic_source import compose
from agent2_source_relations import generators,extend,inv,cat
n=3;G=generators(n);unit=tuple((i+1,) for i in range(n))
found=pickle.load(open('workspace/agent2_nielsen_lifts.pkl','rb'))
targets={}
for a in range(n):
    for b in range(n):
        if a==b:continue
        U=list(unit);Ui=list(unit);U[b]=cat(unit[b],unit[a]);Ui[b]=cat(unit[b],inv(unit[a]));U=tuple(U);Ui=tuple(Ui)
        for k,g in enumerate(G):
            if (a,b,k) not in found:targets[a,b,k]=compose(compose(U,extend(unit,g,1)),Ui)
seen={unit:()};layer=[(unit,())]
for d in range(1,5):
    nxt=[]
    for A,w in layer:
        for a,g in enumerate(G):
            for s in (1,-1):
                letter=s*(a+1)
                if w and w[-1]==-letter:continue
                B=extend(A,g,s);ww=w+(letter,)
                if B not in seen:seen[B]=ww;nxt.append((B,ww))
    layer=nxt
print('ball',len(seen),'targets',len(targets),flush=True)
def evaluate(w):
    A=unit
    for x in w:A=extend(A,G[abs(x)-1],1 if x>0 else -1)
    return A
for A,w in seen.items():
    Ai=evaluate(inv(w))
    for key,target in list(targets.items()):
        B=compose(Ai,target)
        if B in seen:
            word=w+seen[B]
            assert evaluate(word)==target
            found[key]=word;targets.pop(key)
            print('FOUND',key,'length',len(word),'word',word,flush=True)
    if not targets:break
print('remaining',len(targets),flush=True)
pickle.dump(found,open('workspace/agent2_nielsen_lifts_complete.pkl','wb'))
