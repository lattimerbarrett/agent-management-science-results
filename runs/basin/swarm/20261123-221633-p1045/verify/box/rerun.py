from pathlib import Path
for f in ['final_book_certificate.py','agent3_greedy_certificate.py','agent2_finite_audit.py','agent4_mixed_audit.py','agent4_highmiddle_cert.py','agent3_lower.py','agent3_finitecheck.py']:
    print('\nRUN', f, flush=True)
    exec(compile(Path('/mnt/no-such-path').read_text() if False else Path('workspace',f).read_text(), f,'exec'),{'__name__':'__main__'})
