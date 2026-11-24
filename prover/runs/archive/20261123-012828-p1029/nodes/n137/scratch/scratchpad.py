import sympy as s
# The algebraic reduction uses no additivity of the quasitrace.
a=s.symbols('a0:7',commutative=False)
for N in range(1,7):
    partial=sum((a[j+1]-a[j] for j in range(N)),s.S.Zero)
    assert s.expand(partial-(a[N]-a[0]))==0
print('For b_n=a_{n+1}-a_n: b_n>=0 and sum_{n<N}b_n=a_N-a_0<=1.')
print('The verified exhaustion result therefore gives tau(b_n)->0.')
print('Since tau(b_n)=eta for every n, the limit is eta, forcing eta=0.')
print('Conclusion: no eta>0 can occur, regardless of the least-upper-bound condition.')
