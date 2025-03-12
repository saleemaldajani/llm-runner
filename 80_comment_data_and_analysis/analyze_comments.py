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

# Read and parse the JSON file line by line
with open(json_file, "r", encoding="utf-8") as file:
    data = [json.loads(line) for line in file if line.strip()]

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
        result_json = {
            "comment": comment,
            "sentiment": "unknown",
            "hate": False,
            "angry": False,
            "spam": False,
            "troll": False,
            "response": False
        }
    
    result_json.update({
        "cid": item["cid"],
        "author": item["author"],
        "index": index
    })
    
    return result_json

# Process each comment
output_data = [analyze_comment(item, index) for index, item in enumerate(data)]

# Save results to a file
output_file = "processed_comments.json"
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(output_data, f, indent=4)

print(f"Processing complete. Results saved to {output_file}")
