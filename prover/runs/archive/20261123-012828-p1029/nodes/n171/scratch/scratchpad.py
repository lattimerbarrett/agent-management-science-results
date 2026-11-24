from fractions import Fraction
P=Fraction(1)
for r in range(1,101):
    t=Fraction(1,(r+1)**2)
    P*=1-t
    assert P==Fraction(r+2,2*(r+1))
print('Summable interpolation weights t_n=1/(n+2)^2 give product -> 1/2, not 0.')
print('Thus interpolation does not preserve upper bounds without enough total weight.')
print('In constant-gap interpolation, g_n <= 1 gives t_n >= eta > 0, closing this gap.')
