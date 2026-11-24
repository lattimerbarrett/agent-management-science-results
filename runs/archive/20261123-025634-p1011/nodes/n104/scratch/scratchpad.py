from fractions import Fraction
print('e3 degree-eight patches: eps=2^(-k^4), mu=2^(-k^2), delta=mu*eps^7')
print('For n=19, log2(eps^(n-2)/delta^2)=-(n-16)*k^4+2*k^2, before distance factors')
for k in [3,5,10,20]:
 print('k=',k,'energy ratio log2=',-3*k**4+2*k**2,'source ratio log2=',Fraction(-3*k**4,2)+k**2)
print('Smoothness at a degree-eight cutoff: ||D^m h_k|| <= C_m mu*r_k^(8-m).')
for m in [2,8,20,100]:
 vals=[-k*k-(k+3)*(8-m) for k in [10,50,200]]
 print('m=',m,'log2 upper-bound factors at k=10,50,200:',vals)
print('\ne7 proposed scales: delta=eps^8; background energy/leading energy = eps^(n-18).')
for n in [18,19,20,25]: print('n=',n,'power=',n-18)
