from transformers import AutoModelForCausalLM, AutoTokenizer, AutoConfig
from huggingface_hub import login
import argparse
from multigec_2025_utils import md_to_dict, dict_to_md, sentences
import logging

max_length = 2048

# NOTE: You need a HuggingFace🤗 auth key that can access llama to use this code

if __name__ == "__main__":


    # Logger configuration

    logging.basicConfig()
    logger = logging.getLogger("MultiGEC_baseline")
    logger.setLevel(logging.INFO)


    # Argument parser

    parser = argparse.ArgumentParser()

    parser.add_argument("hf_key", help="HuggingFace authentication key")
    parser.add_argument("in_path", help="Path to the file with the essays")
    parser.add_argument("out_path", help="Path where the output will be saved to")
    parser.add_argument("lang", help="Name of the target language of the essays (in English)")
    parser.add_argument("mode", help="Which kind of correction to use; must be one of minimal|fluency")
    parser.add_argument("--device", default="auto", help="Device for the model to run on. Default 'auto'", required=False)

    args = parser.parse_args()

    hf_key   = args.hf_key
    in_path  = args.in_path
    out_path = args.out_path
    lang     = args.lang.title()
    mode     = args.mode.lower()
    device   = args.device


    # Asserting for valid values
    assert mode in ["minimal","fluency"]


    logger.info("We will evaluate for {} corrections in {}.".format(mode,lang))


    # Model thingies

    logger.info("Loading the language model...")

    login(hf_key)

    checkpoint = "meta-llama/Meta-Llama-3.1-8B-Instruct"
    
    tokenizer = AutoTokenizer.from_pretrained(checkpoint)
    config = AutoConfig.from_pretrained(checkpoint, max_new_tokens=3000)
    model = AutoModelForCausalLM.from_pretrained(checkpoint, config=config, torch_dtype="auto",
                                                 device_map=device)#, max_length=3000)
    
    logger.info("Language model loaded successfully!")


    # Data loader

    logger.info("Loading essays from: {}".format(in_path))

    out_essays = {}

    with open(in_path) as f:
        md = f.read()
    essay_dict = md_to_dict(md)
    n_essays   = len(essay_dict)

    if n_essays != 0:
        logger.info("Loaded {} essays successfully!".format(n_essays))
        if n_essays < 10:
            logger.warning("A very small ammount of essays was loaded. If this was intended, you can ignore this warning. Otherwise, make sure that both your dataset and the dataloader work as expected.")
    else:
        logger.critical("No essays were loaded, make sure that the dataloader works properly for your data!")



    # Inference phase

    for n, (essay_id, essay_text) in enumerate(essay_dict.items()):

        logger.info("Correcting essay {} of {}...".format(n+1, n_essays))


        # Prompt things

        # The prompt changes depending on whether we want minimal or fluent edits
        if mode == "minimal":
            task_prompt = "Make the smallest possible change in order to make the essay grammatically correct. Change as few words as possible. Do not rephrase parts of the essay that are already grammatical. Do not change the meaning of the essay by adding or removing information. If the essay is already grammatically correct, you should output the original essay without changing anything."
        else:
            task_prompt = "You may rephrase parts of the essay to improve fluency. Do not change the meaning of the essay by adding or removing information. If the essay is already grammatically correct and fluent, you should output the original essay without changing anything."

        # One-shot examples (in English)
        example_in  = "My name is Susanna. I come from Berlin, in the middl of Germany, bot I live in Bungaborg. I am studying data science in the University of Bungaborg and work extra as a teacher."
        example_out = "My name is Susanna. I come from Berlin, in the middle of Germany, but I live in Bungaborg. I am studying data science in the University of Bungaborg and work extra as a teacher."

        # Given an essay, generate a prompt
        def generate_prompt(text):
            prompt =  """<|begin_of_text|><|start_header_id|>system<|end_header_id|>

You are a grammatical error correction tool. Your task is to correct the grammaticality and spelling of the input essay written by a learner of {}. {} Return only the corrected text and nothing more.

Input essay:
<|eot_id|><|start_header_id|>user<|end_header_id|>
{}<|eot_id|>

<|start_header_id|>assistant<|end_header_id|>
Output essay:
{}<|eot_id|>

Input essay:
<|eot_id|><|start_header_id|>user<|end_header_id|>
{}<|eot_id|>
<|start_header_id|>assistant<|end_header_id|>
Output essay:
""".format(lang, task_prompt, example_in, example_out, text) 
            return prompt


        # Parsing a single essay
        def divide_text(text, max_len=max_length//2):

            # Given some text, generate a prompt and check its length
            prompt = generate_prompt(text)
            inputs = tokenizer(prompt, return_tensors="pt").to("cuda")
            n_tokens = inputs["input_ids"].shape[1]

            # Returns the prompt if it is below the model's max length
            if n_tokens < max_len:
                return [inputs]
            
            # Else splits the text into two and repeats the process
            else:
                sentence_list = sentences(text)
                halfpoint = len(sentence_list)//2
                flatten = lambda xss: [x for xs in xss for x in xs]
                return flatten([divide_text("".join(sentence_list[:halfpoint])),divide_text("".join(sentence_list[halfpoint:]))])


        inputs_list = divide_text(essay_text)
        correction_list = []
        
        # For each part of the split, generate a corrected version
        for inputs in inputs_list:
            n_tokens = inputs["attention_mask"].shape[1]
            outputs = model.generate(**inputs, max_length=max_length, pad_token_id=tokenizer.eos_token_id)
            out_text = tokenizer.decode(outputs[0])
            correction = out_text.split("Output essay:\n")[-1].strip("<|eot_id|>")

            correction_list.append(correction)

        # Once we have every part of the essay corrected, reform them into a single text
        out_essays[essay_id] = "".join(correction_list)


    logger.info("All essays corrected! 🦙")


    # Reformat the corrected versions and save them
    
    md_output = dict_to_md(out_essays)

    with open(out_path, "w") as f:
        f.write(md_output)

    logger.info("Baseline corrections saved to: {}".format(out_path))






