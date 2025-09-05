from datetime import datetime
start = datetime.now()
from services.classification.get_categorys import fetch_categories

from transformers import pipeline

classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

def classify(product_name) : 
    
    labels = fetch_categories().get("categories")
    labels.append("shoes")
    result = classifier(product_name, labels)
    scores = result.get("scores")
    labels = result.get("labels")
    res = [{"category" : labels[i] , "score":scores[i]} for i in range(len(scores))]
    return res[0]

if __name__ == "__main__":
    print(classify("nike air force 1"))
    end = datetime.now()
    print(f"Time taken: {end - start}")
