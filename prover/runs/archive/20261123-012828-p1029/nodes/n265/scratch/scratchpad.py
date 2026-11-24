import numpy as np
# Audit the tempting weighted-shift/norm-quotient candidate.
# S_n e_j = sqrt((j+1)/n) e_(j+1), j=0,...,n-2.
# D_n = S_n S_n* - S_n* S_n.
print('n, norm(D_positive), norm(D_negative), normalized_trace(D_positive)')
for n in (4, 16, 64, 256):
    eig = np.r_[-np.ones(n-1)/n, (n-1)/n]
    pos=np.maximum(eig,0)
    neg=np.maximum(-eig,0)
    print(n, pos.max(), neg.max(), pos.sum()/n)
print('\nIn the norm-product quotient D is positive and nonzero,')
print('but the ultralimit normalized trace vanishes on D.')
print('Therefore this candidate fails faithfulness; quotienting by the')
print('quasitrace-null ideal removes D rather than repairing the example.')
