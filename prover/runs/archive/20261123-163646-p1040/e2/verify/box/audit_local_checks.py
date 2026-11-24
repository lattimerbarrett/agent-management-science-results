from pathlib import Path
for path, stop in [('workspace/agent4_column_word_checks.py', "Path('workspace/agent4_column_word_checks.py')"), ('workspace/agent3_odd_hilbert_norm_checks.py', "Path('workspace/agent3_odd_hilbert_norm_checks.py')"), ('workspace/agent2_hilbert_checks.py', 'json.dump('), ('workspace/agent2_odd_hilbert_checks.py', 'from pathlib import Path')]:
    print('\nAUDIT',path, flush=True)
    source=Path(path).read_text().split(stop)[0]
    exec(compile(source,path,'exec'), {'__name__':'__main__','__file__':path})
