from itertools import product
from math import isqrt


def pair(a, b):
    return (a+b)*(a+b+1)//2+b


def unpair(z):
    w = (isqrt(8*z+1)-1)//2
    b = z-w*(w+1)//2
    return w-b, b


def decode(r):
    k = (r+1).bit_length()-1
    p = (1 << (k+1))-2-r
    assert 0 <= p < (1 << k)
    return k, p


# Check the numerical recursion measures and the reservoir partition.
for n in range(100000):
    tag = n % 3
    if tag == 0:
        j = n//3
        k, p = decode(j)
        assert k <= j
        assert k == 0 or k-1 < n
    elif tag == 1:
        t = n//3
        assert t < n
        assert t == 0 or t-1 < n
    else:
        j, t = unpair(n//3)
        assert 3*pair(j,t)+2 == n
        assert j < n and t < n
        k, p = decode(j)
        assert k == 0 or k-1 < n
print('100000 reservoir/rank checks passed')

# Finite interval model: k <= 2, seven positive children,
# two negative-reservoir coordinates, and seven diagonal markers.
K = 2
M = (1 << (K+1))-1
D = [1 << j for j in range(M)]
V = [1 << (M+t) for t in range(K)]
R = [1 << (M+K+j) for j in range(M)]
B, lower, upper = [], [], []
for r in range(M):
    k, p = decode(r)
    b = sum(V[t] for t in range(K) if t >= k or ((p >> t) & 1))
    b |= sum(R[j] for j in range(r+1, M))
    lo = b | sum(D[j] for j in range(r, M))
    B.append(b)
    lower.append(lo)
    upper.append(lo | R[r])

# An arbitrary negative-child set and an arbitrary set of positive tests.
# The only hypotheses used are the positive prefix gate and monotonicity
# within each fixed k-block.
models = 0
unions = 0
for a in range(1 << K):
    aneg = sum(V[t] for t in range(K) if (a >> t) & 1)
    for q in range(1 << M):
        valid = True
        for r in range(M):
            if not ((q >> r) & 1):
                continue
            k, p = decode(r)
            if p & ~a:
                valid = False
                break
            for s in range(M):
                ell, h = decode(s)
                if ell == k and not (p & ~h) and not (h & ~a):
                    assert not (B[r] & ~B[s])
                    if not ((q >> s) & 1):
                        valid = False
                        break
            if not valid:
                break
        if not valid:
            continue
        models += 1
        active = [r for r in range(M) if (q >> r) & 1]
        if active:
            r0 = min(active)
            k, p = decode(r0)
            assert p == a & ((1 << k)-1)
            assert not (aneg & ~lower[r0])
            for s in active[1:]:
                assert not (upper[s] & ~lower[r0])
        for choices in range(1 << M):
            children = [lower[r] | (R[r] if ((choices >> r) & 1) else 0)
                        for r in range(M)]
            union = aneg
            for r in active:
                union |= children[r]
            assert union == (children[active[0]] if active else aneg)
            unions += 1
print(f'{models} admissible test models and {unions} child-union checks passed')

# Exhaustive finite checks of the Pi_2 conjunction/disjunction normal forms.
def pi2(table):
    return all(any(row) for row in table)

matrices = [((a,b),(c,d)) for a,b,c,d in product((False,True), repeat=4)]
for A, Bm in product(matrices, repeat=2):
    for use_or in (False, True):
        op = (lambda a,b: a or b) if use_or else (lambda a,b: a and b)
        lhs = op(pi2(A), pi2(Bm))
        rhs = all(any(op(A[u][v], Bm[w][z])
                      for v,z in product(range(2), repeat=2))
                  for u,w in product(range(2), repeat=2))
        assert lhs == rhs
print('512 Pi_2 finite-closure normal-form checks passed')

# Check antitonicity of Phi(complement Psi(.)) for all monotone
# maps P({0,1})->P({0,1}).
N = 4
maps = [f for f in product(range(N), repeat=N)
        if all((a & ~b) or not (f[a] & ~f[b])
               for a in range(N) for b in range(N))]
for phi, psi in product(maps, repeat=2):
    h = [phi[3 ^ psi[a]] for a in range(N)]
    assert all((a & ~b) or not (h[b] & ~h[a])
               for a in range(N) for b in range(N))
print(f'{len(maps)**2} antitonicity checks passed')

# Construct the finite positive Boolean Pi_2 formula DAGs.
# ('T', node, r) is the atomic Pi_2 bounded-witness test in the proof.
# All other leaves are obtained by strictly lower-rank recursion.
from functools import lru_cache
calls = 0

@lru_cache(None)
def formula(node, n):
    global calls
    calls += 1
    def child(label, t):
        assert t < n, (node, n, label, t)
        return formula(node+(label,), t)
    def Q(r):
        k, p = decode(r)
        return ('AND', ('T', node, r),
                tuple(child(-1, t) for t in range(k) if (p >> t) & 1))
    if n % 3 == 0:
        j = n//3
        return ('OR', tuple(Q(r) for r in range(j+1)))
    if n % 3 == 1:
        t = n//3
        return ('OR', child(-1,t),
                tuple(Q(r) for r in range((1 << (t+1))-1)))
    j,t = unpair(n//3)
    return ('OR', tuple(Q(r) for r in range(j)),
            ('AND', Q(j), child(j,t)))

for n in range(25):
    formula((),n)
print(f'Pi_2 formula DAGs for inputs 0..24 constructed; {calls} recursive nodes checked')
