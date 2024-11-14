from wtpsplit import SaT
import syntok.segmenter as segmenter
import os

# Some useful constants
SPLITS = ["train", "dev", "test"]

LANGS = [
    "czech", 
    "english", 
    "estonian", 
    "german", 
    "greek", 
    "icelandic", 
    "italian", 
    "latvian", 
    "russian", 
    "slovene", 
    "swedish", 
    "ukrainian"]

CODE2LANG = {
    "cs" : "czech", 
    "en" : "english", 
    "et" : "estonian", 
    "de" : "german", 
    "el" : "greek", 
    "is" : "icelandic", 
    "it" : "italian", 
    "lv" : "latvian", 
    "ru" : "russian", 
    "sl" : "slovene", 
    "sv" : "swedish", 
    "uk" : "ukrainian"    
}

TOP_META = [
    "target_language", 
    "source_corpus", 
    "learner_type", 
    "short_description", 
    "links", 
    "contact", 
    "availability", 
    "license", 
    "sentence_aligned", 
    "original_essays", 
    "reference_essays_1"]


def md_to_dict(md):
    """
    Parse shared task format into a dictionary where keys are essay IDs
    and values are essay texts.

    Arguments:

    md --- a string with the content of a shared task Markdown file.
    """
    essay_dict = {}
    for essay in md.split("### essay_id = ")[1:]:
        (essay_id,text) = essay.split("\n", maxsplit=1)
        essay_dict[essay_id] = text.strip("\n")
    return essay_dict

def dict_to_md(essay_dict):
    """
    Given a dictionary where keys are essay IDs and values are essay texts,
    return a string in shared task format.
    
    Arguments:

    essay_dict --- a dictionary representing the contents of a shared task
    Markdown file (typically obtained via md_to_dict).
    """
    md = ""
    for essay_id, essay_text in essay_dict.items():
        md += "### essay_id = {}\n{}\n\n".format(essay_id, essay_text)
    return md

def split_to_dict(folder, split, newline_replacement="\n"):
    """
    Parse an entire subcorpus split, such as the *-test.md files of 
    swedish/SweLL, to a nested dictionary in the form 

    {"essay_id": {"orig": String, "refs": [String]}}

    Note that the validity of the arguments is not checked.

    Arguments:
    
    folder              --- the path to a subcorpus directory, such as 
                            swedish/swell
    split               --- 'test'|'dev'|'train'
    newline_replacement --- character to use to replace newlines (default:
                            "\n", meaning that they are not replaced)
    """
    corpus_dict = {}

    orig_path = [os.path.join(folder,name) for name in os.listdir(folder) 
                 if name.endswith("orig-{}.md".format(split))][0]
    with open(orig_path) as handle:
        orig_md = handle.read()
    orig_dict = md_to_dict(orig_md)
    for (essay_id, txt) in orig_dict.items():
        corpus_dict[essay_id] = {}
        corpus_dict[essay_id]["orig"] = txt.replace("\n", newline_replacement)

    ref_paths = sorted(
        [os.path.join(folder,name) for name in os.listdir(folder)
         if name.endswith(".md") 
         and "-" in name
         and name.split("-")[3].split(".")[0] == split
         and name.split("-")[2].startswith("ref")])
    for ref_path in ref_paths:
        with open(ref_path) as ref_handle:
            ref_md = ref_handle.read()
        ref_dict = md_to_dict(ref_md)
        for (essay_id, txt) in ref_dict.items():
            txt = txt.replace("\n", newline_replacement)
            if "refs" not in corpus_dict[essay_id]:
                corpus_dict[essay_id]["refs"] = [txt]
            else:
                corpus_dict[essay_id]["refs"].append(txt)
    return corpus_dict

def split_to_parfiles(folder,split,copy_ref1=True):
    """
    Convert an entire subcorpus split, such as the *-test.md files of 
    swedish/SweLL, to a set of parallel files containing one essay/reference
    per line (the format required by https://pypi.org/project/gleu/).
    Output files are named like the input files, but their extension is .tmp
    rather than .md. For instance,
    
    swedish/swell/sv-swell_gold-ref1-test.md

    becomes

    swedish/swell/sv-swell_gold-ref1-train.tmp

    Note that the validity of the arguments is not checked and that \n 
    characters are replaced with \t.

    Arguments:
    
    folder    --- the path to a subcorpus directory, such as swedish/swell
    split     --- 'test'|'dev'|'train'
    copy_ref1 --- whether to copy the first reference to fill gaps in case  
                  different essays have different numbers of references
                  (default: True). If set to False, lines for missing 
                  references are left blank. 
    """
    corpus_dict = split_to_dict(folder,split, newline_replacement="\t") 
    n_refs = max([len(corpus_dict[essay]["refs"]) for essay in corpus_dict])
    orig_name = [item for item in os.listdir(folder)
                 if item.endswith("orig-{}.md".format(split))][0].replace(
                     ".md", ".tmp")
    refi_name = [item for item in os.listdir(folder)
                 if item.endswith("ref1-{}.md".format(split))][0].replace(
                     "ref1", "ref{}").replace(".md", ".tmp")
    
    for tmp_file in [item for item in os.listdir(folder) 
                     if item.endswith("{}.tmp".format(split))]:
        os.remove(os.path.join(folder,tmp_file))

    for essay in corpus_dict:
        with open(os.path.join(folder, orig_name), "a") as handle:
            handle.write(corpus_dict[essay]["orig"])
            handle.write("\n")
        corpus_dict[essay]["orig"]
        for i in range(n_refs):
            with open(os.path.join(
                folder, refi_name.format(i + 1)), "a") as handle:
                try: 
                    handle.write(corpus_dict[essay]["refs"][i])
                except IndexError:
                    if copy_ref1:
                        handle.write(corpus_dict[essay]["refs"][0])
                handle.write("\n")
                
def sentences(essay_text):
    """
    Multilingual sentence splitting, for essays too long to fit in the 
    model's context window.
    
    Arguments:
    
    essay_text --- a string of text
    """
    sat = SaT("sat-3l")
    return sat.split(essay_text)

def syntok_count(path, unit="sentences"):
    """
    Returns sentence counts for given subcorpus.
    The output is a dictionary in the form
    {"orig": {"train": a, "dev": b, "test": c, "total": a + b + c},
     "ref1": {...},
     ...}

    Arguments:

    path --- the path to a subcorpus directory, such as swedish/swell_gold
    unit --- "paragraphs"|"sentences"|"tokens" (default: "sentences")
    """
    counts = {}
    flatten = lambda xss: [x for xs in xss for x in xs]
    for item in [item for item in os.listdir(path) 
         if item.endswith(".md") and item not in ["README.md", "LICENSE.md"]]:
        (_,_,vers,split) = os.path.splitext(item)[0].split("-")
        with open(os.path.join(path,item)) as data_h:
            md = data_h.read()
        if vers not in counts:
            counts[vers] = {}
        for txt in md_to_dict(md).values():
            segmented = segmenter.process(txt)
            pars = [par for par in segmented]
            sents = flatten([[sent for sent in par] for par in pars])
            toks = flatten([[tok for tok in sent] for sent in sents])
            if unit == "paragraphs":
                units = pars
            elif unit == "sentences":
                units = sents
            else: # "tokens"
                units = toks
            if split not in counts[vers]:
                counts[vers][split] = len(units)
            else:
                counts[vers][split] += len(units)
    for vers in counts:
        counts[vers]["total"] = sum(counts[vers].values())
    return counts
