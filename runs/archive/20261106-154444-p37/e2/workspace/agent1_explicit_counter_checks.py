from fractions import Fraction as F
c=10**12
n=c+1
assert n>4096
# Container bounds: w>=2^n/(4sqrt(n)), n>=10^12.
K_over_w=F(160,10**6)+F(1,n)
tails_over_w=F(8,10**18)
D_exponent=F(11,10)+38*K_over_w+tails_over_w
assert 3*n < 40*(2**37) # log_2(e*n/40)<37, using e<3
assert D_exponent < F(111,100)
# Small-r crossing capacity.
assert c//320>=1000
assert 640*F(3,4)**1000 < F(1,100)
central_ratio=4-F(4,c+4)
small=F(49,100)*F(99,100)*central_ratio
assert small>F(19,10)
# Interior-r crossing capacity.
interior=F(3,2)**320/F(12*c+6)
assert interior>F(19,10)
# Large-r crossing capacity, sqrt(c+1)>10^6.
near=F(10**6,12)
large=F(10**6,4)
assert min(near,large)>F(19,10)
print('Explicit d =',c+3)
print('log2 D(c+1) / w <',float(D_exponent),'< 1.11')
print('minimum certified freebits / w >',float(min(small,interior,near,large)),'> 1.9')
print('All checks use exact integer/rational arithmetic.')
from pathlib import Path
Path('workspace/agent1_explicit_counter_checks.py').write_text(Path('scratchpad.py').read_text())
