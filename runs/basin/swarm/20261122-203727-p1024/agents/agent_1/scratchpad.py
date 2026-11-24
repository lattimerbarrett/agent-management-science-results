import sympy as sp
from fractions import Fraction as Q
from math import comb, factorial

def add(a,b):
    c=a.copy()
    for e,v in b.items():
        c[e]=c.get(e,Q(0))+v
        if not c[e]: del c[e]
    return c

def scale(a,c=1,shift=0):
    return {e+shift:v*c for e,v in a.items() if v*c}

def mul(a,b):
    c={}
    for e,u in a.items():
        for f,v in b.items(): c[e+f]=c.get(e+f,Q(0))+u*v
    return {e:v for e,v in c.items() if v}

def rising(a,l):
    z=Q(1)
    for j in range(l): z*=a+j
    return z/Q(factorial(l))

# Entries are Laurent polynomial times s^epsilon, s=(1-t^(4g+2))^(1/2).
def transitions(g,b,kind,inverse=False):
    r=(g+2)//3; k=g-r; N=4*g-3
    assert len(b)==r
    phi={-(2*g-1-2*j):Q(v) for j,v in enumerate(b) if v}
    phip={e-1:e*v for e,v in phi.items()}
    a=scale(phi,k,0 if inverse else k)
    powers=[{0:Q(1)}]
    for l in range((N-1)//k+1): powers.append(mul(powers[-1],a))
    # List entries (row, col, Laurent polynomial, epsilon).
    entries=[]
    def put(i,j,p,e=0):
        if p: entries.append((i,j,p,e))
    for n in range(N):
        for l in range((N-1-n)//k+1):
            m=n+l*k
            c=(-1)**l if inverse else 1
            A=scale(powers[l],c*rising(Q(n,k),l),-n if inverse else n)
            B=scale(powers[l],c*rising(Q(n,k)-1,l),-n if inverse else n)
            if kind=='O': put(m,n,A)
            elif kind=='L':
                put(m,n,scale(B,-1,2*g-2 if inverse else 2-2*g),-1 if inverse else 1)
            else:
                if inverse:
                    put(2*m,2*n,scale(A,-1,2*g-2),-1)
                    put(2*m+1,2*n,scale(B,1,-1))
                    if m+k<N: put(2*(m+k)+1,2*n,mul(A,phip))
                else:
                    put(2*m,2*n,scale(A,-1,2-2*g),1)
                    put(2*m+1,2*n,scale(A,1,1-2*g),1)
                    if m+k<N:
                        put(2*(m+k)+1,2*n,scale(mul(A,phip),1,2-2*g+k),1)
                put(2*m+1,2*n+1,B)
    return N*(2 if kind=='S' else 1),entries

def mat_columns(g,b,kind):
    r=(g+2)//3; k=g-r; N=4*g-3; J=(N-1)//k
    D=N+J*(2*g-1); M=D+2*g-1; P=M+2*D
    d,entries=transitions(g,b,kind)
    K=M+D
    basis=[(m,0) for m in range(0,K+1,2)]+[(m,1) for m in range(2*g+1,K+1,2)]
    bycol=[[] for _ in range(d)]
    for i,j,p,e in entries: bycol[j].append((i,p,e))
    def sqrt_series(power,maxdeg):
        # power is 0,1,2 in the forward matrices.
        ans={}; v=Q(1)
        for l in range(maxdeg//(4*g+2)+1):
            if l: v*= (Q(power,2)-(l-1))*(-1)/l
            if v: ans[l*(4*g+2)]=v
        return ans
    cols=[]
    for j in range(d):
        for pole,zflag in basis:
            col={}
            for i,p,e in bycol[j]:
                maxdeg=pole-min(p)-1
                if maxdeg<0: continue
                ser=sqrt_series(e+zflag,maxdeg)
                for u,v in p.items():
                    for h,w in ser.items():
                        exponent=u-pole+h
                        if -P<=exponent<0:
                            row=i*P+(exponent+P)
                            col[row]=col.get(row,Q(0))+v*w
            cols.append({i:v for i,v in col.items() if v})
    return d,M,P,cols

def rank_sparse(cols,keep=lambda i:True,prime=None):
    piv={}
    for c0 in cols:
        if prime:
            c={i:(v.numerator*pow(v.denominator,-1,prime))%prime for i,v in c0.items() if keep(i)}
            c={i:v for i,v in c.items() if v}
        else: c={i:v for i,v in c0.items() if keep(i)}
        while c:
            i=min(c)
            if i not in piv:
                v=c[i]
                if prime:
                    iv=pow(v,-1,prime); c={j:(w*iv)%prime for j,w in c.items()}
                else: c={j:w/v for j,w in c.items()}
                piv[i]=c; break
            v=c[i]
            for j,w in piv[i].items():
                z=c.get(j,0)-v*w
                if prime: z%=prime
                if z: c[j]=z
                elif j in c: del c[j]
    return len(piv)

def compute(g,b,prime=None,verbose=True):
    hs=[]
    for kind in ['O','S','L']:
        d,M,P,cols=mat_columns(g,b,kind)
        ra=rank_sparse(cols,prime=prime)
        rb=rank_sparse(cols,keep=lambda i:i%P<P-M,prime=prime)
        h=d*M-ra+rb; hs.append(h)
        if verbose: print(g,b,kind,'dimensions',d*P,len(cols),'ranks',ra,rb,'h1',h,flush=True)
    return hs,hs[0]-hs[1]+hs[2]

def check_inverse(g,b):
    # Test the exact transition/inverse identities at t=2, s=3.
    for kind in ['O','S','L']:
        mats=[]
        for inv in [False,True]:
            d,entries=transitions(g,b,kind,inv)
            A=sp.zeros(d)
            for i,j,p,e in entries:
                A[i,j]+=sum(sp.Rational(v.numerator,v.denominator)*sp.Rational(2)**u for u,v in p.items())*sp.Rational(3)**e
            mats.append(A)
        assert mats[0]*mats[1]==sp.eye(d)
    # Verify the claimed pole bounds on both matrices.
    r=(g+2)//3; k=g-r; N=4*g-3
    D=N+((N-1)//k)*(2*g-1)
    for kind in ['O','S','L']:
        for inv in [False,True]:
            for i,j,p,e in transitions(g,b,kind,inv)[1]:
                assert min(p)>=-D # s is a unit

def zero_expected(g):
    H=lambda m: sum(1 for a in range(m+1) if a%2==0 or a>=2*g+1)
    l=sum(H(m) for m in range(4*g-3))
    return [g*g,g*g+l-1,l]

if __name__=='__main__':
    for g in range(2,9):
        r=(g+2)//3
        check_inverse(g,list(range(1,r+1)))
        z,delta=compute(g,[0]*r,verbose=False)
        assert z==zero_expected(g) and delta==1
    print('Transition identities, pole bounds, and independent zero-vector checks passed for g=2,...,8.',flush=True)
    for g,b in [(2,[1]),(3,[1]),(4,[1,0]),(4,[0,1]),(4,[1,1]),(7,[0,0,1])]:
        result=compute(g,b)
        print('RESULT',result,flush=True)
