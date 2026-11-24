from pathlib import Path
import sympy as s
p=Path('workspace/agent2_n7_exhaustive_grading.md')
t=p.read_text()
t=t.replace('The only potentially dangerous E-linear weights are therefore4(f2E) and5(f3E), already handled by Young.','The E-linear terms of weight at most5 are exactly4(f2E),5(f3E), and5(E times two weight1 factors, such as f2^2 or f2Phi2). The first two are the dangerous terms handled by Young. The third has coefficient b^2logR=O(epsilon^2logR), hence tends to zero. This extra harmless class must be included for literal exhaustiveness.')
t=t.split('\n\n## Finite smooth normal extension, not field analyticity')[0]
t+=r'''

## Finite smooth normal extension, not field analyticity

Normal shifts of Phi2/Phi3 do not require an analytic extension. Use the finite Seeley reflection
Phi_ext(z,t)=sum_(k=1)^8 A_k Phi(z,-kt), t<0,
A_k=(-1)^(k+1) k binom(9,k+1),
so (A1,...,A8)=(36,-168,378,-504,420,-216,63,-8).
For every m=0,...,7, sum A_k(-k)^m=1. Thus derivatives through order7 match at the plane. Uniform weighted derivative estimates persist because k ranges over a fixed finite set and 1+|(z,-kt)| is uniformly comparable to1+|(z,t)|. Taylor's theorem with these C7 bounds gives the required finite weighted remainder O((epsilon r)^6) for the total grading; no analyticity of Phi or of the actual graph is needed. The Jacobi equation still matches at the plane through its second derivatives, so its extension residual is O(|t|) times the weighted third-derivative bound, exactly as used in the earlier source estimates.
'''
p.write_text(t)
A=[(-1)**(k+1)*k*s.binomial(9,k+1) for k in range(1,9)]
assert A==[36,-168,378,-504,420,-216,63,-8]
for m in range(8):assert sum(A[k-1]*(-k)**m for k in range(1,9))==1
# One E contributes weight3, and at least one shape factor must occur.
def parts(nn,minimum=1):
    if nn==0:yield ()
    for k in range(minimum,nn+1):
        for tail in parts(nn-k,k):yield(k,)+tail
unknown=[]
for rem in [1,2]:
    for pp in parts(rem):unknown.append((3,pp))
assert unknown==[(3,(1,)),(3,(1,1)),(3,(2,))]
print('Patched exhaustive unknownE list; exact C7 extension identities all verified.')
Path('workspace/agent2_n7_C7_extension_checks.py').write_text(Path(__file__).read_text())
