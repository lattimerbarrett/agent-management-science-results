import numpy as np
import pathlib

def chart_map(h,qp):
    q=np.asarray(qp[:2],dtype=complex); p=np.asarray(qp[2:],dtype=complex)
    X=np.array([q[0]/2-p[1],q[1]/2+p[0]])
    Y=np.array([q[0]/2+p[1],q[1]/2-p[0]])
    XX=X@X; YY=Y@Y
    v=X*np.sqrt(1-h*h*XX/4);w=Y*np.sqrt(1-h*h*YY/4)
    xz=1-h*h*XX/2;yz=-1+h*h*YY/2
    S=v+w;Z=(YY-XX)/2;c=np.sqrt(1+h*h)
    R=S@S+h*h*Z*Z;D=h*h+c*c*R
    J=lambda u:np.array([u[1],-u[0]])
    U=(h*h*v+c*c*R*w+2*c*(J(S)*xz-h*h*Z*J(v)))/D
    V=(h*h*w+c*c*R*v+2*c*(J(S)*yz-h*h*Z*J(w)))/D
    uz=((h*h-c*c*R)*xz+2*c*h*h*(S[0]*v[1]-S[1]*v[0])+c*c*h*h*R*Z)/D
    vz=((h*h-c*c*R)*yz+2*c*h*h*(S[0]*w[1]-S[1]*w[0])+c*c*h*h*R*Z)/D
    ca=(h*h-1)/(h*h+1);sah=2/(1+h*h)
    Xout=np.array([U[0],ca*U[1]-sah*uz]);xzout=h*h*sah*U[1]+ca*uz
    Yout=np.array([ca*V[0]+sah*vz,V[1]]);yzout=-h*h*sah*V[0]+ca*vz
    Xout/=np.sqrt((1+xzout)/2);Yout/=np.sqrt((1-yzout)/2)
    return np.array([Xout[0]+Yout[0],Xout[1]+Yout[1],(Xout[1]-Yout[1])/2,(Yout[0]-Xout[0])/2])

def limiting_map(qp):
 q1,q2,p1,p2=qp;r=q1*q1+q2*q2
 return np.array([2*p2+4*q2/r+2,2*p1+4*q1/r+2,1-q2/2,1-q1/2])

rng=np.random.default_rng(3102)
for i in range(100):
 qp=rng.normal(size=4)
 if np.linalg.norm(qp[:2])<.1:continue
 assert np.max(abs(chart_map(0,qp)-limiting_map(qp)))<1e-11
 assert np.max(abs(chart_map(1e-6,qp)-limiting_map(qp)))<1e-6
print('PASS: 100 reproducible direct evaluations of exact analytic chart and h=0 limit.')

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
