from pathlib import Path
for a in range(1,5):
 p=Path(f'record/transcripts/agent_{a}.md'); lines=p.read_text().splitlines(); print('\n====',p,'lines',len(lines),'====\n');
 for i,s in enumerate(lines[-60:],len(lines)-59): print(f'{i}: {s}')
