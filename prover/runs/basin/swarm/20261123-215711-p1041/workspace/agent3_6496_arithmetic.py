from math import ceil,log2
V=list(range(208,269,4))
assert V==[334-2*c for c in range(63,32,-2)]
for v in V:
 i=(v-206)//2
 assert i%2 and 1<=i<=31
 if v>=256:
  j=(556-v)//4
  assert v+128-2*j==3*v//2-150<=252
  assert i>=25
  for k in (224,240):
   inter=(128+k-v)//2
   assert inter>=42 and ceil(log2(inter))>=6
   assert 7+9-6==10 and 7+10-ceil(log2(i))<=12
for v in (224,240):
 assert (v-206)//2>=9
 assert 7+9-ceil(log2((v-206)//2))<=12
print('All (64,96) rank-one/fat-flat arithmetic checked')
