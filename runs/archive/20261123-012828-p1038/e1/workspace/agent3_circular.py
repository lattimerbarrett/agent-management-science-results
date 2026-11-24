"""Exact circular-minor checks for the proved moment Laplacian lemma."""
import sympy as s
from itertools import combinations

def check(max_m=10):
    r,R=s.Rational(2),s.Rational(3)
    nodes=[s.Rational(1,10),s.Rational(1,3),s.Rational(1,2)]
    weights=[s.Rational(2),s.Rational(3),s.Rational(5)]
    count=0
    for m in range(2,max_m+1):
        q=[sum(w*(1+a**m)/(1-a**m) for a,w in zip(nodes,weights))]
        q += [sum(w*(a**j+a**(m-j))/(1-a**m) for a,w in zip(nodes,weights)) for j in range(1,m)]
        c=[R*q[(j+1)%m]-r*q[j] for j in range(m)]
        C=s.Matrix(m,m,lambda i,j:c[(i-j)%m])
        S=s.Matrix(m,m,lambda i,j:int((i-j)%m==1))
        L=-(s.eye(m)-S)*C
        for k in range(1,m//2+1):
            for inds in combinations(range(m),2*k):
                I=list(inds[:k]);J=list(reversed(inds[k:]))
                minor=L.extract(I,J).det()
                assert (-1)**k*minor>0
                count+=1
    return count
if __name__=='__main__':print('Exact strict circular minors:',check())
