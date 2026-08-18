from langchain_ollama import ChatOllama


llm = ChatOllama(
    model="llama3.2:3b",
    temperature=0,
)


response = llm.invoke(
    "Say exactly: AutoMind AI V2 connection successful"
)

print("\n==============================")
print("LANGCHAIN + OLLAMA TEST")
print("==============================")
print(response.content)
print("==============================")