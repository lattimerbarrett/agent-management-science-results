import sympy as S
from pathlib import Path
s=S.symbols('s');t=1+s
D=S.diag(t,1);A=S.Matrix([[1,s],[0,1]]);B=S.Matrix([[1,0],[-s,1]])
def simp(M):return M.applyfunc(S.cancel)
def comm(P,Q):return simp(P*Q*P.inv()*Q.inv())
Bk=B
for c in range(3,17):
 k=c-3;b=(-1)**(k+1)*s**(k+1)/t**k
 assert simp(Bk-S.Matrix([[1,0],[b,1]]))==S.zeros(2)
 a=s;q=a*b;d=1-q
 left=S.Matrix([[1,-a*a*b/d],[0,1]])
 tor=S.diag(1/d,d)
 right=S.Matrix([[1,0],[a*b*b/d,1]])
 inner=comm(A,Bk)
 assert simp(inner-left*tor*right)==S.zeros(2)
 W=comm(D,inner)
 orders=[]
 for e in W-S.eye(2):
  num,den=S.fraction(S.cancel(e))
  if num==0:orders.append(999)
  else:
   assert S.expand(den).subs(s,0)!=0
   orders.append(min(m[0] for m,v in S.Poly(num,s).terms() if v))
 assert min(orders)>=c+1
 print('c=',c,'B_k closed form / exact Gauss factorization verified; w order',min(orders))
 Bk=comm(D,Bk)
Path('workspace/agent4_laurent_word_checks.py').write_text(Path('scratchpad.py').read_text())
