"""Certified construction giving b(d,k)<=d-2, d>=3,k>=1.
This is only a weaker bound than the requested b(d,k)=1.
"""
from itertools import combinations
from agent3_check import k_certificate
from agent1_filling import check_certificate,lift_filling_certificate
from agent2_dim3_upper import prefix_order,complete_ridges_dim3

def bits(mask):return [1<<i for i in range(mask.bit_length()) if mask>>i&1]
def uniform(W,q):return tuple(sorted(sum(c) for c in combinations(bits(W),q)))
def uniform_cert(W,q):
    if q==0:return ('simplex',0)
    if W.bit_count()==q:return ('simplex',W)
    v=W&-W
    return ('shed',v,uniform_cert(W^v,q),uniform_cert(W^v,q-1))
def complete(F,k):
    F=tuple(sorted(F));q=F[0].bit_count();d=q-1
    assert d>=3 and k>=1
    oldW=0
    for f in F:oldW|=f
    fc=k_certificate(F,k);assert fc is not None
    G=tuple(sorted(set(f^v for f in F for v in bits(f))))
    gc=k_certificate(G,k);assert gc is not None
    if d==3:
        glist=complete_ridges_dim3(F,k)
        W=oldW
    else:
        W,glist=complete(G,k)
    a=1<<W.bit_length();current=set(F);out=[]
    for h,hc in prefix_order(G,k,gc):
        f=a|h;current.add(f);c=('shed',a,fc,hc)
        assert check_certificate(tuple(sorted(current)),k,c)
        out.append((f,c))
    for h,hc in glist:
        G=tuple(sorted(G+(h,)));f=a|h;current.add(f)
        c=lift_filling_certificate(G,F,a,k,hc)
        assert check_certificate(tuple(sorted(current)),k,c)
        out.append((f,c))
    assert G==uniform(W,d)
    gc=uniform_cert(W,d);fills=set(F)
    for f in uniform(W,d+1):
        if f in fills:continue
        fills.add(f);current.add(f)
        c=lift_filling_certificate(G,tuple(sorted(fills)),a,0,gc)
        assert check_certificate(tuple(sorted(current)),0,c)
        out.append((f,c))
    assert current==set(uniform(W|a,d+1))
    assert (W|a).bit_count()-oldW.bit_count()==d-2
    return W|a,out

if __name__=='__main__':
    cases=steps=0
    for n,q in [(5,5),(6,5),(6,6)]:
        pool=uniform((1<<n)-1,q)
        for mask in range(1,1<<len(pool)):
            F=tuple(f for i,f in enumerate(pool) if mask>>i&1)
            if k_certificate(F,1) is None:continue
            W,out=complete(F,1)
            cases+=1;steps+=len(out)
    print('Certified weaker all-dimensional bound:',cases,'inputs;',steps,'additions')
