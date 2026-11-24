import itertools

def rotate(P,k):
 # Posa rotation at nonfinal vertex P[k], keeping final endpoint fixed.
 assert 0<k<len(P)-1
 return P[k::-1]+P[k+1:]

def es(P):return {frozenset((a,b))for a,b in zip(P,P[1:])}

count=0
for n in range(5,20):
 P=list(range(n))
 for i in range(1,n-1):
  for j in range(1,n-1):
   if i==j:continue
   u,w,z=P[0],P[i],P[j]
   P1=rotate(P,j);P2=rotate(P1,P1.index(w))
   assert P2[0]==w and P2[-1]==P[-1] and sorted(P2)==P
   a=P[j+1];b=P[i-1]if j>i else P[i+1]
   assert es(P2)<=es(P)|{frozenset((u,a)),frozenset((z,b))}
   # For fixed u,z,w the inverse sequence is UNIQUE.
   R1=rotate(P2,P2.index(z));R2=rotate(R1,R1.index(u));assert R2==P
   count+=1
print('Two-rotation identities/inverses PASS',count)

# Exact prefix half-density inequality, allowing exceptional monochromatic steps.
count=0
for n in range(1,12):
 for word in itertools.product(range(2),repeat=n):
  for a in range(2):
   c=sum(x==a for x in word);bad=sum(x==y==a for x,y in zip(word,word[1:]))
   assert 2*c<=n+bad+1
   count+=1
print('Prefix half-density inequality PASS',count)

count=0
for n in range(4,20):
 P=list(range(n));w=n
 for j in range(1,n-1):
  u=P[0];z=P[j];a=P[j+1];R=rotate(P,j);Q=[w]+R
  assert Q[0]==w and Q[-1]==P[-1] and sorted(Q)==list(range(n+1))
  assert es(Q)<=es(P)|{frozenset((u,a)),frozenset((w,z))}
  R=Q[1:];back=rotate(R,R.index(u));assert back==P
  count+=1
print('Missing-target insertion/rotation inverses PASS',count)
