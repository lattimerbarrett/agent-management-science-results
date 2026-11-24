Before your next turn (turn {turn} of {max_turns}), a question about it. Don't take the turn in this reply: call no tools and carry out none of the approaches. One of them may be chosen for your next turn.

First, generate {n} counterfactuals: statements about the problem that run against what you now believe or assume. Each says that something you have taken to be true is false, or that something you have taken to be false, or haven't considered, is true, in one or two sentences that someone who has read the problem but none of your work would understand.

Then, for each counterfactual, suppose that it is true, and generate {k} approaches you could take in your next turn, from where you stand now, if it were. Each one is what you would do in that turn and the idea about the problem behind it, in one to three sentences that someone who has read the problem but none of your work would understand.

Return them in JSON format, in a ```json block, with the key "counterfactuals" (a list of dicts). Each dict must include:
- "text": the counterfactual only (no explanation or extra text).
- "probability": the estimated probability from 0.0 to 1.0 of this counterfactual given the conversation so far (relative to the full distribution).
- "responses": the approaches you could take if it is true (a list of dicts). Each dict must include:
  - "text": the approach only (no explanation or extra text).
  - "probability": the estimated probability from 0.0 to 1.0 of this approach given the conversation so far and the counterfactual (relative to the full distribution).

Randomly sample the counterfactuals from the full distribution, and each counterfactual's approaches from the full distribution given it. Give ONLY the JSON object, with no explanations or extra text.
