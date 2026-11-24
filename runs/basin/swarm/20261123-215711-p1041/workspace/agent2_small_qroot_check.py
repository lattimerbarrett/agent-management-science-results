# A small, exact test only. This is NOT a proof at c=7.
import z3
n=7; N=1<<n; w=18
v=[z3.Bool('v'+str(i)) for i in range(N)]
s=z3.SolverFor('QF_FD'); s.set(timeout=120000)
s.add(z3.PbEq([(x,1) for x in v],w))
# q'=J forces full affine span. An affine plane exists because C(18,2)>127.
# An affine transformation therefore puts these nine points in S.
for i in [0,3]+[1<<j for j in range(n)]:s.add(v[i])
def xor(a):
    while len(a)>1:
        a=[z3.Xor(a[i],a[i+1]) if i+1<len(a) else a[i] for i in range(0,len(a),2)]
    return a[0]
# I^3 membership: all squarefree moments of degree<3 vanish.
for mask in range(N):
    if mask.bit_count()<3:
        s.add(z3.Not(xor([v[x] for x in range(N) if x&mask==mask])))
# Each nonzero difference occurs an odd number of unordered times.
for a in range(1,N):
    s.add(xor([z3.And(v[x],v[x^a]) for x in range(N) if x<(x^a)]))
result=s.check()
assert result==z3.unsat,result
print('Checked n7,w18,I3,qtop: UNSAT')
