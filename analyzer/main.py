from convert_utils import *
activated = spacy.require_gpu()
print(activated)

nlp = spacy.load("hu_core_news_trf")
TEXT_NAME = "pal_utcai"
CHARACTER_NAMES = ["Kolnay", "Boka", "Weisz", "Pásztor", "Csónakos", "Nemecsek", "Leszik", "Csele", "Áts", "Pásztor", "Szebenics", "Wendauer"]

with open(f"{TEXT_NAME}.txt", "r", encoding="utf-8") as f:
    text = f.read()
text = [t for t in text.split('\n') if t and t.strip()]
doc_list = []
print(f"There are {len(text)} sections.")

for i in range(len(text)):
    doc = nlp(text[i])
    doc_list.append(doc)
    if (i+1) % 100 == 0:
        print(f"Processed {i+1} / {len(text)} sections.")

sections_important_tokens = [extract_important_tokens(doc, CHARACTER_NAMES) for doc in doc_list]

total_dict = {}
for important_tokens in sections_important_tokens:
    for token in important_tokens:
        total_dict[token[0]] = total_dict.get(token[0], 0) + token[1]
total_dict = sorted(total_dict.items(), key=lambda x: x[1], reverse=True)

cum_list = []
cum = 0
for i in range(len(total_dict)):
    cum += total_dict[i][1]
    cum_list.append(cum)

total_cum = cum_list[-1]
for i in range(len(total_dict)):
    cum_list[i] = round(cum_list[i]/total_cum* 100,2)     

with open(f"../results/{TEXT_NAME}.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["token", "type", "score","cummulative percentage"])

    for i in range(len(total_dict)):
        writer.writerow([
            total_dict[i][0].split(" ")[0], 
            total_dict[i][0].split(" ")[1],
            total_dict[i][1],
            cum_list[i]
        ])
