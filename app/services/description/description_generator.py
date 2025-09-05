from flask import Flask, request, render_template, jsonify
import os
import json
import dotenv
from openai import OpenAI

app = Flask(__name__)


dotenv.load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=API_KEY)

def generate_description(name, category, attributes, tone="professional"):
    prompt = f"""
    Write a {tone} e-commerce description for this product:
    Product: {name}
    Category: {category}
    Attributes: {', '.join(attributes)}

    Respond ONLY in JSON with this exact format:
    {{
      "description": "..."
    }}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300,
        response_format={"type": "json_object"}
    )

    try:
        return json.loads(response.choices[0].message.content.strip())["description"]
    except (KeyError, json.JSONDecodeError):
        return "Error: Unable to parse response."

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    
    name = request.form.get('name')
    category = request.form.get('category')
    attributes = request.form.get('attributes').split(',')  # Split attributes by comma
    tone = request.form.get('tone', 'professional')  # Default to professional if not provided

    
    if not name or not category or not attributes:
        return jsonify({"error": "Missing required fields"}), 400

    
    attributes = [attr.strip() for attr in attributes if attr.strip()]

    
    description = generate_description(name, category, attributes, tone)
    return jsonify({"description": description})

if __name__ == "__main__":
    app.run(debug=True)
