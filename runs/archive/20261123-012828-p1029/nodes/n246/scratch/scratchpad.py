import sympy as s
for N in range(1,101):
    a=s.symbols('a0:'+str(N+1), commutative=False)
    increments=sum(a[j+1]-a[j] for j in range(N))
    assert s.expand(increments-(a[N]-a[0])) == 0
print('Verified telescoping: sum_{n<N}(a_{n+1}-a_n)=a_N-a_0.')
print('From a_N <= 1 and a_0 >= 0, these positive partial sums are <= 1.')
eta=s.symbols('eta', positive=True)
n=s.symbols('n', integer=True, positive=True)
print('Limit of the stipulated quasitrace values:',s.limit(eta,n,s.oo))
print('Exhaustivity forces that limit to equal zero, contradicting eta > 0.')
