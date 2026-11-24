from sage.all import *

def check(g, bs):
    r=(g+2)//3; k=g-r; h=2*g-2; N=4*g-4
    d=2*g-1-k; Q=N//k; B=2*h+1+d*Q; J=B+N+d*Q+1
    R=LaurentSeriesRing(QQ,'t',default_prec=200); t=R.gen()
    phi=sum(QQ(bs[j])*t**(-(2*g-1-2*j)) for j in range(r))
    q=k*t**k*phi; root=(1-t**(4*g+2)).sqrt(); a=-QQ(1)/2*t**(-h)*root
    n=N+1
    P=matrix(R,n,n)
    for col in range(n):
        for j in range((N-col)//k+1):
            rising=prod(QQ(col)/k+i for i in range(j))
            P[col+j*k,col]=t**col*rising/factorial(j)*q**j
    D=identity_matrix(R,n); C=-t**(-1)*identity_matrix(R,n)
    for col in range(n-k):
        D[col+k,col]=-q
        C[col+k,col]=-t**k*phi.derivative()
    TS=block_matrix([[a*P,zero_matrix(R,n,n)],[a*C*P,D*P]])
    Ts=[P,TS,a*D*P]
    ss=[s for s in range(B+1) if s%2==0 or s>=2*g+1]
    fs=[t**(-s)*(1 if s%2==0 else root) for s in ss]
    ranks=[]
    for T in Ts:
        H=a**(-1)*T.inverse().transpose(); m=T.nrows()
        M=matrix(QQ,m*J,m*len(ss))
        for alpha in range(m):
            for i in range(m):
                for si,f in enumerate(fs):
                    val=H[alpha,i]*f
                    for j in range(1,J+1):
                        M[alpha*J+j-1,i*len(ss)+si]=val[-j]
        ranks.append(M.rank())
    print('g=',g,'b=',bs,'ranks=',ranks,'Delta=',ranks[1]-ranks[0]-ranks[2],flush=True)

check(2,[0])
check(2,[1])
