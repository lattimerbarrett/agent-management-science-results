from pathlib import Path
p=Path('experiments/e3')
for f in ['agent3_local_pohozaev_bridge.md','agent4_green_mass_reduction.md','agent4_certificate_notes.txt','agent3_block_notes.txt']:
 t=(p/f).read_text();print('\nFILE',f,'\n',t[:10500])
print('\nPOSSIBLE SUMMARY FILES')
print([x.name for x in p.iterdir() if any(z in x.name.lower() for z in ['final','proof','theorem','summary'])])