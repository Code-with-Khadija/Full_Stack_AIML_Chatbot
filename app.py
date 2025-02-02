import aiml
from glob import glob
from flask import Flask, render_template, request, redirect, url_for, flash, session
from nltk import sent_tokenize, word_tokenize
from nltk.corpus import wordnet as wn
from pytholog import KnowledgeBase, Expr
from neo4j import GraphDatabase
import hashlib
from datetime import datetime

# Initialize the Prolog knowledge base
kb = KnowledgeBase("family")
kb.from_file("E:/khadija/chatbot/chatbotproject/facts_rules.pl")  # Load the Prolog facts and rules

def get_description(word):
    print('inside get description')
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
    print("define:", define)
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

DEMO_USERNAME = 'demo'
DEMO_PASSWORD = 'password'

# Add Neo4j connection configuration
class Neo4jConnection:
    def __init__(self):
        self.uri = "bolt://localhost:7687"  # Update with your Neo4j URI
        self.username = "neo4j"  # Update with your username
        self.password = "12345678"  # Update with your password
        self.driver = None

    def connect(self):
        self.driver = GraphDatabase.driver(
            self.uri,
            auth=(self.username, self.password)
        )

    def close(self):
        if self.driver:
            self.driver.close()

    def verify_connection(self):
        try:
            with self.driver.session() as session:
                session.run("MATCH (n) RETURN n LIMIT 1")
            return True
        except Exception as e:
            print(f"Neo4j connection error: {e}")
            return False

# Add these helper functions
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def store_user(neo4j_conn, username, password, email):
    with neo4j_conn.driver.session() as session:
        # First check if user already exists
        check_query = """
        MATCH (u:User)
        WHERE u.username = $username OR u.email = $email
        RETURN u
        """
        result = session.run(check_query, username=username, email=email)
        if result.single():
            raise ValueError("Username or email already exists")

        # If no user exists, create new user
        hashed_password = hash_password(password)
        create_query = """
        CREATE (u:User {
            username: $username,
            password: $password,
            email: $email,
            created_at: datetime()
        })
        RETURN u
        """
        try:
            session.run(create_query,
                       username=username,
                       password=hashed_password,
                       email=email)
        except Exception as e:
            raise Exception(f"Error creating user: {str(e)}")

def verify_user(neo4j_conn, username, password):
    with neo4j_conn.driver.session() as session:
        hashed_password = hash_password(password)
        query = """
        MATCH (u:User {username: $username, password: $password})
        RETURN u
        """
        result = session.run(query, username=username, password=hashed_password)
        return result.single() is not None

def store_chat_history(neo4j_conn, username, query, response):
    with neo4j_conn.driver.session() as session:
        query = """
        MATCH (u:User {username: $username})
        CREATE (c:ChatMessage {
            query: $query,
            response: $response,
            timestamp: datetime()
        })
        CREATE (u)-[:SENT]->(c)
        """
        session.run(query, username=username, response=response)

def get_user_chat_history(neo4j_conn, username):
    with neo4j_conn.driver.session() as session:
        query = """
        MATCH (u:User {username: $username})-[:SENT]->(c:ChatMessage)
        RETURN c.query as query, c.response as response, c.timestamp as timestamp
        ORDER BY c.timestamp DESC
        LIMIT 10
        """
        results = session.run(query, username=username)
        return [dict(record) for record in results]

# Modify your Flask routes to use Neo4j
# Initialize Neo4j connection
neo4j_conn = Neo4jConnection()

def initialize_app():
    neo4j_conn.connect()
    if not neo4j_conn.verify_connection():
        print("Warning: Could not connect to Neo4j database!")
    bot_learn()

def bot_learn():
    aiml_files = [
        'E:/khadija/chatbot/chatbotproject/greetings.aiml',
        'E:/khadija/chatbot/chatbotproject/emotional support.aiml',
        'E:/khadija/chatbot/chatbotproject/diseases and medicine.aiml',
        'E:/khadija/chatbot/chatbotproject/lifestyle.aiml',
        'E:/khadija/chatbot/chatbotproject/therapy.aiml',
        'E:/khadija/chatbot/chatbotproject/daily motivation.aiml',
        'E:/khadija/chatbot/chatbotproject/support.aiml',
        'E:/khadija/chatbot/chatbotproject/therapy.aiml'
    ]

    for file in aiml_files:
        bot.learn(file)

@app.route("/")
def home():
    if 'username' in session:
        return render_template("home.html")
    return redirect(url_for('login'))


@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        email = request.form.get('email')

        # Basic validation
        if not all([username, password, confirm_password, email]):
            flash('All fields are required', 'danger')
            return render_template("signup.html")

        if password != confirm_password:
            flash('Passwords do not match', 'danger')
            return render_template("signup.html")

        if len(password) < 6:
            flash('Password must be at least 6 characters long', 'danger')
            return render_template("signup.html")

        try:
            store_user(neo4j_conn, username, password, email)
            flash('Account created successfully! Please login.', 'success')
            return redirect(url_for('login'))
        except ValueError as e:
            flash(str(e), 'danger')
        except Exception as e:
            flash('An error occurred while creating your account', 'danger')
            print(f"Error: {str(e)}")

    return render_template("signup.html")


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if verify_user(neo4j_conn, username, password):
            session['username'] = username
            flash('Logged in successfully!', 'success')
            return redirect(url_for('home'))
        flash('Invalid username or password', 'error')

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))
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
    if "father of" in query:
        response = ""
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
        response = ""
        name = query.split("mother of")[-1].strip()
        prolog_query = Expr(f"mother_of({name}, Y)")
        prolog_response = kb.query(prolog_query)

        if prolog_response:
            mother_name = prolog_response[0]['Y']
            response += f" The mother of {name} is {mother_name}."
        else:
            response += f" I couldn't find the mother of {name}."

    elif "grandfather of" in query:
        response = ""
        name = query.split("grandfather of")[-1].strip()
        prolog_query = Expr(f"grandfather_of({name}, Y)")
        prolog_response = kb.query(prolog_query)

        if prolog_response:
            grandfather_name = prolog_response[0]['Y']
            response += f" The grandfather of {name} is {grandfather_name}."
        else:
            response += f" I couldn't find the grandfather of {name}."

    elif "therapist of" in query:
        response = ""
        name = query.split("therapist of")[-1].strip()
        prolog_query = Expr(f"therapist_of(Therapist, {name})")
        prolog_response = kb.query(prolog_query)

        if prolog_response:
            therapist_name = prolog_response[0]['Therapist']
            response += f" The therapist of {name} is {therapist_name}."
        else:
            response += f" I couldn't find the therapist of {name}."

    elif "clients of" in query:
        response = ""
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
    initialize_app()  # Call initialization before running the app
    app.run(host='0.0.0.0', port='5000')
