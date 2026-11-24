from fractions import Fraction
# Numerical illustration of the uniformity gap: unbounded sums of
# nonnegative row-values do not force any fixed positive lower bound
# on arbitrarily long rows.
for n in [2,4,8,16,32]:
    number=n*n
    value=Fraction(1,n)
    print({'row_length':number, 'individual_value':str(value), 'sum_of_values':str(number*value)})
# This is only a scalar illustration, not a quasitrace construction.
