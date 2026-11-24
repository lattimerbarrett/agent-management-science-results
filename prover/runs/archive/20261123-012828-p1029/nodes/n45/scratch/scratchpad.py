from pathlib import Path
print(Path('experiments/e1/agent3_qt_ultraproduct_notes.md').read_text())
print('\nFiles:\n');print('\n'.join(p.name for p in Path('experiments/e1').iterdir()))
