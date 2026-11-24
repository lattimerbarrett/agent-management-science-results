import mpmath as mp
mp.mp.dps=60
c=mp.sqrt(2)-1
x=[mp.sqrt(10001)-100,2+mp.sqrt(5)]
y=[(mp.sqrt(10205)-101)/2,(1+mp.sqrt(5))/2]
def mul(a,b):
 out=[mp.mpf(0)]*(len(a)+len(b)-1)
 for i,u in enumerate(a):
  for j,v in enumerate(b):out[i+j]+=u*v
 return out
A=mul(mul([1,-c],[x[0],1]),[x[1],1]);B=mul(mul([c,1],[y[0],1]),[y[1],1])
V=list(zip(A,B));w=[list(V[0])]
for k in [1,2,3]:
 z=list(V[k])
 if k<=2:
  ss=x[k-1]+y[k-1]
  z=[z[i]+ss*w[-1][i] for i in range(2)]
 if k>=2:
  pp=x[k-2]*y[k-2]
  z=[z[i]-pp*w[-2][i] for i in range(2)]
 w.append(z)
cross=lambda a,b:a[0]*b[1]-a[1]*b[0]
print('Valid configuration: m=1, a=b=1, lambda=-100, h_-=0, h_+=1, mu=2, r=1, R=2')
print('Wronskian source terms:',[mp.nstr(cross(w[j],V[j+1]),30) for j in range(3)])
print('Final determinant:',mp.nstr(cross(w[2],w[3]),30))