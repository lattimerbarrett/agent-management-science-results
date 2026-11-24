from pathlib import Path
p=Path('workspace/agent2_push_p42_13.py')
s=p.read_text();s=s.replace("Path('workspace/agent2_push_p42_13.py').write_text(Path(__file__).read_text())",'')
p.write_text(s)
print('Removed self-copy from',p,'bytes',p.stat().st_size)
# Execute the exact rational FZ verifier as a directly invoked file would, without subprocess.
p=Path('workspace/fz25_agent2_exact.py')
exec(compile(p.read_text(),str(p),'exec'),{'__name__':'__main__','__file__':str(p.resolve())})
