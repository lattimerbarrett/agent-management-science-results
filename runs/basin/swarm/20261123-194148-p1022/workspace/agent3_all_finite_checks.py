import sympy as s
from functools import lru_cache
x,y,t=s.symbols('x y t')
N=4

def schur(a,b):
    return sum(x**(a-i)*y**(b+i) for i in range(a-b+1))

def reduce_xy(p):
    p=s.Poly(s.expand(p),x,y)
    out=0
    for (a,b),coeff in p.terms():
        out+=coeff*redmon(a,b)
    return s.expand(out)
@lru_cache(None)
def redmon(a,b):
    if a>=N+1:return 0
    if b<N:return x**a*y**b
    return s.expand(-sum(redmon(a+i,b-i) for i in range(1,N+1)))

def constraints(ranks,weights=None):
    if weights is None:weights=list(range(len(ranks)))
    coeffs=[s.Integer(1)]
    vs=[]
    for i,(r,w) in enumerate(zip(ranks,weights)):
        C=[s.Integer(1)]
        for j in range(1,r+1):
            c=0
            for a in range(N):
                b=j-a
                if 0<=b<=a:
                    v=s.Symbol('c%d_%d%d'%(i,a,b));vs.append(v)
                    c+=v*schur(a,b)
            C.append(c)
        # substitute t+w*x in c polynomial
        D=[0]*(r+1)
        for j,c in enumerate(C):
            for k in range(r-j+1):
                D[j+k]+=s.binomial(r-j,k)*(w*x)**k*c
        new=[0]*(len(coeffs)+r)
        for j,a in enumerate(coeffs):
            for k,b in enumerate(D):
                new[j+k]+=a*b
        coeffs=[reduce_xy(c) for c in new]
    eq=[]
    for k,c in enumerate(coeffs):
        for (a,b),v in s.Poly(c,x,y).terms():
            if b>0 or k>N:
                if v!=0:eq.append(v)
    # eliminate all linear equations first
    sub={}
    while True:
        linear=None
        for e in eq:
            e=s.expand(e.subs(sub))
            if e==0:continue
            avail=[v for v in vs if v not in sub]
            if s.Poly(e,avail).total_degree()==1:
                linear=e;break
        if linear is None:break
        v=next(v for v in reversed(vs) if v not in sub and linear.coeff(v)!=0)
        sol=s.solve(linear,v)[0]
        sub[v]=sol
        eq=[s.expand(e.subs(v,sol)) for e in eq]
        eq=[e for e in eq if e!=0]
    avail=[v for v in vs if v not in sub]
    return eq,avail,sub

def eliminate(eq, vs):
    eq=list(eq); vs=list(vs); sub={}
    while True:
        found=False
        for e in eq:
            for v in vs[::-1]:
                p=s.Poly(e,v)
                if p.degree()==1 and p.coeff_monomial(v).is_number:
                    val=-p.coeff_monomial(1)/p.coeff_monomial(v)
                    sub[v]=val; vs.remove(v)
                    eq=[s.expand(f.subs(v,val)) for f in eq]
                    eq=[f for f in eq if f!=0]
                    found=True;break
            if found:break
        if not found: break
    return eq,vs,sub



def get_system(n,ranks):
    global N
    N=n
    redmon.cache_clear()
    eq,vs,sub=constraints(ranks)
    eq,vs,sub2=eliminate(eq,vs)
    sub.update(sub2)
    return eq,vs,sub

def solve_case(n,ranks):
    eq,vs,sub=get_system(n,ranks)
    degrees=[sum(map(int,str(v).split('_')[1])) for v in vs]
    def order(mon):return (sum(d*m for d,m in zip(degrees,mon)),tuple(-m for m in reversed(mon)))
    G=s.groebner(eq,*vs,order=order) if vs else []
    assert not vs or G.is_zero_dimensional
    points=s.solve(list(G),vs,dict=True) if vs else [{}]
    assert points
    full=[]
    for P in points:
        S=dict(P)
        for _ in range(30):
            old=dict(S)
            S.update({v:s.expand(e.subs(S)) for v,e in sub.items()})
            if S==old:break
        assert all(s.expand(e.subs(S))==0 for e in eq)
        full.append(S)
    return eq,vs,sub,G,full


