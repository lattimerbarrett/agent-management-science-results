"""Checked constructive lower bound, not a complete spectrum proof."""
import json

def dyadic_blocks(lo,hi):
    out=[]
    while lo<hi:
        size=(lo&-lo) if lo else 1<<((hi-lo).bit_length()-1)
        while size>hi-lo:size//=2
        out.append((lo,size));lo+=size
    return out

def witnesses(c=7):
    n=1<<c; ans={}
    for a in range(n+1):
        for b in range(n+1):
            w=n*(a+b)-2*a*b
            zeros=[];ones=[]
            for x0,x1,y0,y1,kind in [(0,a,0,b,zeros),(a,n,b,n,zeros),(0,a,b,n,ones),(a,n,0,b,ones)]:
                for x,sx in dyadic_blocks(x0,x1):
                    for y,sy in dyadic_blocks(y0,y1):
                        if sx*sy>=n:kind.append((x,sx,y,sy))
            z=sum(sx*sy for x,sx,y,sy in zeros)//n
            o=sum(sx*sy for x,sx,y,sy in ones)//n
            for t in range(-o,z+1):ans.setdefault(w+n*t,(a,b,t))
    return ans

def truth_table(a,b,t,c=7):
    import numpy as np
    n=1<<c
    arr=np.array([[int((x<a) != (y<b)) for y in range(n)] for x in range(n)],dtype=np.uint8)
    ranges=[(0,a,0,b),(a,n,b,n)] if t>=0 else [(0,a,b,n),(a,n,0,b)]
    left=abs(t)
    for x0,x1,y0,y1 in ranges:
        for x,sx in dyadic_blocks(x0,x1):
            for y,sy in dyadic_blocks(y0,y1):
                if sx*sy<n:continue
                # partition rectangle into aligned affine c-flats
                ex=sx;ey=sy
                while ex*ey>n:
                    if ex>=ey:ex//=2
                    else:ey//=2
                for xx in range(x,x+sx,ex):
                    for yy in range(y,y+sy,ey):
                        if left:arr[xx:xx+ex,yy:yy+ey]^=1;left-=1
    assert left==0
    return arr.reshape(-1)

def degree(values):
    a=values.copy();m=len(a).bit_length()-1
    for i in range(m):
        for j in range(len(a)):
            if j>>i&1:a[j]^=a[j^(1<<i)]
    return max((j.bit_count() for j,v in enumerate(a) if v),default=-1)

if __name__=='__main__':
    import random
    ws=witnesses()
    missing=[w for w in range(256,8193,2) if w not in ws]
    assert missing==[258,260,262,264,266,268,270,274,276,278,280,282,284,286,290,292,294,298,300,302,306,310,322,326,330,334,358,362,370]
    assert all(w in ws for w in range(372,16013,2))
    rng=random.Random(12)
    checked=[372,374,8190,8192,16012]+rng.sample(list(ws),30)
    for w in checked:
        a,b,t=ws[w]; table=truth_table(a,b,t)
        assert int(table.sum())==w
        assert degree(table)<=7
    print('Covered all even weights 372..16012; tested actual degree <=7 for',len(checked),'witnesses.')
    print('No nonexistence conclusion follows from this lower bound.')
