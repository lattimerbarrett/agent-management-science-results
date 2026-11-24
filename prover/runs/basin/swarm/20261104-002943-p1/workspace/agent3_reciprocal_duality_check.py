import sympy as S

def monic_values(nodes,w,s):
    M=S.Matrix([[sum(wi*x**(j+k) for x,wi in zip(nodes,w)) for k in range(s)] for j in range(s)])
    c=M.inv()*S.Matrix([-sum(wi*x**(j+s) for x,wi in zip(nodes,w)) for j in range(s)]) if s else []
    return [x**s+sum(c[j]*x**j for j in range(s)) for x in nodes]

def norm(w):
    return [S.factor(x/sum(w)) for x in w]

def F(nodes,w,s):
    p=monic_values(nodes,w,s)
    return norm([a*b*b for a,b in zip(w,p)])

for n in range(3,10):
    nodes=list(map(S.Integer,range(1,n+1)))
    c=[1/S.prod(x-y for y in nodes if y!=x) for x in nodes]
    w=norm([S.Integer(j*j+1) for j in range(1,n+1)])
    iw=norm([a*a/b for a,b in zip(c,w)])
    for s in range(1,n):
        lhs=F(nodes,w,s)
        rhs=F(nodes,iw,n-s-1)
        assert lhs==rhs
print('Exact reciprocal duality F_s = F_(n-s-1) o I checked, n=3,...,9, all s.')
