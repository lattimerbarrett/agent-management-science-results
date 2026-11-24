def reduce(w):
 s=[]
 for x in w:
  if s and s[-1]==-x:s.pop()
  else:s.append(x)
 return tuple(s)
def inv(w):return tuple(-x for x in w[::-1])
def mul(*ws):return reduce(sum(ws,()))
def comm(a,b):return mul(a,b,inv(a),inv(b))
def subst(a,w):
 return mul(*(a[x-1] if x>0 else inv(a[-x-1]) for x in w))
def compose(a,b):return tuple(subst(a,w) for w in b)
def mag(n):
 out=[]
 for i in range(n):
  for j in range(n):
   for k in range(j+1,n):
    a=[(s+1,) for s in range(n)];b=a.copy()
    if i==j:
     # x_i -> x_k^-1 x_i x_k, leading [x_i,x_k]
     a[i]=(-(k+1),i+1,k+1);b[i]=(k+1,i+1,-(k+1))
    elif i==k:
     # x_i -> x_j x_i x_j^-1, leading [x_j,x_i]
     a[i]=(j+1,i+1,-(j+1));b[i]=(-(j+1),i+1,j+1)
    else:
     w=comm((j+1,),(k+1,));a[i]=mul(w,(i+1,));b[i]=mul(inv(w),(i+1,))
    out.append(((i,j,k),tuple(a),tuple(b)))
 return out
