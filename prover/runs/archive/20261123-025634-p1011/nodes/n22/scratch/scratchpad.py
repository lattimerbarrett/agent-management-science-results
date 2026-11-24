import os
p='experiments/e3'
for f in ['agent3_local_pohozaev_bridge.md','agent4_green_mass_reduction.md','agent2_n19_critical_certificate.py','agent2_finite_profiles.txt']:
 print('\nFILE',f,'\n',open(p+'/'+f).read()[:24000])
