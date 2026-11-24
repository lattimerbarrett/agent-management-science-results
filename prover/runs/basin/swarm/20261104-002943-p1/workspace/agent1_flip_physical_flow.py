import sys;sys.path.insert(0,'workspace');import agent1_flip_augode as m
import numpy as np
from scipy.integrate import solve_ivp
m.x*=3;m.V=m.x[:,None]**np.arange(4);m.p=m.x**4-10*m.x*m.x+11;m.q=m.x**4-10*m.x*m.x+23;m.C=28.
wref=m.w0.copy();T=np.zeros(8);T[:6]=-wref[:6]/m.x[:6]

def flow(t,z):
 w=wref+T*z[0];zz=m.ode(t,np.r_[w,z[1:]])
 return np.r_[T@zz[:8]/(T@T),zz[8:]]
def fuel(z):
 w=wref+T*z[0];return -(m.V.T@(w*m.p**3))@z[1:5]/m.C

def eventF(t,z):return fuel(z)
eventF.terminal=True;eventF.direction=-1
def eventB(t,z):return 1-abs(z[0])-1e-6
eventB.terminal=True;eventB.direction=-1

def initial(E,K1=0,K0=1,K2=1,A1=.1,A2=.1):
 h1,h3=np.linalg.solve(np.array([[-14,-70],[5,36]])*24/11,[K0,K2]);h2=K1/24;h0=E/12-5*h2
 return np.r_[0,[h0,h1,h2,h3],[A1,A2]]
