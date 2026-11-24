from pathlib import Path
# Execute the team's unchanged final script; it writes no files.
exec(compile(Path('agents/agent_1/scratchpad.py').read_text(), 'team_scratchpad.py', 'exec'))
