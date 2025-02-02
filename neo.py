from neo4j import GraphDatabase

uri = 'bolt://localhost:7687'
username = 'neo4j'
password = '12345678'

driver = GraphDatabase.driver(uri, auth=(username, password))

# User Management
def create_user(name, age, email):
    with driver.session() as session:
        query = """
        CREATE (u:User {name: $name, age: $age, email: $email, created_at: datetime()})
        RETURN u
        """
        session.run(query, name=name, age=age, email=email)
        print(f"User created: {name}")

# Emotion and Mood Tracking
def create_emotion(emotion_type, intensity):
    with driver.session() as session:
        query = """
        MERGE (e:Emotion {type: $emotion_type, intensity: $intensity})
        RETURN e
        """
        session.run(query, emotion_type=emotion_type, intensity=intensity)
        print(f"Emotion tracked: {emotion_type}")

def link_user_emotion(username, emotion_type, timestamp):
    with driver.session() as session:
        query = """
        MATCH (u:User {name: $username})
        MATCH (e:Emotion {type: $emotion_type})
        CREATE (u)-[:FELT {timestamp: $timestamp}]->(e)
        """
        session.run(query, username=username, emotion_type=emotion_type, timestamp=timestamp)

# Therapy and Support
def create_therapist(name, specialization):
    with driver.session() as session:
        query = """
        CREATE (t:Therapist {
            name: $name, 
            specialization: $specialization,
            created_at: datetime()
        })
        RETURN t
        """
        session.run(query, name=name, specialization=specialization)

def assign_therapist(username, therapist_name):
    with driver.session() as session:
        query = """
        MATCH (u:User {name: $username})
        MATCH (t:Therapist {name: $therapist_name})
        CREATE (u)-[:ASSIGNED_TO]->(t)
        """
        session.run(query, username=username, therapist_name=therapist_name)

# Coping Mechanisms and Activities
def create_coping_mechanism(activity, category):
    with driver.session() as session:
        query = """
        MERGE (c:CopingMechanism {
            name: $activity,
            category: $category
        })
        RETURN c
        """
        session.run(query, activity=activity, category=category)

def link_emotion_to_coping(emotion_type, activity):
    with driver.session() as session:
        query = """
        MATCH (e:Emotion {type: $emotion_type})
        MATCH (c:CopingMechanism {name: $activity})
        MERGE (e)-[:RECOMMENDED_COPING]->(c)
        """
        session.run(query, emotion_type=emotion_type, activity=activity)

# Support Groups
def create_support_group(name, focus_area):
    with driver.session() as session:
        query = """
        CREATE (g:SupportGroup {
            name: $name,
            focus_area: $focus_area,
            created_at: datetime()
        })
        RETURN g
        """
        session.run(query, name=name, focus_area=focus_area)

def join_support_group(username, group_name):
    with driver.session() as session:
        query = """
        MATCH (u:User {name: $username})
        MATCH (g:SupportGroup {name: $group_name})
        CREATE (u)-[:MEMBER_OF]->(g)
        """
        session.run(query, username=username, group_name=group_name)

# Progress Tracking
def record_progress(username, category, rating, notes):
    with driver.session() as session:
        query = """
        MATCH (u:User {name: $username})
        CREATE (p:Progress {
            category: $category,
            rating: $rating,
            notes: $notes,
            timestamp: datetime()
        })
        CREATE (u)-[:RECORDED]->(p)
        """
        session.run(query, username=username, category=category, rating=rating, notes=notes)

# Symptoms and Triggers
def create_symptom(name, category):
    with driver.session() as session:
        query = """
        MERGE (s:Symptom {
            name: $name,
            category: $category,
            created_at: datetime()
        })
        RETURN s
        """
        session.run(query, name=name, category=category)

def link_emotion_to_symptom(emotion_type, symptom_name):
    with driver.session() as session:
        query = """
        MATCH (e:Emotion {type: $emotion_type})
        MATCH (s:Symptom {name: $symptom_name})
        MERGE (e)-[:MANIFESTS_AS]->(s)
        """
        session.run(query, emotion_type=emotion_type, symptom_name=symptom_name)

