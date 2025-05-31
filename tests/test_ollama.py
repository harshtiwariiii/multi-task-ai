from langchain_ollama import OllamaLLM
llm = OllamaLLM(model="llama3")
print(llm.invoke("Hello in 3 words:"))