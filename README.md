# ![MultiGEC](multigec.png)
MultiGEC is a dataset for Multilingual Grammatical Error Correction in 12 European languages (Czech, English, Estonian, German, Greek, Icelandic, Italian, Latvian, Russian, Slovene, Swedish and Ukrainian) compiled by [the CompSLA working group and over 20 external data providers](https://spraakbanken.github.io/multigec-2025/contributors.html) in the context of [MultiGEC-2025](https://spraakbanken.github.io/multigec-2025/shared_task.html), the first text-level GEC shared task.

## Access and citation
The MultiGEC dataset is subject to the terms of use listed [here](https://spraakbanken.github.io/multigec-2025/terms_of_use.html).
To get the data, go to the [download page](https://lt3.ugent.be/resources/multigec-dataset).
Information on how to cite the dataset is available [here](https://spraakbanken.gu.se/en/resources/multigec).

## Overview
The MultiGEC dataset is divided into 17 subcorpora covering different languages, domains and correction styles, summarized below. 
More detailed information about each subcorpus is available with the data as machine-readable metadata, whose format is described [here](https://spraakbanken.github.io/multigec-2025/data_format.html). 
See also the full [dataset statistics](https://spraakbanken.github.io/multigec-2025/stats.html).


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
