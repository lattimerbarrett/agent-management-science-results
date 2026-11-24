"""Exact exhaustive Chern-factor checks for P2 ranks<=3 and P3 ranks<=5.
The geometric justification for the tested case labels is in
agent2_lower_proof.txt. Requires SymPy. All systems and roots are exact.
"""
import sympy as S
import importlib.util
from itertools import product
from pathlib import Path

def module(filename,name):
 spec=importlib.util.spec_from_file_location(name,Path(__file__).with_name(filename))
 m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

def check(n,maxrank,filename):
 m=module(filename,'chow'+str(n));counts={};systems=roots=0
 for r in range(2,maxrank+1):
  for parts in m.compositions(r):
   if len(parts)==1:continue
   eq,us=m.equations(parts)
   gb=S.groebner(eq,*reversed(us))
   assert gb.is_zero_dimensional
   sols=S.solve_poly_system(list(gb),*reversed(us))
   assert sols is not None
   # Independently certify solve_poly_system completeness: constrain each
   # coordinate to the finite claimed values by exact ideal membership.
   coordinate_values=[sorted(set(v[j] for v in sols)) for j in range(len(us))]
   for v,values in zip(reversed(us),coordinate_values):
    squarefree=S.prod(v-a for a in values)
    assert any(gb.reduce(S.expand(squarefree**power))[1]==0 for power in range(1,9))
   # Every complex solution is therefore one of these Cartesian tuples.
   independently_found=[]
   for values in product(*coordinate_values):
    ss=dict(zip(reversed(us),values))
    if all(e.subs(ss)==0 for e in gb):independently_found.append(values)
   assert set(independently_found)==set(sols)
   systems+=1
   for values in sols:
    sol=dict(zip(reversed(us),values));roots+=1
    assert all(S.simplify(e.subs(sol))==0 for e in eq)
    A=[sol.get(S.Symbol(f'u{i}_1_0'),0) for i in range(len(parts))]
    assert all(v.is_Integer for v in sol.values())
    if any(sum(A[:i])==0 for i in range(1,len(A))):label='partial descent'
    elif n==3 and (parts[:2]==(1,1) or parts[-2:]==(1,1)):
     label='edge differential rank contradiction'
    elif n==3 and parts[0]>=2 and all(sol.get(S.Symbol(f'u0_2_{j}'),0)==0 for j in range(2)):
     label='peel top lines'
    elif n==3 and parts[-1]>=2 and all(sol.get(S.Symbol(f'u{len(parts)-1}_2_{j}'),0)==0 for j in range(2)):
     label='peel bottom lines'
    elif parts[0]==1 and A[0]==-1:label='Q recognition'
    elif parts[-1]==1 and A[-1]==1:label='dual Q recognition'
    elif n==2:
     assert parts==(1,1,1) and A==[-2,0,2]
     label='symmetric square recognition'
    else:
     assert parts in ((1,2,2),(2,2,1))
     if parts==(1,2,2):
      assert A==[-2,0,2]
      assert sol[S.Symbol('u1_2_0')]==sol[S.Symbol('u1_2_1')]==0
      assert sol[S.Symbol('u2_2_0')]==4 and sol[S.Symbol('u2_2_1')]==-4
     else:
      assert A==[-2,0,2]
      assert sol[S.Symbol('u1_2_0')]==sol[S.Symbol('u1_2_1')]==0
      assert sol[S.Symbol('u0_2_0')]==4 and sol[S.Symbol('u0_2_1')]==-4
     label='quadratic differential contradiction'
    counts[label]=counts.get(label,0)+1
 print('P%d:'%n,systems,'systems;',roots,'solutions;',counts)

def pencil_check():
 a,b,c,d,e,f,u=S.symbols('a b c d e f u')
 A=S.Matrix([[0,1,0],[1,0,0],[0,0,0]])
 B=S.Matrix([[a,b,c],[b,d,e],[c,e,f]])
 det=S.Poly((A+u*B).det(),u)
 assert det.coeff_monomial(u)==-f
 assert det.coeff_monomial(u**2).subs(f,0)==2*c*e
 assert det.coeff_monomial(u**3).subs(f,0)==-a*e**2+2*b*c*e-c**2*d
 # Therefore f=0,ce=0,ae²+c²d=0; c!=0 forces e=d=0,
 # e!=0 forces c=a=0. If c=e=0 the pencil lies in Sym² C².
 assert all(z==0 for z in B.subs({e:0,d:0,f:0})[1:,1:])
 X,Y,Z=S.symbols('X Y Z')
 phi=S.Matrix([X*X,Y*Y,Y*Z,Z*Z])
 jac=phi.jacobian([X,Y,Z])
 from itertools import combinations
 minors=[S.factor(jac.extract(rows,range(3)).det()) for rows in combinations(range(4),3)]
 assert minors==[4*X*Y**2,8*X*Y*Z,4*X*Z**2,0]
 assert all(v.subs({X:1,Y:0,Z:0})==0 for v in minors)
 assert S.gcd_list(minors)==4*X
 print('Singular-pencil identities and line-plus-external-point ramification verified.')
if __name__=='__main__':
 check(2,3,'agent2_p2_chow.py')
 check(3,5,'agent2_p3_chow.py')
 pencil_check()
