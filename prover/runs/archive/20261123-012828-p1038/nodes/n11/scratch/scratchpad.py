import mpmath as mp
import sympy as s

def mul(a,b):
 out=[mp.mpf(0)]*(len(a)+len(b)-1)
 for i,x in enumerate(a):
  for j,y in enumerate(b):out[i+j]+=x*y
 return out

def eliminate_ring(v,x,y):
 k=len(x); z=[]
 for j in range(k+2):
  t=v[j]
  if 1<=j<=k:t+=(x[j-1]+y[j-1])*z[j-1]
  if j>=2:t-=x[j-2]*y[j-2]*z[j-2]
  z.append(t)
 return z

def physical_case(k,style=0):
 mp.mp.dps=4*k+100
 c=mp.sqrt(2)-1 # r=1,R=2,d=1
 a=k//2;b=k-a
 if style==0:heights=[-mp.mpf(i+1)/a for i in reversed(range(a))]+[1+mp.mpf(i+1)/b for i in range(b)]
 else:heights=[-mp.exp(mp.mpf(10*i)/max(1,a-1)-4) for i in reversed(range(a))]+[1+mp.exp(mp.mpf(10*i)/max(1,b-1)-4) for i in range(b)]
 x=[h+mp.sqrt(h*h+1) for h in heights]
 y=[(h-1+mp.sqrt((h-1)**2+4))/2 for h in heights]
 A=[mp.mpf(1),-c];B=[c,mp.mpf(1)]
 for u,v in zip(x,y):A=mul(A,[u,1]);B=mul(B,[v,1])
 al=eliminate_ring(A,x,y);be=eliminate_ring(B,x,y)
 D=al[k]*be[k+1]-al[k+1]*be[k]
 sources=[al[j]*B[j+1]-be[j]*A[j+1] for j in range(k+1)]
 R=mp.mpf(0)
 for j in range(k+1):R=(x[j-1]*y[j-1]*R if j else 0)+sources[j]
 relative=abs((R-D)/D)
 norm=abs(al[k]*be[k+1])+abs(al[k+1]*be[k])
 coupling=max(abs((v-c)*(v+1/c)/v-mp.mpf('.5')*(u-c)*(u+1/c)/u) for u,v in zip(x,y))
 return k,style,mp.sign(D),sum(t<0 for t in sources),mp.nstr(D/norm,8),mp.nstr(relative,3),mp.nstr(coupling,3)

# Symbolically check the elimination recurrence against the full determinant.
for k in [1,2,3]:
 x=s.symbols('x:'+str(k));y=s.symbols('y:'+str(k));c=s.symbols('c');T=s.symbols('T')
 A=s.Poly((1-c*T)*s.prod(T+u for u in x),T)
 B=s.Poly((T+c)*s.prod(T+v for v in y),T)
 av=[A.nth(j) for j in range(k+2)];bv=[B.nth(j) for j in range(k+2)]
 def elim(v):
  out=[]
  for j in range(k+2):
   q=v[j]
   if 1<=j<=k:q+=(x[j-1]+y[j-1])*out[j-1]
   if j>=2:q-=x[j-2]*y[j-2]*out[j-2]
   out.append(q)
  return out
 aa,bb=elim(av),elim(bv)
 rows=[]
 for i in range(k):
  row=[s.S.Zero]*(k+2);row[i:i+3]=[1,-x[i]-y[i],x[i]*y[i]];rows.append(row)
 rows.extend([av,bv]);mat=s.Matrix(rows)
 # Gaussian elimination with pivots identically 1 gives the same 2x2 corner.
 for i in range(k):
  for j in range(i+1,k+2):
   fac=mat[j,i]
   for q in range(i,k+2):mat[j,q]=s.expand(mat[j,q]-fac*mat[i,q])
 ok=all(s.expand(mat[k,j]-aa[j])==0 and s.expand(mat[k+1,j]-bb[j])==0 for j in [k,k+1])
 print('symbolic elimination check k=',k,ok)
print('k style determinant_sign negative_source_terms normalized_D recurrence_error coupling_error')
for k in [2,4,8,16,32,64,128,256]:
 for style in [0,1]:print(*physical_case(k,style),flush=True)
