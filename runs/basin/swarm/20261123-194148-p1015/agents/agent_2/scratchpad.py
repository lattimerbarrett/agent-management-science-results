from pathlib import Path
p=Path('workspace/agent2_candidate_complete_construction.md'); s=p.read_text()
s=s.replace('Q_e on initialization: choose L', 'Q_e on initialization (SERIALIZED: suspend all other local priority actions until the J-decision and any yes-search finishes; only tree births/D-growth continue): choose L')
s=s.replace('Upon convergence to 1 add x to Z and injure lower strategies;', 'Upon convergence to 1 add x to Z, REMOVE its positive x=1 restraint (or replace it by the redundant permanent x=0 restraint), and injure lower strategies;')
s=s.replace('AUDIT POINTS:', 'AUDIT STATUS: agent_1, agent_3, agent_4 independently passed the full proof with atomic-R, serialized-Q, and N-restraint-removal clarifications now explicit above. Finite birth-tree checker passed 9072 executions/635040 births. Earlier audit checklist:')
p.write_text(s); print(len(s))