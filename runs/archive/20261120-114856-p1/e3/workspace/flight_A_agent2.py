exec(open('workspace/flight_A_agent2.py').read())
eig,xi=S.symbols('eig xi',real=True)
mp=m+2;var=S.Rational(3,4)-m-m*m;varp=S.Rational(3,4)+mp-mp*mp
da=(m*h-z)/var;dc=(mp*F[1][1]-F[2][1])/varp
dtau=S.factor(-da-dc)
print('DTAU',dtau,flush=True)
print('DTAU endpoint',S.factor(dtau.subs(m,-1-eig)),flush=True)
# Negative-extra logfitness differential on face: logM = -2(deltaQ+deltaH)/H = -4deltaH/H+2P3(xi)dtau/H
# P3(xi)=P4(xi)/(xi-eig)= -2H/(xi-eig)
logM=S.factor(-8*z/H-4*dtau/(xi-eig))
print('logM endpoint',S.factor(logM.subs(m,-1-eig)),flush=True)
from pathlib import Path
Path('workspace/endpoint_ell_agent2.py').write_text(Path(__file__).read_text())
