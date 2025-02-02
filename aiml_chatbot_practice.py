from aiml import Kernel
from glob import glob
import pytholog as pl

kb = pl.KnowledgeBase("relation")
kb.clear_cache()
kb.from_file(r"E:\khadija\chatbot\chatbotproject\facts_rules.pl")

def person(x, rel):
  expr = rel+"_of(Y,"+x+")."
  y = kb.query(pl.Expr(expr))[0]['Y']
  return y

bot =Kernel()
def check_meaning():
    word = bot.getPredicate("word")
    if word == "":
        return
    else:
        bot.setPredicate("description", get_description(word))
        return

def get_info(query):
    bot.respond(query)
    x = bot.getPredicate("X")
    rel = bot.getPredicate("rel")
    Y = person(x, rel)
    # father_of(Y,simon)
    bot.setPredicate("Y", "Y")


aiml_files = glob(r'E:\khadija\chatbot\chatbotproject\aimlfiles/*.aiml')


for file in aiml_files:
    bot.learn(str(file))

while True:
    query = input("user: ")
    get_info(query)
    response = bot.respond(query)
    print(response)



    #while True:
    #   query=input("user: ")
    #   bot.respond(query)
    #    check_meaning()
    #    response=bot.respond(query)
    #   print(response)

