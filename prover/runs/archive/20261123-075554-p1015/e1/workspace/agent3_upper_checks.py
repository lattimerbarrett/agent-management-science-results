from itertools import product
from pathlib import Path

def run_checks():
    counts = {}
    # Sigma_2 normal form: x in A iff exists u, every v R(x,u,v).
    # The oracle H is the complement of halting indices h(x,u), where
    # h(x,u) searches v for a failure of R. Projection is an enum operator.
    n = 2
    cases = 0
    for bits in product((False, True), repeat=n**3):
        R = dict(zip(product(range(n), repeat=3), bits))
        halted = {(x,u) for x,u in product(range(n), repeat=2)
                  if any(not R[x,u,v] for v in range(n))}
        H = set(product(range(n), repeat=2)) - halted
        projected = {x for x,u in H}
        A = {x for x in range(n)
             if any(all(R[x,u,v] for v in range(n)) for u in range(n))}
        assert projected == A
        cases += 1
    counts['normal_form_predicates'] = cases

    # Oracle-independent operators give ordinary halting <=m K_A, uniformly
    # in A. Rows indexed i have axiom (i,empty) exactly when i halts.
    cases = 0
    U = set(range(3))
    subsets = [set(i for i in U if mask >> i & 1) for mask in range(8)]
    for A in subsets:
        for K in subsets:
            rows = {i: ([(i,frozenset())] if i in K else []) for i in U}
            diag = {i for i in U
                    if any(x == i and F <= A for x,F in rows[i])}
            assert diag == K
            assert U-diag == U-K
            cases += 1
    counts['constant_operator_embeddings'] = cases

    # K_A <=e A: flatten a family of enumeration-operator rows onto its
    # diagonal. Check every 2-element-oracle family (256 choices per row).
    V = set(range(2))
    finite = [frozenset(i for i in V if mask >> i & 1) for mask in range(4)]
    axioms = [(x,F) for x in V for F in finite]
    rows_available = [[a for k,a in enumerate(axioms) if mask >> k & 1]
                      for mask in range(256)]
    cases = 0
    for row0 in rows_available:
        for row1 in rows_available:
            rows = [row0,row1]
            flattened = [(i,F) for i in V for x,F in rows[i] if x == i]
            for A in finite:
                diagonal = {i for i in V if any(x == i and F <= A
                                               for x,F in rows[i])}
                reduced = {i for i,F in flattened if F <= A}
                assert diagonal == reduced
                cases += 1
    counts['diagonal_flattening'] = cases

    # If complement(S) <=e S via operator Phi, T=S join complement(S)
    # is equivalent to S. Its complement enumerates T by swapping tags.
    cases = 0
    for S in finite:
        for row in rows_available:
            image = {x for x,F in row if F <= S}
            if image != V-set(S):
                continue
            T = {(0,x) for x in S} | {(1,x) for x in image}
            ambient = set(product(range(2), repeat=2))
            complement_T = ambient-T
            swap_image = {(1-b,x) for b,x in complement_T}
            assert swap_image == T
            # Reduction T <=e S uses identity on first tag and Phi on second.
            T_from_S = {(0,x) for x in S} | {(1,x) for x,F in row if F <= S}
            assert T_from_S == T
            cases += 1
    counts['total_to_cototal_witnesses'] = cases
    return counts

if __name__ == '__main__':
    result = run_checks()
    print(result)
    Path('workspace/agent3_upper_checks.py').write_text(Path(__file__).read_text())
