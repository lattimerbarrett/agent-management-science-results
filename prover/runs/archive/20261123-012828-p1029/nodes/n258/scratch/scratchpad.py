import sympy as s
# This verifies only the algebraic telescoping used to apply the supplied
# exhaustion theorem; it is not a computational proof of that theorem.
for N in range(1,21):
    a=s.symbols(f'a0:{N+1}')
    partial=s.expand(sum(a[j+1]-a[j] for j in range(N)))
    assert partial == a[N]-a[0]
print('Verified: sum_{n<N} (a_{n+1}-a_n) = a_N-a_0.')
print('Order assumptions give 0 <= a_N-a_0 <= 1-a_0 <= 1.')
print('The verified exhaustion theorem therefore gives tau(a_{n+1}-a_n) -> 0.')
print('A constant such sequence equals eta, so eta=0, contrary to eta>0.')
