"""Exact algebra checks used in horizontal-integrability obstructions."""
import sympy as s
from itertools import combinations

def check():
 a,b,c,d=s.symbols('a b c d')
 z=s.Matrix([a,b,c,d])
 determinant=a*d-b*c
 H=s.hessian(determinant,(a,b,c,d))
 assert H.det()!=0 and H.rank()==4
 # Hence the determinant quadric is nondegenerate in dimension4;
 # a totally isotropic vector subspace has dimension at most2.
 u,v,w,z=s.symbols('u v w z')
 M=s.Matrix([[a,b],[c,d]])
 X=s.Matrix([[u,v],[w,z]])
 comm=M*X-X*M
 L=s.Matrix([comm[i,j] for i in range(2) for j in range(2)]).jacobian((u,v,w,z))
 assert all(s.expand(L.extract(I,J).det())==0
            for I in combinations(range(4),3) for J in combinations(range(4),3))
 minors2={s.expand(L.extract(I,J).det())
          for I in combinations(range(4),2) for J in combinations(range(4),2)}
 assert b*b in minors2 or -b*b in minors2
 assert c*c in minors2 or -c*c in minors2
 assert (a-d)**2 in minors2 or s.expand((a-d)**2) in minors2 or -s.expand((a-d)**2) in minors2
 # Thus rankL=2 for every nonscalar M, and centralizer dimension=4-2=2.
 print({'determinant_polar_rank':H.rank(),
        'commutator_max_rank':2,
        'nonscalar_rank_drop_conditions':['b=0','c=0','a=d']})

if __name__=='__main__':check()
