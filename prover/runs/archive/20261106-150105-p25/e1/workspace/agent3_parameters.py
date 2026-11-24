"""Compute exact upper-bound parameters for rational c>1/5."""
from fractions import Fraction

def parameters(c):
    c=Fraction(c)
    assert Fraction(1,5)<c<=1
    m=3
    while (5*m-8)*c<=m-1:m+=1
    d=m+1
    # Sufficient exact rational inequality replacing fractional exponent:
    # 2*(2t+1)^d < 2^floor(c*t/2).
    t=max(1,(8*c.denominator+c.numerator-1)//c.numerator)
    while 2*(2*t+1)**d >= 2**((c*t/2).__floor__()):t*=2
    assert (5*m-8)*c>m-1
    assert c*t>=8
    assert 2*(2*t+1)**d < 2**((c*t/2).__floor__())
    return {'m':m,'VC_bound':d,'target_color_count':t,'target_order':t*2**(t-1)}
if __name__=='__main__':
    for c in [Fraction(1,1),Fraction(1,2),Fraction(1,3),Fraction(1,4),Fraction(21,100),Fraction(201,1000)]:
        p=parameters(c)
        print(str(c),{k:v for k,v in p.items() if k!='target_order'},'target_order_bits',p['target_order'].bit_length())
