from pathlib import Path
p=Path('workspace/agent3_spectral_norm_detector.md')
print(p.read_text())
s=Path('workspace/agent3_spectral_norm_detector_checks.py')
print('\n--- INDEPENDENT RERUN ---')
exec(compile(s.read_text(),str(s),'exec'),{'__name__':'__main__'})
