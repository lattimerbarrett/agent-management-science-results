import sympy as sp
# Check the finite telescoping identity used to apply exhaustivity.
for N in range(1,101):
    a=sp.symbols('a0:'+str(N+1), commutative=False)
    assert sp.expand(sum((a[n+1]-a[n] for n in range(N)),sp.S.Zero)-(a[N]-a[0])) == 0
print('Telescoping identity verified for N=1,...,100, without commutativity.')
print('For b_n=a_(n+1)-a_n, positivity gives b_n>=0;')
print('sum_(n<N) b_n=a_N-a_0<=a_N<=1.')
print('The supplied exhaustivity theorem therefore gives tau(b_n)->0.')
print('If tau(b_n)=eta for every n, the same limit is eta, so eta=0.')
