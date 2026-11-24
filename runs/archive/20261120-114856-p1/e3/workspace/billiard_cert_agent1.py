"""Rigorous interval checker for a proposed two-endpoint billiard word.
Sage AA isolates all spectral roots exactly; RIF outward-rounded interval
Riemann sums rigorously enclose the only integral. This does NOT prove
existence of an iteration orbit: a separate return-map theorem is needed.
"""
from sage.all import *

def data(a,L,H,N=20000,bits=100):
    a,L,H=map(QQ,(a,L,H)); RIF=RealIntervalField(bits)
    P=PolynomialRing(QQ,"x");x=P.gen();Q=x*(x-1)*(x-a)*(x-L)
    core=(Q-H).roots(AA,multiplicities=False)
    extra=(Q+H).roots(AA,multiplicities=False)
    assert len(core)==len(extra)==4
    v=a+L; d=a*L
    ml,mr=1-core[2],1-core[1]
    mi,ma=RIF(ml),RIF(mr); width=ma-mi
    integral=RIF(0)
    for i in range(N):
        t=RIF(QQ(i)/N,QQ(i+1)/N);m=mi+width*t
        R=m*(m-1)*(d+m*m+(v-2)*m-v+1)
        assert R.lower()>0
        T=d+2*m*m+(v-3)*m-v+1
        integral+=T/(2*R.sqrt())*width/N
    J=integral/RIF(H).sqrt()
    F=matrix(RIF,[[1,J],[0,1]]);G=matrix(RIF,[[1,-J],[0,1]])
    refs=[];fitness=[]
    for missing in [core[2],core[1]]:
        lam=RIF(missing);rr=[];ll=[]
        for xi in extra:
            xi=RIF(xi);k=RIF(d)*(xi-1)/((v-1)*xi-d)
            col=vector(RIF,[1,k-lam]);row=vector(RIF,[xi-lam,-1])
            rr.append(identity_matrix(RIF,2)+2/(k-xi)*col.column()*row.row())
            ll.append(vector(RIF,[-1,1/(xi-lam)]))
        refs.append(rr);fitness.append(ll)
    return F,G,refs,fitness

def check(a,L,H,right_word,left_word,N=20000,bits=100):
    F,G,refs,fit=data(a,L,H,N,bits);RIF=F.base_ring()
    PR=identity_matrix(RIF,2);PL=PR
    for j in right_word: PR=refs[1][j]*PR
    for j in left_word: PL=refs[0][j]*PL
    M=PL*G*PR*F
    det=(-1)**(len(right_word)+len(left_word))
    tr=M.trace();disc=tr*tr-4*det
    assert disc.lower()>0
    eig=[(tr+disc.sqrt())/2,(tr-disc.sqrt())/2]
    rho=next(r for r in eig if r.lower()>0 and r.upper()<1)
    X=vector(RIF,[M[0,1],rho-M[0,0]])
    assert not X[0].contains_zero()
    X=-X/X[0]  # E=-1
    assert X[1].upper()<0
    Y=F*X
    assert Y[0].upper()<0
    for side,word in [(1,right_word),(0,left_word)]:
        for j in word:
            assert (fit[side][j]*Y).lower()>0
            Y=refs[side][j]*Y
            assert Y[0].upper()<0
        if side==1:
            assert Y[1].lower()>0
            Y=G*Y
            assert Y[0].upper()<0
        else:assert Y[1].upper()<0
    return rho,X,M
