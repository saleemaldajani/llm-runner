from langchain_ollama import OllamaLLM

model = OllamaLLM(model="llama3.2:1b")
result = model.invoke(input="Hello World!")
print(result)