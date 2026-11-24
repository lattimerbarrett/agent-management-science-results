from sage.all import *
from agent2_validated_taylor import ValidatedTaylor
K=RealBallField(160);S=identity_matrix(K,7)
class Riccati:
 def __init__(self,ref):self.ref=ref
 def field(self,q):return [(self.ref[i]+q[i])**2 for i in range(7)]
 def jac(self,q):return [[2*(self.ref[i]+q[i]) if i==j else K(0) for j in range(7)] for i in range(7)]
vv=ValidatedTaylor(K,S,Riccati);r,rad,M,info=vv.flow([K(1)]*7,K(1)/10,2,degree=16)
for i in range(7):
 out=r[i].add_error(rad[i]);exact=K(10)/9;assert exact in out;assert exact**2 in M[i,i]
print('PASS Riccati 7D intervalTaylor flow+variational; maxradius',max(rad),'rem',info['max_remainder'])
