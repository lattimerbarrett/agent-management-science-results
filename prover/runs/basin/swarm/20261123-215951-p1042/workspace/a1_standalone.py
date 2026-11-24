from itertools import combinations, product
from math import comb

def assignments(m,k):
    for J in combinations(range(m),k):
        for colors in product(range(3),repeat=k):
            if max((colors.count(c) for c in range(3)),default=0)<=2:
                yield tuple(zip(J,colors))

def explicit_matrix(m):
    """Return sparse columns of the explicitly defined integer matrix B_m."""
    rows=[]
    for A in assignments(m,3):
        S=[j for j in range(m) if j not in dict(A)]
        rows += [(A,q) for q in S[1:]]
    index={x:i for i,x in enumerate(rows)}
    cols=[];labels=[]
    for A in assignments(m,4):
        labels.append(A);out={}
        S=[j for j in range(m) if j not in dict(A)]
        for h,(j,c) in enumerate(A):
            A1=A[:h]+A[h+1:]
            if j>S[0]:out[index[A1,j]]=(-1)**h
            else:
                for b,q in enumerate(S):out[index[A1,q]]=(-1)**(h+b)
        cols.append(out)
    assert len(rows)==24*(m-4)*comb(m,3)
    assert len(cols)==54*comb(m,4)
    return rows,labels,cols

def euler(m):
    return (m**4+14*m**3-m*m+34*m+24)//24


def invariant_data(m):
    import heapq
    from sympy import Matrix, ZZ
    from sympy.matrices.normalforms import smith_normal_form
    rows,labels,C=explicit_matrix(m)
    R=[{} for _ in rows]
    for j,col in enumerate(C):
        for i,v in col.items(): R[i][j]=v
    heap=[];serial=0
    def push(j):
        nonlocal serial
        if C[j]:
            units=[i for i,v in C[j].items() if abs(v)==1]
            if units:
                i=min(units,key=lambda i:(len(R[i]),i));a=len(C[j]);b=len(R[i])
                heapq.heappush(heap,((a-1)*(b-1),a+b,serial,j,i));serial+=1
    for j in range(len(C)):push(j)
    pivots=0
    while heap:
        _,_,_,j,i=heapq.heappop(heap)
        if C[j] is None or abs(C[j].get(i,0))!=1:continue
        a=C[j][i];affected=set()
        for k in list(R[i]):
            if k==j:continue
            c=C[k][i]*a
            for l,v in C[j].items():
                z=C[k].get(l,0)-c*v
                if z:C[k][l]=z;R[l][k]=z
                else:C[k].pop(l,None);R[l].pop(k,None)
                affected.update(R[l])
            affected.add(k)
        for l in C[j]:R[l].pop(j,None)
        C[j]=None;pivots+=1
        for k in affected:push(k)
        if len(heap)>2000000:
            heap=[]
            for k in range(len(C)):push(k)
    cc=[c for c in C if c]
    rr=sorted({i for c in cc for i in c})
    if cc:
        D=smith_normal_form(Matrix([[c.get(i,0) for c in cc] for i in rr]),domain=ZZ)
        ds=[abs(int(D[i,i])) for i in range(min(D.shape)) if D[i,i]]
    else:ds=[]
    rank=pivots+len(ds)
    top=len(labels)-rank
    return top-euler(m),top,[t for t in ds if t>1]

if __name__=='__main__':
    for m in range(7,11): print(m,invariant_data(m))
