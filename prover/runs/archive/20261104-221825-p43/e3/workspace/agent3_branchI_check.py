import sympy as s
w,p,z,X,Y,r=s.symbols('w p z X Y r',real=True)
def R(q):
 a,b,c,d=q
 return s.Matrix([[1-2*(c*c+d*d),2*(b*c-a*d),2*(b*d+a*c)],[2*(b*c+a*d),1-2*(b*b+d*d),2*(c*d-a*b)],[2*(b*d-a*c),2*(c*d+a*b),1-2*(b*b+c*c)]])
x=s.Matrix([X,Y,r/2]);y=s.Matrix([-X,-Y,r/2]);v=s.Matrix([0,0,r]);a=R([w,p,0,z])*x;b=R([w,-p,0,z])*y
print('sum constraint',s.simplify(a+b-v))
# sum constraint solves X=pr/(2z), Y free, if z !=0
ax=s.simplify(a.subs(X,p*r/(2*z)))
print('ax',ax)
print('dot',s.expand((x.dot(ax)-r*r/4).subs(X,p*r/(2*z))))
print('cross',s.expand((ax.cross(x)[2]).subs(X,p*r/(2*z))))
# Correct unsolved line constraint: z X+w Y=p r/2.
ax_correct=s.simplify(a.subs(X,(p*r/2-w*Y)/z))
assert s.simplify(ax_correct[2]-r/2)==0
assert s.simplify((a+b-v)[2]-2*p*(2*X*z+2*Y*w-p*r))==0
print('Verified branch-I constraint zX+wY=pr/2 and preserved individual height.')
from pathlib import Path
Path('workspace/agent3_branchI_check.py').write_text(Path('scratchpad.py').read_text())
