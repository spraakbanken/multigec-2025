# for shinyapps deployment
import spacy
nlp = spacy.load("en_core_web_sm")
nlp.to_disk(f"spacy_models/en_core_web_sm/")
