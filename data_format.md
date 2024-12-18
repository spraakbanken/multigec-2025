---
title: Data format
---

Each MultiGEC subcorpus is composed of a train, a development and a test set, each of which consists of 2+ essay-aligned files, one containing original learner essays and one or more containing reference (i.e. corrected/normalized) texts.

## Naming conventions
Data files are named according to the following convention:

```
langcode-corpus-orig|refn-train|dev|test.md
```

where

- `langcode` is the [two-letter ISO 639 code for the language](https://en.wikipedia.org/wiki/List_of_ISO_639_language_codes)
- `corpus` is the name of the subcorpus, lowercased
- `orig` indicates that the file contains original essays, whereas `ref1`, `ref2`, `refn` indicate the `n`-th reference file
- `test`, `dev` and `train` indicate the corresponding dataset splits

__Example__: `cs-natwebinf-ref2-dev.md` is the file containing the second reference set for the development split of the NatWebInf Czech subcorpus.  

## File format
Internally, each file follows this simple Markdown-based format:

```
### essay_id = 1
Full text of the first essay/reference.

Whitespace, including newline characters, is preserved, but for the sake of readability TWO consecutive newline characters spearate subsequent essays.

### essay_id = 2
Full text of the second essay/reference.

...
```

`orig` and `refn` files are aligned at the essay level in the sense that reference corrections with `essay_id = Y` are relative to the essay with `essay_id = Y` in the corresponding `orig` file. 
Note, however, that __not all__ `refn` files contain corrections for __all__ essays in their `orig` counterpart (that is, some subcorpora only have a second reference for some of the essays).

## Metadata
Each subcorpus is assicuated with a README file and YAML file that summarizes basic metadata in a machine-readable format:

```yaml
target_language: two-letter ISO language code of the texts in the corpus, e.g. "sv" for Swedish
source_corpus: name of the source corpus
learner_type: L1|L2|mixed # whether the authors of the essays are first-language speakers, second language learners or both/unknown (e.g if the corpus is crowdsources)
short_description: short description of the corpus
links: # optional
  - link to paper
  - link to data sheet or similar 
  - ...
contact: maintainer@institution.xx # contact information for the main data provider
availability: open|restricted # "open" if the subcorpus is free to use outside of the shared task, restricted otherwise. This refers to the MultiGEC subcorpus, not necessarily to the source corpus
license: 
  name: name of the license
  url: link to the full text of the license
sentence_aligned: false|true # true if the source corpus is sentence-aligned, false otherwise
original_essays: # stats in reference to the *-orig-*.md files
  n_essays: 
    total: a+b+c
    train: a
    dev: b
    test: c
reference_essays_1: # stats in reference to the *-refX-*.md files
  correction_style: minimal|fluency
  n_essays: 
    total: a+b+c
    train: a
    dev: b
    test: c
# reference_essays_2, reference_essays_3...
```