import sympy as s
I=s.eye(2); Z=s.zeros(2)
a=s.diag(s.Rational(1,3),0)
b=s.Matrix([[2,1],[1,1]])/3
lo=(3-s.sqrt(5))/6
hi=(3+s.sqrt(5))/6
p=s.diag(1,0)
q=s.simplify((b-lo*I)/(hi-lo))
assert s.simplify(q*q-q)==Z
assert (b-a).det()==0 and s.trace(b-a)>0
assert s.simplify((q-p).det())==-s.Rational(1,2)+s.sqrt(5)/10
G0=I.col_join(Z)
Gb=I.col_join(b)
assert G0.row_join(Gb).rank()==4
print('0 <= a <= b <= 1, but spectral cuts at 1/4 are not ordered:')
print('det(q-p) =',s.simplify((q-p).det()),'< 0')
print('The join of the graphs of 0 and b is the entire doubled space, not a graph.')
print('Thus projection joins neither order the spectral cuts nor directly construct an operator supremum.')
print('Infinite-matrix multiplication would require positive infinite sums in M: this cannot be assumed in a proof of monotone completeness.')
