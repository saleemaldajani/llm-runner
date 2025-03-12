# Dependency: pip install langchain-ollama
from langchain_ollama import OllamaLLM

# Prompt template
def build_prompt(comment):
    prompt = f"""
    What do you think about this comment?
    --- Comment:
    ```
    {comment}
    ```
    """
    return prompt

# Sample hateful comment
comment = """Generative-AI is going to destroy
humanity. I hate everyone working on AI. You are all
evil."""

# Build prompt
prompt = build_prompt(comment)

# Specify the model to use
model = OllamaLLM(model="llama3.2:1b")

# Invoke the model
result = model.invoke(input=prompt)

# Print result
print(result)
