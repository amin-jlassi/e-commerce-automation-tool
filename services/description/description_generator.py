from openai import OpenAI
import os
import json
import dotenv

dotenv.load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=API_KEY)

def generate_description(name, category, attributes, tone="professional"):
    prompt = f"""
    Write a {tone} e-commerce site description for this product:
    Product: {name}
    Category: {category}
    Attributes: {', '.join(attributes)}
    Please respond only in JSON format.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300,
        response_format={"type": "json_object"}
    )

    return json.loads(response.choices[0].message.content.strip())


if __name__ == "__main__":
    print(generate_description(
        "Nike Air Force 1",
        "Shoes > Sneakers",
        ["White", "Leather", "Unisex", "Classic design"]
    ))