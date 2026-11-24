import sympy as sp
N=5
b=sp.symbols('b0:'+str(N), commutative=False)
# The signed-sum estimate is purely an order identity and needs no trace additivity.
for mask in range(1<<N):
 eps=[1 if mask>>i&1 else -1 for i in range(N)]
 total=sum(b)
 signed=sum(eps[i]*b[i] for i in range(N))
 assert sp.expand(total-signed-2*sum(b[i] for i in range(N) if eps[i]==-1))==0
 assert sp.expand(total+signed-2*sum(b[i] for i in range(N) if eps[i]==1))==0
print('Verified the noncommutative signed-sum identities for all 32 sign choices.')
print('If b_i>=0 and sum b_i<=1, then -1<=sum eps_i*b_i<=1.')
a=sp.symbols('a0:'+str(N+1), commutative=False)
print('Positive partial-sum identity:', sp.expand(sum(a[i+1]-a[i] for i in range(N))))
print('Apply the supplied quasitracial exhaustion principle: tau(a_(n+1)-a_n) -> 0.')
print('If every value is eta, their limit is eta, so eta=0; this excludes every allowed eta>0.')