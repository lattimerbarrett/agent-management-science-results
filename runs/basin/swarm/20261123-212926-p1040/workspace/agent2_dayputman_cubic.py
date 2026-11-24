import sys,pickle
sys.path.insert(0,'workspace')
from agent2_source_relations import generators,red,inv,extend,cat
from agent2_cubic_source import magnus3,IntegralLattice
from agent2_cubic_nonlinear_closure import actions
from agent2_sparse_closure import apply
from itertools import permutations,product
import sympy as S
from sympy.matrices.normalforms import smith_normal_form
from sympy.polys.domains import ZZ
from collections import Counter

def gapcomm(a,b):return cat(inv(a),inv(b),a,b)
def power(a,b):return cat(inv(b),a,b)
def div(a,b):return cat(a,inv(b))
def seeds():
    n=3;C={};M={};G=generators(n);gi={g:i+1 for i,g in enumerate(G)};nextidx=1;conv={}
    for i,j in permutations(range(n),2):
        C[i,j]=(nextidx,);C[i,j+n]=(-nextidx,);conv[nextidx]=(gi['C',i,j],);nextidx+=1
    for i,j,k in permutations(range(n),3):
        if j>k:continue
        M[i,j,k]=(nextidx,);M[i,k,j]=(-nextidx,)
        a=gi['C',i,j];b=gi['C',i,k];c=gi['M',i,j,k]
        conv[nextidx]=(-b,-a,b,a,c);nextidx+=1
        M[i,k,j+n]=power(M[i,j,k],C[i,j])
        M[i,j,k+n]=power(M[i,k,j],C[i,k])
        M[i,k+n,j+n]=power(M[i,j,k+n],C[i,j])
        M[i,j+n,k+n]=power(M[i,k,j+n],C[i,k])
        M[i,k+n,j]=power(M[i,j,k],C[i,k])
        M[i,j+n,k]=power(M[i,k,j],C[i,j])
        for s,t in product((0,n),repeat=2):
            M[i+n,j+s,k+t]=div(gapcomm(inv(C[i,j+s]),inv(C[i,k+t])),M[i,j+s,k+t])
            M[i+n,k+s,j+t]=div(gapcomm(inv(C[i,k+s]),inv(C[i,j+t])),M[i,k+s,j+t])
    # Verify semantic meaning of every signed-M table entry.
    unit=((1,),(2,),(3,))
    from agent2_source_relations import cm
    bad=[]
    for (i,j,k),r in M.items():
        word=cat(*(conv[x] if x>0 else inv(conv[-x]) for x in r[::-1]))
        A=unit
        for x in word:A=extend(A,G[abs(x)-1],1 if x>0 else -1)
        c=cm(((j%n+1)*(1 if j<n else -1),),((k%n+1)*(1 if k<n else -1),))
        B=list(unit);B[i%n]=cat(c,unit[i%n]) if i<n else cat(unit[i%n],inv(c))
        if A!=tuple(B):bad.append((i,j,k))
    print('Signed M semantic failures',bad,flush=True)
    R=[]
    for p in permutations(range(n),3):
        a,b,c=p
        for sa,sb,sc in product((0,n),repeat=3):R.append(cat(M[a+sa,b+sb,c+sc],M[a+sa,c+sc,b+sb]))
    for sa,sb,sc,ta,tb,tc in product((0,n),repeat=6):
        if sa!=ta:R.append(gapcomm(M[sa,1+sb,2+sc],M[ta,1+tb,2+tc]))
    R.append(gapcomm(C[0,1],C[2,1]))
    a,b,c=0,1,2
    R.append(gapcomm(cat(C[c,b],C[a,b]),C[c,a]))
    for sa,sb,sc in product((0,n),repeat=3):
        R.append(div(power(M[a+sa,b+sb,c+sc],C[a,b+sb]),M[a+sa,c+sc,b+n-sb]))
        R.append(div(cat(M[a+n-sa,b+sb,c+sc],M[a+sa,b+sb,c+sc]),gapcomm(inv(C[a,b+sb]),inv(C[a,c+sc]))))
    for sa,sb,sc,sd in product((0,n),repeat=4):
        d=b
        R.append(div(cat(M[c+sc,b+sb,a+sa],M[c+sc,a+sa,d+sd],power(M[c+sc,a+sa,b+sb],C[c,d+n-sd])),power(M[c+sc,a+sa,d+sd],C[a,b+sb])))
    out=[]
    unit=((1,),(2,),(3,))
    for r in R:
        # Reverse GAP order, then replace package left-M by exact right-M words.
        word=cat(*(conv[x] if x>0 else inv(conv[-x]) for x in r[::-1]))
        A=unit
        for x in word:A=extend(A,G[abs(x)-1],1 if x>0 else -1)
        if A!=unit:
            print('INVALID seed index',len(out),'package word',r,flush=True)
            continue
        out.append(word)
    print('Verified exact Day-Putman seed relators',len(out),'maxlength',max(map(len,out)),flush=True)
    return out

def run():
    N=9;off=81;L=IntegralLattice()
    for v in pickle.load(open('workspace/agent2_ia3_mixed_relations.pkl','rb')).values():L.insert(v)
    for v in pickle.load(open('workspace/agent2_ia3_cubic_relations.pkl','rb')).values():L.insert({i+off:c for i,c in v.items()})
    for word in seeds():
        p=magnus3(word,N);vec={}
        assert not any(len(w)==1 for w in p)
        for w,c in p.items():
            if len(w)==2:vec[w[0]*N+w[1]]=c
            elif len(w)==3:vec[off+(w[0]*N+w[1])*N+w[2]]=c
        L.insert(vec)
    acts=actions();idx=0
    while idx<len(L.queue):
        v=L.queue[idx];idx+=1
        for act in acts:L.insert(apply(act,v))
    for iteration in range(20):
        changed=0
        for v in list(L.b.values()):
            for act in acts:
                if L.insert(apply(act,v)):changed+=1
        print('Independent bulk closure iteration',iteration,'changes',changed,flush=True)
        if not changed:break
    else:raise Exception('bulk closure not stable')
    C={p-off:{i-off:c for i,c in v.items()} for p,v in L.b.items() if p>=off}
    Mat=S.zeros(729,len(C))
    for j,v in enumerate(C.values()):
        for i,c in v.items():Mat[i,j]=c
    D=smith_normal_form(Mat,domain=ZZ);ds=[abs(D[i,i]) for i in range(len(C))]
    print('Cubic rank',len(C),'SNF',dict(Counter(ds)),flush=True)
    assert len(C)==197
    pickle.dump(C,open('workspace/agent2_ia3_cubic_primitive_relations.pkl','wb'))
if __name__=='__main__':run()
