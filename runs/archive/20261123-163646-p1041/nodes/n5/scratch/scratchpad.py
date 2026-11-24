import z3
n=13;k=5;r=7
s=z3.Solver();s.set(timeout=50000)
a=[z3.Int('a%d'%j) for j in range(32)]
s.add(*[z3.And(x>=0,x<=n) for x in a],sum(a)==n)
for i in range(k):s.add(sum(a[t] for t in range(32) if t>>i&1)==r)
def pow2(x,lim):return sum(z3.If(x==i,1<<i,0) for i in range(lim+1))
w=0;j=0
for mask in range(1,32):
 d=13-sum(a[t] for t in range(32) if t&mask)
 e=7-sum(a[t] for t in range(32) if t&1 and t&mask)
 w+=(-2)**(mask.bit_count()-1)*pow2(d,13)
 j+=(-2)**(mask.bit_count()-1)*pow2(e,7)
s.add(w-j==97)
print(s.check(),flush=True)
if s.check()==z3.sat:print('w,j',s.model().eval(w),s.model().eval(j),[(t,s.model()[a[t]]) for t in range(32)])