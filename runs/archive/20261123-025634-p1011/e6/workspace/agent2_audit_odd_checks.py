from pathlib import Path
import sympy as S
import sys
sys.path.insert(0,'workspace')
import agent3_odd_gram_checks as C
k,a,q,n=S.symbols('k a q n')
def ir(s):
 return (k+s)*(k+s+1)*(k+a+1)*(k+a+2)/((k+1)*(k+2)*(k+2*a-s+2)*(k+2*a-s+3))
hinv=(2*k+2*a+5)*(k+1)*(k+2)*(k+2*a+1)*(k+2*a+2)/((2*k+2*a+1)*(k+a+1)**2*(k+a+2)**2)
lamratio=((k+q+1)*(k+q+n+1)/((k+q-1)*(k+q+n-1)))**2
dinvratio=(k+q-1)*(k+q+n)/((k+q)*(k+q+n+1))
s,t=S.symbols('s t')
true_ratio=S.factor(ir(s)*ir(t)*hinv*lamratio*dinvratio)
num=[q+1,q+1,q+n+1,q+n,2*a+5,2*a+1,2*a+2,s,s+1,t,t+1]
den=[q-1,q+n-1,q+n-1,q,2*a+1,1,2,2*a-s+2,2*a-s+3,2*a-t+2,2*a-t+3]
# fifth factors are 2k+shift, all other factors k+shift.
code_ratio=S.prod((2*k+x if i==4 else k+x) for i,x in enumerate(num))/S.prod((2*k+x if i==4 else k+x) for i,x in enumerate(den))
assert S.factor(true_ratio-code_ratio)==0
from fractions import Fraction as F
tan2=2*F(1,5)/(1-F(1,5)**2)
tan4=2*tan2/(1-tan2**2)
assert tan2==F(5,12) and tan4==F(120,119)
assert (tan4-F(1,239))/(1+tan4*F(1,239))==1
count=0
for N in range(3,18,2):
 for Q in range((N-1)//2+1):
  if C.check(N,Q) is not None:count+=1
assert count==39
print('Independent audit: exact recurrence, Machin tangent identity, and all39 rational-interval positive blocks PASS.')
Path('workspace/agent2_audit_odd_checks.py').write_text(Path(__file__).read_text())
