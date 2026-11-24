import itertools, numpy as np, os

def regular(A, eps_num=1, eps_den=3):
    m,n=A.shape; total=int(A.sum())
    for xs in range(1,1<<m):
        I=[i for i in range(m) if xs>>i&1]
        if len(I)*eps_den<eps_num*m: continue
        for ys in range(1,1<<n):
            J=[j for j in range(n) if ys>>j&1]
            if len(J)*eps_den<eps_num*n: continue
            e=int(A[np.ix_(I,J)].sum())
            if abs(e*m*n-total*len(I)*len(J))*eps_den>eps_num*m*n*len(I)*len(J):return False
    return True

def test():
    rng=np.random.default_rng(206); pairs=[]
    # Exact epsilon=1/3 regularity tests, not sampled subpairs.
    for _ in range(60):
        A=(rng.random((6,6))<.92).astype(int)
        if A.sum()*5>=4*36 and regular(A):pairs.append(A)
    sets=[np.array([i for i in range(6) if mask>>i&1]) for mask in range(1,64) if mask.bit_count()>=5]
    direct=two=distinct=0
    for A in pairs:
        for X in sets:
            for Y in sets:
                assert A[np.ix_(X,Y)].sum()>0;direct+=1
                for B in pairs:
                    # Both A,B orient endpoint cluster rows to common center columns.
                    degA=A[X,:].sum(axis=0);degB=B[Y,:].sum(axis=0)
                    assert any((degA>=2)&(degB>=2));two+=1
                # Equal endpoint cluster: require two distinct vertices, valid even X=Y.
                assert any((A[X,:].sum(axis=0)>=2)&(A[Y,:].sum(axis=0)>=2));distinct+=1
    print('exact regular pairs:',len(pairs),'direct connectors:',direct,'two-pair connectors:',two,'distinct endpoint connectors:',distinct)

if __name__=='__main__':
    test()
