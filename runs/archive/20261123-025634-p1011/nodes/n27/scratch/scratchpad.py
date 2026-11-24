import os
p='experiments/e3'
print('\n'.join(os.listdir(p)))
for f in ['agent3_local_pohozaev_bridge.md','agent4_green_mass_reduction.md']:
 print('\n\n===== '+f+' =====\n')
 t=open(p+'/'+f).read();print(t[:24000])
