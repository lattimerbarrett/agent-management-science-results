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
    from a3_fiber import reduce_bd
    from sympy import Matrix, ZZ
    from sympy.matrices.normalforms import smith_normal_form
    rows,labels,cols=explicit_matrix(m)
    n=len(rows)
    bd=[{} for _ in rows]+cols
    bd,alive=reduce_bd(bd,[3]*n+[4]*len(cols),False)
    rr=sorted({i for j in alive for i in bd[j]})
    cc=[j for j in alive if bd[j]]
    D=smith_normal_form(Matrix([[bd[j].get(i,0) for j in cc] for i in rr]),domain=ZZ)
    ds=[abs(int(D[i,i])) for i in range(min(D.shape)) if D[i,i]]
    rank=(n+len(cols)-len(alive))//2+len(ds)
    top=len(cols)-rank
    return top-euler(m),top,[t for t in ds if t>1]

if __name__=='__main__':
    for m in range(7,11): print(m,invariant_data(m))
