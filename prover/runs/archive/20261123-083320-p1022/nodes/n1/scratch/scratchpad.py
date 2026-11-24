# Central characters for the tautological line bundle on P^n.
# The center of SL(n+1) consists of scalar matrices zeta I.
# It fixes every projective point, but acts by zeta on O(-1).
import sympy as s
for n in range(2, 6):
    m = n+1
    print(f'P^{n}: O(1) is SL({m})-linearized; its central character has order {m}. '
          f'O(k) descends to a PGL({m}) linearization iff k == 0 mod {m}.')
