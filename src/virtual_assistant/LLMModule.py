from openai import OpenAI

def getLLMText():
    # Point to the local server
    client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

    completion = client.chat.completions.create(
        model="model-identifier",
        messages=[
            {"role": "system", "content": "Always answer in rhymes."},
            {"role": "user", "content": "Introduce yourself."}
        ],
        temperature=0.7,
        max_tokens=100  # Set maximum tokens here
    )

    # Access the content attribute directly
    print(completion.choices[0].message.content)
    return completion.choices[0].message.content