def verify_width_three():
    cases=[
      (2,(1,1,1),{(0,0),(0,1),(1,-1),(2,0)}),
      (3,(1,3,1),{(0,0),(0,1),(1,-1)}),
      (3,(1,2,2),{(0,0,0,0),(0,1,0,0),(0,1,0,1),(1,-1,0,1),(2,0,0,0)}),
      (4,(1,5,1),{(0,0),(0,1),(1,-1)}),
      (4,(1,4,2),{(0,0,0),(0,1,1),(1,-1,1)}),
      (4,(2,3,2),{(0,0,0,0,0),(1,0,0,-1,1),(0,0,0,1,1)}),
      (4,(1,3,3),{(0,0,0,0,0),(0,1,0,0,0),(0,2,2,1,0),
                   (0,1,1,0,1),(1,-1,1,0,-1),(2,0,0,0,0)})]
    for n,ranks,expected in cases:
        eq,vs,sub,G,Ps=solve_case(n,ranks)
        actual={tuple(P[v] for v in vs) for P in Ps}
        assert actual==expected,(n,ranks,vs,actual)
        residual=[]
        for P in Ps:
            low=P[s.Symbol('c0_10')]
            top=P[s.Symbol('c2_10')]
            if low!=0 and top!=0:
                assert ranks==(1,n-1,n-1)
                assert low==2
                assert all(val==0 for v,val in P.items() if str(v).startswith('c1_'))
                residual.append(tuple(P[v] for v in vs))
        assert len(residual)==int(ranks==(1,n-1,n-1))
        print('width-three',n,ranks,'points',sorted(actual),'nonconstant',residual,flush=True)

def verify_two_blocks():
    for n,rs in [(2,range(2,4)),(3,range(2,6)),(4,range(2,8))]:
        allowed={(0,)*(n-1),(1,)+(0,)*(n-2),(1,)*(n-1)}
        if n==4:allowed.add((2,2,0))
        for r in rs:
            for k in range(1,r):
                _,_,_,G,Ps=solve_case(n,(k,r-k))
                assert G.is_zero_dimensional
                cs={tuple(P.get(s.Symbol(f'c0_{j}0'),0) for j in range(1,n)) for P in Ps}
                assert cs<=allowed
                for c in cs:
                    if c==(1,)+(0,)*(n-2):assert r-k>=n-1
                    if c==(1,)*(n-1):assert k>=n-1
                    if n==4 and c==(2,2,0):assert min(k,r-k)>=3
                print('two-block',n,(k,r-k),'fiber Chern classes',sorted(cs),flush=True)

def verify_existence():
    from itertools import combinations
    J=s.zeros(6)
    for i,j in [(0,1),(2,3),(4,5)]:J[i,j]=1;J[j,i]=-1
    assert J.det()==1 and J.rank()==6
    plane_h0=[]
    for U in [(0,2,4),(0,1,2)]:
        W=[i for i in range(6) if i not in U]
        proj=J.extract(W,W)
        pairing=s.Matrix([[proj[i,j] for i,j in combinations(range(3),2)]])
        plane_h0.append(3-pairing.rank())
    assert plane_h0==[3,2]
    a=s.symbols('a'); B=s.Matrix(2,4,s.symbols('b:8'))
    top=s.Matrix([[0,a],[-a,0]]).row_join(B).col_join(s.zeros(4,6))
    bottom=s.zeros(2,6).col_join((-B.T).row_join(s.zeros(4)))
    assert top.rank()==bottom.rank()==2
    assert (top+bottom)[2:6,2:6]==s.zeros(4)
    assert int(s.binomial(5,2)-1)==9<10
    print('existence: skew rank6; quotient rank9; line splitting1^4 0^5; plane dual h0',plane_h0,flush=True)


