import numpy as np
r,R,d=1.,2.,1.
heights=np.r_[np.arange(-100.,-90.),2.]
x=(heights+np.hypot(heights,r))/r
y=(heights-d+np.hypot(heights-d,R))/R
c=(R-r)/(d+np.hypot(d,R-r))
A=np.array([1.,-c]);B=np.array([c,1.])
for xx,yy in zip(x,y):A=np.convolve(A,[xx,1]);B=np.convolve(B,[yy,1])
print('constant and linear ratios:',A[:2]/B[:2])
print('minor A0B1-A1B0:',A[0]*B[1]-A[1]*B[0])
C=len(x);Q=np.zeros((C+2,C+2))
for i,(xx,yy) in enumerate(zip(x,y)):Q[i,i:i+3]=[1,-xx-yy,xx*yy]
Q[-2]=A;Q[-1]=B
print('block determinant:',np.linalg.det(Q))
