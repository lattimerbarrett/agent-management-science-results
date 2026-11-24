from pathlib import Path
for filename in ['agent1_lefschetz_check.py','agent2_hamiltonian_check.py','agent3_quantum_check.py','agent4_singleton_obstruction.py']:
    path=Path('workspace')/filename
    source=path.read_text()
    print('\nRUNNING',path)
    exec(compile(source,str(path),'exec'),{'__name__':'__main__','__file__':str(path)})
    assert path.read_text()==source, 'Unexpected self-modification'
print('\nAll four scripts passed; source contents unchanged.')
