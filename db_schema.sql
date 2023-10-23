CREATE TABLE IF NOT EXISTS players(
	name VARCHAR(255) NOT NULL UNIQUE,
	score INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS q_and_a(
	question TEXT NOT NULL UNIQUE,
	answers TEXT NOT NULL,
	correct_answer TEXT NOT NULL
)