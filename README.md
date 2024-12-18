# ![MultiGEC](multigec.png)
MultiGEC is a dataset for Multilingual Grammatical Error Correction in 12 languages (Czech, English, Estonian, German, Greek, Icelandic, Italian, Latvian, Russian, Slovene, Swedish and Ukrainian) that was originally compiled in the context of [MultiGEC-2025](https://spraakbanken.github.io/multigec-2025/shared_task.html), the first text-level GEC shared task.

## Access
At the moment, the data can be accessed by registering to the [MultiGEC-2025 shared task](https://spraakbanken.github.io/multigec-2025/shared_task.html).
A stable download link will be provided soon.

## Dataset overview
The MultiGEC is divided into 17 subcorpora covering different languages, domains and correction styles, detailed below.

| language code | subcorpus       | learners              |   # essays (train) |   # essays (dev) |   # essays (test) |   # essays (total) |   hypothesis sets | minimal   | fluency   | peculiarities                                             |
|-----------:|:----------------|:----------------------|--------:|------:|-------:|--------:|------------------:|:----------|:----------|:----------------------------------------------------------|
| cs         | NatWebInf       | L1 (web)              |    3620 |  1291 |   1256 |    6167 |                 2 | ✓         |           |                                                           |
| cs         | Romani          | L1 (Romani children)  |    3247 |   179 |    173 |    3599 |                 2 | ✓         |           |                                                           |
| cs         | SecLearn        | L2                    |    2057 |   173 |    177 |    2407 |                 2 | ✓         |           |                                                           |
| cs         | NatForm         | L1 (students)         |     227 |    88 |     76 |     391 |                 2 | ✓         |           |                                                           |
| en         | Write & Improve | L2                    |    4040 |   506 |    504 |    5050 |                 1 | ✓         |           | separate download                                         |
| et         | EIC             | L2                    |     206 |    26 |     26 |     258 |                 3 | ✓         | ✓         |                                                           |
| et         | EKIL2           | L2                    |    1202 |   150 |    151 |    1503 |                 2 |           | ✓         |                                                           |
| de         | Merlin          | L2                    |     827 |   103 |    103 |    1033 |                 1 | ✓         |           | pre-tokenized                                             |
| el         | GLCII           | L2                    |    1031 |   129 |    129 |    1289 |                 1 | ✓         |           |                                                           |
| is         | IceEC           | L1 (mixed)            |     140 |    18 |     18 |     176 |                 1 |           | ✓         | pre-tokenized                                             |
| is         | IceL2EC         | L2                    |     155 |    19 |     19 |     193 |                 1 |           | ✓         | pre-tokenized; includes text fragments                    |
| it         | Merlin          | L2                    |     651 |    81 |     81 |     813 |                 1 | ✓         |           |                                                           |
| lv         | LaVA            | L2                    |     813 |   101 |    101 |    1015 |                 1 | ✓         |           |                                                           |
| ru         | RULEC-GEC       | mixed (L2 + heritage) |    2539 |  1969 |   1535 |    6043 |                 3 | ✓         | ✓         | pre-tokenized; includes text fragments; separate download |
| sl         | Solar-Eval      | L1 (students)         |      10 |    50 |     49 |     109 |                 1 | ✓         |           |                                                           |
| sv         | SweLL_gold      | L2                    |     402 |    50 |     50 |     502 |                 1 | ✓         |           |                                                           |
| uk         | UA-GEC          | mixed (crowdsourced)  |    1706 |    87 |     79 |    1872 |                 4 | ✓         | ✓         |                                                           |

## Data format
Each subcorpus contains a train and a development set, each of which consists of 2+ essay-aligned files, one containing original learner essays and one or more containing reference (i.e. corrected/normalized) texts.

### Naming conventions
Data files are named according to the following convention:

```
langcode-corpus-orig|refn-train|dev|test.md
```

where

- `langcode` is the [two-letter ISO 639 code for the language](https://en.wikipedia.org/wiki/List_of_ISO_639_language_codes)
- `corpus` is the name of the subcorpus, lowercased
- `orig` indicates that the file contains original essays, whereas `ref1`, `ref2`, `refn` indicate the `n`-th reference file
- `test`, `dev` and `train` indicate the corresponding dataset splits

> __Example__: `cs-natwebinf-ref2-dev.md` is the second reference file for the development split of the NatWebInf Czech subcorpus.  

### File format
Internally, each file follows this simple Markdown-based format:

```
### essay_id = 1
Full ext of the first essay/reference.

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
availability: open|restricted # "open" if the subcorpus is free to use outside of the shared task, restricted otherwise. This refers to the MultiGEC subcorpus, not to the source corpus
license: 
  name: name of the license
  url: link to the full text of the license
sentence_aligned: false|true # true if sentence alignments are available in the source corpus, false otherwise
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