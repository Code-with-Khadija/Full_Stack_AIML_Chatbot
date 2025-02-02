# import aiml
# from glob import glob
# import nltk
#
# # Download necessary NLTK data
# nltk.download('wordnet')
# from nltk.corpus import wordnet
#
# # Initialize AIML Kernel
# bot = aiml.Kernel()
#
# # Load AIML files
# aiml_files = glob('*.aiml')
# for file in aiml_files:
#     bot.learn(file)
#
# # Function to get word definition using WordNet
# def get_definition(word):
#     try:
#         synset = wordnet.synsets(word + '.n.01')
#         return synset.definition()
#     except Exception as e:
#         return "Definition not found."
#
# # Set a default predicate for the chatbot
# bot.setPredicate("definition", "XYZ")
#
# while True:
#     query = input("User: ")
#     if query.lower() in ["exit", "quit", "bye"]:
#         print("Bot: Goodbye!")
#         break
#
#     response = bot.respond(query)
#
#     # Handle 'command' predicate
#     command = bot.getPredicate("command")
#     if command:
#         response += f" Command received: {command}."
#
#     # Simulate fetching temperature data
#     temperature = "30"  # Simulated temperature
#     bot.setPredicate("temp", temperature)
#     response += f" Current temperature is {temperature}°C."
#
#     # Handle WordNet-based definitions
#     word = bot.getPredicate("word")
#     if word:
#         definition = get_definition(word)
#         bot.setPredicate("definition", definition)
#         response += f" Definition of '{word}': {definition}."
#
#     print("Bot:", response)
import aiml
bot = aiml.Kernel()

# Load AIML files
# aiml_files = glob('*.aiml')
# for file in aiml_files:
#     bot.learn(file)
bot.learn("emotional support.aiml")


from nltk.corpus import wordnet as wn
def definition():
    word = bot.getPredicate("word")
    print(word)
    description = '\n'
    sn = wn.synsets(word)
    length = len(sn)
    for i in range(length):
        description += str(i + 1) + ". " + sn[i].definition()
        if i + 1 != length:
            description += '\n'

    return description

def define_word():
    define = bot.getPredicate("define")
    print(define)
    if define == "Yes":
        bot.setPredicate("define", "No")
        bot.setPredicate("definition", definition())
    return

while True:
    query = input("user: ")
    bot.respond(query)
    #check_meaning()
    define_word()
    response = bot.respond(query)

    print(response)