from math import comb, gcd
j,d=6,9
# X=S^d x S^d; W=(R_A + R_B + R_C)^j.
# a and b flip the orientation of the first/second hyperplane;
# t exchanges the two hyperplanes.
orientation_X={'a':(-1)**(d+1),'b':(-1)**(d+1),'t':(-1)**(d*d)}
orientation_W={'a':((-1)*1*(-1))**j,'b':(1*(-1)*(-1))**j,'t':(-1)**j}
twist={g:orientation_X[g]*orientation_W[g] for g in orientation_X}
relations=[1-v for v in twist.values()]
modulus=gcd(*relations)
print('domain orientation character:',orientation_X)
print('target orientation character:',orientation_W)
print('top-degree local-coefficient twist:',twist)
print('coinvariant relations:',relations)
print('coinvariant group: Z/',modulus,'Z',sep='')
c=comb(j,j//2)//2
print('count =',c,'; mod 4 =',c%4,'; in obstruction coinvariants =',c%modulus)
