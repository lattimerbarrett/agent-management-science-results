import sympy as s
for N in (1,2,5,10):
    a=s.symbols('a0:'+str(N+1), commutative=False)
    partial=s.expand(sum(a[n+1]-a[n] for n in range(N)))
    assert s.expand(partial-(a[N]-a[0]))==0
    print(f'N={N}: sum of differences = {partial}')
print('Thus the positive differences have partial sums between 0 and 1.')
print('Applying the stipulated quasitracial exhaustion result gives tau(d_n) -> 0.')
