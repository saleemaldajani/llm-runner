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

# Create results folder if it doesn’t exist
results_folder = "results"
os.makedirs(results_folder, exist_ok=True)

# Identify already processed chunks
processed_indices = set()
for file in os.listdir(results_folder):
    if file.startswith("processed_") and file.endswith(".json"):
        try:
            index = int(file.replace("processed_", "").replace(".json", ""))
            processed_indices.add(index)
        except ValueError:
            continue  # Ignore files that don't match the naming pattern

# Determine the starting point
start_index = max(processed_indices, default=-1) + 1

# Function to analyze a comment
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

# Process comments in chunks of 100
batch_size = 100
total_comments = len(data)

for batch_start in range(start_index * batch_size, total_comments, batch_size):
    batch_end = min(batch_start + batch_size, total_comments)
    
    if batch_start // batch_size in processed_indices:
        print(f"Skipping already processed batch {batch_start // batch_size}")
        continue  # Skip already processed batches
    
    batch_data = [analyze_comment(data[i], i) for i in range(batch_start, batch_end)]
    
    # Save batch to a new file
    output_file = os.path.join(results_folder, f"processed_{batch_start // batch_size}.json")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(batch_data, f, indent=4)

    print(f"Processed {batch_end}/{total_comments} comments... (Saved: {output_file})")

print(f"Processing complete. Results saved in '{results_folder}/' folder.")
