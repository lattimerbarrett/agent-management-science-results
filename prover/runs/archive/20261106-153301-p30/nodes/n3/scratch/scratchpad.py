from math import comb
for s in range(3,9):
    j=2**s-2
    n=comb(j,j//2)//2
    v=0
    a=n
    while a%2==0:
        v+=1
        a//=2
    print(f's={s}, j={j}, d={3*j//2}, half-central-binomial parity={n%2}, v2={v}, residue mod 2^(s-1)={n%(2**(s-1))}')
print('Six-measure test: binom(6,3)/2 =',comb(6,3)//2, '; modulo 4 =', (comb(6,3)//2)%4)
