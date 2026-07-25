import os
import sqlite3

DATABASE = "database/database.db"


# ----------------------------
# Database Connection
# ----------------------------

def get_connection():
    db_dir = os.path.dirname(DATABASE)
    if db_dir:
        os.makedirs(db_dir, exist_ok=True)
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# ----------------------------
# Initialize Database
# ----------------------------

def init_db():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS quiz_history (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        subject TEXT NOT NULL,

        topic TEXT,

        difficulty TEXT,

        exam_type TEXT,

        total_questions INTEGER,

        score INTEGER DEFAULT 0,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )
    """)

    conn.commit()
    conn.close()


# ----------------------------
# Save Quiz
# ----------------------------

def save_quiz(
    subject,
    topic,
    difficulty,
    exam_type,
    total_questions
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""

    INSERT INTO quiz_history
    (
        subject,
        topic,
        difficulty,
        exam_type,
        total_questions
    )

    VALUES (?, ?, ?, ?, ?)

    """, (

        subject,
        topic,
        difficulty,
        exam_type,
        total_questions

    ))

    quiz_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return quiz_id


# ----------------------------
# Update Quiz Score
# ----------------------------

def update_score(
    quiz_id,
    score
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""

    UPDATE quiz_history

    SET score = ?

    WHERE id = ?

    """, (

        score,
        quiz_id

    ))

    conn.commit()
    conn.close()


# ----------------------------
# Get Full History
# ----------------------------

def get_history():

    conn = get_connection()

    quizzes = conn.execute("""

    SELECT *

    FROM quiz_history

    ORDER BY id DESC

    """).fetchall()

    conn.close()

    return quizzes


# ----------------------------
# Dashboard Statistics
# ----------------------------

def get_dashboard_stats():

    conn = get_connection()

    cursor = conn.cursor()

    # Total Quizzes
    cursor.execute("""

    SELECT COUNT(*)

    FROM quiz_history

    """)

    total_quizzes = cursor.fetchone()[0]


    # Total Questions
    cursor.execute("""

    SELECT IFNULL(SUM(total_questions),0)

    FROM quiz_history

    """)

    total_questions = cursor.fetchone()[0]


    # Average Percentage
    cursor.execute("""

    SELECT
    IFNULL(
        AVG(
            CAST(score AS FLOAT)
            /
            total_questions
            *100
        ),
    0)

    FROM quiz_history

    WHERE total_questions>0

    """)

    average_score = round(cursor.fetchone()[0],2)


    # Best Score
    cursor.execute("""

    SELECT IFNULL(MAX(score),0)

    FROM quiz_history

    """)

    best_score = cursor.fetchone()[0]


    # Recent Quizzes
    cursor.execute("""

    SELECT *

    FROM quiz_history

    ORDER BY id DESC

    LIMIT 5

    """)

    recent_quizzes = cursor.fetchall()

    conn.close()

    return {

        "total_quizzes": total_quizzes,

        "total_questions": total_questions,

        "average_score": average_score,

        "best_score": best_score,

        "recent_quizzes": recent_quizzes

    }


# ----------------------------
# Delete Quiz
# ----------------------------

def delete_quiz(quiz_id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

    DELETE FROM quiz_history

    WHERE id = ?

    """, (quiz_id,))

    conn.commit()

    conn.close()


# ----------------------------
# Clear History
# ----------------------------

def clear_history():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

    DELETE FROM quiz_history

    """)

    conn.commit()

    conn.close()