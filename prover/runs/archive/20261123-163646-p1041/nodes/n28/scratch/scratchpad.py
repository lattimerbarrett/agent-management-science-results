from math import comb
low=[0,128,192,224,240,248,252,254,256,272,288,296,304,308,310,312,314,316,318,320,324,328,332]
for w in [322,326,330,334]:
 qs=[(t,(w-t)//2) for t in low if t<w and t%4==0]
 print(w,qs,'excess mod4',(comb(w,2)-(2**14-1))%4)
# maximal runs in the proposed bounded fringe
runs=[]
for x in low:
 if runs and runs[-1][1]+2==x:runs[-1]=(runs[-1][0],x)
 else:runs.append((x,x))
print('runs',runs,'total incl central and mirrors',2*len(runs)+1)
