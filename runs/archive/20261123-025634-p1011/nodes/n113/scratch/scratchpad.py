import os
p='experiments/e3'
print(open(p+'/agent1_exact_Q_19.txt').read()[:5000])
for f in sorted(os.listdir(p)):
 if any(t in f for t in ['certificate','borderline','verify','summary']):print(f)
print('\nBRIDGE END\n',open(p+'/agent3_local_pohozaev_bridge.md').read()[14000:])
print('\nMASS\n',open(p+'/agent4_green_mass_reduction.md').read()[:26000])
