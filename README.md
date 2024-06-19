# Shared task on Multilingual Grammatical Error Correction (MultiGEC-2025)

The [Computational SLA](https://spraakbanken.gu.se/en/compsla) working group invites you to participate in the shared task on Multilingual Grammatical Error Correction, **MultiGEC**, covering over 10 languages, including Czech, English, Estonian, German, Icelandic, Italian, Latvian, Slovene, Swedish and Ukrainian.

The results will be presented on March 5 (or 2), 2025 (date to be confirmed), at the [NLP4CALL workshop](https://spraakbanken.gu.se/en/research/themes/icall/nlp4call-workshop-series/), colocated with the [NoDaLiDa conference](https://www.nodalida-bhlt2025.eu/conference) to be held in Estonia, Tallinn, on 2--5 March 2025. 

The publication venue for system descriptions will be the proceedings of the NLP4CALL workshop. 

To register for/express interest in the shared task, please fill in [this form](https://forms.gle/nTPfARVqy1XmqT4t6).   

To get important information and updates about the shared task, please join the [MultiGEC-2025 Google Group](https://groups.google.com/g/multigec-2025).

Official system evaluation will be carried out on CodaLab.  

## Task description
In this shared task, your goal is to rewrite learner-written texts to make them grammatically correct or both grammatically correct and idiomatic, that is either adhering to the "minimal correction" principle or applying fluency edits. 

For instance, the text 

> My mother became very sad, no food. But my sister better five months later.

can be corrected minimally as 

> My mother became very sad, __and ate__ no food. But my sister __felt better__ five months later. 

or with fluency edits as

> My mother __was__ very __distressed__ __and refused to eat. Luckily__ my sister __recovered__ five months later. 

For fair evaluation of both approaches to the correction task, we will provide two evaluation metrics, one favoring minimal correction, one suited for fluency-edited output (read more under [Evaluation](#evaluation)). 

We particularly encourage development of multilingual systems that can process all (or several) languages using a single model, but this is not a mandatory requirement to participate in the task. 

## Data

We provide training, development and test data for each of the languages.
The training and development splits will be made available through Github. 
Evaluation will be performed on a separate test set. 

### Data access

To get access, you need to agree to the [Terms of Use](https://forms.gle/VLJ18WbwsxitEBYi7). 

### Data Format
The dataset, divided into folders based on language, consists of essay-aligned files, one containing the original learner essays, and one or more containing reference (corrected/normalized) texts.

Internally, each file follows this simple markdown-based format:

```
### essay_id = 1
Full text of the first essay/reference.

Whitespace, including newline characters, is preserved, but for the sake of readability TWO consecutive newline characters spearate subsequent essays.

### essay_id = 2
Full text of the second essay/reference.

...
```

### External Data
Participants may use additional resources to build their systems __provided that the resource is publicly available for research purposes__. This includes monolingual data, artificial data, pretrained models, syntactic parsers, etc. After the shared task, we encourage participants to share any newly created resources with the community.

### Data Licenses

| Language |  Corpus name | Corpus license | MultiGEC license | 
|:---------|:-------------|:---------------|:------------------|
| Czech    | 
| English  | 
| Estonian |
| German   |
| Icelandic | 
| Italian  | 
| Latvian  | 
| Slovene  |
| Swedish  |
| Ukrainian |

## Evaluation 
During the shared task, evaluation will be based on cross-lingually applicable __automatic metrics__, primarily:

 * [GLEU score](https://github.com/cnap/gec-ranking) (reference-based)
 * [Scribendi score](https://github.com/gotutiyan/scribendi_score) (reference-free)

For comparability with previous results, we will also provide F0.5 scores.

After the shared task, we also plan on carrying out a __human evaluation__ experiment on a subset of the submitted results. 

## Timeline (preliminary)
* June 18, 2024 - first call for participation
* September 20, 2024 - second call for participation 
* October 20, 2024 - third call for participation. Training and validation data released, CodaLab opens for team registrations
* October 30, 2024 - reminder. Validation server released online
* November 13, 2024 - test data released
* November 20, 2024 - system submission deadline (system output)
* November 29, 2024 - results announced
* December 20, 2024 - paper submission deadline with system descriptions
* January 20, 2025 - paper reviews sent to the authors
* February 7, 2025 - camera-ready deadline
* March 5 (or March 2), 2025 - presentations of the systems at the NLP4CALL workshop 


## Publication
We encourage you to submit a paper with your system description to the NLP4CALL workshop special track. 
We follow the same requirements for paper submissions as the NLP4CALL workshop, i.e. we use the same template and apply the same page limit. 
All papers will be reviewed by the organizing committee. 
Upon paper publication, we encourage you to share models, code, fact sheets, extra data, etc. with the community through GitHub or other repositories.

## Organizers

* [Arianna Masciolini](https://harisont.github.io/research.html), University of Gothenburg, Sweden
* [Andrew Caines](https://www.cl.cam.ac.uk/~apc38/), University of Cambridge, UK
* [Orphee De Clecrq](https://research.flw.ugent.be/en/orphee.declercq), Ghent university, Belgium
* [Murathan Kurfali](https://www.su.se/english/profiles/muku8726-1.373629), Stockholm University, Sweden
* [Ricardo Muñoz Sánchez](https://rimusa.github.io/about/), University of Gothenburg, Sweden
* [Elena Volodina](https://spraakbanken.gu.se/en/about/staff/elena), University of Gothenburg, Sweden
* [Robert Östling](https://www.su.se/english/profiles/robe-1.187515), Stockholm University, Sweden

## Data providers
- Czech:
  - Alexandr Rosen, Charles University, Prague 
- English:
  - Andrew Caines, University of Cambridge 
- Estonian: 
  - Mark Fishel, University of Tartu, Estonia
  - Kais Allkivi-Metsoja, Tallinn University, Estonia
  - Kristjan Suluste, Eesti Keele Instituut, Estonia 
- German: 
  - Andrea Horbach, Universität Hildesheim, Germany
  - Katrin Wisniewski, Universität Leipzig
  - Torsten Zesch, FernUniversität in Hagen, Germany
- Icelandic:
  - Isidora Glisič, University of Iceland
- Italian:
  - Jennifer-Carmen Frey, Eurac Research Bolzano, Italy
- Latvian: 
  - Roberts Darģis, University of Latvia
  - Ilze Auzina, University of Latvia
- Slovene:
  - Špela Arhar Holdt, University of Ljubljana, Slovenia
- Swedish:
  - Arianna Masciolini, University of Gothenburg, Sweden
- Ukrainian:
  - Oleksiy Syvokon, Microsoft and Mariana Romanyshyn, Grammarly

## Contact information and forum for discussions

Please join the [MultiGEC-2025 Google group](https://groups.google.com/g/multigec-2025) in order to ask questions, hold discussions and browse for already answered questions.
