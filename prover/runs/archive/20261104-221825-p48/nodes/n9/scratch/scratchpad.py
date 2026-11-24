import numpy as np
# At ||v||^2=1, the normal block of the Levi form of ||v||^{-2}
# has eigenvalues +1 and -1. The horizontal block is curvature
# evaluated on v (up to a positive factor).
for name, horizontal in [('positive trace only',[-1.,3.]),('Griffiths positive',[1.,3.])]:
    eig=np.array(horizontal+[1.,-1.])
    print(name, ': eigenvalues',np.sort(eig),'; positive count',np.count_nonzero(eig>0))
