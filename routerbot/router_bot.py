from config import client, MODEL_NAME, classifier_prompt

from handlers import handle_chat, handle_summarize, handle_email, handle_code


def classify_intent(user_input): #  this is a function that takes the user's input as an argument and classifies the intent of the message based on the defined rules in the classifier_prompt. It makes an API call to the Groq client to get the classification result, which is then returned as a string.
       
    response = client.chat.completions.create(
        model = MODEL_NAME,
        messages=[
            {"role": "system", "content": classifier_prompt},
            {"role": "user", "content": user_input}
        ],
        temperature=0.0 # We set the temperature to 0 to make the output deterministic, ensuring that the same input will always yield the same classified intent. This is important for consistent behavior in intent classification tasks.
    )
     
    raw_intent = response.choices[0].message.content.strip().lower()
    intent = raw_intent.split()[0]

    valid_intents = ["chat", "summarize", "email", "code"]

    if intent not in valid_intents:
        intent = "chat"

    return intent


# We create a dictionary called handlers that maps each intent label to its corresponding handler function. This allows us to easily call the appropriate function based on the classified intent of the user's message. When the user inputs a message, we classify the intent using the classify_intent function, and then use the handlers dictionary to call the correct function to generate the bot's response.
handlers = {
    "chat": handle_chat,
    "summarize": handle_summarize,
    "email": handle_email,
    "code": handle_code
} 

class Chatbot:
    def __init__(self):
        pass

    def run(self):    
        while True:
            user_input = input("User: ")

            if user_input.lower() == "exit":
                print("Exiting the program.")
                break
            
            # We classify the intent of the user's input using the classify_intent function, which makes an API call to the Groq client with the user's message and the defined classifier_prompt. The response from the API is then processed to extract the classified intent, which is printed to the console for debugging purposes.
            intent = classify_intent(user_input)
            print("Intent:", intent)

            bot_reply = handlers[intent](user_input)
            print("Bot:", bot_reply)

def main(): # here we made a main function in which we create an instance of the Chatbot class and call its run method. 
    bot = Chatbot()
    bot.run()

if __name__ == "__main__": #this condtions helps us in a way that when we try to import this file in another file, the code inside this block will not run. It will only run when we execute this file directly
    main()
    