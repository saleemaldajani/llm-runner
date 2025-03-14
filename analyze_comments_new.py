import json
import zipfile
import requests
import os
from langchain_ollama import OllamaLLM

# URL to download the dataset
url = "https://compuxo.org/assets/data/altman.json.zip"
zip_path = "altman.json.zip"
extract_path = "."

# Download the dataset
response = requests.get(url)
with open(zip_path, "wb") as file:
    file.write(response.content)

# Extract the zip file
with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall(extract_path)

# Locate the extracted JSON file
json_file = None
for file in os.listdir(extract_path):
    if file.endswith(".json"):
        json_file = os.path.join(extract_path, file)
        break

# Read JSON File
try:
    with open(json_file, "r", encoding="utf-8") as file:
        raw_data = file.read().strip()
        if not raw_data:
            raise ValueError("JSON file is empty")
        data = json.loads(raw_data)
        
        # If JSON is an object, extract list of comments
        if isinstance(data, dict):
            data = data.get("comments", data.get("data", []))

except (json.JSONDecodeError, ValueError) as e:
    print(f"Error loading JSON file: {e}")
    data = []

# Initialize the model
model = OllamaLLM(model="llama3.2:1b")

# Function to analyze comment
def analyze_comment(item, index):
    comment = item['text']
    
    prompt = f"""
    Classify the following comment:
    --- Comment:
    ```
    {comment}
    ```
    Answer in JSON format with the following fields:
    - sentiment: "positive" or "negative"
    - hate: true or false
    - angry: true or false
    - spam: true or false
    - troll: true or false
    - response: true or false
    """

    result = model.invoke(input=prompt)

    try:
        result_json = json.loads(result)
    except json.JSONDecodeError:
        result_json = {}

    # Ensure the comment and metadata are included in the final output
    result_json.update({
        "comment": comment,   # Ensure original comment is included
        "cid": item.get("cid", "unknown"),
        "author": item.get("author", "unknown"),
        "index": index,
        "sentiment": result_json.get("sentiment", "unknown"),
        "hate": result_json.get("hate", False),
        "angry": result_json.get("angry", False),
        "spam": result_json.get("spam", False),
        "troll": result_json.get("troll", False),
        "response": result_json.get("response", False)
    })
    
    return result_json

# Process each comment
output_data = [analyze_comment(item, index) for index, item in enumerate(data)]

# Save results to a file
output_file = "processed_comments.json"
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(output_data, f, indent=4)

print(f"Processing complete. Results saved to {output_file}")
