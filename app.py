import os

from dotenv import load_dotenv

from flask import (
    Flask,
    render_template,
    request,
    session,
    send_file,
    redirect,
    url_for
)

from werkzeug.utils import secure_filename

from utils.ai import generate_mcqs
from utils.pdf_generator import create_pdf

from utils.document_reader import (
    extract_pdf,
    extract_docx,
    extract_pptx
)

from database.db import (
    init_db,
    save_quiz,
    update_score,
    get_history,
    get_dashboard_stats,
    delete_quiz,
    clear_history
)
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# ----------------------------
# Load Environment Variables
# ----------------------------

load_dotenv()

if not app.secret_key:
    app.secret_key = os.getenv("SECRET_KEY", "default-secret-key")

# ----------------------------
# Initialize Database
# ----------------------------

init_db()

# ----------------------------
# Upload & Export Folders
# ----------------------------

UPLOAD_FOLDER = Config.UPLOAD_FOLDER
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs("exports", exist_ok=True)

# ----------------------------
# Home
# ----------------------------

@app.route("/")
def home():
    return render_template("index.html")


# ----------------------------
# Generate MCQs
# ----------------------------

@app.route("/generate", methods=["POST"])
def generate():

    subject = request.form["subject"]

    topic = request.form.get("topic", "").strip()

    notes = request.form.get("notes", "").strip()

    difficulty = request.form["difficulty"]

    exam_type = request.form["exam_type"]

    num_questions = int(request.form["num_questions"])

    pdf_file = request.files.get("pdf_file")

    # ----------------------------
    # File Upload Mode
    # ----------------------------

    if pdf_file and pdf_file.filename != "":

        filename = secure_filename(pdf_file.filename)

        file_path = os.path.join(
            app.config["UPLOAD_FOLDER"],
            filename
        )

        pdf_file.save(file_path)

        extension = filename.lower().split(".")[-1]

        if extension == "pdf":

            document_text = extract_pdf(file_path)

        elif extension == "docx":

            document_text = extract_docx(file_path)

        elif extension == "pptx":

            document_text = extract_pptx(file_path)

        else:

            return "Unsupported File Type"

        mcqs = generate_mcqs(

            subject,

            document_text,

            difficulty,

            exam_type,

            num_questions

        )

    # ----------------------------
    # Paste Notes
    # ----------------------------

    elif notes:

        mcqs = generate_mcqs(

            subject,

            notes,

            difficulty,

            exam_type,

            num_questions

        )

    # ----------------------------
    # Topic Mode
    # ----------------------------

    else:

        mcqs = generate_mcqs(

            subject,

            topic,

            difficulty,

            exam_type,

            num_questions

        )

    # ----------------------------
    # Session
    # ----------------------------

    session["mcqs"] = mcqs

    session["subject"] = subject

    session["topic"] = topic

    session["difficulty"] = difficulty

    session["exam_type"] = exam_type

    quiz_id = save_quiz(

        subject,

        topic,

        difficulty,

        exam_type,

        num_questions

    )

    session["quiz_id"] = quiz_id

    return render_template(

        "result.html",

        subject=subject,

        topic=topic,

        difficulty=difficulty,

        exam_type=exam_type,

        mcqs=mcqs

    )


# ----------------------------
# Quiz Page
# ----------------------------

@app.route("/quiz")
def quiz():

    mcqs = session.get("mcqs")

    if not mcqs:

        return redirect(url_for("home"))

    return render_template(

        "quiz.html",

        mcqs=mcqs

    )


# ----------------------------
# Submit Quiz
# ----------------------------

@app.route("/submit-quiz", methods=["POST"])
def submit_quiz():

    mcqs = session.get("mcqs", [])

    score = 0

    results = []

    for index, mcq in enumerate(mcqs):

        selected_answer = request.form.get(f"q{index}")

        correct_answer = mcq["answer"]

        is_correct = selected_answer == correct_answer

        if is_correct:

            score += 1

        results.append({

            "question": mcq["question"],

            "selected_answer": selected_answer,

            "correct_answer": correct_answer,

            "is_correct": is_correct,

            "explanation": mcq["explanation"]

        })

    quiz_id = session.get("quiz_id")

    if quiz_id:

        update_score(

            quiz_id,

            score

        )

    return render_template(

        "score.html",

        score=score,

        total=len(mcqs),

        results=results

    )
# ----------------------------
# Download PDF
# ----------------------------

@app.route("/download-pdf")
def download_pdf():

    mcqs = session.get("mcqs")

    if not mcqs:

        return "No MCQs available."


    subject = session.get(
        "subject",
        "Generated MCQs"
    )

    topic = session.get(
        "topic",
        "Quiz"
    )


    filename = os.path.join(
    "exports",
    "MCQ_Report.pdf"
)


    create_pdf(

        filename,

        subject,

        topic,

        mcqs

    )


    return send_file(

        filename,

        as_attachment=True

    )



# ----------------------------
# Quiz History
# ----------------------------

@app.route("/history")
def history():

    quizzes = get_history()


    return render_template(

        "history.html",

        quizzes=quizzes

    )



# ----------------------------
# Dashboard
# ----------------------------

@app.route("/dashboard")
def dashboard():

    stats = get_dashboard_stats()


    return render_template(

        "dashboard.html",

        total_quizzes=stats["total_quizzes"],

        total_questions=stats["total_questions"],

        average_score=stats["average_score"],

        best_score=stats["best_score"],

        recent_quizzes=stats["recent_quizzes"]

    )



# ----------------------------
# Delete Single Quiz History
# ----------------------------

@app.route("/delete-quiz/<int:quiz_id>")
def delete_history_quiz(quiz_id):

    delete_quiz(quiz_id)


    return redirect(

        url_for("history")

    )



# ----------------------------
# Clear All History
# ----------------------------

@app.route("/clear-history")
def clear_all_history():

    clear_history()


    return redirect(

        url_for("history")

    )



# ----------------------------
# Error Handling
# ----------------------------

@app.errorhandler(404)
def page_not_found(error):

    return render_template(
        "404.html"
    ), 404



# ----------------------------
# Run Application
# ----------------------------

if __name__ == "__main__":

    app.run(

        debug=True

    )