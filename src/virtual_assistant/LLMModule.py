from openai import OpenAI
import re

def getLLMText(text, tokens, language):
    try:
        # Point to the local server
        client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

        if language == "es-ES":
            system_message = "Eres un asistente inteligente. Siempre proporcionas respuestas bien razonadas que son correctas y útiles."
            user_message = f"Por favor, responde en español. {text}"
        elif language == "en-US":
            system_message = "You are an intelligent assistant. You always provide well-reasoned answers that are correct and useful."
            user_message = f"Please respond in English. {text}"
        else:
            raise ValueError("Unsupported language")

        completion = client.chat.completions.create(
            model="model-identifier",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7,
            max_tokens=tokens,  # Set maximum tokens here
            stop=None  # Optionally set a stopping sequence if needed
        )

        # Access the content attribute directly
        response = completion.choices[0].message.content

        # Ensure the response ends with a complete sentence
        complete_response = ensure_complete_sentence(response)

        print("---------------------------")
        print(complete_response)
        print("---------------------------")
        return complete_response
    
    except Exception as e:
        print("An error occurred:", e)
        return None

def ensure_complete_sentence(text):
    # Use a regex to find the last complete sentence
    matches = list(re.finditer(r'[.!?]', text))
    if matches:
        last_match = matches[-1]
        complete_sentence = text[:last_match.end()]
        return complete_sentence.strip()
    return text.strip()
