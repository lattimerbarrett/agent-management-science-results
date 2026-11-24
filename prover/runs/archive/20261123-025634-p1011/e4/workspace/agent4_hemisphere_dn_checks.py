import sympy as s
from pathlib import Path
n,l,z=s.symbols('n l z', positive=True)
# y(theta)=sin(theta)^l F(sin(theta)^2). Derive polar ODE by chain rule.
r=s.symbols('r', positive=True)
F=s.Function('F')
y=r**l*F(r*r)
# r=sin(theta), dtheta r=cos(theta): y''=(1-r²)y_rr-r y_r.
expr=s.expand((1-r*r)*s.diff(y,r,2)+((n-1)/r-n*r)*s.diff(y,r)+(n-l*(l+n-2)/r**2)*y)
a=(l-1)/2;b=(l+n)/2;c=l+n/2
expected=4*r**l*(r*r*(1-r*r)*s.Subs(s.diff(F(z),z,2),z,r*r)+(c-(a+b+1)*r*r)*s.Subs(s.diff(F(z),z),z,r*r)-a*b*F(r*r))
res=s.simplify(expr-expected)
assert res==0, res
# Hypergeometric continuation at z=1 has exponents 0 and 1/2.
assert s.simplify(c-a-b-s.Rational(1,2))==0
A=s.gamma(c)*s.gamma(s.Rational(1,2))/(s.gamma(c-a)*s.gamma(c-b))
B=s.gamma(c)*s.gamma(-s.Rational(1,2))/(s.gamma(a)*s.gamma(b))
mu=2*s.gamma((l+n+1)/2)*s.gamma(l/2)/(s.gamma((l-1)/2)*s.gamma((l+n)/2))
assert s.simplify(-B/A-mu)==0
# Positive for integer n>=3,l>=2 because all four gamma arguments positive.
assert all(float(mu.subs({n:nn,l:ll}))>0 for nn in range(3,41) for ll in range(2,31))
print('Exact polar ODE reduction: residual =',res)
print('Exact gamma quotient DN eigenvalue:',mu)
print('Finite positivity checks: n=3..40,l=2..30 passed (general positivity follows from positive gamma arguments).')
print('n=3,l=2:',s.simplify(mu.subs({n:3,l:2})))
# Ratio recurrence is exact and useful for quadrature-free checks.
ratio=s.simplify(s.expand_func(mu.subs(l,l+2)/mu))
expected_ratio=l*(l+n+1)/((l-1)*(l+n))
assert s.simplify(ratio-expected_ratio)==0
print('mu_(l+2)/mu_l =',expected_ratio)
Path('workspace/agent4_hemisphere_dn_checks.py').write_text(Path(__file__).read_text())

import numpy as np
from scipy.special import gammaln
for nn in range(12,31):
    j=np.arange(100001,dtype=float)
    ll=j+2
    logmu=np.log(2)+gammaln((ll+nn+1)/2)+gammaln(ll/2)-gammaln((ll-1)/2)-gammaln((ll+nn)/2)
    logw=2*np.log((j+1)*(j+nn+1))-logmu+gammaln(j+1)+np.log(j+(nn+2)/2)-gammaln(j+nn+2)
    w=np.exp(logw-logw[0])
    rr=2*(j+1)*(j+nn+1)/(nn-1)-1
    A=w.sum(); BB=np.dot(w,rr); C=np.dot(w,rr*rr)
    print('ratio n=',nn, 'B²/AC=',BB*BB/(A*C))
    if nn>=17:
        import math
        RR=[]
        for kk in range(4):
            vv=np.zeros_like(j)
            for mm in range(kk+1):
                term=np.ones_like(j)
                for ss in range(mm):
                    term *= (j+mm-ss)/(ss+1)*(nn+1+j-ss)/((nn-1)/2-ss)
                vv += (-1)**(kk-mm)*math.comb(kk,mm)*term
            RR.append(vv)
        R=np.array(RR)
        G=(R*w)@R.T
        k=np.arange(4)
        DG=(k[:,None]+k[None,:]+1)*G
        DG=DG/np.sqrt(np.diag(G)[:,None]*np.diag(G)[None,:])
        print('degree2 dilation eigenvalues',np.linalg.eigvalsh(DG[:3,:3]))
        print('degree3 dilation eigenvalues',np.linalg.eigvalsh(DG))

def gram(nn,ss,KK=3):
    from scipy.special import gammaln
    import math
    j=np.arange(20001,dtype=float)
    ell=j+ss; aa=ss+(nn-3)/2
    logI=2*aa*np.log(2)+gammaln(aa+1)+gammaln(aa)-gammaln(2*aa+1)
    lognorm=np.log(np.pi)-2*aa*np.log(2)+gammaln(j+2*aa+1)-gammaln(j+1)-np.log(j+aa+.5)-2*gammaln(aa+.5)
    logmu=np.log(2)+gammaln((ell+nn+1)/2)+gammaln(ell/2)-gammaln((ell-1)/2)-gammaln((ell+nn)/2)
    with np.errstate(divide='ignore',invalid='ignore'):
        W=np.exp(2*logI-lognorm+2*np.log((ell-1)*(ell+nn-1))-logmu)
    W[ell==1]=0
    Rs=[]
    for kk in range(KK+1):
        vv=np.zeros_like(j)
        for mm in range(kk+1):
            qq=ss-1+mm
            if qq==0: continue # pure degree-one mode, zero quadratic response
            rat=np.exp(gammaln(qq+j)-gammaln(qq)-gammaln(j+1)+(1-qq)*np.log(2)+gammaln(aa-qq+1)-gammaln(aa)+gammaln(2*aa+j+1)-gammaln(2*aa+j-qq+2))
            vv += (-1)**(kk-mm)*math.comb(kk,mm)*2**mm*rat
        Rs.append(vv)
    RR=np.array(Rs)
    return (RR*W)@RR.T

