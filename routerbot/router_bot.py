from config import client, MODEL_NAME, classifier_prompt
from handlers import handle_chat, handle_summarize, handle_email, handle_code
import argparse
from memory_manager import MemoryManager

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
    def __init__(self, debug=False): # debug is a boolean parameter that allows us to enable or disable debug mode when creating an instance of the Chatbot class. When debug
        self.memory = MemoryManager("chat_history.json") # This line creates an instance of the MemoryManager class and assigns
        self.chat_history = self.memory.load() # This line calls the load method of the MemoryManager instance to load the chat history from the specified JSON file. The loaded chat history is then stored in the chat_history attribute of the Chatbot instance, allowing us to maintain context and continuity in the conversation with the user.
        self.debug = debug 

    def run(self):    
        while True:
            user_input = input("User: ")
            if self.debug: # If debug mode is enabled, we print the user's input to the console for debugging purposes. This allows us to see exactly what the user has entered before we process it, which can be helpful for troubleshooting and understanding the flow of the program.
                print("[DEBUG] User input:", user_input)

            if user_input.lower() == "exit":
                print("Exiting the program.")
                break

            if user_input.lower() == "reset":
                self.chat_history = self.memory.clear()
                print("Bot: Memory cleared.")
                continue
            
            # We classify the intent of the user's input using the classify_intent function, which makes an API call to the Groq client with the user's message and the defined classifier_prompt. The response from the API is then processed to extract the classified intent, which is printed to the console for debugging purposes.
            intent = classify_intent(user_input)
            if self.debug: # If debug mode is enabled, we print the classified intent and the name of the handler function that will be called to generate the bot's response. This allows us to see how the user's input is being classified and which function is being used to handle it, which can be helpful for troubleshooting and understanding the flow of the program.
                print("[DEBUG] Intent:", intent)
                print("[DEBUG] Handler:", handlers[intent].__name__) # .__name__ is a special attribute in Python that returns the name of the function as a string. In this case, it will print the name of the handler function that corresponds to the classified intent, such as "handle_chat", "handle_summarize", "handle_email", or "handle_code". This is useful for debugging purposes to verify that the correct handler function is being called based on the classified intent.

            bot_reply = handlers[intent](user_input, self.chat_history)
            print("Bot:", bot_reply)
            self.memory.save(self.chat_history)


#day 5 additions are everything below.

# class Chatbot:
#    def __init__(self):
#        pass
#    def run(self):

def main(debug=False): # This is the main function that serves as the entry point of the program. It takes an optional debug parameter that allows us to enable or disable debug mode when running the chatbot. If debug mode is enabled, it prints a message indicating that debug mode is on. Then, it creates an instance of the Chatbot class, passing the debug parameter to its constructor, and calls the run method to start the chatbot's interaction loop.
    if debug:
        print("Debug mode is ON.")
    bot = Chatbot(debug)
    bot.run()

if __name__ == "__main__": # This is a common Python idiom that checks if the script is being run directly (as the main program) rather than imported as a module in another script. If this condition is true, it executes the code block that follows, which in this case is responsible for parsing command-line arguments and calling the main function with the appropriate debug flag based on the user's input.
    parser = argparse.ArgumentParser() # This line creates an ArgumentParser object from the argparse module, which is used to handle command-line arguments. The parser allows us to define what arguments our program accepts and how they should be processed. In this case, we will use it to add a debug flag that can be set when running the script from the command line.
    parser.add_argument("--debug", action="store_true", help="Enable debug mode") # This line adds a command-line argument called --debug to the parser. The action="store_true" parameter means that if the user includes the --debug flag when running the script, the debug variable will be set to True. If the flag is not included, debug will be False by default. The help parameter provides a description of what the --debug flag does, which will be displayed when the user runs the script with the --help option. This allows users to easily enable debug mode when running the chatbot for troubleshooting or development purposes.
    args = parser.parse_args() # This line parses the command-line arguments that were defined using the parser. It processes the arguments passed to the script when it is run and stores the results in the args variable. In this case, if the user included the --debug flag, args.debug will be set to True; otherwise, it will be False. This allows us to control whether debug mode is enabled when we call the main function.

    main(debug=args.debug) # This line calls the main function, passing the value of args.debug as the debug parameter. This means that if the user included the --debug flag when running the script, debug mode will be enabled in the main function, which will then be passed to the Chatbot instance to control whether debug information is printed during the chatbot's operation.
    