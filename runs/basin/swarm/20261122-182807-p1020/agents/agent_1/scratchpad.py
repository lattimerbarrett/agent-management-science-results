import sympy as S
n=S.symbols('n', positive=True)
p=2*n/(n-2); q=(n+2)/(n-2); s=(n-2)/2; a=n*(n-2)/(n+2)
checks={
'p=q+1':p-q-1,
'bubble gain exponent':s*p/q-a,
'cutoff beats gain':(n-2-a)-2*(n-2)/(n+2),
'mixed remainder exponent':(2+s*(2-p)/q)-8/(n+2),
'weighted Holder threshold':n/q-a,
'p/q < 2 difference':(2-p/q)-4/(n+2),
'critical Pohozaev cancellation':(n-2)/2-n/p,
'KO exponent':s*q-s-2,
}
for k,v in checks.items():
    z=S.factor(v); assert z==0,(k,z)
    print(k,': verified')
print('n, critical exponent, E_n')
for N in range(5,31):
    A=S.Rational(N*(N-2),N+2)
    es=[b for b in range(2,N+1,2) if b<A]
    # equality cannot occur: (n+2)(beta-n+4)=8
    assert all(S.Rational(b)!=A for b in range(2,2*N+1,2))
    assert es==list(range(2,2*((N-4)//2)+1,2)) if N>=7 else es==[2]
    print(N,str(A),es)
print('Equality requires n+2 to divide 8; for n>=5 only n=6, giving beta=3 (odd).')

# Exact symbolic checks of the radial integral exponents used in the proof.
beta=S.symbols('beta', positive=True)
radial_checks = {
    'h v^p, inner scaling': n + (n+beta) - 2*n - beta,
    'h v^q, outer power': (n-1+beta)-2*s*q-(beta-3),
    'h v^(p-2), outer power': (n-1+beta)-2*s*(p-2)-(n+beta-5),
    'v^q scaling': n-s*q-s,
    'v^(p-2) numerator': s*(p-2)-2,
}
for name, expr in radial_checks.items():
    assert S.factor(expr)==0, (name,expr)
    print(name, ': verified')

# Check the exact bubble integral constants by independent quadrature.
import mpmath as mp
mp.mp.dps=45
for N in range(5,16):
    area=2*mp.pi**(mp.mpf(N)/2)/mp.gamma(mp.mpf(N)/2)
    # r=tan(theta) makes all integrals finite-interval beta integrals.
    A=area*mp.quad(lambda z: mp.sin(z)**(N-1)*mp.cos(z)**(N-1), [0,mp.pi/4,mp.pi/2])
    B=area*mp.quad(lambda z: mp.sin(z)**(N-1)*mp.cos(z), [0,mp.pi/4,mp.pi/2])
    E=area*(N-2)**2*mp.quad(lambda z: mp.sin(z)**(N+1)*mp.cos(z)**(N-3), [0,mp.pi/4,mp.pi/2])
    Aexact=mp.pi**(mp.mpf(N)/2)*mp.gamma(mp.mpf(N)/2)/mp.gamma(N)
    Bexact=mp.pi**(mp.mpf(N)/2)/mp.gamma(mp.mpf(N+2)/2)
    assert abs(A/Aexact-1)<mp.mpf('1e-38')
    assert abs(B/Bexact-1)<mp.mpf('1e-38')
    assert abs(E/(N*(N-2)*A)-1)<mp.mpf('1e-38')
print('Bubble mass, source mass, and Dirichlet energy: independent quadrature verified for n=5,...,15.')

# Check classification and all strict exponent comparisons over a larger range.
for N in range(5,201):
    P=S.Rational(2*N,N-2); Q=P-1
    AA=S.Rational(N*(N-2),N+2)
    bound=max(1,(N-4)//2)
    assert 2< P and 1<P/Q<2 and 0<AA<N-2
    for b in range(2,2*N+1,2):
        assert (b<AA)==(b<=2*bound)
        if b>AA:
            assert b>2 and min(b,N)>AA
            assert S.Rational(8,N+2)>0
print('Classification and trial-function strict inequalities verified through n=200.')