for nn in [18,19,20,21]:
    GG=gram(nn,2); G1=gram(nn,1); G3=gram(nn,3)
    dd=nn-1; kk=np.arange(4); cc=2+4*kk/(dd+2)
    TT=cc[:,None]*cc[None,:]*(dd+2)/2*G1
    for k in range(4):
        for l in range(4):
            if k and l: TT[k,l]+=4*k*l*dd/(dd+2)*G3[k-1,l-1]
            if l: TT[k,l]+=2*l*(2*l+dd+2)*GG[k,l-1]
    TT=(TT+TT.T)/2
    HH=(kk[:,None]+kk[None,:]+1)*GG
    sc=np.sqrt(np.diag(GG)); HH/=sc[:,None]*sc[None,:]; TT/=sc[:,None]*sc[None,:]
    print('TRANSLATION TRACE: n',nn,'H-eig',np.linalg.eigvalsh(HH),'T-eig',np.linalg.eigvalsh(TT))
    # Necessary joint criterion H=0,T<0 ruled out whenever T+tH is PSD.
    from scipy.optimize import minimize_scalar
    fun=lambda t:-np.linalg.eigvalsh(TT+t*HH)[0]
    opt=minimize_scalar(fun,bounds=(-1000,1000),method='bounded')
    print('best PSD certificate shift',opt.x,'min eigenvalue',-opt.fun)

from scipy.optimize import differential_evolution
# The following numerical sections are EXPLORATORY, not dimension-threshold proofs.
for nn in [19,20,21]:
    dd=nn-1; g2=gram(nn,2); g1=gram(nn,1); g3=gram(nn,3)
    ix=np.arange(4); scale=np.sqrt(np.diag(g2))
    def normalize(A):return A/(scale[:,None]*scale[None,:])
    H=normalize((ix[:,None]+ix[None,:]+1)*g2)
    powers=2*ix[:,None]+2*ix[None,:]+2
    K=normalize(powers*(powers-1)*g2)
    def translation(rho):
        c=1+2*ix/(dd+2)
        B=2*(dd+2)*rho*c[:,None]*c[None,:]*g1
        for k in range(4):
            for l in range(4):
                if k and l:B[k,l]+=4*(1/(dd+4)+2*dd*rho/((dd+2)*(dd+4)))*k*l*g3[k-1,l-1]
                if l:B[k,l]+=l*(2+8*rho+4*(1+4*rho)*(l-1)/(dd+4))*g2[k,l-1]
        return normalize((B+B.T)/2)
    p=dd//2; q=dd-p
    rhos=[q/(p*dd),p/(q*dd)]
    Bs=[translation(rho) for rho in rhos]
    eig,V=np.linalg.eigh(H)
    assert eig[0]<0 and eig[1]>0
    def vec(angles):
        theta,phi=angles
        uu=np.array([np.sin(theta)*np.cos(phi),np.sin(theta)*np.sin(phi),np.cos(theta)])
        return V[:,0]+V[:,1:]@(np.sqrt(-eig[0]/eig[1:])*uu)
    def objective(angles):
        v=vec(angles)
        return max([v@K@v/np.linalg.norm(K)]+[v@B@v/np.linalg.norm(B) for B in Bs])
    opt=differential_evolution(objective,[(0,np.pi),(0,2*np.pi)],tol=1e-10,seed=21)
    v=vec(opt.x)
    coeff=v/scale
    coeff/=coeff[0]
    print('FULL HESSIAN n',nn,'objective',opt.fun,'coeff',coeff,'scaleH',v@H@v,'scaleK',v@K@v,'translation',[v@B@v for B in Bs])

for nn in list(range(19,61))+[70,80,100,150,200]:
    GG=gram(nn,2); dd=nn-1
    aa=np.array([1,-8/nn,18/nn**2,-9/nn**3])
    coef=np.zeros(7)
    for k in range(4):
        for l in range(4):coef[k+l]+=(k+l+1)*GG[k,l]*aa[k]*aa[l]
    coef/=max(abs(coef))
    roots=np.polynomial.polynomial.polyroots(coef)
    good=[]
    for rr in roots:
        if abs(rr.imag)>1e-8 or rr.real<=0:continue
        xx=rr.real
        av=aa*xx**np.arange(4)
        curvature=sum((k+l)*(k+l+1)*GG[k,l]*av[k]*av[l] for k in range(4) for l in range(4))
        if curvature<0:good.append((xx,curvature/GG[0,0]))
    print('UNIVERSAL p n',nn,'scale minima',good)
    if good:
        g1=gram(nn,1); g3=gram(nn,3)
        xx=good[0][0]; av=aa*xx**np.arange(4)
        trans=[]
        for rho in [(dd-dd//2)/(dd//2*dd),(dd//2)/((dd-dd//2)*dd)]:
            cc=1+2*np.arange(4)/(dd+2)
            B=2*(dd+2)*rho*cc[:,None]*cc[None,:]*g1
            for k in range(4):
                for l in range(4):
                    if k and l:B[k,l]+=4*(1/(dd+4)+2*dd*rho/((dd+2)*(dd+4)))*k*l*g3[k-1,l-1]
                    if l:B[k,l]+=l*(2+8*rho+4*(1+4*rho)*(l-1)/(dd+4))*GG[k,l-1]
            trans.append(av@B@av/GG[0,0])
        print('UNIVERSAL translation brackets',trans)
Path('workspace/agent4_hemisphere_dn_checks.py').write_text(Path(__file__).read_text())
