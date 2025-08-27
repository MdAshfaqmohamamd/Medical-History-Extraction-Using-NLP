from transformers import pipeline
import pandas as pd

ner = pipeline("ner", model="dslim/bert-base-NER", grouped_entities=True)

def extract_entities(text):
    entities = ner(text)
    results = []
    for ent in entities:
        results.append({
            "Entity": ent['word'],
            "Label": ent['entity_group'],
            "Score": round(ent['score'], 3)
        })
    df = pd.DataFrame(results)
    return df
