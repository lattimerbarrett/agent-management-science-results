from pathlib import Path
from itertools import product
count=0
for N in range(1,5):
    for H in product(range(2), repeat=N):
        # finite approximation with each coordinate making at most one final change
        for g in product(range(3), repeat=N):
            for delta in product(range(2), repeat=N):
                f=tuple(g[n]+delta[n] for n in range(N))
                for n in range(N):
                    for k in range(5):
                        Hk=H[n] if k>=g[n] else 1-H[n]
                        for b in range(2):
                            left=(b!=H[n] or k<f[n])
                            right=(b!=Hk or k<f[n])
                            assert left==right
                            count+=1
print({'modulus_lowergraph_identity_cases':count,'all_valid':True})
