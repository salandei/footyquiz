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

def db_conn_close():
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# return the results from a database query
def db_query(query, args=()):
    conn = get_db()
    cursor = conn.execute(query, args)
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

def add_player(player_name, score):
    # Usernames must be unique. Prevent adding an already existing username
    try:
        db_execute("INSERT INTO players (name, score) VALUES (:name, :score)", {
            "name": player_name,
            "score": score,
        })
        return True
    except sqlite3.IntegrityError:
        return False

def update_player_score(player_name, score):
    db_execute("UPDATE players SET score = :score WHERE name = :name", {
        "name": player_name,
        "score": score,
    })

def get_questions():
    q_and_a =  db_query("SELECT * FROM q_and_a")
    questions = []
    answers = []
    for q_and_a_item in q_and_a:
        questions.append(q_and_a_item[0])
        answers.append(q_and_a_item[1].split(":"))
    return (questions, answers)

def get_correct_answers():
    query_results =  db_query("SELECT correct_answer FROM q_and_a")
    correct_answers = []
    for correct_answer in query_results:
        correct_answers.append(correct_answer[0])
    return correct_answers

def get_leaderboard():
    return db_query("SELECT * FROM players ORDER BY score DESC")


# Close the database connection when the app shuts down
@app.teardown_appcontext
def close_db_connection(exception):
    db_conn_close()


##################
# Main App Routes
##################

@app.get("/")
def index():
    return render_template("index.html")

@app.get("/leaderboard")
def show_leaderboard():
    query_result = get_leaderboard()
    leaderboard = []
    for row in query_result:
        player_name = row[0]
        player_score = row[1]
        leaderboard.append((player_name, player_score))
    return render_template('leaderboard.html', leaderboard=leaderboard)

@app.post("/quiz")
def quiz():
    username = request.form['username']
    if not add_player(username, 0):
        return render_template('index.html', duplicate_username=True)

    query_result = get_questions()
    db_conn_close()

    return render_template('quiz.html', questions=query_result[0], answers=query_result[1], num_of_questions=len(query_result[0]), username=username)

@app.post("/score/<username>")
def score(username):
    correct_answers = get_correct_answers()

    player_score = 0
    for i in range(1, len(correct_answers)+1):
        player_choice = request.form[str(i)]

        if player_choice == correct_answers[i-1]:
            player_score += 1
    update_player_score(username, player_score)

    db_conn_close

    return render_template('score.html', score=player_score, number_of_questions=len(correct_answers))


##################
# ADMIN FUNCTIONS
##################

@app.get("/admin/clean_db")
def clean_table_players():
    db_execute("DELETE FROM players")
    query_result = db_query("SELECT * FROM players")
    db_conn_close()
    if query_result == None:
        return "Database table (players) cleaned!"
    



