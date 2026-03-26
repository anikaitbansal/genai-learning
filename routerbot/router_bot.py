from config import client, MODEL_NAME, classifier_prompt
from handlers import handle_chat, handle_summarize, handle_email, handle_code
import argparse

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
    def __init__(self, debug=False):
        self.chat_history = [] # This list will store the history of the conversation, including both user inputs and bot responses. This allows us to maintain context across multiple interactions, which can be useful for generating more relevant responses from the AI. We do not need history in email summarization or code debugging tasks as they are generally one shot replies and dont need context, so we will only maintain history for general chat interactions.
        self.debug = debug

    def run(self):    
        while True:
            user_input = input("User: ")
            if self.debug:
                print("[DEBUG] User input:", user_input)

            if user_input.lower() == "exit":
                print("Exiting the program.")
                break
            
            # We classify the intent of the user's input using the classify_intent function, which makes an API call to the Groq client with the user's message and the defined classifier_prompt. The response from the API is then processed to extract the classified intent, which is printed to the console for debugging purposes.
            intent = classify_intent(user_input)
            if self.debug:
                print("[DEBUG] Intent:", intent)
                print("[DEBUG] Handler:", handlers[intent].__name__)

            bot_reply = handlers[intent](user_input, self.chat_history)
            print("Bot:", bot_reply)


#day 5 additions are everything below.

# class Chatbot:
#    def __init__(self):
#        pass
#    def run(self):

def main(debug=False): # here we made a main function in which we create an instance of the Chatbot class and call its run method. 
    if debug:
        print("Debug mode is ON.")
    bot = Chatbot(debug)
    bot.run()

if __name__ == "__main__": #this condtions helps us in a way that when we try to import this file in another file, the code inside this block will not run. It will only run when we execute this file directly
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    args = parser.parse_args()

    main(debug=args.debug)
    