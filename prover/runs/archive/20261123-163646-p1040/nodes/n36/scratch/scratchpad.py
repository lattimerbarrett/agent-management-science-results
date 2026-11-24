# Check the two independent depth calculations used by the alternative family.
import sympy as S
s,t=S.symbols('s t')
E=lambda a:S.Matrix([[1,a],[0,1]])
F=lambda a:S.Matrix([[1,0],[a,1]])
D=S.diag(t,1)
C=lambda a,b:a*b*a.inv()*b.inv()
B=E(-s)
for c in range(3,9):
 if c>3:B=C(D,B).subs(t,s+1).applyfunc(S.simplify)
 assert S.simplify(B-E(-s**(c-2)))==S.zeros(2)
 inner=C(F(s),B)
 w=C(D,inner).subs(t,s+1).applyfunc(S.simplify)
 vals=[]
 for a in w-S.eye(2):
  num,den=S.fraction(S.cancel(a))
  if num: vals.append(min(k[0] for k,v in S.Poly(num,s).terms()))
 print('c=',c,'matrix word depth=',min(vals),'inner root depths',c,2*c-3)
# Rank-dependent relations actually located in the supplied notes.
p='experiments/e1/agent4_degree2_relations.md'
print('\nLocated genuine spare-index relation:\n',open(p).read().split('## Dummy contraction index')[1])
