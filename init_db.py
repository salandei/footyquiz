import sqlite3

connection = sqlite3.connect('database.db')

print("Initializing db...")
with open('db_schema.sql') as f:
    connection.executescript(f.read())
    
connection.commit()
print("DONE!")

import json

print("Inserting questions...")

query = "INSERT INTO q_and_a (question, answers, correct_answer) VALUES (:question, :answers, :correct_answer)"
questions = dict()
with open("questions.json", "r") as question_file:
    questions = json.load(question_file)
for data in questions.values():
    args = {
        "question": data["question"],
        "answers": data["answers"],
        "correct_answer": data["correct_answer"]
    }
    connection.execute(query, args)

connection.commit()
connection.close()

print("Inserting questions...DONE!")