#!/usr/bin/env python
# ERRANT evaluation script for MultiGEC at NLP4CALL 2025
# Authors: Andrew Caines & Joni Kruijsbergen (ERRANT originally by Christopher Bryant, Mariano Felice, Ted Briscoe)
# Tested with Python version 3.12.5

import sys, re
import os
import subprocess
import utils_transform_markdown_to_one_essay_per_line
import pandas as pd


def score(input_dir, output_dir, data_split, team_name):
    submission_dir = os.path.join(input_dir, 'res')
    submission_files = []
    
    for el in os.listdir(submission_dir):
        el = el.lower()
        print(el)
        if el.startswith(('cs-natform-', 'cs-natwebinf-', 'cs-romani-', 'cs-seclearn-', 'en-', 'et-eic-', 'et-ekil2-', 'de-', 'el-', 'is-iceec-', 'is-icel2ec-', 'it-', 'lv-', 'ru-', 'sl-', 'sv-', 'uk-')) and el.endswith(f'-{data_split}.tmp'):
            submission_files.append(el)
        elif el.startswith(('cs-natform-', 'cs-natwebinf-', 'cs-romani-', 'cs-seclearn-', 'en-', 'et-eic-', 'et-ekil2-', 'de-', 'el-', 'is-iceec-', 'is-icel2ec-', 'it-', 'lv-', 'ru-', 'sl-', 'sv-', 'uk-')):
            continue
        else:
            print(el, "Warning: one or more of the submission files does not start with one of the following language codes: 'cs-natform-|cs-natwebinf-|cs-romani-|cs-seclearn-|en-|et-eic-|et-ekil2-|de-|el-|is-iceec-|is-icel2ec-|it-|lv-|ru-|sl-|sv-|uk-'. Process terminated.")
            sys.exit()
    
    if len(submission_files) == 0:
        print("Warning: the submission folder should contain at least 1 file starting with one of the following language codes: 'cs-natform-|cs-natwebinf-|cs-romani-|cs-seclearn-|en-|et-eic-|et-ekil2-|de-|el-|is-ec-|is-l2ec|it-|lv-|ru-|sl-|sv-|uk-'. Process terminated.")
        sys.exit()
    
    with open(os.path.join(output_dir, 'scores.txt'), 'w') as output_file:
        all_scores = []
        for submission_file in submission_files:
            submission_file_name = submission_file.lower()
            submission_path = os.path.join(submission_dir, submission_file_name)
            lang = submission_file_name[0:2]
            corpus = submission_file_name.split('-')[1]
            minimal_fluency = "minimal"
            if "fluency" in submission_file_name:
                minimal_fluency = "fluency"
            
            ref2_file = None
            ref3_file = None
            ref4_file = None
            
            if submission_file_name.startswith(('cs-natform', 'CS-NATFORM')):
                lang_code = "CS_NATFORM"
                ref_file = 'cs-natform-ref1-dev.tmp'
                ref2_file = 'cs-natform-ref2-dev.tmp'
                orig_file = 'cs-natform-orig-dev.tmp'
            elif submission_file_name.startswith(('cs-natwebinf', 'CS-NATWEBINF')):
                lang_code = "CS_NATWEBINF"
                ref_file = 'cs-natwebinf-ref1-dev.tmp'
                ref2_file = 'cs-natwebinf-ref2-dev.tmp'
                orig_file = 'cs-natwebinf-orig-dev.tmp'
            elif submission_file_name.startswith(('cs-romani', 'CS-ROMANI')):
                lang_code = "CS_ROMANI"
                ref_file = 'cs-romani-ref1-dev.tmp'
                ref2_file = 'cs-romani-ref2-dev.tmp'
                orig_file = 'cs-romani-orig-dev.tmp'
            elif submission_file_name.startswith(('cs-seclearn', 'CS-SECLEARN')):
                lang_code = "CS_SECLEARN"
                ref_file = 'cs-seclearn-ref1-dev.tmp'
                ref2_file = 'cs-seclearn-ref2-dev.tmp'
                orig_file = 'cs-seclearn-orig-dev.tmp'
            elif submission_file_name.startswith(('en', 'EN')):
                lang_code = "EN"
                ref_file = 'en-writeandimprove2024-ref1-dev.tmp'
                orig_file = 'en-writeandimprove2024-orig-dev.tmp'
            elif submission_file_name.startswith(('et-eic', 'ET-EIC')):
                lang_code = "ET_EIC"
                ref_file = 'et-eic-ref1-dev.tmp'
                ref2_file = 'et-eic-ref2-dev.tmp'
                ref3_file = 'et-eic-ref3-dev.tmp'
                orig_file = 'et-eic-orig-dev.tmp'
            elif submission_file_name.startswith(('et-ekil2', 'ET-EKIL2')):
                lang_code = "ET_EKIL2"
                ref_file = 'et-ekil2-ref1-dev.tmp'
                ref2_file = 'et-ekil2-ref2-dev.tmp'
                orig_file = 'et-ekil2-orig-dev.tmp'
            elif submission_file_name.startswith(('de', 'DE')):
                lang_code = "DE"
                ref_file = 'de-merlin-ref1-dev.tmp'
                orig_file = 'de-merlin-orig-dev.tmp'
            elif submission_file_name.startswith(('el', 'EL')):
                lang_code = "EL"
                ref_file = 'el-glcii-ref1-dev.tmp'
                orig_file = 'el-glcii-orig-dev.tmp'
            elif submission_file_name.startswith(('is-ec', 'IS-EC', 'is-IceEC', 'is-iceec')):
                lang_code = "IS_EC"
                ref_file = 'is-iceec-ref1-dev.tmp'
                orig_file = 'is-iceec-orig-dev.tmp'
            elif submission_file_name.startswith(('is-l2ec', 'IS-L2EC', 'is-IceL2EC', 'is-icel2ec')):
                lang_code = "IS_L2EC"
                ref_file = 'is-icel2ec-ref1-dev.tmp'
                orig_file = 'is-icel2ec-orig-dev.tmp'
            elif submission_file_name.startswith(('it', 'IT')):
                lang_code = "IT"
                ref_file = 'it-merlin-ref1-dev.tmp'
                orig_file = 'it-merlin-orig-dev.tmp'
            elif submission_file_name.startswith(('lv', 'LV')):
                lang_code = "LV"
                ref_file = 'lv-lava-ref1-dev.tmp'
                orig_file = 'lv-lava-orig-dev.tmp'
            elif submission_file_name.startswith(('ru', 'RU')):
                lang_code = "RU"
                ref_file = 'ru-rulec-ref1-dev.tmp'
                orig_file = 'ru-rulec-orig-dev.tmp'
            elif submission_file_name.startswith(('sl', 'SL')):
                lang_code = "SL"
                ref_file = 'sl-solar_eval-ref1-dev.tmp'
                orig_file = 'sl-solar_eval-orig-dev.tmp'
            elif submission_file_name.startswith(('sv', 'sw', 'SV')):
                lang_code = "SV"
                ref_file = 'sv-swell_gold-ref1-dev.tmp'
                orig_file = 'sv-swell_gold-orig-dev.tmp'
            elif submission_file_name.startswith(('uk', 'UK')):
                lang_code = "UK"
                ref_file = 'uk-ua_gec-ref1-dev.tmp'
                ref2_file = 'uk-ua_gec-ref2-dev.tmp'
                ref3_file = 'uk-ua_gec-ref3-dev.tmp'
                ref4_file = 'uk-ua_gec-ref4-dev.tmp'
                orig_file = 'uk-ua_gec-orig-dev.tmp'
            else:
                print(f"Language not found for {submission_file_name}. Please double-check the language code.")
                continue
            
            hyp_file = submission_path  # hypothesis is the submitted file
            ref_file_path = os.path.join(input_dir, 'ref', ref_file)  # reference from input/ref
            orig_file_path = os.path.join(input_dir, 'ref', orig_file)  # original from input/ref
            
            with open(hyp_file, 'r') as hyp_f, open(orig_file_path, 'r') as orig_f:
                hyp_lines = hyp_f.readlines()
                orig_lines = orig_f.readlines()

                if len(hyp_lines) != len(orig_lines):
                    print(f"Warning: The number of essays in the submission file {hyp_file} for {lang_code.lower()} ({len(hyp_lines)}) does not correspond with the number of essays in the original file ({orig_file_path, len(orig_lines)}).")
                    #sys.exit()
            
            ## GLEU scoring
            gleu_command = ['gleu', '-s', orig_file_path, '-r', ref_file_path]
            
            if ref2_file:
                ref2_file_path = os.path.join(input_dir, 'ref', ref2_file)
                gleu_command.append(ref2_file_path)
            if ref3_file:
                ref3_file_path = os.path.join(input_dir, 'ref', ref3_file)
                gleu_command.append(ref3_file_path)
            if ref4_file:
                ref4_file_path = os.path.join(input_dir, 'ref', ref4_file)
                gleu_command.append(ref4_file_path)
            
            gleu_command.extend(['-o', hyp_file, '-d', '4', '-f', '-n', '4', '-t', 'word'])
            
            print(f"Running GLEU command: {' '.join(gleu_command)}")
            gleu_output = os.popen(' '.join(gleu_command)).read()
            print(gleu_output)
            if gleu_output != "":
                gleu_split = gleu_output.split()
                gleu_score = gleu_split[1]
            else:
                gleu_score = "n/a"
            output_file.write(f"GLEU = {gleu_score}\n")
            
            ## start ERRANT scoring here
            
            # run ERRANT alignment for reference(s), from one-essay-per-line .tmp file(s) to M2 output
            refs = [ref_file_path]
            if ref2_file:
                ref2_file_path = os.path.join(input_dir, 'ref', ref2_file)
                refs.append(ref2_file_path)
            if ref3_file:
                ref3_file_path = os.path.join(input_dir, 'ref', ref3_file)
                refs.append(ref3_file_path)
            if ref4_file:
                ref4_file_path = os.path.join(input_dir, 'ref', ref4_file)
                refs.append(ref4_file_path)
            
            ref_m2 = ref_file_path.replace('.tmp', '.m2')
            errant_par_ref = "errant_parallel -orig " + orig_file_path + " -cor " + ' '.join(refs) + " -out " + ref_m2 + " -lang " + lang
            #os.system(errant_par_ref)  # to save time: do not need to run this, store preprocessed files instead
            
            # run ERRANT alignment on hypothesis file, from one-essay-per-line .md file to M2 output
            hyp_m2 = hyp_file.replace('.tmp', '.m2')
            errant_par_hyp = "errant_parallel -orig " + orig_file_path + " -cor " + hyp_file + " -out " + hyp_m2 + " -lang " + lang
            os.system(errant_par_hyp)
            
            # run ERRANT scoring
            print("Comparing M2 files:")
            errant_compare = "errant_compare -hyp " + hyp_m2 + " -ref " + ref_m2
            print(errant_compare)
            #errant_out = subprocess.run(errant_compare, capture_output=True, text=True)
            #errant_scores = errant_out.stdout
            errant_scores = os.popen(errant_compare).read()
            print(errant_scores)
            
            # capture the output which looks like this, add prec/rec/F0.5 to the output file
            #=========== Span-Based Correction ============
            #TP      FP      FN      Prec    Rec     F0.5
            #12      4       6       0.75    0.6667  0.7317
            #==============================================
            
            prf = re.compile(r"\d\.\d+\s+\d\.\d+\s+\d\.\d+")  # regex for expected output
            if errant_scores != "":
                prf_search = prf.search(errant_scores)
                prf_list = prf_search.group(0).split('\t')
                prf_values = [x for x in prf_list if x]
                #print("Captured the following P/R/F scores:")
                #print(prf_values)
                prec = prf_values[0]
                rec = prf_values[1]
                f05 = prf_values[2]
                output_file.write(f"==========\n")
                output_file.write(f"ERRANT scores for {lang_code}:\n")
                output_file.write(f"precision = {prec}\n")
                output_file.write(f"recall = {rec}\n")
                output_file.write(f"f0.5 = {f05}\n")
                output_file.write(f"\n")
                newline = {'team_name': team_name, 'language': lang, 'corpus': corpus, 'track': minimal_fluency, 'language': lang, 'GLEU': gleu_score, 'precision': float(prec)*100, 'recall': float(rec)*100, 'F0.5': float(f05)*100}
                print(newline)
                print("=============================")
                all_scores.append(newline)
            
    output_file.close()
    return pd.DataFrame(all_scores).sort_values(by=["language", "corpus"])

def main():
    [_, input_dir, output_dir, data_split] = sys.argv
    team_name = "some_team_name"  # placeholder
    # Run utils to preprocess .md files into one-essay-per-line format
    print("=============================")
    print("Transforming input data to one-essay-per-line...")
    team_name = utils_transform_markdown_to_one_essay_per_line.split_to_parfiles_all(os.path.join(input_dir, 'ref'), os.path.join(input_dir, 'res'), data_split)
    #print(team_name)
    # And run scoring function...
    print("=============================")
    print("Ok scoring the predictions files with ERRANT...")
    scores_df = score(input_dir, output_dir, data_split, team_name)
    scores_df.to_csv(os.path.join(output_dir, 'scores.csv'), sep=',', encoding='utf-8', index=False, header=True)
    print("Scores from GLEU & ERRANT have been stored in the scores.csv and scores.txt files in the specified output directory")
    print("=============================")

if __name__ == "__main__":
    main()
