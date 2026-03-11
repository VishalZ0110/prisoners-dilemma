from smolagents import LiteLLMModel

model = LiteLLMModel(
        model_id="ollama_chat/qwen2:7b",  # Or try other Ollama-supported models
        api_base="http://127.0.0.1:11434",  # Default Ollama local server
        num_ctx=8192,
    )

response = model.generate(
    messages=[
        {"role": "user", "content": [{"type": "text", "text": "What is the capital of France?"}]}
    ],
    max_tokens=100,
    temperature=0.7,
    top_p=1,
    stop=["\n"],
)

print(response)