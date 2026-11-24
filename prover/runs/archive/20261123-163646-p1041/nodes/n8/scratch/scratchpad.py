import z3,itertools
s=z3.Solver();s.set(timeout=50000)
d={a:z3.Int('d%d'%a) for a in range(1,16)}
for a in d:s.add(d[a]>=0,d[a]<=8)
for a in [1,2,4,8]:s.add(d[a]==8)
for a in d:
 for b in d:
  if a&b==a:s.add(d[a]>=d[b])
  s.add(d[a]+d[b]<=d[a|b]+(d[a&b] if a&b else 14))
for a,b,c,e in itertools.permutations([1,2,4,8]):
 s.add(d[a|b]+d[a|c]+d[a|e]+d[b|c]+d[b|e]<=d[a]+d[b]+d[c|e]+d[a|b|c]+d[a|b|e])
def pow2(x):return sum(z3.If(x==i,1<<i,0) for i in range(8))
w=z3.Int('w');s.add(w==sum((-2)**(a.bit_count()-1)*pow2(d[a]) for a in d),w>256,w<320)
known=[272,288,296,304,308,312,314,316,318]
for x in known:s.add(w!=x)
print(s.check(),flush=True)
if s.check()==z3.sat:print('w',s.model()[w],{a:s.model()[d[a]] for a in d})