import aiml
from glob import glob
from flask import Flask, render_template, request, redirect, url_for, flash, session
from nltk import sent_tokenize, word_tokenize
from nltk.corpus import wordnet as wn
from pytholog import KnowledgeBase, Expr

# Initialize the Prolog knowledge base
kb = KnowledgeBase("family")
kb.from_file("E:/khadija/chatbot/chatbotproject/facts_rules.pl")  # Load the Prolog facts and rules

def connect_neo4j():
    # Define the Neo4j connection details
    uri = "bolt://localhost:7687"
    username = "neo4j"
    password = "Staticroad321@"
    # Create a Neo4j driver instance
    driver = GraphDatabase.driver(uri, auth=(username, password))
    return driver



def validate_data(email, password):
    driver = connect_neo4j()
    neo4j_session = driver.session()

    query = """
 MATCH (u:User{email:$email, password:$password})
 RETURN u
 """
    password = hash_password(password)
    user = neo4j_session.run(query, email=email, password=password).data()
    neo4j_session.close()
    driver.close()
    if user:
        return True

    return False

def check_email(email):
    driver = connect_neo4j()
    neo4j_session = driver.session()
    query = """
    MATCH (u:User{email:$email})
    RETURN u
    """
    user = neo4j_session.run(query, email=email).data()
    neo4j_session.close()
    driver.close()
    if user:
        print(user)
        return True
    return False




def get_description(word):
    print('inside get description')
    # word = bot.getPredicate("word")
    description = '\n'
    sn = wn.synsets(word)
    length = len(sn)
    for i in range(length):
        description += str(i + 1) + ". " + sn[i].definition()
        if i + 1 != length:
            description += '\n'
    print('description: ', description)
    return description


def define_word():
    print('inside define_word')
    define = bot.getPredicate("define")
    print("define:",define)
    if define == "Yes":
        bot.setPredicate("define", "No")
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


bot = aiml.Kernel()
app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = 'your-secret-key-here'  # Change this to a secure secret key

# Load AIML files
# aiml_files = glob('*.aiml')
# for file in aiml_files:
#     bot.learn(file)
# bot.learn("emotional support.aiml")

# Hardcoded credentials for demo
DEMO_USERNAME = 'demo'
DEMO_PASSWORD = 'password'


@app.route("/")
def home():
    if 'username' in session:
        return render_template("home.html")
    return redirect(url_for('login'))


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username == DEMO_USERNAME and password == DEMO_PASSWORD:
            session['username'] = username
            return redirect(url_for('home'))
        flash('Invalid username or password')
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

def bot_learn():
    aiml_files = [
        'E:/khadija/chatbot/chatbotproject/greetings.aiml',
        'E:/khadija/chatbot/chatbotproject/aimlfiles/emotional support.aiml',
        'E:/khadija/chatbot/chatbotproject/diseases and medicine.aiml',
        'E:/khadija/chatbot/chatbotproject/lifestyle.aiml',
        'E:/khadija/chatbot/chatbotproject/therapy.aiml',
        'E:/khadija/chatbot/chatbotproject/daily motivation.aiml',
        'E:/khadija/chatbot/chatbotproject/support.aiml',
        'E:/khadija/chatbot/chatbotproject/therapy.aiml'
    ]
    # aiml_files = glob(r'E:/khadija/chatbot/chatbotproject/bot.aiml')

    for file in aiml_files:
        bot.learn(file)

@app.route("/get")
def get_bot_response():
    if 'username' not in session:
        return redirect(url_for('login'))
    query = request.args.get('msg')
    print('user query: ', query)
    print(bot.respond(query))
    define_word()
    response = bot.respond(query)
    print('AIML response: ', response)

    # Example of querying Prolog based on the user's query
    # You may need to parse the query to determine what to ask Prolog
    if "father of" in query:
        response = "" #empty the previous response
        # Extract the name from the query
        name = query.split("father of")[-1].strip()
        prolog_query = Expr(f"father_of({name}, Y)")
        prolog_response = kb.query(prolog_query)
        print('prolog_response: ', prolog_response)

        if prolog_response:
            father_name = prolog_response[0]['Y']
            response += f" The father of {name} is {father_name}."
        else:
            response += f" I couldn't find the father of {name}."
    elif "mother of" in query:
        response = ""  # empty the previous response
        name = query.split("mother of")[-1].strip()
        prolog_query = Expr(f"mother_of({name}, Y)")
        prolog_response = kb.query(prolog_query)

        if prolog_response:
            mother_name = prolog_response[0]['Y']
            response += f" The mother of {name} is {mother_name}."
        else:
            response += f" I couldn't find the mother of {name}."

    elif "grandfather of" in query:
        response = ""  # empty the previous response
        name = query.split("grandfather of")[-1].strip()
        prolog_query = Expr(f"grandfather_of({name}, Y)")
        prolog_response = kb.query(prolog_query)

        if prolog_response:
            grandfather_name = prolog_response[0]['Y']
            response += f" The grandfather of {name} is {grandfather_name}."
        else:
            response += f" I couldn't find the grandfather of {name}."

    elif "therapist of" in query:
        response = ""  # empty the previous response
        name = query.split("therapist of")[-1].strip()
        prolog_query = Expr(f"therapist_of(Therapist, {name})")
        prolog_response = kb.query(prolog_query)

        if prolog_response:
            therapist_name = prolog_response[0]['Therapist']
            response += f" The therapist of {name} is {therapist_name}."
        else:
            response += f" I couldn't find the therapist of {name}."

    elif "clients of" in query:
        response = ""  # empty the previous response
        therapist_name = query.split("clients of")[-1].strip()
        prolog_query = Expr(f"clients_of({therapist_name}, Clients)")
        prolog_response = kb.query(prolog_query)

        if prolog_response:
            clients = prolog_response[0]['Clients']
            response += f" The clients of {therapist_name} are: {', '.join(clients)}."
        else:
            response += f" I couldn't find any clients for {therapist_name}."

    print('Final response: ', response)

    return str(response) if response else str(":)")

if __name__ == "__main__":
    bot_learn()
    app.run(host='0.0.0.0', port='5000')