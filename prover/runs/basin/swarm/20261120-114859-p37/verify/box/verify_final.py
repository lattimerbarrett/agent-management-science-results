from pathlib import Path
# Run exactly the code printed in the final proof, not cached outputs.
text = Path('record/finals.md').read_text()
code = text.split('```python\n',1)[1].split('\n```',1)[0]
exec(compile(code, 'final_proof.py', 'exec'), {'__name__':'__main__'})
