from fractions import Fraction as F
from sympy import symbols, factor, diff, simplify

def delta(r,q):
    return -F(2*r,r-2)+F(4*r*(q-1),q*(r-1)*(r-2))+F(r*(q-2)*(q-3),(r-1)**2*q)

def finite_branch_check(r,q):
    alpha=F(q-1,q); A=F(2*r,r-1); B=F(r,r-2); C=F(4*r,(r-1)*(r-2)); K=F(r,(r-1)*(r-2))
    bound=K*(4*alpha-2)
    for j in range(r):
        n=10*r*q+j; k=n//r; scores=[]
        for v in range(q):
            rows=[]
            for m in range(k-2*q,k+2*q+1):
                base,rem=divmod(n-m,r-1)
                sizes=[m]+[base+1]*rem+[base]*(r-1-rem)
                Q=F(sum((r*z-n)**2 for z in sizes),r*r)
                E=m-((m-v+q-1)//q)
                edge=F(E)-Q/2
                score=A*E-B*Q+C*alpha*F(r*m-n,r)
                rows.append((edge,score,m))
            em=max(x[0] for x in rows)
            bestE=max(x[1] for x in rows if x[0]==em)
            bestC=max(x[1] for x in rows)
            assert bestC==bestE,(r,q,j,v,'single branch mismatch')
            scores.append(bestE-A*em)
        assert max(scores)-min(scores)<=bound,(r,q,j,'range bound')
    return r*q*(4*q+1)

def algebra_certificate():
    r,q=symbols('r q',positive=True)
    d=-2*r/(r-2)+4*r*(q-1)/(q*(r-1)*(r-2))+r*(q-2)*(q-3)/((r-1)**2*q)
    assert simplify(d.subs(q,2*r)+(r-4)/((r-1)*(r-2)))==0
    assert simplify(d.subs(q,2*r+1)-6*r/((r-2)*(r-1)*(2*r+1)))==0
    assert simplify(diff(d,q)-r*((r-2)*q*q-(2*r-8))/((r-1)**2*(r-2)*q*q))==0
    assert delta(3,5)==-F(3,10) and delta(3,6)==F(1,2)
    assert delta(4,7)==-F(4,9) and delta(4,8)==0
    return factor(d)

if __name__=='__main__':
    print('Symbolic certificate:',algebra_certificate())
    rows=0
    for r in range(3,11):
        for q in range(2,2*r+2): rows+=finite_branch_check(r,q)
    print('Exact residue checks passed;',rows,'candidate rows checked.')
