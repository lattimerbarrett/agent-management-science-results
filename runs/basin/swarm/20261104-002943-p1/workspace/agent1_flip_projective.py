import sys;sys.path.insert(0,'workspace');import agent1_flip_augode as m
import numpy as np
from scipy.integrate import solve_ivp
S=m.V.T@((m.w0*m.p*m.p)[:,None]*m.V);T=np.zeros(8);T[:6]=-m.w0[:6]/m.x[:6];wref=m.w0.copy()

def projode(t,z):
 tt=z[0];w=wref+T*tt;h=z[1:5];amps=z[5:];dz=m.ode(t,np.r_[w,h,amps]);b=dz[:8];hd=dz[8:12];ad=dz[12:];norm=h@S@h+amps@amps
 rr=(h@S@hd+amps@ad)/norm
 return np.r_[np.dot(T,b)/np.dot(T,T),hd-rr*h,ad-rr*amps]

def event(t,z):return 1/3-abs(z[0])-1e-7
event.terminal=True;event.direction=-1
