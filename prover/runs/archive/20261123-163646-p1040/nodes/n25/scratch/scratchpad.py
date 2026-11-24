from sage.all import *
R=PolynomialRing(QQ,'z'); z=R.gen()
for c in [4,8,16]:
 f=z**(c//2)-2*z**(c//4)+2
 K=NumberField(f,'a'); a=K.gen(); P=K.primes_above(2)[0]
 print(c,K.hilbert_symbol(1+a,1+a**(c-1),P))
# The defect in the question is a KERNEL.  An index-three image need not give one.
M=matrix(ZZ,[[3]])
print('multiplication by 3: kernel rank',M.right_kernel().rank(),'cokernel order',abs(M.det()))
print('degree c kernel: (gamma_c intersection A_(c+1))/gamma_(c+1)')
print('degree 7 cokernel: A_7/(A_8 gamma_7), not degree 6 kernel')
