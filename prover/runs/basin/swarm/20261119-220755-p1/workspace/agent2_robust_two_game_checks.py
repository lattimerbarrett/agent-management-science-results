import sympy as S, random, math
from z3 import Real,Solver,Q,sat,unsat
A,B=S.symbols('a b');R0=S.Matrix([[-1,0],[2*B,1]]);R1=S.Matrix([[1,2*A],[0,-1]]);M=R1*R0
assert S.expand(M.trace()-(4*A*B-2))==0 and M.det()==1
assert S.simplify(M*M-(4*A*B-2)*M+S.eye(2))==S.zeros(2)
rng=random.Random(882)
for trial in range(100):
 k=S.Rational(rng.randint(1,98),100);theta=math.acos(float(2*k-1));N=math.floor(math.pi/theta)+5
 u,v=Real('u'),Real('v');sl=Solver();sl.add(u>=0,v>=0,u+v==1);previous,current=u,v
 for i in range(N):
  new=Q(int(4*k.p-2*k.q),int(k.q))*current-previous;sl.add(new>=0);previous,current=current,new
 assert sl.check()==unsat,(k,N)
print('PASS exact symbolic reflection recurrence and 100 exact-rational Z3 finite-play certificates')