def create_trigger(name, category):
    with driver.session() as session:
        query = """
        MERGE (t:Trigger {
            name: $name,
            category: $category,
            created_at: datetime()
        })
        RETURN t
        """
        session.run(query, name=name, category=category)

def link_trigger_to_emotion(trigger_name, emotion_type):
    with driver.session() as session:
        query = """
        MATCH (t:Trigger {name: $trigger_name})
        MATCH (e:Emotion {type: $emotion_type})
        MERGE (t)-[:CAUSES]->(e)
        """
        session.run(query, trigger_name=trigger_name, emotion_type=emotion_type)

# Medication and Treatment
def create_medication(name, category, dosage):
    with driver.session() as session:
        query = """
        CREATE (m:Medication {
            name: $name,
            category: $category,
            dosage: $dosage,
            created_at: datetime()
        })
        RETURN m
        """
        session.run(query, name=name, category=category, dosage=dosage)

def link_medication_to_symptom(medication_name, symptom_name):
    with driver.session() as session:
        query = """
        MATCH (m:Medication {name: $medication_name})
        MATCH (s:Symptom {name: $symptom_name})
        MERGE (m)-[:TREATS]->(s)
        """
        session.run(query, medication_name=medication_name, symptom_name=symptom_name)

# Goals and Achievements
def create_goal(username, title, category, target_date):
    with driver.session() as session:
        query = """
        MATCH (u:User {name: $username})
        CREATE (g:Goal {
            title: $title,
            category: $category,
            target_date: date($target_date),
            status: 'In Progress',
            created_at: datetime()
        })
        CREATE (u)-[:HAS_GOAL]->(g)
        RETURN g
        """
        session.run(query, username=username, title=title, 
                   category=category, target_date=target_date)

def track_goal_progress(username, goal_title, progress_note):
    with driver.session() as session:
        query = """
        MATCH (u:User {name: $username})-[:HAS_GOAL]->(g:Goal {title: $goal_title})
        CREATE (p:Progress {
            note: $progress_note,
            timestamp: datetime()
        })
        CREATE (g)-[:HAS_PROGRESS]->(p)
        """
        session.run(query, username=username, goal_title=goal_title, 
                   progress_note=progress_note)

# Mood Patterns and Analysis
def record_mood_pattern(username, pattern_type, description):
    with driver.session() as session:
        query = """
        MATCH (u:User {name: $username})
        CREATE (p:Pattern {
            type: $pattern_type,
            description: $description,
            identified_at: datetime()
        })
        CREATE (u)-[:EXHIBITS]->(p)
        """
        session.run(query, username=username, pattern_type=pattern_type, 
                   description=description)

def link_pattern_to_triggers(pattern_type, trigger_names):
    with driver.session() as session:
        for trigger in trigger_names:
            query = """
            MATCH (p:Pattern {type: $pattern_type})
            MATCH (t:Trigger {name: $trigger})
            MERGE (p)-[:ASSOCIATED_WITH]->(t)
            """
            session.run(query, pattern_type=pattern_type, trigger=trigger)

# Support Network
def create_support_contact(username, contact_name, relationship_type):
    with driver.session() as session:
        query = """
        MATCH (u:User {name: $username})
        CREATE (c:SupportContact {
            name: $contact_name,
            relationship: $relationship_type,
            added_at: datetime()
        })
        CREATE (u)-[:HAS_SUPPORT]->(c)
        """
        session.run(query, username=username, contact_name=contact_name,
                   relationship_type=relationship_type)

