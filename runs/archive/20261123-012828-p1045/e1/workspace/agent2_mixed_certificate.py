"""Exact computer-assisted certificate for the mixed k=3 book-density lemma.
Requires SymPy and Sage (both available in the specified environment).
All comparisons take place EXACTLY in Q(sqrt(3)); no floating point is used.
"""
import sympy as S
from sage.all import QuadraticField, PolynomialRing, QQ, binomial


def nonnegative(v):
    """Exact sign of a+b*sqrt(3), taking the positive square root."""
    v=K(v)
    ab=v.list()+[QQ(0),QQ(0)]
    a,b=ab[:2]
    if b==0:return a>=0
    if a>=0 and b>0:return True
    if a<=0 and b<0:return False
    if a>0:return a*a>=3*b*b
    return 3*b*b>=a*a


def check_general_matrix_formulas():
    A,B,C,D,x,y=S.symbols('A B C D x y')
    z=1-x-y
    e2=x*y+x*z+y*z
    e3=x*y*z
    N=S.Matrix([[A+B*x,C+D*z,C+D*y],
                [C+D*z,A+B*y,C+D*x],
                [C+D*y,C+D*x,A+B*z]])
    det=(A**3+A*A*B+2*C**3+2*C*C*D-3*A*C*C-2*A*C*D
         -B*C*C-A*D*D-2*B*C*D-B*D*D
         +(A*B*B+2*C*D*D+2*A*D*D+4*B*C*D+3*B*D*D)*e2
         +(B**3+2*D**3-3*B*D*D)*e3)
    adj=(3*(A-C)**2+2*(B-D)*(A-C)-D*D-2*B*D
         +(B+2*D)**2*e2)
    assert S.expand(N.det()-det)==0
    assert S.expand(sum(N.adjugate())-adj)==0
    d,e=S.symbols('d e')
    assert S.expand((d+e*x)*(d+e*y)*(d+e*z)
                       -(d**3+d*d*e+d*e*e*e2+e**3*e3))==0
    assert S.expand(x*(d+e*y)*(d+e*z)+y*(d+e*x)*(d+e*z)
                    +z*(d+e*x)*(d+e*y)-(d*d+2*d*e*e2+3*e*e*e3))==0


K=QuadraticField(3,'hh')
hh=K.gen()
p,r,h,u,w=S.symbols('p r h u w')


def convert(c):
    c=S.Poly(S.rem(S.expand(c),h*h-3,h),p,r,h)
    out={}
    for (ip,ir,ih),a in c.terms():
        key=(int(ip),int(ir))
        out[key]=out.get(key,K(0))+K(QQ(str(a)))*hh**ih
    return out


def check_rectangle(f,lo,hi,label):
    """Certify f>=0 on p in [lo,hi], r in [0,1/9]."""
    aa={}
    np=max(i for i,j in f)
    nr=max(j for i,j in f)
    for (i,j),a in f.items():
        for k in range(i+1):
            key=(k,j)
            aa[key]=aa.get(key,K(0))+a*binomial(i,k)*lo**(i-k)*(hi-lo)**k/9**j
    bern={}
    for i in range(np+1):
        for j in range(nr+1):
            v=sum(a*binomial(i,k)/binomial(np,k)*binomial(j,l)/binomial(nr,l)
                  for (k,l),a in aa.items() if k<=i and l<=j)
            assert nonnegative(v),(label,i,j,v)
            bern[i,j]=v
    # Independently reconstruct every power coefficient from Bernstein data.
    for k in range(np+1):
        for l in range(nr+1):
            val=sum(bern[i,j]*binomial(np,i)*binomial(np-i,k-i)*(-1)**(k-i)
                            *binomial(nr,j)*binomial(nr-j,l-j)*(-1)**(l-j)
                    for i in range(k+1) for j in range(l+1))
            assert val==aa.get((k,l),0),(label,k,l,val,aa.get((k,l),0),type(val))
    print(label,':',len(bern),'nonnegative exact Bernstein coefficients; reconstruction OK')
    return len(bern)


def main():
    check_general_matrix_formulas()
    s=1-r
    e2=(1-u)/3
    e3=((1-u)/3-w)/9
    A=2*p
    B=6*(p+h-2)
    C=2*s*(1-p)-p*r
    D=3*p*r
    DET=(A**3+A*A*B+2*C**3+2*C*C*D-3*A*C*C-2*A*C*D-B*C*C
         -A*D*D-2*B*C*D-B*D*D
         +(A*B*B+2*C*D*D+2*A*D*D+4*B*C*D+3*B*D*D)*e2
         +(B**3+2*D**3-3*B*D*D)*e3)
    ADJ=(3*(A-C)**2+2*(B-D)*(A-C)-D*D-2*B*D+(B+2*D)**2*e2)
    d=2-2*r+p*r
    e=3*p*r
    BD=d**3+d*d*e+d*e*e*e2+e**3*e3
    BN=d*d+2*d*e*e2+3*e*e*e3
    base=2*p*s*(1-p)/3+(p+h-2)*r*(p*p/3-r)/(p*s)
    mid=4*p/3-2*p*p/3
    hom=2*p*h/3-p*p/3
    # F=base+4*p*s*BN/(3*BD)+2*p*r*ADJ/(3*DET).
    # The following numerator is 3*p*s*BD*DET*(target-F).
    common=4*p*p*s*s*BN*DET+2*p*p*r*s*ADJ*BD
    numerator_mid=S.rem(S.expand(3*p*s*(mid-base)*BD*DET-common),h*h-3,h)
    numerator_hom=S.rem(S.expand(3*p*s*(hom-base)*BD*DET-common),h*h-3,h)
    assert S.Poly(numerator_mid,r).nth(0)==0
    numerator_mid=S.cancel(numerator_mid/r)
    verts=[(S.Rational(0),S.Rational(0)),(S.Rational(1),S.Rational(0)),
           (S.Rational(1,4),S.Rational(1,4))]
    count=0
    for name,NN,lo,hi in [('middle',numerator_mid,K(1)/2,4-2*hh),
                          ('homogeneous',numerator_hom,4-2*hh,hh/3)]:
        assert S.Poly(NN,u,w).total_degree()<=2
        co=[NN.subs({u:x,w:y}) for x,y in verts]
        for i in range(3):
            for j in range(i+1,3):
                x=(verts[i][0]+verts[j][0])/2
                y=(verts[i][1]+verts[j][1])/2
                co.append(2*NN.subs({u:x,w:y})-(co[i]+co[j])/2)
        # Check the triangular Bernstein identity, independently of its formula.
        aa,bb=S.symbols('aa bb')
        recon=(co[0]*(1-aa-bb)**2+co[1]*aa**2+co[2]*bb**2
               +2*co[3]*(1-aa-bb)*aa+2*co[4]*(1-aa-bb)*bb+2*co[5]*aa*bb)
        assert S.expand(NN.subs({u:aa+bb/4,w:bb/4})-recon)==0
        for i,c in enumerate(co):
            count+=check_rectangle(convert(c),lo,hi,f'{name}-{i}')
    print('CERTIFIED:',count,'exact nonnegative coefficients. Mixed-triangle inequality proved.')


if __name__=='__main__':main()
