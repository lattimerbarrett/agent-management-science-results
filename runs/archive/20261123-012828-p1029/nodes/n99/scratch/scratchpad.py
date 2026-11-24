import sympy as s
I=s.eye(2); Z=s.zeros(2)
P0=s.diag(1,0)
P1=s.Matrix([[1,1],[1,1]])/2
Q=[P0/4,P1/4,I/4]
b=[x*x for x in Q]
S=sum(b,Z)
A=I-S
r=s.sqrt(A.det())
D=(A+r*I)/s.sqrt(s.trace(A)+2*r)
assert s.simplify(D*D-A)==Z
W=D.col_join(Q[0]).col_join(Q[1]).col_join(Q[2])
assert s.simplify(W.T*W-I)==Z
q=W*W.T
assert s.simplify(q*q-q)==s.zeros(8)
for n in range(1,4):
 E=s.diag(*([0,0]+[1]*(2*n)+[0]*(6-2*n)))
 expected=sum(b[:n],Z)
 assert s.simplify(W.T*E*W-expected)==Z
 assert s.simplify(W.T*(q*E*q)*W-expected)==Z
print('Noncommuting increments:',b[0]*b[1]!=b[1]*b[0])
print('W*W=I; q=WW* is a projection: exact checks passed.')
print('Each compressed coordinate projection gives the corresponding partial sum: exact checks passed.')
print('The corner q M_8(C) q is identified with M_2(C) by x -> W*xW.')
print('Infinite audit: require a genuine bounded infinite-matrix algebra with e00 corner M,')
print('and order-continuity of compression; neither follows from a merely formal array.')
