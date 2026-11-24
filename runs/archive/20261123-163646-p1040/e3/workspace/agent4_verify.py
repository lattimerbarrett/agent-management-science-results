from agent4_tensor import *
from itertools import product

def compose(a,b): return tuple(substitute(w,a) for w in b)
def power(a,k):
    out=((1,),(2,))
    for _ in range(k): out=compose(out,a)
    return out
S=((2,),(-1,)); T=((1,),(1,2)); R=((-1,),(2,))
Si=((-2,),(1,)); Ti=((1,),(-1,2))
identity=((1,),(2,))
assert power(S,4)==identity
assert compose(compose(compose(R,S),R),S)==identity
assert compose(compose(compose(R,T),R),T)==identity
w=(1,-2)
assert compose(power(S,2),power(compose(Ti,Si),3))==tuple(reduce_word(w+(i,)+inverse_word(w)) for i in (1,2))
for n,dmax in [(2,7),(3,3),(4,2)]:
    for d in range(1,dmax+1):
        M=homogeneous_centralizer_matrix(n,d)
        assert M.rank()==n**d
for u,v,s,t in [((1,),(2,),1,1),(commutator_word((1,),(2,)),(1,),2,1),(commutator_word(commutator_word((1,),(2,)),(1,)),(2,),3,1)]:
    U=homogeneous(magnus(u,s+t),s); V=homogeneous(magnus(v,s+t),t)
    actual=magnus(commutator_word(u,v),s+t)
    assert all(not homogeneous(actual,k) for k in range(1,s+t))
    assert homogeneous(actual,s+t)==bracket(U,V)
print("All exact checks passed: Nielsen relators, tensor centralizers, and Magnus leading commutators.")
