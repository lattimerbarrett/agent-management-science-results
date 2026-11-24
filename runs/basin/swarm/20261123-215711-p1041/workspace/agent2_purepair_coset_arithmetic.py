from math import floor
TARGETS=(194,198,202,206)
# Nondecomposable-row cases.
assert 64+2*56+2*16==208>max(TARGETS)
assert 16*(1+3+5+5)==224>max(TARGETS)
assert 3*(max(TARGETS)-192)==42<48
# Pairwise disjoint decomposable planes.
assert 2*(max(TARGETS)-192)==28<48
# Excess bound and affine image rank reduction.
Emin=next(e for e in range(0,300,2) if 4*e>=174)
assert Emin==44
assert 192+Emin>206 and 176+Emin>206
for h in TARGETS:
    if h<206: assert h-160<Emin
# Exhaust the integer constraints of the exceptional rank2 row0 argument.
feasible=[]
for m in (1,3):
 for e in range(0,47,2):
  for z in range(17):
   for r in range(e+2*m+1):
    if 4*e-3*r+16*z<=-8: feasible.append((m,e,z,r))
assert feasible
assert all(m==3 and e<=10 and z==0 for m,e,z,r in feasible)
assert 6*(64-13)>206-64
assert 6*(32-13)>206-128
assert 16>13
# Final small-weight bound, and known <2d spectrum as theorem input.
assert floor((9*80+512)/5)==246
kt_below_256=(0,128,192,224,240,248,252,254)
assert tuple(v for v in kt_below_256 if v<=246)==(0,128,192,224,240)
# Dimensions of intersections with two complementary6-spaces.
origin_in=max(2**p+2**q-2 for p in range(7) for q in range(7) if p+q<=9)
assert origin_in==70
# If g(0)=0, its even axis restrictions omit0; a0-dimensional section contributes0.
def even_omit_zero(p):return max(0,2**p-2)
origin_out=max(even_omit_zero(p)+even_omit_zero(q) for p in range(7) for q in range(7) if p+q<=9)
assert origin_out==68
avoid_L=max(2**p+2**q for p in range(7) for q in range(7) if p+q<=8)
assert avoid_L==68
assert min((v+126-h)//2 for v in (224,240) for h in TARGETS)==72>70
# N32 appendix.
assert 32+2*28+2*8==104>82
assert 32+2*28==88>82
emin5=next(e for e in range(0,100,2) if 4*e>=78)
assert emin5==20
assert 64+emin5>82 and 80+emin5>82
assert 64//2>max(74-62,82-62)
assert all(w==62 or w-62<64//2 for w in range(0,83,2))
print('Checked every numerical inequality in pure-pair-six and pure-pair-five proofs.')
