import sympy as s
pi=s.pi
# Homological quantum grading: |M|=4, |A|=|B|=2, |pt|=0.
# q has degree -4 and valuation 4*pi, so c(q*alpha,H)=c(alpha,H)-4*pi.
deg={'M':4,'A':2,'B':2,'pt':0}
for left,right,out,qpower in [('A','B','pt',0),('A','A','M',1),('B','B','M',1),('A','pt','B',1),('B','pt','A',1),('pt','pt','M',2)]:
    assert deg[left]+deg[right]-4==deg[out]-4*qpower
    print(f'{left} * {right} = q^{qpower} {out}: degree {deg[out]-4*qpower}; action shift {-4*qpower*pi}')
print('Recapping by m(A+B generators counted by total degree): index shift -4m; action shift -4*pi*m.')
print('Thus three distinct capped spectral levels alone are not a distinct-geometric-point proof.')
print('The applicable degenerate cup-length theorem gives the needed geometric count: cup-length 2 plus 1 = 3.')
