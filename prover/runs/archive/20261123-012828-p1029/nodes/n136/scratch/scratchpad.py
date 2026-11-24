from fractions import Fraction
# Exact coefficient checks for the supplied projection-family construction.
checks=0
for d in range(1,21):
 delta=Fraction(1,d)
 for c in range(1,21):
  C=Fraction(c)
  for j in range(1,11):
   eta=delta/C*Fraction(j,10)
   for k in range(11):
    t=delta+(1-delta)*Fraction(k,10)
    coefficient=eta/t
    assert coefficient>0
    assert coefficient<=1/C
    assert coefficient*t==eta
    checks+=1
print(checks,'exact rational coefficient and increment checks passed.')
print('General proof: t>=delta and eta<=delta/C imply eta/t<=1/C.')
print('Therefore b_n=(eta/tau(p_n))*p_n has tau(b_n)=eta and')
print('sum_(n<N) b_n <= (1/C)sum_(n<N) p_n <=1.')
print('By the supplied verified no-supremum result, this witnesses every eta in (0,delta/C].')
