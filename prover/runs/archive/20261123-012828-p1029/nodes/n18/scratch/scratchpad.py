import sympy as s
I=s.eye(2); Z=s.zeros(2)
e=s.diag(1,0)
X=s.Matrix([[1,1],[1,2]])/4
# Graph of the bounded column X restricted to e, and full graph of X.
W1=e.col_join(X*e)
W2=I.col_join(X)
p1=s.simplify(W1*W1.pinv())
p2=s.simplify(W2*(W2.T*W2).inv()*W2.T)
assert p1*p1==p1 and p2*p2==p2
assert p2*p1==p1 and p1*p2==p1
print('Compatible graph columns give nested projections:',p2*p1==p1)
print('No commutation of the domain and column is needed; [X,e] =',X*e-e*X)
# By contrast, graph projections of ordered full-domain operators are not nested.
A=Z; B=s.Matrix([[2,1],[1,2]])/4
GA=I.col_join(A); GB=I.col_join(B)
print('Rank of join of graphs of 0 and positive invertible B:',GA.row_join(GB).rank())
print('Ambient dimension:',4)
print('Thus joining graphs of a_n directly does not construct their order supremum.')
