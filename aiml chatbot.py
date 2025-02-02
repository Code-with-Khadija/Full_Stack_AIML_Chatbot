from aiml import Kernel
from glob import glob
#from nltk_practice import sentiment_analysis
from nltk_practice import get_description

bot =Kernel()
def check_meaning():
    print('inside check_meaning')
    define = bot.getPredicate("define")
    print('define: ', define)
    if define == "Yes":
        word = bot.getPredicate("word")
        print('word: ', word)
        if word == "":
            print('word is empty returning')
            return
        else:
            print('setting the predicate of description')
            bot.setPredicate("description", get_description(word))
            return
    else:
        return



def run():


    aiml_files = [
        'E:/khadija/chatbot/chatbotproject/greetings.aiml',
        'E:/khadija/chatbot/chatbotproject/aimlfiles/emotional support.aiml',
        'E:/khadija/chatbot/chatbotproject/diseases and medicine.aiml'
        'E:/khadija/chatbot/chatbotproject/lifestyle.aiml',
        'E:/khadija/chatbot/chatbotproject/therapy.aiml',
        'E:/khadija/chatbot/chatbotproject/daily motivation.aiml',
        'E:/khadija/chatbot/chatbotproject/facts_rules.pl'

    ]
    #aiml_files = glob('E:/khadija/chatbot/chatbotproject/bot.aiml')


    for file in aiml_files:
        bot.learn(file)

    while True:
        query=input("user: ")
        bot.respond(query)
        check_meaning()
        response=bot.respond(query)
        print(response)




if __name__ == '__main__':
    run()