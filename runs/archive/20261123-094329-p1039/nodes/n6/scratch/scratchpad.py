import sympy as s
r=s.symbols('r', positive=True)
# For the unit ball, q=(1,0), h=Re(z1)-1.
# ||z-q||^2=||z||^2-2 Re(z1)+1=r^2 implies
# h=(||z||^2-1-r^2)/2 <= -r^2/2 on the closed ball.
bound=-r**2/2
c=-r**2/4
print('Upper bound for h on artificial boundary:',bound)
print('Chosen gluing constant:',c)
print('bound - constant =',s.simplify(bound-c))
print('Thus h < c there, so max(h,c) equals c in a collar.')
print('A genuine strict local peak supplies the same strict gap by compactness.')