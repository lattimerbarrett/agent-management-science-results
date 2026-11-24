import itertools, math
import numpy as np
import sympy as sp
from scipy.integrate import quad

# Angular integration of the radial function of the union of balls.
u, t, th = sp.symbols('u t theta', real=True)
rows = []
for d in (2,3):
    k = sp.pi if d == 2 else 4*sp.pi/3
    # R(theta)^d/d = 1/d + u*sin(theta) + d*u^2*sin(theta)^2/2 + O(u^3)
    f = 1/sp.Integer(d) + u*sp.sin(th) + sp.Rational(d,2)*u**2*sp.sin(th)**2
    radial = u*sp.sin(th) + sp.sqrt(1+u**2*sp.sin(th)**2)
    assert sp.simplify(sp.series(radial**d/d,u,0,3).removeO()-f) == 0
    if d == 2:
        V = sp.integrate(f, (th, 0, sp.pi))*2
    else:
        V = sp.integrate(f*2*sp.pi*sp.sin(th), (th, 0, sp.pi))
    V = sp.expand(V)
    L, M = 2**(d-1), 2**(d-1)-1
    h = sp.series(L*(1-k/V), u, 0, 3).removeO()
    # Compute the coordinate conversion rather than assuming it.
    ut = sp.series(sp.sqrt(sp.exp(2*t**2)-1),t,0,3).removeO()
    assert sp.simplify(ut-sp.sqrt(2)*t) == 0
    F = sp.expand(h.subs(u, ut)/M)
    c, q = F.coeff(t,1), F.coeff(t,2)
    K = sp.simplify(sp.Rational(1,2)+q/c**2)
    rows.append((d,V,sp.simplify(c),sp.simplify(q),K))
assert sp.simplify(rows[0][-1]-sp.pi**2/32) == 0
assert sp.simplify(rows[1][-1]-(4/sp.pi**2-sp.Rational(1,4))) == 0
for row in rows:
    print('d, volume through u^2, c, q, K:', row)

# Independently integrate the unexpanded geometric volume and the Campbell integral.
for d in (2,3):
    k = math.pi if d==2 else 4*math.pi/3
    for uu in (0.01,0.1,0.25):
        def radial(theta):
            z = uu*math.sin(theta)
            return z + math.sqrt(1+z*z)
        if d==2:
            V = 2*quad(lambda z: radial(z)**2/2, 0, math.pi, epsabs=1e-12)[0]
        else:
            V = quad(lambda z: 2*math.pi*math.sin(z)*radial(z)**3/3,0,math.pi,epsabs=1e-12)[0]
        numerical = 2**(d-1)*d*k*quad(lambda r: r**(d-1)*(math.exp(-k*r**d)-math.exp(-V*r**d)),0,np.inf,epsabs=1e-11)[0]
        closed = 2**(d-1)*(1-k/V)
        assert abs(numerical-closed) < 2e-10
print('Independent volume/Campbell quadrature checks passed.')


def data(X):
    n, d = X.shape
    ds = np.sum((X[:,None,:]-X[None,:,:])**2,axis=2)
    edges = sorted(itertools.combinations(range(n),2), key=lambda e: ds[e])
    index = {e:i for i,e in enumerate(edges)}
    births = np.array([ds[e]/4 for e in edges])
    tris=[]
    for vs in itertools.combinations(range(n),3):
        i,j,k=vs
        sides=sorted([ds[i,j],ds[i,k],ds[j,k]])
        if sides[2] >= sides[0]+sides[1]:
            rad=sides[2]/4
        else:
            v,w=X[j]-X[i],X[k]-X[i]
            gram=np.dot(v,v)*np.dot(w,w)-np.dot(v,w)**2
            rad=np.prod(sides)/(4*gram)
        mask=sum(1<<index[e] for e in itertools.combinations(vs,2))
        tris.append((rad,vs,mask))
    tris.sort()
    pivots={}
    pairs=[]
    for death,vs,col in tris:
        while col:
            pivot=col.bit_length()-1
            if pivot in pivots:
                col ^= pivots[pivot]
            else:
                pivots[pivot]=col
                birth=births[pivot]
                if death > birth*(1+1e-10):
                    pairs.append((birth,death,pivot))
                break
    gab=[]
    for ei,(i,j) in enumerate(edges):
        mid=(X[i]+X[j])/2
        dd=np.sum((X-mid)**2,axis=1)
        gab.append(all(dd[k] > births[ei]*(1+1e-12) for k in range(n) if k not in (i,j)))
    assert len(pairs)==sum(gab)-n+1, (len(pairs),sum(gab),n)
    return ds,edges,births,tris,pairs,gab

rng=np.random.default_rng(56429)
checked=0
for d in (2,3):
    for rep in range(140):
        n=int(rng.integers(4,17))
        X=rng.random((n,d))
        ds,edges,births,tris,pairs,gab=data(X)
        tr={vs:rad for rad,vs,_ in tris}
        for uu in (0.015,0.05,0.12,0.25):
            A=sum(death <= birth*(1+uu**2)*(1+1e-12) for birth,death,_ in pairs)
            H=B=0
            for ei,(i,j) in enumerate(edges):
                if not gab[ei]: continue
                r2=births[ei]; r=math.sqrt(r2)
                mid=(X[i]+X[j])/2
                axis=(X[j]-X[i])/(2*r)
                hit=bad=False
                for k in range(n):
                    if k in (i,j): continue
                    z=X[k]-mid
                    xx=np.dot(z,axis)
                    rho2=max(0,np.dot(z,z)-xx*xx)
                    hit |= np.dot(z,z)-r2 <= 2*uu*r*math.sqrt(rho2)+1e-13
                    rad=tr[tuple(sorted((i,j,k)))]
                    bad |= (rad <= r2*(1+uu**2)+1e-13 and max(ds[i,k],ds[j,k]) >= 4*r2-1e-13)
                H+=hit; B+=bad
            assert abs(A-H)<=B, (d,rep,uu,A,H,B)
            checked+=1
print('Exact F2 triangle-boundary reductions and deterministic error bound:',checked,'checks passed.')

# Check the cap enclosure used in the error estimate on samples of bad triples.
cap_count=0
for d in (2,3):
    for trial in range(100000):
        uu=0.25
        # Mix targeted samples with samples not restricted to the asserted cap.
        if trial%2:
            z=np.r_[rng.uniform(1-8*uu**2,1+uu**2),rng.uniform(-4*uu,4*uu,d-1)]
        else:
            z=rng.uniform(-2,2,d)
        p=np.r_[-1.,np.zeros(d-1)]; q=np.r_[1.,np.zeros(d-1)]
        X=np.array([p,q,z]); ds=np.sum((X[:,None,:]-X[None,:,:])**2,axis=2)
        sides=sorted([ds[0,1],ds[0,2],ds[1,2]])
        if sides[-1]>=sum(sides[:2]): rad=sides[-1]/4
        else:
            v,w=q-p,z-p; gram=np.dot(v,v)*np.dot(w,w)-np.dot(v,w)**2
            rad=np.prod(sides)/(4*gram)
        if rad<=1+uu**2 and ds[0,2]>=4:
            assert np.linalg.norm(z-q)<=4*uu+1e-12
            assert 1-8*uu**2-1e-12<=z[0]<=1+uu**2+1e-12
            assert np.linalg.norm(z[1:])<=4*uu+1e-12
            cap_count+=1
print('Additional nonvacuous cap checks:',cap_count)
