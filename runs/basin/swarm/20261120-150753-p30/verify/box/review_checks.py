from pathlib import Path
import runpy
import sympy as S

# Execute the final posted code verbatim (it does not write files).
text = Path('record/finals.md').read_text()
code = text.split('```python\n', 1)[1].split('```', 1)[0]
ns = {'__name__': '__main__'}
exec(compile(code, 'final_answer_code', 'exec'), ns)
print('Final posted code rerun without changes: PASS')

# Independently verify that every unshifted real matrix represents the
# intended complex-polynomial bilinear form on a real basis.
for s in (3, 4):
    roots, P, K, A = ns['matrices'](s)
    n = A[0].rows
    m = n//2
    t = P.gen
    basis = [t**a for a in range(m)] + [S.I*t**a for a in range(m)]
    B = []
    for a in A[1:]:
        # All coefficient matrices and the extra Hermitian matrix have
        # total real trace zero, so their shifts can be recovered exactly.
        shift = S.trace(a)/n
        assert shift.is_Integer
        B.append(a - shift*S.eye(n))
    for a in range(n):
        for b in range(n):
            U, V = basis[a], basis[b]
            rem = S.Poly(S.rem(U*V, P.as_expr(), t), t)
            vals = []
            for ell in range(2*m-2):
                c = rem.nth(ell)
                vals.extend([S.re(c), S.im(c)])
            vals.append(S.re(S.I*(S.conjugate(U.subs(t,0))*V.subs(t,1)-S.conjugate(U.subs(t,1))*V.subs(t,0))))
            assert all(Bi[a,b] == v for Bi,v in zip(B, vals))
    print(f'Independent real-basis check of all bilinear forms, s={s}: PASS')
