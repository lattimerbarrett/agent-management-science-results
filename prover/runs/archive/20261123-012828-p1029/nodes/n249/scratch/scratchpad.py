import sympy as s
r=s.symbols('r', positive=True)
t=s.sqrt(r*(1-r))
G=s.Matrix([[r,t],[t,1-r]])
print('Graph-projection identity G^2-G:')
print((G*G-G).applyfunc(s.simplify))
x=1/r-1
print('Candidate positive contraction s =',x)
print('Graph of sqrt(s), first diagonal entry:',s.simplify(1/(1+x)))
print('Graph of sqrt(s), second diagonal entry:',s.simplify(x/(1+x)))
print('If 1/2 <= r <= 1, then 0 <= s <= 1.')
print('Order argument:')
print('r=inf_n (1+a_n)^(-1) implies s=r^(-1)-1 >= a_n.')
print('Any upper bound b>=a_n satisfies (1+b)^(-1)<=r, hence b>=s.')
