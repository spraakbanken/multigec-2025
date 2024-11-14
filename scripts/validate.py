import argparse
import os
import yaml
from multigec_2025_utils import *

"""
validate shared task data files by trying to parse them into a dictionary in 
the form { essay_id: full essay text } and comparing the size of the resulting
dictionary with the expected number of essays

usage: python PATH <n>
"""
REPOS = ["multigec-2025-data", "multigec-2025-data-providers", "multigec-2025-participants"]

def validate_file(path, n):
    print("Validating {}...".format(path),end="")
    with open(path) as f:
        md = f.read()
    n_essays = len(md_to_dict(md))
    try:
        assert n_essays == n
    except AssertionError:
        print("ERROR in file {}. Parsed {} essay(s) instead of the expected {}.".format(path, n_essays, n))
        print("""Please check that each essay_id line starts with THREE hashtag signs and that every essay ends with TWO newline characters. The data format specification is available in the README file.""")
        return
    print(" OK")

def validate_metadata(meta, lang, subcorpus):
    # only checks that the top-level keys are there, but there is potentially muuuuuch more that is checkable. Might be worth thinking about it if the dataset is published more "officially"
    for item in TOP_META:
        try:
            assert item in meta
        except AssertionError:
            print("ERROR. Missing {} in the metadata file for the {}/{} subcorpus.".format(item, lang, subcorpus))

def validate_subcorpus(path):
    lang = os.path.split(path)[-2]
    subcorpus = os.path.basename(path)
    try:
        with open(os.path.join(path,"metadata.yaml")) as meta_handle:
            meta = yaml.load(meta_handle, Loader=yaml.SafeLoader)
    except FileNotFoundError:
        print("ERROR. No metadata file for the {}/{} subcorpus.".format(lang,subcorpus))
        return
    except:
        print("ERROR. The metadata file for the {}/{} subcorpus could not be parsed.".format(lang,subcorpus))
        return
    validate_metadata(meta, lang, subcorpus)
    try:
        orig_stats = meta["original_essays"]["n_essays"]
        for split in SPLITS:
            try:
                validate_file(
                    os.path.join(path,[item for item in os.listdir(path) if item.endswith("-orig-{}.md".format(split))][0]), 
                    orig_stats[split])
            except FileNotFoundError:
                print("ERROR. No {} split for the {} subcorpus (original essays). Please check that the file exists and that it matches the naming conventions, available in the README.".format(split,subcorpus))

        n_refs = len(meta) - 10
        for i in range(n_refs):
            refi_stats = meta["reference_essays_{}".format(i + 1)]["n_essays"]
            for split in SPLITS:
                try:
                    if refi_stats[split] > 0:
                        validate_file(
                            os.path.join(path,[item for item in os.listdir(path) if item.endswith("-ref{}-{}.md".format(i + 1, split))][0]), 
                            refi_stats[split])
                except FileNotFoundError:
                    print("ERROR. No {} split for the {} subcorpus (reference file n. {}). Please check that the file exists and that it matches the naming conventions, available in the README.".format(split, subcorpus, i + 1))
    except KeyError:
        print("ERROR. Missing or incorrect information about split size(s). Please check {}/metadata.yaml".format(os.path.basename(path)))
        
def validate_language(path):
    lang = os.path.basename(path)
    subcorpora = [item for item in os.listdir(path) if os.path.isdir(os.path.join(path,item))]
    if not subcorpora:
        print("WARNING. No data for {}.".format(lang))
    for subcorpus in subcorpora:
        validate_subcorpus(os.path.join(path,subcorpus))

def validate_corpus(path):
    for lang in LANGS:
        try:
            validate_language(os.path.join(path,lang))
        except FileNotFoundError: 
            print("ERROR. No directory for {}.".format(lang))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('path', help='path to the file, subcorpus, language or full MultiGEC dataset to be validated', default=".")
    parser.add_argument('-n', help='expected number of sentences; only required if the path points to a single file', type=int, required=False)

    args = parser.parse_args()

    if os.path.isfile(args.path):
        validate_file(args.path, args.n)
    elif os.path.isdir(args.path):
        abs_path = os.path.abspath(os.path.normpath(args.path))
        if os.path.basename(abs_path) in REPOS:
            validate_corpus(abs_path)
        elif os.path.basename(abs_path) in LANGS:
            validate_language(abs_path)
        else: # trust that it should be a subcorpus
            validate_subcorpus(abs_path)
    else:
        print("Invalid path!")
        exit(-1)

    
