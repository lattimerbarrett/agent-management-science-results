from itertools import product
# Affine-image baseline and even model-excess inequality.
assert all(32+2*(32-32//(1<<d))>=88 for d in range(3,6))
Emin=next(E for E in range(0,100,2) if 4*E>=3*32-18)
assert Emin==20 and 80+Emin>86
# Last row/column bound at H86 leaves only the minimum lower-code word.
assert (9*(86-62)+256)//5==94
assert 64<=94<96
I=(64+62-86)//2
assert I==20
origin=[(a,b) for a,b in product(range(6),repeat=2) if a+b<=6 and 2**a+2**b-2==I]
no_origin=[(a,b) for a,b in product(range(6),repeat=2) if a+b<=5 and 2**a+2**b==I]
assert not origin and not no_origin
assert I not in [2**a for a in range(6)]
print('Pure-pair5 weight86: all image/excess/KT bounds and affine-intersection cases checked')
