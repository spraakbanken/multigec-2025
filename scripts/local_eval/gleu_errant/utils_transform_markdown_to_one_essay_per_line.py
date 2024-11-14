import os
from syntok.tokenizer import Tokenizer

def pretokenize(txt):
    tok = Tokenizer()
    return ' '.join([str(token).strip() for token in tok.tokenize(txt)])

def md_to_dict(md):
    """
    Parse shared task format into a dictionary where keys are essay IDs
    and values are essay texts.
    
    Arguments:
    
    md --- a string with the content of a shared task Markdown file.
    """
    essay_dict = {}
    for essay in md.split("### essay_id = ")[1:]:
        (essay_id, text) = essay.split("\n", maxsplit=1)
        text_tokd = pretokenize(text)
        essay_dict[essay_id] = text_tokd.strip("\n")
    return essay_dict

def get_corpus_names(folder):
    """
    Get a list of unique corpus names from the folder by extracting
    the part before -orig in filenames.
    
    Arguments:
    
    folder --- the path to a subcorpus directory containing *-orig- files
    """
    corpus_names = set()
    for filename in os.listdir(folder):
        if "-orig-" in filename:
            corpus_name = filename.split("-orig")[0]
            corpus_names.add(corpus_name)
        #elif "-hypo" in filename:  # i think we're not expecting -hypo files in same directory as -orig files
        #    corpus_name = filename.split("-hypo")[0]
        #    corpus_names.add(corpus_name)
    return list(corpus_names)

def process_corpus_files(orig_folder, sub_folder, corpus_name, split, copy_sub1=False):
    """
    Process each orig file and its corresponding submissions (previously called refs), 
    converting them into .tmp files as required.
    
    Arguments:
    
    orig_folder --- the path to the folder containing already converted orig files
    sub_folder  --- the path to the folder containing submission files to be converted  
    corpus_name --- the unique name of the corpus to process
    split       --- 'test'|'dev'|'train'
    copy_sub1   --- whether to copy the first submission if some submissions are missing (default: True)
    """
    
    orig_files = [f for f in os.listdir(orig_folder) if f.startswith(corpus_name) and f.endswith(f"orig-{split}.md")]
    
    if not orig_files:
        print(f"File not found for {corpus_name}")
        #raise FileNotFoundError(f"No original file found for corpus '{corpus_name}' with split '{split}' in {orig_folder}")
    else:
        orig_file = orig_files[0]
        print(f"Full filename = {orig_file}")
        sub_files = sorted([f for f in os.listdir(sub_folder) if f.startswith(corpus_name) and f.endswith(f"-{split}.md")])  # could be hypo- or baseline-
        
        # If no hypo files exist, skip this corpus
        if not sub_files:
            print(f"Skipping corpus '{corpus_name}' as no submission files were found in {sub_folder}")
            return
        
        corpus_dict = {}
        
        with open(os.path.join(orig_folder, orig_file)) as handle_in:
            orig_md = handle_in.read()
        handle_in.close()
        orig_dict = md_to_dict(orig_md)
        print(f"Number of essays in original file = {len(orig_dict)}")
        
        # make a dictionary of original essays
        for essay_id, txt in orig_dict.items():
            txt = txt.replace("\n", "\t")
            corpus_dict[essay_id] = {"orig": txt, "subs": []}
        
        # make a dictionary of corrected essays from the submissions file
        for sub_file in sub_files:
            team_name = "unknown"
            print(sub_file)
            if "baseline" in sub_file:
                if "fluency" in sub_file:
                    team_name = "baseline_fluency"
                else:
                    team_name = "baseline_minimal"
            with open(os.path.join(sub_folder, sub_file)) as sub_handle:
                sub_md = sub_handle.read()
            sub_handle.close()
            sub_dict = md_to_dict(sub_md)
            print(f"Number of essays in submission file = {len(sub_dict)}")
            for essay_id, txt in sub_dict.items():
                txt = txt.replace("\n", "\t")
                if essay_id in corpus_dict:
                    print(f"Found essay {essay_id} and adding a submission essay for it")
                    corpus_dict[essay_id]["subs"].append(txt)
            
        # check for essays not found in the predictions file and replace with an empty string
        for essay_id in corpus_dict:
            if len(corpus_dict[essay_id]["subs"]) == 0:
                print(f"Did not find a corrected version of essay {essay_id} so inserting an exclamation mark for it")
                corpus_dict[essay_id]["subs"].append("!")
        
        # how many submissions for this corpus by this team
        #n_subs = max(len(corpus_dict[essay_id]["subs"]) for essay_id in corpus_dict)  # this broke for me and i'm not sure why
        n_subs = len(sub_files)
        #print(n_subs)
        
        for i in range(n_subs):
            if "fluency" in sub_file:  # preserve "fluency" in the .tmp filename (for track parsing in the scoring script)
                sub_file_name = os.path.join(sub_folder, f"{corpus_name}-fluency-hypo{i+1}-{split}.tmp").lower()  # the output .tmp filename, lowercased
            else:
                sub_file_name = os.path.join(sub_folder, f"{corpus_name}-hypo{i+1}-{split}.tmp").lower()  # the output .tmp filename, lowercased
            print(f"Writing to {sub_file_name}")
            if os.path.exists(sub_file_name):
                os.remove(sub_file_name)  # remove any existing files to prevent over-accumulation of data
            with open(sub_file_name, "a") as handle_out:
                for essay_id in corpus_dict:
                    try:
                        handle_out.write(corpus_dict[essay_id]["subs"][i] + "\n")
                    except IndexError:  # if not found (tho i think the missing essay thing above prevents this), output an empty line
                        if copy_sub1:
                            handle_out.write(corpus_dict[essay_id]["subs"][0] + "\n")
                        else:
                            handle_out.write("!\n")
            handle_out.close()
        return team_name

def split_to_parfiles_all(orig_folder, sub_folder, split, copy_sub1=False):
    """
    Process all orig files and corresponding submission files in the folders.
    
    Arguments:
    
    orig_folder --- the path to the folder containing already converted orig files
    sub_folder  --- the path to the folder containing baseline submission files to be converted
    split       --- 'test'|'dev'|'train'
    copy_sub1   --- whether to copy the first submission if some submissions are missing (default: True) .. AC: i think this should be false? (makes sense for references but not predictions)
    """
    corpus_names = get_corpus_names(orig_folder)
    team_names = []
    for corpus_name in corpus_names:
        print(f"Processing {corpus_name}")
        team_name = process_corpus_files(orig_folder, sub_folder, corpus_name, split, copy_sub1)
        if team_name:  # append if not None
            team_names.append(team_name)
    return team_names[0]  # return the first one
