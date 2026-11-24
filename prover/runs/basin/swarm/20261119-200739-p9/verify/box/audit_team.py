from pathlib import Path

def run_piece(name,start=0,end=None):
    lines=Path('workspace/'+name).read_text().splitlines()
    text='\n'.join(lines[start:end])
    print('\n====',name,'====',flush=True)
    exec(compile(text,name,'exec'),{'__name__':'__main__'})

run_piece('agent1_complete_lower_checks.py',0,80)
run_piece('agent3_lower_audit_checks.py',0,79)
run_piece('agent2_comb_characteristic_checks.py',51,96)
run_piece('agent2_comb_full_Ap_checks.py',19,56)
run_piece('agent2_upper_checks.py',0,25)
run_piece('agent4_duality_checks.py',0,50)
