import z3,json
c=7;k=4;n=13;s=z3.Solver();a=[z3.Int('a%d'%j) for j in range(16)]
s.add(*[z3.And(x>=0,x<=n) for x in a],sum(a)==n)
for i in range(k):s.add(sum(a[t] for t in range(16) if t>>i&1)==c)
def power(x):return sum(z3.If(x==i,1<<i,0) for i in range(c+1))
expr=0
for mask in range(1,16):expr+=(-2)**(mask.bit_count()-1)*power(sum(a[t] for t in range(16) if t&mask==mask))
s.add(expr==316)
print(s.check());ns=[s.model().eval(x).as_long() for x in a];print(ns)
free=[0]*4;j=0
for mask,num in enumerate(ns):
 for _ in range(num):
  for i in range(4):
   if mask>>i&1:free[i]|=1<<j
  j+=1
S=set()
for fm in free:
 F={0}
 for j in range(n):
  if fm>>j&1:F|={x^(1<<j) for x in list(F)}
 S^=F
assert len(S)==316
json.dump(sorted(S),open('T316_projection_example.json','w'))
print('free masks',free)
