from fractions import Fraction
# Test proposed slice projection for a standard smooth compact obstacle.
# rho(z1,z2,w)=|z1|^2+|z2|^2+|w|^4-|w|^2-1.
def rho(z1,z2,w): return abs(z1)**2+abs(z2)**2+abs(w)**4-abs(w)**2-1
p=(0,2,0)
projected=(p[0],0,p[2])
print('rho(p) =',rho(*p),'; p is in the full exterior')
print('rho(projection(p)) =',rho(*projected),'; projection(p) lies inside K')
print('At q=(1,0,0), the w-tangential Levi value of rho is -1.')
print('Thus the two-dimensional slice has a strictly pseudoconvex exterior point,')
print('but coordinate projection is not a retraction of the full exterior onto it.')
print('A slice obstruction cannot simply be transferred by Oka inheritance.')
