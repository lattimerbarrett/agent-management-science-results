from pathlib import Path
p=Path('experiments/e1/agent4_reduction_notes.md')
text=p.read_text()
start=text.index('## 2.')
end=text.index('## 3.')
print(text[start:end])
print(Path('experiments/e1/agent3_completion_audit.md').read_text())
