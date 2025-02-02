# Full Stack AIML Chatbot with NLP, Prolog, Flask and Neo4j

This project is a rule-based chatbot that leverages **AIML (Artificial Intelligence Markup Language)** for natural language processing, **Prolog** for logical reasoning, and **Neo4j** as a graph database for managing relationships and structured data. The chatbot is integrated with **Flask** to provide a user-friendly web interface.

## 🚀 Features

- **AIML-based Chatbot**: Uses AIML for natural language understanding and response generation.
- **Prolog Integration**: Handles logical reasoning, particularly for family relationships and therapy-related queries.
- **Neo4j Graph Database**: Stores and manages complex relationships between users, emotions, therapists, and other entities.
- **Flask Web Interface**: Provides a browser-accessible interface for seamless interaction.
- **Emotional Support**: Offers therapy recommendations based on user input.
- **Family Relationship Queries**: Supports queries like *"Who is the father of Simon?"* using Prolog rules.

## 🛠 Installation

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

### 2️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 3️⃣ Set Up Neo4j
- Install Neo4j and start the server.
- Update the Neo4j connection details in **app.py** and **neo.py**.

### 4️⃣ Run the Flask Application
```bash
python app.py
```

### 5️⃣ Access the Chatbot
Open your browser and navigate to:
```
http://localhost:5000
```

## 📌 Usage

1. **Login/Signup**: Users must log in or sign up to interact with the chatbot.
2. **Chat Interface**: Enter queries to receive responses.
3. **Family Relationship Queries**: Ask questions like *"Who is the father of John?"*.
4. **Therapy Recommendations**: Receive therapist suggestions based on user needs.

## 📂 Project Structure
```
📦 AIML-Chatbot-Project
├── 📜 aiml_chatbot.py       # AIML chatbot implementation
├── 📜 app.py               # Flask web application
├── 📜 facts_rules.pl       # Prolog rules for logical reasoning
├── 📜 neo.py               # Neo4j database operations
├── 📜 login_withneo4j.py   # Login system integrated with Neo4j
├── 📂 templates/           # HTML templates for the web interface
├── 📂 static/              # CSS, JS, and images
└── 📜 requirements.txt     # Python dependencies
```

## 🤝 Contributing

Contributions are welcome! If you'd like to improve this project:
1. Fork the repository.
2. Create a new branch for your feature/fix.
3. Submit a pull request.

## 📜 License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

