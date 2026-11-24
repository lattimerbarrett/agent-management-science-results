from fractions import Fraction
# In l-infinity, let phi = (weighted point-evaluation state + a free
# ultrafilter state)/2. For c_n=1_{k>=n}, its ultrafilter value is 1.
for n in range(7):
    weighted_tail=Fraction(1,2)**n
    phi_tail=(1+weighted_tail)/2
    print(f'n={n}: weighted tail={weighted_tail}, phi(c_n)={phi_tail}')
print('Yet inf_n c_n=0 coordinatewise. Positive weights make phi faithful.')
print('Thus faithfulness alone cannot prove order continuity at a given infimum.')
print('For the supplied sequence with supremum s: c_n=s-a_n decreases to 0,')
print('while c_n >= a_(n+1)-a_n implies tau(c_n) >= eta.')
