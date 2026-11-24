from pathlib import Path
from math import comb
# Given the standard <2d low-weight classification at deficit7,
# the only weights <=256 are 0,128,192,224,240,248,252,254,256.
# In full divided-square syndrome, quotient weights are divisible4.
w=258; d=15
low={0,128,192,224,240,248,252,254,256}
ks=sorted(k for k in range(1,w//2+1,2) if w-2*k in low)
assert ks==[1,3,5,9,17,33,65,129]
# Classification puts quotient supports of weights<254 in dimension <=13.
# Full span15 excludes k<32 unless quotient weight is256.
admissible=[k for k in ks if k==1 or 2*k>=64]
assert admissible==[1,33,65,129]
assert all((k-1)%32==0 for k in admissible)
excess=comb(w,2)-((1<<d)-1)
assert excess==386 and excess%32==2
print({'k':ks,'after_span_bound':admissible,'excess':excess,'residue':excess%32})
