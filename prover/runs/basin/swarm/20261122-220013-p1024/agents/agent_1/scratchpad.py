from sage.all import *

def matrices(g,b,K=QQ,N=None,B=None,D=3):
    r=(g+2)//3; k=g-r
    assert len(b)==r
    b=list(map(K,b))
    N=4*g-3 if N is None else N
    B=4*g if B is None else B
    R=LaurentPolynomialRing(K,'t'); t=R.gen()
    T=20*g+20*N+10*B
    s=sum((K(binomial(QQ(1)/2,j))*(-1)**j*t**(j*(4*g+2))
           for j in range(T//(4*g+2)+1)),R.zero())
    a=-t**(-2*g+2)*s/2
    phi=sum((b[j]*t**(-(2*g-1-2*j)) for j in range(r)),R.zero())
    u=-k*t**k*phi
    deriv=t**k*phi.derivative()
    def basis(M):
        return ([t**(-2*i) for i in range(M//2+1)] +
                [t**(-2*i-2*g-1)*s for i in range(max(0,(M-2*g-1)//2+1))])
    result={}
    for kind in ['O','S','L']:
        comps=['h','v'] if kind=='S' else ['q']
        rows={}
        for c in comps:
            for m in range(N):
                for e in range(-B-D*m+int(c=='h'),0):
                    rows[c,m,e]=len(rows)
        cols=[]
        for typ in (['H','V'] if kind=='S' else [kind]):
            c={'H':'h','V':'v'}.get(typ,'q')
            for n in range(N):
                cap=n+B+D*n+{'H':-2*g+1,'L':-2*g+2}.get(typ,0)
                for f in basis(cap):
                    col={}
                    def put(poly,c,m):
                        for e,v in poly.dict().items():
                            i=rows.get((c,m,e))
                            if i is not None:
                                col[i]=col.get(i,K.zero())+v
                    for ell in range((N-1-n)//k+1):
                        m=n+ell*k
                        alpha=(1 if typ in ['V','L'] else 0)-QQ(n)/k
                        pol=f*t**n*K(binomial(alpha,ell))*u**ell
                        if typ in ['H','L']: pol*=a
                        put(pol,c,m)
                        if typ=='H':
                            put(-pol/t,'v',m)
                            if m+k<N: put(-pol*deriv,'v',m+k)
                    cols.append(col)
        entries={(i,j):v for j,c in enumerate(cols) for i,v in c.items() if v}
        result[kind]=matrix(K,len(rows),len(cols),entries,sparse=True)
    return result

def delta(g,b,K=QQ,**options):
    A=matrices(g,b,K,**options)
    h={s:M.nrows()-M.rank() for s,M in A.items()}
    return h['O']-h['S']+h['L'],h

if __name__=='__main__':
    for g in range(2,7):
        r=(g+2)//3
        for b in [[int(i==j) for i in range(r)] for j in range(r)]+[[i+2 for i in range(r)]]:
            d,h=delta(g,b)
            assert delta(g,b,B=4*g+2)==(d,h)
            assert delta(g,b,N=4*g-1)==(d,h)
            print(g,b,d,h,flush=True)
    print('All checks passed')
