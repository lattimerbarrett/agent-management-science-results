from pathlib import Path
code=r'''"""Small exact-arithmetic certificate of all numerical margins for c=10^12.
No huge binomial coefficients or implicit enumeration is performed.
Symbolic lemmas supplying these inequalities are in the proof files.
"""
from fractions import Fraction as F
from math import isqrt
c=10**12;n=c+1;L=320
assert c < 2**40 and n < 2**40
assert L==8*40
assert 3**L >= 2**L*c**4  # (3/2)^L >= c^4
assert c//L > 21
# Four times union bound is safe even without the balanced-size refinement.
delta=F(4*L,2**21)
assert delta<F(1,1000)
# Central(c+3)/central(c+1) for even c.
central_ratio=F(2*(c+3),c//2+2)
assert central_ratio>F(39,10)
odd_star_fraction=F(c+2,2*(c+3))
assert odd_star_fraction>F(49,100)
low_ratio=(1-delta)*central_ratio*odd_star_fraction
assert low_ratio>F(19,10)
# Uniform crude middle and near-r=c lower margins.
mid_ratio=F(c**4,6*(2*c+1))
assert mid_ratio>F(3,2)
# (near ratio >= sqrt(c+2)/(12sqrt2)); compare squares exactly.
assert F(c+2,288)>F(9,4)
# Dedekind container: fingerprint/width <= 81e-6;
# all fingerprints entropy <=40 times their size.
fpratio=F(81,10**6)
container_exponent=F(11,10)+41*fpratio+F(1,10**6)
assert container_exponent<F(111,100)
assert F(40*2,isqrt(n))+F(1,10**9)<fpratio
print('explicit d =',c+3)
print('safe low-r capacity bits / central:',float(low_ratio))
print('safe log2 Dedekind / central:',float(container_exponent))
print('All exact integer/rational finite margins passed.')
'''
Path('workspace/agent2_explicit_margin_certificate.py').write_text(code)
exec(compile(code,'workspace/agent2_explicit_margin_certificate.py','exec'))
