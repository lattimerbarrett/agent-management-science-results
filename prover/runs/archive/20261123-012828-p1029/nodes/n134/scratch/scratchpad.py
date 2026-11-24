from fractions import Fraction
# Check the interpolation upper-bound certificate algebraically, with no quasitrace additivity.
# For t_j >= eta, the coefficient of the initial element tends geometrically to zero.
eta=Fraction(1,7)
ts=[Fraction(1,7),Fraction(2,7),Fraction(1,2),Fraction(3,4)]*5
P=Fraction(1)
for r,t in enumerate(ts,1):
 assert eta <= t <= 1
 P*=1-t
 assert 0 <= P <= (1-eta)**r
print('Verified product bound for',len(ts),'exact rational interpolation steps.')
print('Upper-bound preservation: a_(n+r) >= P*a_n + (1-P)*s_j, with P -> 0.')
print('Therefore y >= all a_n implies y >= s_j by norm-closedness of the positive cone.')
print('No quasitrace continuity is used in this upper-bound argument.')
print('To extract uniform tail gaps from a sequence without a supremum, one additionally uses bounded quasitracial completeness and order-closedness.')
print('To deduce no supremum from constant gaps alone instead requires an order-continuity argument, and is not automatic.')