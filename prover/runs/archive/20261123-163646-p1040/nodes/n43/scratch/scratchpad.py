from sage.all import *
x=polygen(QQ)
for c in [4,8,16]:
 d=c//4
 K=NumberField(x**(2*d)-2*x**d+2,'pi'); pi=K.gen(); P=K.ideal(pi)
 assert P.is_prime() and P.norm()==2
 assert (1-pi**d)**2==-1
 h=K.hilbert_symbol(1+pi,1+pi**(c-1),P)
 print('c =',c,': critical quadratic Hilbert symbol =',h,flush=True)
 assert h==-1