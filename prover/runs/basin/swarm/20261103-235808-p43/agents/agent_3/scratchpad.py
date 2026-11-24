from pathlib import Path
p=Path('workspace/agent3_chart_formulas.py')
text=p.read_text()
extra='''
# Independent direct geometric evaluation, not the pole-cancelled implementation.
def direct_geometry(h,qp):
 q=np.asarray(qp[:2]);p=np.asarray(qp[2:])
 X=np.array([q[0]/2-p[1],q[1]/2+p[0]])
 Y=np.array([q[0]/2+p[1],q[1]/2-p[0]])
 x=np.r_[h*X*np.sqrt(1-h*h*(X@X)/4),1-h*h*(X@X)/2]
 y=np.r_[h*Y*np.sqrt(1-h*h*(Y@Y)/4),-1+h*h*(Y@Y)/2]
 ss=x+y;r2=ss@ss;C=np.sqrt(1+h*h)/(h*h)
 def bend(x):return ((1-C*C*r2)*x+2*C*np.cross(ss,x)+C*C*r2*ss)/(1+C*C*r2)
 xx=bend(x);yy=bend(y);ca=(h*h-1)/(h*h+1);sa=2*h/(1+h*h)
 A=np.array([[1,0,0],[0,ca,-sa],[0,sa,ca]])
 B=np.array([[ca,0,sa],[0,1,0],[-sa,0,ca]])
 xx=A@xx;yy=B@yy
 X=xx[:2]/(h*np.sqrt((1+xx[2])/2))
 Y=yy[:2]/(h*np.sqrt((1-yy[2])/2))
 return np.array([X[0]+Y[0],X[1]+Y[1],(X[1]-Y[1])/2,(Y[0]-X[0])/2])
for j in range(100):
 qp=rng.normal(size=4)
 if np.linalg.norm(qp[:2])<.1:continue
 assert np.max(abs(direct_geometry(.001,qp)-chart_map(.001,qp)))<1e-9
print('PASS: 100 independent direct Rodrigues/rotation evaluations match cancelled chart formula.')
'''
if 'def direct_geometry' not in text:p.write_text(text+extra)
exec(compile(p.read_text(),str(p),'exec'),{'__name__':'__main__','__file__':str(p)})
