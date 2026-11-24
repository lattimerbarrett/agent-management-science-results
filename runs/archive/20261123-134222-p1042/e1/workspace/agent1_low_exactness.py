from itertools import combinations, product
from math import comb
from pathlib import Path
import json
import sympy as sp
import sympy as sp

# Lexicographic shelling check for X_{m,q}: maximal faces are all color
# words with distinguished color 3 occurring at most q times.  Given G<F,
# replace in F the first differing entry by its smaller value in G.
def shelling_check(m,q):
    facets=[f for f in product(range(4),repeat=m) if f.count(3)<=q]
    checks=0
    for i,F in enumerate(facets):
        for G in facets[:i]:
            j=next(j for j in range(m) if G[j]!=F[j])
            H=F[:j]+(G[j],)+F[j+1:]
            assert H<F and H.count(3)<=q
            assert all(H[k]==F[k] for k in range(m) if G[k]==F[k])
            checks+=1
    return checks

# Quotient calculation for each forbidden monochromatic triple T.
# contains the boundaries of all codimension-one faces of the simplex
# on U=[m]\T.  Its image is exactly the cycle group one degree below.
# Delete one coordinate to get an explicit unimodular cycle basis:
# z_j = boundary(U\{j}), j!=anchor.  Coefficients on faces omitting
# anchor and j give a diagonal +/-1 minor.
def quotient_surjectivity(s):
    verts=tuple(range(s)); faces=list(combinations(verts,s-2)); facets=list(combinations(verts,s-1))
    idx={f:i for i,f in enumerate(faces)}
    B=sp.zeros(len(faces),len(facets))
    for j,F in enumerate(facets):
        for k in range(len(F)):
            B[idx[F[:k]+F[k+1:]],j]=(-1)**k
    anchor=s-1
    selected_cols=[i for i,F in enumerate(facets) if anchor in F]
    selected_rows=[i for i,F in enumerate(faces) if anchor not in F]
    minor=B.extract(selected_rows,selected_cols)
    assert minor.rows==minor.cols==s-1
    assert abs(minor.det())==1
    assert B.rank()==s-1
    return {'s':s,'rank':s-1,'minor_det':int(minor.det())}

if __name__=='__main__':
    shelling={f'{m},{q}':shelling_check(m,q) for m in range(1,5) for q in range(m+1)}
    quotient=[quotient_surjectivity(s) for s in range(3,18)]
    result={'shelling_pairs_checked':shelling,'quotient_unimodular_checks':quotient}
    Path('workspace').mkdir(exist_ok=True)
    Path('workspace/agent1_low_exactness_results.json').write_text(json.dumps(result,indent=2))
    Path('workspace/agent1_low_exactness.py').write_text(Path(__file__).read_text())
    Path('workspace/agent1_low_exactness.md').write_text(r'''# Low-degree integral exactness
Let q=m-5. Filtering augmented chains by the number a of vertices in rows 1,2,3 gives D_a in total degree m-6+a, where
D_a = direct sum over admissible colored a-subsets A of H_{q-1}(skel_{q-1} Delta([m] minus cols(A))).
Only 0<=a<=4 occur: the coefficient rank is binom(m-a-1,4-a). The all-empty row4 fiber at a=m is absent because a<=6<m. The spectral sequence has one row and collapses, so this is an integral chain model for reduced homology.

Let E use unrestricted first-three rows, retaining 0<=a<=4. The corresponding whole simplicial complex L has all m-column color words with at most q occurrences of 4 as facets. Lexicographic order with 1<2<3<4 is a shelling: for G<F choose the first differing coordinate j and replace F_j by G_j. The replacement decreases the color and cannot increase the number of 4s. It differs from F in exactly one vertex, is earlier, and contains F intersect G. Therefore L has reduced homology only in degree m-1. Its row4-first spectral sequence has E at row4 size q and an exceptional term at a=m,row4size0. A differential from the exceptional term can only hit a=4. Hence H_a(E)=0 for a<=3.

The quotient Q=E/D is supported in a=3,4, since capacity violations in a<=4 consist of a unique color occurring >=3 times. At a=3 Q splits over monochromatic triples T. Let U=[m] minus T, |U|=s=m-3. The coefficient is the group of cycles in degree s-3 of the (s-3)-skeleton on U, of rank s-1. For each j in U append a vertex of either different color at j. Its Q4 boundary is, up to sign, boundary(U minus {j}). These boundaries span the cycle group integrally: fix an anchor h; the s-1 boundaries indexed by j!=h form a basis because their coefficients on faces U minus {h,j} give a diagonal +/-1 minor. Thus Q4 -> Q3 is onto, H3(Q)=0.

The integral long exact sequence of 0 -> D -> E -> Q -> 0 now gives H_a(D)=0 for a<=2. Equivalently reduced H_i(K_m;Z)=0 for i<=m-4. Combined with the elementary simple-connectivity proof this gives (m-4)-connectivity.

The supplied Python checks every shelling pair for m<=4 and exhibits the exact determinant +/-1 certificate for all s from 3 through 17. The formulas above prove the same certificate for arbitrary s.
''')
    print(json.dumps(result,indent=2))
