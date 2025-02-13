from transformers import pipeline

chat_model = pipeline("text-generation", model="gpt2")

def get_chat_response(user_input):
    response = chat_model(user_input, max_length=50, num_return_sequences=1)
    return response[0]["generated_text"]
