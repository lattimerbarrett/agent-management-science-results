from pathlib import Path
# Save standalone exact check of the explicit polynomial factor separator.
code=r'''import itertools, math

def mul(a,b):
 c=[0]*(len(a)+len(b)-1)
 for i,x in enumerate(a):
  for j,y in enumerate(b): c[i+j]+=x*y
 return c

def rootpoly(roots):
 p=[1]
 for r in roots: p=mul(p,[-r,1])
 return p

def separator(k):
 assert k>=2
 M=math.factorial(2*k-1);T=2*M*M+2
 A=[[0]*k for _ in range(k)];e=0
 for i in range(k):
  for j in range(i+1,k):
   A[i][j]=T**e;A[j][i]=-T**e;e+=1
 return M,T,A

def verify(k):
 roots=tuple(range(1,2*k-1)); P=rootpoly(roots)
 M,T,A=separator(k);count=0
 for S in itertools.combinations(roots,k-1):
  U=rootpoly(S); V=rootpoly(set(roots)-set(S))
  assert mul(U,V)==P
  assert max(map(abs,U+V))<=M
  h=sum(u*v for u,v in zip(U,V));assert h>0
  coeff=[U[i]*V[j]-U[j]*V[i] for i in range(k) for j in range(i+1,k)]
  assert any(coeff) # distinct complementary root sets imply independent monic factors
  assert max(map(abs,coeff))<=2*M*M<T-1
  s=sum(U[i]*A[i][j]*V[j] for i in range(k) for j in range(k))
  assert s!=0
  assert s==sum(c*T**e for e,c in enumerate(coeff))
  # The two scalar equations have coefficient matrix diag(h,-s)
  # on Re(conj(a)b), Im(conj(a)b), hence determinant -h*s !=0.
  assert -h*s!=0
  count+=1
 return count

if __name__=='__main__':
 for k in (2,3,4,8):
  print('k=',k,'all factor pairs verified:',verify(k))
'''
Path('workspace/agent3_explicit_separator.py').write_text(code)
exec(compile(code,'workspace/agent3_explicit_separator.py','exec'))
