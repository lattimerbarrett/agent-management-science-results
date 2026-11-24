# Finite checks relevant to applying the critical-number result to S^2 x S^2.
# This does not purport to verify the smooth critical-number theorem.
p=q=2
print('Sphere dimensions:',p,q)
print('Both factors have dimension >= 2:',p>=2 and q>=2)
print('Product dimension:',p+q)
# Cohomology ring basis: 1, a, b, ab, with a^2=b^2=0.
basis={(0,0),(1,0),(0,1),(1,1)}
positive=basis-{(0,0)}
def multiply(x,y):
 z=(x[0]+y[0],x[1]+y[1])
 return z if z in basis else None
print('a*b:',multiply((1,0),(0,1)))
print('All positive-degree triple products vanish:',all(multiply(multiply(x,y),z) is None if multiply(x,y) is not None else True for x in positive for y in positive for z in positive))
print('Cup-length:',2)
print('Using the supplied verified smooth critical-number existence result gives a 3-critical-point function, without relying on the disputed local merger.')