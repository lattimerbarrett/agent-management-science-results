from pathlib import Path
terms=['forsythe','counterexample theorem','known counterexample','doi','arxiv']
count=0
for p in Path('experiments').rglob('*'):
 if p.is_file() and p.suffix in ('.md','.txt','.py') and p.stat().st_size<150000:
  text=p.read_text(errors='replace')
  for num,line in enumerate(text.splitlines(),1):
   if any(t in line.lower() for t in terms):
    print(f'{p}:{num}: {line[:500]}');count+=1
print('Matching lines:',count)
