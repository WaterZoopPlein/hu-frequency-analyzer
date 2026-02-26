import json
import csv

IGEKOTOK = {
    "meg", "el", "ki", "be", "fel", "le", "át", "össze", "szét",
    "vissza", "rá", "ide", "oda", "túl", "alá", "elő", "bele"
}
IGEKOTOK = sorted(IGEKOTOK, key=len, reverse=True)

with open("jsons/noun-dict.json","r") as f:
    noun_json = json.load(f)
with open("jsons/verb-dict.json","r") as f:
    verb_json = json.load(f)
with open("jsons/adj-dict.json","r") as f:
    adj_json = json.load(f)
with open("jsons/adv-dict.json","r") as f:
    adv_json = json.load(f)

token_csv = []

with open("../results/pal_utcai.csv", "r", newline="", encoding="utf-8") as f:
    reader = csv.reader(f)
    for row in reader:
        token_csv.append(row)

token_csv[0].append("english")
for i in range(1, len(token_csv)):
    current_entry = token_csv[i]
    current_headword = current_entry[0]
    if current_entry[1] == "NOUN" and current_headword in noun_json:
        token_csv[i].append("####".join(noun_json[current_headword]))
    elif current_entry[1] == "VERB":
        if current_headword in verb_json:
            token_csv[i].append("####".join(verb_json[current_headword]))
        else:
            for pref in IGEKOTOK:    
                if current_headword.startswith(pref):
                    base = current_headword[len(pref):]
                    if base in verb_json:
                        token_csv[i].append(f"**{base.upper()}**"+"####".join(verb_json[base]))
                        print(f"Prefixed verb {current_headword} not found. Use {base} instead")
                    else:
                        print(f"Prefixed verb {current_headword} not found." +f" But {base} isn't defined".upper())
                    break
    elif current_entry[1] == "ADJ" and current_headword in adj_json:
        token_csv[i].append("####".join(adj_json[current_headword]))
    elif current_entry[1] == "ADV" and current_headword in adv_json:
        token_csv[i].append("####".join(adv_json[current_headword]))
    else:
        token_csv[i].append("")

# Writing to a CSV file
with open('results/pal_utcai_ENG.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(token_csv[0])
    writer.writerows(token_csv[1:])
