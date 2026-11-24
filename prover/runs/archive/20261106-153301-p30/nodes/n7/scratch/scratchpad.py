import sympy as sp
s=sp.symbols('s',integer=True,positive=True)
j=2**s-2
target=3*2**(s-1)-3
# Standard reduction: Delta(j,k) <= Delta(j+1,k)-1.
# Sharp known cases above j have j+r=2**s-1, 2**s, 2**s+1.
for r,sharp in [(1,3*2**(s-1)-1),(2,3*2**(s-1)),(3,3*2**(s-1)+2)]:
    reduced=sp.simplify(sharp-r)
    print('Added masses:',r,'sharp dimension:',sharp,'reduced bound:',reduced,'gap from target:',sp.simplify(reduced-target))
print('Lower bound:',sp.simplify(3*j/2))
for ss in range(3,7):
    print('s=',ss,'j=',int(j.subs(s,ss)),'stated exact d=',int(target.subs(s,ss)))