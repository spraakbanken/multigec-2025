# Local evaluation

To evaluate your system output locally, please use:

## Reference-based metrics
- GLEU scores & ERRANT-based Precision, Recall, F0.5: instructions are given [here](gleu_errant/README.md)

Note that both ERRANT and GLEU rely on line-aligned reference-hypothesis files containing one essay per line, which the GLEU & ERRANT scoring program generates automatically.
We therefore suggest to run the scoring program first and use the `.tmp` parallel files for Scribendi scoring described below (the files will be in the `gleu_errant/res` and `gleu_errant/ref` subfolders.
Alternatively, you can use the functions in [utils_transform_submissions_one_essay_per_line.py](gleu_errant/utils_transform_submissions_one_essay_per_line.py) to convert from shared task format to linewise-parallel files.

_Changes made, 2024-11-13:_ we updated the 'gleu_errant' directory so that (a) both GLEU and ERRANT scores can be obtained with one script, (b) texts are tokenized in a consistent way across languages, (c) Icelandic hypotheses are evaluated in an improved way.

## Scribendi score
Code and instructions are given [here](https://github.com/robertostling/scribendi_score); during the __development phase__, the official leaderboard will report scores obtained with the __[Llama-3.1-8B model](https://huggingface.co/meta-llama/Llama-3.1-8B)__. Note that a different model will be used during the __test phase__. The latter will not be announced until the end of the competition.
