from flask import Flask, g, render_template, request
import sqlite3

app = Flask(__name__)

##################
# Database helpers
##################
DATABASE_FILE = 'database.db'

# Get a useable connection to the database
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE_FILE)
        db.row_factory = sqlite3.Row
    return db

# return the results from a database query
def db_query(query, args=()):
    cursor = get_db().execute(query, args)
    results = cursor.fetchall()
    cursor.close()
    if results:
        return results
    return None

# execute a statement on the database
def db_execute(query, args=()):
    conn = get_db()
    conn.execute(query, args)
    conn.commit()
    conn.close()

def add_player(player_name, score):
    db_execute("INSERT INTO players (name, score) VALUES (:name, :score)", {
        "name": player_name,
        "score": score,
    })

def get_leaderboard():
    return db_query("SELECT * FROM q_and_a")


# Close the database connection when the app shuts down
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


##################
# Main App Routes
##################

@app.get("/")
def index():
    return render_template("index.html")

@app.post("/quiz")
def quiz():
    username = request.form['username']
    db_rows = get_leaderboard()
    questions = []
    answers = []
    for q_and_a_item in db_rows:
        questions.append(q_and_a_item[0])
        answers.append(q_and_a_item[1].split(":"))
    return render_template('quiz.html', questions=questions, answers=answers, num_of_questions=len(questions), username=username)

@app.post("/score/<username>")
def score(username):
    player_choices = []
    for i in range(1, 11):
        player_choices.append(request.form[str(i)])
    return player_choices



