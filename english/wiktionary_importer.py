import json
POS = "adv"

with open(f"dicts/kaikki.org-dictionary-Hungarian-by-pos-{POS}.jsonl","r") as f:
    single_line = f.readlines()

final_dict = {}
for each_line in single_line:
    j = json.loads(each_line)
    glosses = "##".join([f"{i+1} - {'#'.join(j["senses"][i].get('raw_glosses', j["senses"][i].get('glosses'))).strip()}" for i in range(len(j["senses"]))])
    if j['word'] not in final_dict:
        final_dict[j['word']] = [glosses]
    else:
        print(f"Word with multiple glosses found - {j['word']}")
        final_dict[j['word']].append(glosses)

with open(f"{POS}-dict.json","w") as f:
    json.dump(final_dict, f)
