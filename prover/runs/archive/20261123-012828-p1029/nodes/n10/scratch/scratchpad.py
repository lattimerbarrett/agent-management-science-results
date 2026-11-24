import numpy as np
# Finite sections of p_n in B(l2), with p_n the projection onto
# the first n basis vectors.  In the infinite-dimensional algebra,
# p_n increases to 1 but is not operator-norm Cauchy.
N = 32
for n in [1,2,4,8,16]:
    p = np.diag([1.0]*n+[0.0]*(N-n))
    q = np.diag([1.0]*(n+1)+[0.0]*(N-n-1))
    print(n, np.linalg.norm(q-p, ord=2))
print('Logical audit: metric completeness only applies AFTER Cauchyness is proved.')
