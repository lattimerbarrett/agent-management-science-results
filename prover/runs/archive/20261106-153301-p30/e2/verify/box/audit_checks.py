import sys, random
import sympy as sp
sys.path.insert(0, 'workspace')
import agent1_complete_checks as a1
import agent2_gaussian_lower as a2

print('Rerunning integrated exact certificates:')
for s in range(3,11): a1.upper_certificate(s)
for k in (2,4,8): a1.lower_certificate(k)
print('Rerunning independent implementation:')
for s in (3,4,5): print(a2.check(s))

# Independently check matrix coordinates agree with complex quotient and
# Hermitian forms, using exact symbolic arithmetic on integer inputs.
rng=random.Random(2024)
for s in (3,4,5):
    D=a2.data(s)
    n,k,P,C,T,S=D
    H,L=a2.matrices(D)
    for trial in range(3):
        x=[rng.randint(-3,3) for _ in range(n)]
        y=[rng.randint(-3,3) for _ in range(n)]
        z=[x[j]+sp.I*x[k+j] for j in range(k)]
        w=[y[j]+sp.I*y[k+j] for j in range(k)]
        product=[0]*(2*k-1)
        for i in range(k):
            for j in range(k): product[i+j]+=z[i]*w[j]
        rem=[sp.expand(product[j]-product[-1]*P[j]) for j in range(2*k-2)]
        norm=sp.re(sum(sp.conjugate(z[j])*w[j] for j in range(k)))
        q=sp.re(sum(sp.conjugate(z[i])*sp.I*S[i][j]*w[j] for i in range(k) for j in range(k)))
        want=[int(sp.re(v)) for v in rem]+[int(sp.im(v)) for v in rem]+[int(norm),int(q)]
        got=[sum(x[i]*H0[i][j]*y[j] for i in range(n) for j in range(n)) for H0 in H]
        assert got==want==a2.pair(x,y,D)
    print('independent exact coordinate checks passed s=',s)
print('ALL AUDIT CHECKS PASSED')