# Example usage and data population
if __name__ == "__main__":
    # Create some initial data
    emotions = [
        ("Anxiety", "high"),
        ("Depression", "moderate"),
        ("Stress", "high"),
        ("Happiness", "low"),
        ("Anger", "moderate"),
        ("Fear", "high")
    ]

    coping_mechanisms = [
        ("Deep Breathing", "Relaxation"),
        ("Meditation", "Mindfulness"),
        ("Journal Writing", "Self-Expression"),
        ("Exercise", "Physical Activity"),
        ("Talk Therapy", "Professional Support"),
        ("Art Therapy", "Creative Expression")
    ]

    support_groups = [
        ("Anxiety Support", "Anxiety Management"),
        ("Depression Support", "Depression Management"),
        ("Stress Management", "Stress Relief"),
        ("Mindfulness Group", "Meditation and Mindfulness"),
        ("Youth Support", "Teen Mental Health")
    ]

    # Create emotions and coping mechanisms
    for emotion, intensity in emotions:
        create_emotion(emotion, intensity)

    for activity, category in coping_mechanisms:
        create_coping_mechanism(activity, category)

    # Create recommended coping mechanisms for each emotion
    recommendations = {
        "Anxiety": ["Deep Breathing", "Meditation"],
        "Depression": ["Exercise", "Talk Therapy"],
        "Stress": ["Deep Breathing", "Exercise"],
        "Anger": ["Meditation", "Art Therapy"],
        "Fear": ["Talk Therapy", "Journal Writing"]
    }

    for emotion, activities in recommendations.items():
        for activity in activities:
            link_emotion_to_coping(emotion, activity)

    # Create support groups
    for name, focus in support_groups:
        create_support_group(name, focus)

    # Add symptoms
    symptoms = [
        ("Insomnia", "Sleep"),
        ("Panic Attacks", "Anxiety"),
        ("Low Energy", "Depression"),
        ("Racing Thoughts", "Anxiety"),
        ("Loss of Appetite", "Physical"),
        ("Irritability", "Mood")
    ]

    # Add triggers
    triggers = [
        ("Work Deadlines", "Professional"),
        ("Social Media", "Digital"),
        ("Family Conflict", "Relationship"),
        ("Financial Stress", "Environmental"),
        ("Poor Sleep", "Physical"),
        ("Negative News", "Environmental")
    ]

    # Create symptoms and triggers
    for name, category in symptoms:
        create_symptom(name, category)
    
    for name, category in triggers:
        create_trigger(name, category)

    # Link emotions to symptoms
    symptom_emotions = {
        "Anxiety": ["Insomnia", "Panic Attacks", "Racing Thoughts"],
        "Depression": ["Low Energy", "Loss of Appetite"],
        "Stress": ["Insomnia", "Irritability"],
        "Anger": ["Irritability"]
    }

    for emotion, symptom_list in symptom_emotions.items():
        for symptom in symptom_list:
            link_emotion_to_symptom(emotion, symptom)

    # Link triggers to emotions
    trigger_emotions = {
        "Work Deadlines": ["Stress", "Anxiety"],
        "Social Media": ["Anxiety", "Depression"],
        "Family Conflict": ["Anger", "Stress"],
        "Financial Stress": ["Anxiety", "Depression"],
        "Poor Sleep": ["Irritability", "Stress"],
        "Negative News": ["Anxiety", "Depression"]
    }

    for trigger, emotion_list in trigger_emotions.items():
        for emotion in emotion_list:
            link_trigger_to_emotion(trigger, emotion)

    # Add medications
    medications = [
        ("Sertraline", "SSRI", "50mg"),
        ("Alprazolam", "Benzodiazepine", "0.5mg"),
        ("Melatonin", "Sleep Aid", "5mg"),
        ("Propranolol", "Beta Blocker", "10mg")
    ]

    for name, category, dosage in medications:
        create_medication(name, category, dosage)

    # Link medications to symptoms
    medication_symptoms = {
        "Sertraline": ["Panic Attacks", "Low Energy"],
        "Alprazolam": ["Panic Attacks", "Racing Thoughts"],
        "Melatonin": ["Insomnia"],
        "Propranolol": ["Racing Thoughts"]
    }

    for medication, symptom_list in medication_symptoms.items():
        for symptom in symptom_list:
            link_medication_to_symptom(medication, symptom)

    print("Database initialized with comprehensive mental health relationships")
