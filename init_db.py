import sqlite3
import json
import os.path as filepath

DATABASE = 'database.db'
QUESTIONS = 'questions.json'
    
###############################
# POPULATE DB QUESTIONS TABLE
###############################
def add_questions_db(json_file):    
    print("Inserting questions...")

    query = "INSERT INTO q_and_a (question, answers, correct_answer) VALUES (:question, :answers, :correct_answer)"
    questions = dict()
    with open(json_file, "r") as question_file:
        questions = json.load(question_file)

    for data in questions.values():
        args = {
            "question": data["question"],
            "answers": data["answers"],
            "correct_answer": data["correct_answer"]
        }
        connection.execute(query, args)
    connection.commit()

    print("Inserting questions...DONE!")

#############################
# INITIALIZE THE DATABASE
#############################
def initialize_db():
    print("Initializing db...")
    with open('db_schema.sql') as f:
        connection.executescript(f.read())       
    connection.commit()

if __name__ == "__main__":
    # Create database file and connect to it for initialization
    if(not filepath.exists(DATABASE)):
        if(open(DATABASE, "x")):
            connection = sqlite3.connect('database.db')
            initialize_db()
            add_questions_db(QUESTIONS)
            connection.close()