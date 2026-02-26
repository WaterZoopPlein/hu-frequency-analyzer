import spacy
from collections import Counter
import csv

def analyze_file(doc):
    lemmas = [
        token.lemma_.lower()
        for token in doc
        if token.is_alpha
    ]

    freq = Counter(lemmas)

    for lemma, count in freq.most_common():
        print(f"{lemma}: {count}")

def extract_important_tokens(doc, character_names = []):
    important = {}

    for token in doc:
        is_character = token.pos_ == "PROPN" or  token.pos_ == "NOUN" and (token.text in character_names or token.lemma_ in character_names)
        if token.is_stop or token.is_punct or token.is_space or token.pos_ in {"AUX","PROPN"} or is_character:
            continue

        score = 0
        if token.dep_ in {"nsubj", "csubj", "obj", "iobj"}:
            score += 3
        if token.dep_ == "ROOT":
            score += 3
        if token.pos_ in {"NOUN", "ADV", "ADJ", "VERB"}:
            score += 1
        if token.ent_type_:
            score += 3


        if score > 0:
            important[token.lemma_.lower() + " " + token.pos_] = important.get(token.lemma_.lower()  + " " + token.pos_, 0) + score

    return sorted(important.items(), key=lambda x: x[1], reverse=True)


def export_to_csv(doc, filename="example.csv"):
    scored = extract_important_tokens(doc)

    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["token", "type", "score"])

        for token, score in scored:
            writer.writerow([
                token.split(" ")[0],
                token.split(" ")[1],
                score,
            ])

    print(f"Saved to {filename}")
