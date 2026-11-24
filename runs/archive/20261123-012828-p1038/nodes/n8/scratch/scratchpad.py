import mpmath as mp, time, json, os

def mul(a,b):
 c=[mp.mpf(0)]*(len(a)+len(b)-1)
 for i,x in enumerate(a):
  for j,y in enumerate(b):c[i+j]+=x*y
 return c

def coefficients(m, heights, r=1,R=2,d=1):
 r,R,d=map(mp.mpf,(r,R,d))
 CA=[mp.mpf(1)]; CB=[mp.mpf(1)]
 for k in range(m//2+1):
  if k==0 or 2*k==m:
   z=mp.mpf(1) if k==0 else mp.mpf(-1)
  else:z=mp.exp(2j*mp.pi*k/m)
  D=d+mp.sqrt(d*d+abs(R*z-r)**2)
  c=(R/z-r)/D; b=z*c
  if k==0 or 2*k==m:
   CA=mul(CA,[1,-mp.re(c)]);CB=mul(CB,[mp.re(b),1])
  else:
   CA=mul(CA,[1,-2*mp.re(c),abs(c)**2]);CB=mul(CB,[abs(b)**2,2*mp.re(b),1])
 H=[mp.mpf(1)]
 for j in range(1,m):H.append(H[-1]*mp.cot(mp.pi*j/(2*m)))
 A=mul(H,CA);B=mul(H,CB)
 xy=[]
 for h in heights:
  h=mp.mpf(h)
  x=(h+mp.sqrt(h*h+r*r))/r
  y=(h-d+mp.sqrt((h-d)**2+R*R))/R
  xy.append((x,y))
  A=mul(A,[x,1]);B=mul(B,[y,1])
 return A,B,xy

def test(m, a=1,b=1, param=0, extra_precision=0):
 mp.mp.dps=max(90,int(m*.9)+60)+extra_precision
 if param==0:
  lo=[-mp.mpf(j+1)/a for j in range(a)][::-1]
  hi=[1+mp.mpf(j+1)/b for j in range(b)]
  r,R,d=1,2,1
 elif param==1:
  lo=[-mp.exp(mp.mpf(8*j)/max(1,a-1)-4) for j in range(a)][::-1]
  hi=[1+mp.exp(mp.mpf(8*j)/max(1,b-1)-4) for j in range(b)]
  r,R,d=mp.mpf('0.3'),mp.mpf('5'),1
 else:
  lo=[-mp.mpf(j+1)/a/10 for j in range(a)][::-1]
  hi=[mp.mpf('.001')+mp.mpf(j+1)/b/10 for j in range(b)]
  r,R,d=1,mp.mpf('1.001'),mp.mpf('.001')
 A,B,xy=coefficients(m,lo+hi,r,R,d)
 n=len(A); worst=mp.inf; signcounts=[0,0,0]; minr=None
 for q in range(m):
  cols=list(range(q,n,m)); inds=list(range(q,a+b,m))
  C=len(inds); rows=[]
  for j,i in enumerate(inds):
   row=[mp.mpf(0)]*len(cols)
   x,y=xy[i];u=x**m;v=y**m
   for k,t in enumerate([1,-u-v,u*v]):row[j+k]=t/B[cols[j+k]]
   norm=max(abs(x) for x in row)
   rows.append([x/norm for x in row])
  ar=[A[j]/B[j] for j in cols]
  norm=max(abs(x) for x in ar)
  rows.append([x/norm for x in ar]);rows.append([mp.mpf(1)]*len(cols))
  val=mp.det(mp.matrix(rows))
  signcounts[int(mp.sign(val))+1]+=1
  if abs(val)<worst:worst=abs(val);minr=q
 return {'m':m,'a':a,'b':b,'param':param,'signs':signcounts,'minabs':mp.nstr(worst,12),'residue':minr,'dps':mp.mp.dps}

if __name__=='__main__':
 results=[]
 for m in [257,360,420,511,512,720,840,1001,1023,1024]:
  for a,b,p in [(1,1,0),(m//2,m//2+3,1),(m//2+1,m//2+7,2)]:
   t=time.time();res=test(m,a,b,p);res['secs']=round(time.time()-t,2)
   results.append(res);print(res,flush=True)
 with open('highprec_results.json','w') as f:json.dump(results,f,indent=2)
