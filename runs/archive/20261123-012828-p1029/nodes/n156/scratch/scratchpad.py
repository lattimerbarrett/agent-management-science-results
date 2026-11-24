import sympy as s
# q_k is the normalized matrix extension: q_k(diag(x,0,...,0))=q(x)/k.
A,B,C=s.symbols('q_a q_b q_ab', real=True)
delta=C-A-B
for k in (2,3,8,64):
    one_corner=s.expand(delta/k)
    total=s.expand(k*one_corner)
    assert total==delta
    print(f'k={k}: single-corner defect {one_corner}; total over k corners {total}')
k=s.symbols('k',positive=True,integer=True)
print('Limit of a single-corner defect:', s.limit(delta/k,k,s.oo))
print('A positive increment c placed in one corner has normalized value c/k, not c.')
