import json
from langchain_ollama import OllamaLLM

# Prompt template
def build_prompt(comment):
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
    return prompt

# Sample hateful comment
#comment = """Generative-AI is going to destroy
#humanity. I hate everyone working on AI. You are all
#evil."""
comment = "Life is beautiful."

# Build prompt
prompt = build_prompt(comment)

# Specify the model to use
model = OllamaLLM(model="llama3.2:1b")

# Invoke the model
result = model.invoke(input=prompt)

# Parse JSON output
try:
    result_json = json.loads(result)
    result_json["comment"] = comment  # Ensure comment is included
except json.JSONDecodeError:
    # Handle invalid JSON response from the model
    result_json = {
        "comment": comment,
        "sentiment": "unknown",
        "hate": False,
        "angry": False,
        "spam": False,
        "troll": False,
        "response": False
    }

# Print the structured output
print(json.dumps(result_json, indent=4))
