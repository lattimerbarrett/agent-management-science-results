def check_exterior_constructions():
    import sympy as S
    from itertools import combinations,permutations
    pairs=list(combinations(range(6),2));idx={v:i for i,v in enumerate(pairs)}
    # Coordinate incidence kernels force bivectors to be eigenvectors.
    # Pair-sum incidence kernels force equal eigenvalues on adjacent pairs.
    assert [(i,j) for i,o in enumerate(pairs) for j,v in enumerate(pairs) if set(v)<=set(o)]==[(i,i) for i in range(15)]
    rows=[]
    for i,j,k in permutations(range(6),3):
        row=[0]*15;row[idx[tuple(sorted((i,k)))]]=1
        row[idx[tuple(sorted((j,k)))]]=-1;rows.append(row)
    assert S.Matrix(rows).rank()==14 and S.Matrix(rows)*S.ones(15,1)==S.zeros(len(rows),1)
    M=S.zeros(6);z=iter(S.symbols('z:9'))
    for i,j in pairs:
        if i<2:M[i,j]=next(z);M[j,i]=-M[i,j]
    for I in combinations(range(6),5):
        for J in combinations(range(6),5):assert M.extract(I,J).det()==0
    w=S.zeros(6)
    for i in (0,2,4):w[i,i+1]=1;w[i+1,i]=-1
    g=S.diag(2,1,1,1,1,1);v=g*w*g.T
    assert w.det()==1 and w.rank()==v.rank()==6
    assert v[0,1]!=v[2,3] and w[0,1]==w[2,3]
    sym=list(combinations(range(6),2))+[(i,i) for i in range(6)]
    si={p:i for i,p in enumerate(sym)};mu=S.zeros(21,36);a=S.zeros(36,15)
    for i in range(6):
        for j in range(6):mu[si[tuple(sorted((i,j)))],6*i+j]=1
    for k,(i,j) in enumerate(pairs):a[6*i+j,k]=1;a[6*j+i,k]=-1
    assert mu.rank()==21 and a.rank()==15 and mu*a==S.zeros(21,15)
    x,y,b,l,pa=S.symbols('x y b l pa');s=x+y;p=x*y
    c=[1,-2*s,2*s*s-p,-s*p];r=[1,s,s*s-p,s**3-2*s*p]
    assert S.expand(r[1]-3*s-c[1])==S.expand(r[2]-2*s*r[1]+3*s*s-c[2])==0
    assert S.expand(r[3]-s*r[2]+s*s*r[1]-s**3-c[3])==0
    q=S.expand(b*x*(c[2]-b*x*(c[1]-b*x))-c[3])
    assert S.Poly(q,x,y).coeff_monomial(x*y*y)==2*b+1
    assert S.Poly(S.expand(l*x*c[1]+S.Rational(3,2)*l*l*x*x),x,y).coeff_monomial(x*y)==-2*l
    assert S.solve(2*pa-2+(4-2)*2,pa)==[-1]
    def line(k):return [int(S.binomial(k+3,3)) if k>=0 else 0,0,0,int(S.binomial(-k-1,3)) if k<=-4 else 0]
    table=[]
    for i in range(4):
        A=line(-2-i);B=[4*t for t in line(-1-i)]
        if i==3:assert A[3]==B[3]==4;table.append([0]*4)
        else:table.append([B[j]+(A[j+1] if j<3 else 0) for j in range(4)])
    assert table==[[0]*4,[0]*4,[0,0,1,0],[0]*4]
    al,be=S.symbols('al be',nonzero=True)
    assert S.Matrix([[al,be]]).rank()==1 and S.diag(al,al,be,be).det()==al**2*be**2
    assert S.binomial(5,2)-1==9<10 and S.binomial(4,2)==6!=8
    print('P5 rank/uniformity/simplicity/Koszul and P4 wedge/parity/cohomology checks passed.')

check_exterior_constructions()
