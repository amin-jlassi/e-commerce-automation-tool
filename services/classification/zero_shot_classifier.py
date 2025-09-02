from datetime import datetime
start = datetime.now()
from get_categorys import fetch_categories
from transformers import pipeline



def classify(product_name) : 
    classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
    labels = fetch_categories().get("categories")
    labels.append("shoes")
    result = classifier(product_name, labels)
    scores = result.get("scores")
    labels = result.get("labels")
    res = [{labels[i]:scores[i]} for i in range(len(scores))]
    return res[0]

print(classify("nike air force 1 "))
end = datetime.now()
print(f"Time taken: {end - start}")