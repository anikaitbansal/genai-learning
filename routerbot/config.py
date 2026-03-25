from groq import Groq   

client = Groq() #This creates the connection between your Python code and the Groq API. i don not need to pass the api key here as i have set it up in my environment variables. this is so when i push this code to github, i do not accidentally expose my api key. env is created by running this command in terminal: setx GROQ_API_KEY "gsk_abc123xyz"

MODEL_NAME = "llama-3.1-8b-instant"


# This code sets up a simple chatbot that classifies user input into different intents (chat, summarize, email, code) and handles each intent with a specific function. The conversation history is maintained to provide context for the AI's responses. The user can exit the program by typing "exit".
classifier_prompt = """You are a strict intent classifier.
Classify the user's message into exactly one of these labels only:
chat
summarize
email
code

Rules:
- Output only one word
- Allowed outputs are only: chat, summarize, email, code
- Do not explain
- Do not add punctuation
- Do not add extra words
- Do not add new lines
- If the user asks to summarize, shorten, or explain briefly, output summarize
- If the user asks to write, draft, compose, send, or reply to an email or message, output email
- If the user asks about code, programming, bugs, debugging, errors, or fixing code, output code
- Otherwise output chat
"""

chat_history = [] # This list will store the history of the conversation, including both user inputs and bot responses. This allows us to maintain context across multiple interactions, which can be useful for generating more relevant responses from the AI. We do not need history in email summarization or code debugging tasks as they are generally one shot replies and dont need context, so we will only maintain history for general chat interactions.
