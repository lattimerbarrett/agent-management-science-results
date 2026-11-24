import mpmath as mp
mp.mp.dps = 40

# Numerically check the exact Hilbert-transform lower integral for
# f=1_(0,1), w(x)=|x|^(-1+delta).  Only x in (0,1/2) is used.
# R is that restricted output norm divided by the full input norm.
for p in [mp.mpf('1.25'), mp.mpf('1.5'), mp.mpf('3'), mp.mpf('5')]:
    for delta in [mp.mpf('.2'), mp.mpf('.05'), mp.mpf('.01')]:
        lo = delta*mp.log(2)
        def integrand(s):
            t = s/delta
            h = (s + delta*mp.log1p(-mp.exp(-t)))/mp.pi
            return mp.exp(-s)*max(h, mp.mpf(0))**p
        scaled_R = mp.quad(integrand, [lo, 1, 5, 20, mp.inf])**(1/p)
        proven_lower = mp.exp(-2/p)/mp.pi
        assert scaled_R >= proven_lower
        print('p=%s delta=%s delta*R=%s lower=%s' %
              (p, delta, mp.nstr(scaled_R, 10), mp.nstr(proven_lower, 10)))

# Exact positive-parameter formulas checked at rational numerical data:
# scalar power-weight characteristic on (0,1), and its dual identity.
for p in [mp.mpf('1.25'), mp.mpf('1.5'), mp.mpf('3'), mp.mpf('5')]:
    q = p/(p-1)
    for a in [-mp.mpf('.8'), mp.mpf('.1')*(p-1), mp.mpf('.9')*(p-1)]:
        b = -a/(p-1)
        Fp = 1/((1+a)*(1-a/(p-1))**(p-1))
        Fq = 1/((1+b)*(1-b/(q-1))**(q-1))
        assert mp.almosteq(Fq, Fp**(1/(p-1)))
print('All numerical consistency checks passed. These do not prove a sharp matrix lower bound.')