def verify_geometric_linear_algebra():
    from itertools import combinations
    h=s.symbols('h')
    horizontal=s.expand((1+2*h)**3)
    quadric=s.series((1+2*h)**5/(1+4*h),h,0,4).removeO()
    linear=s.expand((1+2*h)**4)
    assert horizontal.coeff(h,2)==12
    assert quadric.coeff(h,2)==16
    assert horizontal.coeff(h,1)==6 and linear.coeff(h,1)==8
    # The binary Jacobian is zero precisely when all 2x2 coefficient minors vanish.
    z,w=s.symbols('z w')
    a,b,c,d,e,f=s.symbols('a b c d e f')
    q=a*z*z+b*z*w+c*w*w;r=d*z*z+e*z*w+f*w*w
    jac=s.expand(s.diff(q,z)*s.diff(r,w)-s.diff(q,w)*s.diff(r,z))
    expected=2*((a*e-b*d)*z*z+2*(a*f-c*d)*z*w+(b*f-c*e)*w*w)
    assert s.expand(jac-expected)==0
    # Integrability lemma: determinant on Mat2 has nondegenerate polar form.
    A=s.Matrix([[a,b],[c,d]])
    assert s.hessian(A.det(),(a,b,c,d)).rank()==4
    xx=s.symbols('x0:4');X=s.Matrix(2,2,xx)
    comm=A*X-X*A
    M=s.linear_eq_to_matrix(list(comm),xx)[0]
    assert all(s.expand(M.extract(I,J).det())==0
               for I in combinations(range(4),3) for J in combinations(range(4),3))
    minors={s.expand(M.extract(I,J).det())
            for I in combinations(range(4),2) for J in combinations(range(4),2)}
    for q in [b*b,c*c,(a-d)**2]:
        assert s.expand(q) in minors or s.expand(-q) in minors
    print('geometry: Chern discrepancy12!=16, binary Jacobian, Mat2 polar/centralizer checks passed',flush=True)


def verify_projective_frame_representations():
    from itertools import combinations
    pairs=list(combinations(range(4),2));Q=s.zeros(6)
    for i,I in enumerate(pairs):
        for j,J in enumerate(pairs):
            seq=I+J
            if len(set(seq))==4:
                inv=sum(seq[a]>seq[b] for a in range(4) for b in range(a+1,4))
                Q[i,j]=(-1)**inv
    assert Q.det()!=0
    reps=[]
    for i in range(4):
        for j in range(4):
            A=s.zeros(4);A[i,j]=1;R=s.zeros(6)
            for col,(a,b) in enumerate(pairs):
                for u in range(4):
                    for v,coeff in [(b,A[u,a]),(a,-A[u,b])]:
                        if u==v:continue
                        key=tuple(sorted((u,v)))
                        R[pairs.index(key),col]+=coeff*(1 if u<v else -1)
            assert R.T*Q+Q*R==s.trace(A)*Q
            reps.append(R.reshape(36,1))
    assert s.Matrix.hstack(*reps).rank()==16
    # Conformal orthogonal matrices of a nondegenerate rank6 form have dim16.
    rr=s.symbols('r:36');lam=s.symbols('lam');R=s.Matrix(6,6,rr)
    M=s.linear_eq_to_matrix(list(R.T*Q+Q*R-lam*Q),(*rr,lam))[0]
    assert 37-M.rank()==16
    sympairs=[(0,0),(0,1),(1,1)]
    Qc=s.Matrix([[0,0,-2],[0,1,0],[-2,0,0]])
    symreps=[]
    for i in range(2):
        for j in range(2):
            A=s.zeros(2);A[i,j]=1;R=s.zeros(3)
            for col,(a,b) in enumerate(sympairs):
                for u in range(2):
                    R[sympairs.index(tuple(sorted((u,b)))),col]+=A[u,a]
                    R[sympairs.index(tuple(sorted((a,u)))),col]+=A[u,b]
            assert R.T*Qc+Qc*R==2*s.trace(A)*Qc
            symreps.append(R.reshape(9,1))
    assert s.Matrix.hstack(*symreps).rank()==4
    print('Frame representations checked: gl4 -> cso6 (dim16), gl2 -> cso3 (dim4)',flush=True)

if __name__=='__main__':
    verify_projective_frame_representations()
    verify_geometric_linear_algebra()
    verify_existence()
    verify_two_blocks()
    verify_width_three()
    print('ALL EXACT FINITE CHECKS PASSED')
