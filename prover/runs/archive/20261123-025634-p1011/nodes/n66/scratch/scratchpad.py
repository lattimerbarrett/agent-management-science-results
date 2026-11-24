# Annular nested-scale boundary: r_k=2^(-2^k), A_k=r_k^k.
# A fixed smooth bump phi supported in 1/2<|x'|<1 gives
# h=sum A_k phi(x'/r_k), smooth and flat at 0.
# Log2 derivative and mass-normalized shape estimates (no underflow).
for n in (10, 18):
 print('ambient n =',n)
 for k in (4,8,12,16):
  log2r=-(2**k)
  derivative_log2=(k-4)*log2r # upper bound for fourth derivative
  shape_log2=(2*k-2)*log2r # square of normalized graph amplitude
  mass_log2=(n-2)*log2r
  print(' k=',k,'log2 ||D^4 h_k|| <=',derivative_log2,
        'log2(shape/mass)=',shape_log2-mass_log2)
print('Every fixed derivative tends to zero as k grows; every Taylor jet at 0 vanishes.')
print('At scale r_k the nonzero normalized shape is nevertheless phi after division by A_k/r_k.')
print('Its isolated-bubble quadratic effect is smaller than mass order eventually.')
