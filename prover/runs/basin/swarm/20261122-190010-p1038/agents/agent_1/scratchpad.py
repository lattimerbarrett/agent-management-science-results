from sage.all import RealIntervalField, QQ, ZZ
from itertools import count

def pmul(a,b):
    F=a[0].parent();out=[F(0) for _ in range(len(a)+len(b)-1)]
    for i,x in enumerate(a):
        for j,y in enumerate(b):out[i+j] += x*y
    return out

def reduced(m, a, b, r=QQ(1), eps=QQ(0), bits=512):
    # eps=0 means the well-defined ordered vertical cluster limit.
    I=RealIntervalField(bits); r=I(r);R=I(100);d=I(QQ(1)/4)
    S=[I(1)]
    for j in range(1,(m-1)//2+1):
        S=pmul(S,[I(1),2*(I.pi()*j/m).sin(),I(1)])
    if m%2==0:S=pmul(S,[I(1),I(1)])
    p=(R-r)/(d+(d*d+(R-r)**2).sqrt())
    A=pmul(S,[I(1),-p]); B=pmul(S,[p,I(1)])
    for j in range(1,(m-1)//2+1):
        c=(2*I.pi()*j/m).cos()
        q2=r*r+R*R-2*r*R*c
        D=d+(d*d+q2).sqrt()
        A=pmul(A,[I(1),2*(r-R*c)/D,q2/D**2])
        B=pmul(B,[q2/D**2,2*(R-r*c)/D,I(1)])
    if m%2==0:
        q=(R+r)/(d+(d*d+(R+r)**2).sqrt())
        A=pmul(A,[I(1),q]);B=pmul(B,[q,I(1)])
    xy=[];uv=[]
    for j in range(a):
        h=I(-75+eps*QQ(j+1)/(a+1))
        x=r/(-h+(h*h+r*r).sqrt())
        y=R/(d-h+((d-h)**2+R*R).sqrt())
        xy.append((x,y));A=pmul(A,[x,I(1)]);B=pmul(B,[y,I(1)])
    for j in range(b):
        h=I(QQ(3)/4+eps*QQ(j+1)/(b+1))
        u=r/(h+(h*h+r*r).sqrt())
        v=R/(h-d+((h-d)**2+R*R).sqrt())
        uv.append((u,v));A=pmul(A,[I(1),u]);B=pmul(B,[I(1),v])
    for j,(x,y) in enumerate(xy):
        for P in (A,B):
            c=P[j];P[j]=I(0)
            P[j+m]+=c*(x**m+y**m)
            P[j+2*m]-=c*(x*y)**m
    for j in reversed(range(b)):
        u,v=uv[j];k=a+j
        for P in (A,B):
            c=P[k+2*m];P[k+2*m]=I(0)
            P[k+m]+=c*(u**m+v**m)
            P[k]-=c*(u*v)**m
    return [A[k]*B[k+m]-B[k]*A[k+m] for k in range(a,a+m)]

def certified_sign(x):
    if x.lower()>0:return 1
    if x.upper()<0:return -1
    return 0 # interval inconclusive, not an assertion of equality

def check_constants():
    I=RealIntervalField(128)
    x=1/(I(75)+(I(75)**2+1).sqrt())
    y=100/(I(QQ(301)/4)+(I(QQ(301)/4)**2+10000).sqrt())
    u=I(QQ(1)/2);v=100/(I(QQ(1)/2)+(I(QQ(1)/2)**2+10000).sqrt())
    assert x.upper()<QQ(1)/100
    assert y.lower()>QQ(49)/100 and y.upper()<QQ(1)/2
    assert v.lower()>QQ(99)/100 and v.upper()<1
    t=(y+(y*y+8*y/v).sqrt())/2
    assert t.lower()>v.upper() and t.upper()<(1/y).lower()
    q=((1+x/u)/(1+x/v))**2*(1+u*u)/(1+u*v)
    assert q.upper()<QQ(2601)/2990
    print('Certified constants:',x,y,u,v,'saddle',t,'decay',q)

def check_division_identity():
    from sage.all import PolynomialRing
    P=PolynomialRing(QQ,'T');T=P.gen()
    for m in range(1,6):
        a,b=2*m,m
        x,y,u,v=map(QQ,[QQ(1)/7,QQ(2)/5,QQ(1)/2,QQ(4)/5])
        g=(1-x**m*T**m)*(1-y**m*T**m)
        h=(T**m-u**m)*(T**m-v**m)
        F=(1+2*T+3*T**(2*m-1))*(T+x)**a*(1+u*T)**b
        # Low-degree quotient coefficients computed exactly, then ordinary remainder.
        Z=F
        for j in range(a):Z-=Z[j]*T**j*g
        R=P(Z//T**a)
        rem=R%h
        V=list(F)+[QQ(0)]*(a+b+2*m-len(list(F)))
        for j in range(a):
            c=V[j];V[j]=0;V[j+m]+=c*(x**m+y**m);V[j+2*m]-=c*(x*y)**m
        for j in reversed(range(b)):
            k=a+j;c=V[k+2*m];V[k+2*m]=0;V[k+m]+=c*(u**m+v**m);V[k]-=c*(u*v)**m
        assert P(V)==T**a*rem
    print('Exact polynomial-division identities checked for m=1,...,5')

def find_bracket(m, Nmin=1):
    # Dovetailing avoids any assumption about a usable precision/cluster size.
    K0=max(1,(max(0,Nmin-2*m)+3*m-1)//(3*m))
    found=None
    for stage in count():
        for j in range(stage+1):
            K=K0*2**j;bits=128*2**(stage-j)
            a,b=2*m*K,m*K
            D=reduced(m,a,b,bits=bits)
            if all(certified_sign(z)==-1 for z in D):
                found=(a,b);break
        if found:break
    a,b=found
    eps=None
    for stage in count(1):
        for j in range(1,stage+1):
            e=QQ(1)/2**j;bits=128*2**(stage-j)
            D=reduced(m,a,b,eps=e,bits=bits)
            if all(certified_sign(z)==-1 for z in D):eps=e;break
        if eps is not None:break
    for stage in count(1):
        for j in range(1,stage+1):
            r=QQ(1)/2**j;bits=128*2**(stage-j)
            D=reduced(m,a,b,r=r,eps=eps,bits=bits)
            if all(certified_sign(z)==1 for z in D):
                return dict(m=m,a=a,b=b,eps=eps,r_left=r,r_right=QQ(1))

def direct_m1(a,b,r=QQ(1),eps=QQ(1)/1000000,bits=2048):
    I=RealIntervalField(bits)
    pts=[(I(-75+eps*QQ(j+1)/(a+1)),I(0)) for j in range(a)]
    pts += [(I(0),I(r)),(I(QQ(1)/4),I(100))]
    pts += [(I(QQ(3)/4+eps*QQ(j+1)/(b+1)),I(0)) for j in range(b)]
    n=len(pts);mat=[]
    for i,(h,w) in enumerate(pts):
        P=[I(1)]
        for j,(g,z) in enumerate(pts):
            if i==j:continue
            dh=abs(g-h);dw=z-w
            D=dh+(dh**2+dw**2).sqrt()
            fac=[I(1),-dw/D] if i<j else [-dw/D,I(1)]
            P=pmul(P,fac)
        mat.append(P)
    det=I(1)
    for k in range(n):
        j=next(j for j in range(k,n) if certified_sign(mat[j][k]))
        if j!=k:mat[k],mat[j]=mat[j],mat[k];det=-det
        p=mat[k][k];det*=p
        for j in range(k+1,n):
            q=mat[j][k]/p
            for e in range(k+1,n):mat[j][e]-=q*mat[k][e]
            mat[j][k]=I(0)
    return det

if __name__=='__main__':
    check_constants()
    check_division_identity()
    print('AUTOMATIC',find_bracket(1,150),flush=True)
    print('AUTOMATIC',find_bracket(3,200),flush=True)
    for r in [QQ(1)/4,QQ(1)]:
        D=direct_m1(64,32,r=r)
        E=reduced(1,64,32,r=r,eps=QQ(1)/1000000,bits=2048)[0]
        assert certified_sign(D)==certified_sign(E)
        assert (D/E-1).contains_zero()
        print('INDEPENDENT FULL 98 by 98 CHECK:',r,certified_sign(D),flush=True)
    l=QQ(1)/4;h=QQ(1)
    for j in range(32):
        t=(l+h)/2
        s=certified_sign(reduced(1,64,32,r=t,eps=QQ(1)/1000000,bits=2048)[0])
        assert s != 0
        if s==1:l=t
        else:h=t
    print('ROOT BRACKET',l,h,float(l),float(h),flush=True)
    for m in [5,8,12,16]:
        for K in [8,16,32,64,128]:
            a=2*m*K;b=m*K
            D=reduced(m,a,b,eps=QQ(1)/1000000,bits=2048)
            signs=list(map(certified_sign,D))
            print('m,K,n,signs',m,K,a+b+2*m,signs,flush=True)
            if all(s==-1 for s in signs):
                for j in range(1,25):
                    r=QQ(1)/2**j
                    Dp=reduced(m,a,b,r=r,eps=QQ(1)/1000000,bits=2048)
                    if all(certified_sign(z)==1 for z in Dp):
                        print('CERTIFIED BRACKET',m,a,b,r,QQ(1),flush=True)
                        break
                break
