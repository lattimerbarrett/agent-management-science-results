from pathlib import Path
for name in ['check_chain_small_atoms_agent4.py','check_d6_tail4_agent4.py','check_d8_endpoints_agent4.py']:
 print('RUN',name,flush=True)
 exec(compile(Path('workspace',name).read_text(),name,'exec'),{'__name__':'__main__'})
print('ALL AGENT4 FINITE CERTIFICATES PASSED')