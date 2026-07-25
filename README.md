# 🤖 QuizMind AI — AI-Powered MCQ Generator

QuizMind AI is an intelligent web application built with **Flask** and **Google Gemini 2.5 Flash** that automatically generates multiple-choice questions (MCQs) from topics, text notes, or uploaded documents (PDF, DOCX, PPTX). Features include interactive quiz taking, score analytics, downloadable PDF reports, and history tracking.

---

## ✨ Features

- 🎯 **Multiple Generation Modes**:
  - **Topic-Based**: Enter any subject & topic (e.g. *Operating Systems - Paging*).
  - **Text / Notes Input**: Paste raw study notes or chapter summaries.
  - **Document Upload**: Upload PDF, Word (.docx), or PowerPoint (.pptx) documents to extract content automatically.
- ⚙️ **Customizable Parameters**: Select difficulty level (Easy, Medium, Hard), exam type (School, University, Competitive Exam), and number of questions.
- 📝 **Interactive Quiz Mode**: Test your knowledge with real-time scoring, detailed explanations, and review.
- 📄 **Export to PDF**: Generate clean, formatted PDF question papers complete with answer keys and explanations.
- 📊 **Analytics Dashboard**: Track total quizzes taken, questions solved, average score, and top performance metrics.
- 📜 **Quiz History**: View, review, or clear past quiz records stored in a local SQLite database.

---

## 🛠️ Tech Stack

- **Backend**: Python, Flask, SQLite
- **AI Engine**: Google Gemini API (`google-genai` SDK)
- **Document Processing**: `pypdf`, `python-docx`, `python-pptx`
- **PDF Generation**: `reportlab`
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5

---

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.9 or higher
- A Google Gemini API Key (Get one from [Google AI Studio](https://aistudio.google.com/))

### 2. Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/NarottamKumar01/QuizMind-AI.git
   cd QuizMind-AI
   ```

2. **Create and activate a virtual environment**:
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS / Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up Environment Variables**:
   Create a `.env` file in the root directory:
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   SECRET_KEY=your_flask_secret_key_here
   ```

5. **Run the Application**:
   ```bash
   python app.py
   ```
   Open your browser and navigate to `http://127.0.0.1:5000`.

---

## 📂 Project Structure

```
QuizMind-AI/
├── app.py                  # Main Flask Application & Routes
├── config.py               # Application Configurations
├── requirements.txt        # Project Dependencies
├── database/
│   └── db.py               # SQLite Database Handler
├── utils/
│   ├── ai.py               # Gemini API Integration
│   ├── document_reader.py  # PDF, DOCX, PPTX Reader Utilities
│   └── pdf_generator.py    # ReportLab PDF Export Utility
├── templates/              # HTML Templates (Bootstrap 5)
│   ├── index.html
│   ├── quiz.html
│   ├── result.html
│   ├── score.html
│   ├── history.html
│   ├── dashboard.html
│   └── 404.html
└── LICENSE
```

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
