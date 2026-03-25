from config import client, MODEL_NAME


def generate_response(system_prompt, user_input, chat_history, use_history=True): #  this is a function that generates a response from the AI based on the provided system prompt, user input, and optional chat history. It constructs the messages for the API call, including the system prompt and user input, and optionally includes the chat history if provided. The function then makes an API call to the Groq client to get the AI's response, which is returned as a string.
    messages = [{"role": "system", "content": system_prompt}]
    
    if use_history and chat_history:
        messages += chat_history
    
    messages.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model= MODEL_NAME,
        messages=messages,
        temperature=0.2
    )

    bot_reply = response.choices[0].message.content.strip()

    if use_history:
        chat_history.append({"role": "user", "content": user_input})
        chat_history.append({"role": "assistant", "content": bot_reply})

    return bot_reply

    

def handle_chat(user_input, chat_history): #  this is a function that takes the user's input as an argument and classifies the intent of the message based on the defined rules in the classifier_prompt. It makes an API call to the Groq client to get the classification result, which is then returned as a string.
    return generate_response(
        "You are a helpful assistant. Use previous conversation context when relevant.",
        user_input,
        chat_history,
        use_history=True
    )

def handle_summarize(user_input, chat_history): #  this is a function that takes the user's input as an argument and classifies the intent of the message based on the defined rules in the classifier_prompt. It makes an API call to the Groq client to get the classification result, which is then returned as a string.
    return generate_response(
        "You summarize text clearly and concisely. Use previous context if the user is referring to earlier text.",
        user_input,
        chat_history,
        use_history=True
    )

def handle_email(user_input, chat_history): #  this is a function that takes the user's input as an argument and classifies the intent of the message based on the defined rules in the classifier_prompt. It makes an API call to the Groq client to get the classification result, which is then returned as a string.
    return generate_response(
        "You are a professional email writer. If the user is refining a previously written email, use conversation context.",
        user_input,
        chat_history,
        use_history=True
    )
 

def handle_code(user_input, chat_history): #  this is a function that takes the user's input as an argument and classifies the intent of the message based on the defined rules in the classifier_prompt. It makes an API call to the Groq client to get the classification result, which is then returned as a string.
    return generate_response(
        "You help debug and explain code clearly. Use previous conversation context if the user is referring to earlier code.",
        user_input,
        chat_history,
        use_history=True
    )