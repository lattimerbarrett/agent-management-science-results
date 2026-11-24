import sympy as s
I=s.eye(2)
a=s.diag(s.Rational(1,3),0)
b=s.Matrix([[2,1],[1,1]])/3
lo=(3-s.sqrt(5))/6
hi=(3+s.sqrt(5))/6
p=s.diag(1,0) # spectral projection of a above 1/4
q=s.simplify((b-lo*I)/(hi-lo)) # spectral projection of b above 1/4
print('eigenvalues of b-a:', list((b-a).eigenvals()))
print('eigenvalues of 1-b:', list((I-b).eigenvals()))
print('q is a projection:',s.simplify(q*q-q)==s.zeros(2))
print('det(q-p):',s.simplify((q-p).det()))
print('rank of the combined ranges of p and q:',p.row_join(q).rank())
print('Thus p join q=1, although the increasing sequence a,b,b,... has supremum b.')
print('Naive joins of ordinary spectral cuts do not construct the order supremum.')
