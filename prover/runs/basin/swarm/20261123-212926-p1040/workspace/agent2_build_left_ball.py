import json,pickle,time,sys,os
sys.path.insert(0,'workspace')
from agent2_source_relations import cat,inv,cm
D=json.load(open('workspace/agent4_gap_ia3_data.json'));G=D['names'];unit=((1,),(2,),(3,));seen={unit:()};layer=[(unit,())]
def extend(A,g,s):
    B=list(A);typ,*labels=g;labels=[x-1 for x in labels];i=labels[0]
    if typ=='C':
        j=labels[1];v=A[j] if s==1 else inv(A[j]);B[i]=cat(v,A[i],inv(v))
    else:
        j,k=labels[1:];v=cm(A[j],A[k]);B[i]=cat(v if s==1 else inv(v),A[i])
    return tuple(B)
start=time.time()
for d in range(1,6):
    nxt=[]
    for A,w in layer:
        for a,g in enumerate(G):
            for s in (1,-1):
                x=s*(a+1)
                if w and w[-1]==-x:continue
                B=extend(A,g,s)
                if B not in seen:
                    ww=w+(x,);seen[B]=ww;nxt.append((B,ww))
    layer=nxt
    print('left-M IA ball depth',d,'size',len(seen),'time',time.time()-start,flush=True)
path='workspace/agent2_ia3_left_ball5.pkl'
with open(path,'wb') as f:pickle.dump(seen,f,protocol=5)
print('saved',path,'bytes',os.path.getsize(path),flush=True)
