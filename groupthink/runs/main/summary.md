| arm | problems | avg % of agents right | avg % on a wrong answer | agents right | no answer | on the leading wrong answer | different answers held | a vote is right | problems solved | collapsed |
|---|---|---|---|---|---|---|---|---|---|---|
| desk | 25 | 37.5% | 51.0% | 75 of 200 | 23 | 55 | 3.2 → 3.0 | 50% (32-68) | 15 of 25 | 0 |
| look_at_others | 25 | 40.0% | 57.0% | 80 of 200 | 6 | 78 | 2.8 → 2.5 | 50% (32-70) | 14 of 25 | 5 |
| always_look_at_others | 25 | 50.0% | 50.0% | 100 of 200 | 0 | 83 | 2.5 → 1.8 | 58% (40-76) | 15 of 25 | 6 |

| arm | first answers right | first answers wrong | ended on another answer | wrong → right | right → wrong | changes of answer | of those that could, onto a leading answer |
|---|---|---|---|---|---|---|---|
| desk | 76 | 101 | 21 | 3 | 4 | 62 | 11 of 36 |
| look_at_others | 82 | 112 | 41 | 6 | 8 | 68 | 24 of 38 |
| always_look_at_others | 91 | 109 | 46 | 14 | 5 | 87 | 37 of 50 |

| arm | against | agents | end on another answer | right only here | right only there |
|---|---|---|---|---|---|
| look_at_others | desk | 200 | 86 | 14 | 9 |
| always_look_at_others | desk | 200 | 107 | 38 | 13 |

| arm | files read | of another agent | reader said something (only when asked again) | called a tool of its own in reply | words that reached the other agent at work |
|---|---|---|---|---|---|
| look_at_others | 467 | 467 | 331 (176) | 308 | 237 |
| always_look_at_others | 1497 | 1497 | 1175 (494) | 812 | 906 |

| arm | reader held another answer than the file printed | then ended on the file's (right; without the look too) | reader held no answer yet | then ended on the file's (right) | the other held another answer than the reader's | then ended on the reader's (right; without the look too) |
|---|---|---|---|---|---|---|
| look_at_others | 57 | 18 (4; 6) | 72 | 40 (20) | 52 | 17 (7; 7) |
| always_look_at_others | 181 | 53 (12; 12) | 172 | 106 (59) | 226 | 69 (18; 28) |

| step | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| desk: right after it | 2 | 5 | 8 | 12 | 15 | 20 | 28 | 31 | 39 | 45 | 52 | 55 | 60 | 62 | 63 | 62 | 66 | 72 | 73 | 75 |
| desk: agents who took it | 200 | 200 | 200 | 198 | 194 | 187 | 177 | 163 | 152 | 137 | 123 | 109 | 100 | 94 | 79 | 73 | 68 | 62 | 52 | 45 |
| look_at_others: right after it | 2 | 5 | 7 | 12 | 19 | 32 | 43 | 48 | 58 | 65 | 67 | 69 | 69 | 73 | 74 | 75 | 76 | 78 | 79 | 80 |
| look_at_others: agents who took it | 200 | 200 | 200 | 198 | 194 | 187 | 178 | 156 | 140 | 123 | 108 | 92 | 78 | 67 | 60 | 48 | 41 | 33 | 26 | 22 |
| always_look_at_others: right after it | 2 | 5 | 7 | 28 | 44 | 57 | 74 | 75 | 80 | 90 | 93 | 94 | 94 | 95 | 95 | 95 | 97 | 99 | 100 | 100 |
| always_look_at_others: agents who took it | 200 | 200 | 200 | 200 | 195 | 180 | 161 | 137 | 113 | 85 | 69 | 53 | 40 | 22 | 16 | 13 | 10 | 10 | 7 | 4 |

| arm | agents | right | problems solved | held an answer | submitted (wrong) | steps used (median) | files written | edits (near, failed) | Python runs | of those, stopped with an error | replies cut off | replies with no call |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| desk | 200 | 75 | 15 | 177 | 168 (96) | 12.5 | 2326 | 16 (0, 0) | 2271 | 675 | 91 | 1 |
| look_at_others | 200 | 80 | 14 | 194 | 186 (107) | 11 | 1985 | 67 (4, 3) | 2014 | 638 | 83 | 8 |
| always_look_at_others | 200 | 100 | 15 | 200 | 198 (100) | 9 | 1585 | 38 (1, 1) | 1588 | 461 | 69 | 9 |

| arm | calls | tokens written | thoughts cut | steps after which no answer was held |
|---|---|---|---|---|
| desk | 2613 | 4,357,300 | 15% | 66% |
| look_at_others | 3130 | 4,592,226 | 15% | 61% |
| always_look_at_others | 4228 | 4,982,091 | 12% | 53% |

avg % of agents right, avg % on a wrong answer: the percent of a problem's agents that end on the known answer, and on any other answer, averaged over problems (the rest end with none): the two numbers an approach is tracked by. agents right, no answer: agents at the end, whether or not they submitted. on the leading wrong answer: agents who end on a problem's most common wrong answer, added up over problems. different answers held: among a problem's agents, their first answers → their last (a mean over problems). a vote is right: a vote over the answers held at the end names the known one, with a 95% interval over problems. collapsed: problems on which at least 85% of the agents end on one wrong answer. A first answer is the first one a run of an agent's file printed. A leading answer is one held by more agents than any other, and by at least two, the step before. A look is one agent reading a file and saying what it makes of it; what the file printed is what Python printed when it last ran; without the look too: the same agent ends on that answer in the arm in which nobody reads anybody. problems solved: some agent ended right. An edit is near when one line of its `old` was miscopied and it was carried out all the same, failed when nothing was changed. thoughts cut: closed at the budget.
