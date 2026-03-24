from flask import Flask, render_template, request, send_file
import os
import pandas as pd
import PyPDF2
import docx2txt
from sklearn.metrics.pairwise import cosine_similarity
import io
from werkzeug.utils import secure_filename

# PDF
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# ---------------- IMPORTANT ---------------- #
# DO NOT LOAD MODEL AT START
model = None

# ---------------- FAST ROOT (CRITICAL FOR RENDER) ---------------- #

@app.route("/")
def root():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    ...

@app.route("/health")
def health():
    return "OK"

# ---------------- SKILLS ---------------- #

SKILLS_DB = [
    "python", "java", "c++", "machine learning", "deep learning",
    "nlp", "data science", "flask", "django", "react", "node.js",
    "sql", "mongodb", "html", "css", "javascript", "tensorflow",
    "pytorch", "pandas", "numpy", "git", "aws", "docker"
]

leaderboard_data = pd.DataFrame()

def extract_skills(text):
    text = text.lower()
    return list(set([skill for skill in SKILLS_DB if skill in text]))

# ---------------- ATS ---------------- #

def calculate_ats_score(text, jd_skills):
    text_lower = text.lower()
    score = 0

    if len(text) > 1000:
        score += 0.2

    resume_skills = extract_skills(text)
    if jd_skills:
        score += 0.4 * (len(set(resume_skills) & set(jd_skills)) / len(jd_skills))

    sections = ["education", "experience", "project", "skills"]
    section_count = sum([1 for sec in sections if sec in text_lower])
    score += 0.4 * (section_count / len(sections))

    return round(score, 2)

# ---------------- AI SUGGESTIONS ---------------- #

def generate_suggestions(missing_skills, score):
    suggestions = []

    if missing_skills:
        suggestions.append("Learn: " + ", ".join(missing_skills[:3]))

    if score < 0.5:
        suggestions.append("Improve projects & resume content")

    if score < 0.3:
        suggestions.append("Add proper resume sections")

    if not suggestions:
        suggestions.append("Strong profile 👍")

    return " | ".join(suggestions)

# ---------------- FILE READING ---------------- #

def extract_text_from_pdf(pdf_path):
    text = ""
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                if page.extract_text():
                    text += page.extract_text()
    except Exception as e:
        print(e)
    return text

def extract_text_from_docx(docx_path):
    try:
        return docx2txt.process(docx_path)
    except:
        return ""

# ---------------- MAIN APP ---------------- #

@app.route("/analyze", methods=["GET", "POST"])
def home():
    global leaderboard_data, model

    if request.method == "POST":

        # ✅ LOAD MODEL ONLY HERE (FIX)
        if model is None:
            from sentence_transformers import SentenceTransformer
            model = SentenceTransformer('all-MiniLM-L6-v2')

        job_description = request.form["job_description"]
        uploaded_files = request.files.getlist("resumes")

        resume_texts = []
        resume_names = []

        for i, file in enumerate(uploaded_files):
            filename = f"{i+1}_{secure_filename(file.filename)}"
            path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(path)

            resume_names.append(filename)

            if filename.endswith(".pdf"):
                text = extract_text_from_pdf(path)
            elif filename.endswith(".docx"):
                text = extract_text_from_docx(path)
            else:
                continue

            resume_texts.append(text)

        if not resume_texts:
            return render_template("index.html", error="Upload valid files")

        job_embedding = model.encode([job_description])
        resume_embeddings = model.encode(resume_texts)
        similarity_scores = cosine_similarity(job_embedding, resume_embeddings)[0]

        jd_skills = extract_skills(job_description)

        matched_skills_list = []
        missing_skills_list = []
        ats_scores = []
        final_scores = []
        status_list = []
        suggestions_list = []

        for i, text in enumerate(resume_texts):
            resume_skills = extract_skills(text)

            matched = list(set(jd_skills) & set(resume_skills))
            missing = list(set(jd_skills) - set(resume_skills))

            matched_skills_list.append(", ".join(matched))
            missing_skills_list.append(", ".join(missing))

            ats = calculate_ats_score(text, jd_skills)
            ats_scores.append(ats)

            final = round(0.7 * similarity_scores[i] + 0.3 * ats, 2)
            final_scores.append(final)

            if final >= 0.7:
                status_list.append("Shortlisted")
            elif final >= 0.4:
                status_list.append("Review")
            else:
                status_list.append("Rejected")

            suggestions_list.append(generate_suggestions(missing, final))

        leaderboard_data = pd.DataFrame({
            "Candidate": resume_names,
            "AI_Score": similarity_scores,
            "ATS_Score": ats_scores,
            "Final_Score": final_scores,
            "Status": status_list,
            "Matched Skills": matched_skills_list,
            "Missing Skills": missing_skills_list,
            "Suggestions": suggestions_list
        }).sort_values(by="Final_Score", ascending=False).reset_index(drop=True)

        leaderboard_data["Rank"] = leaderboard_data.index + 1

        top = leaderboard_data.head(5)

        return render_template(
            "leaderboard.html",
            leaderboard=leaderboard_data.to_dict(orient="records"),
            chart_labels=top["Candidate"].tolist(),
            chart_scores=top["Final_Score"].tolist()
        )

    return render_template("index.html")

# ---------------- PDF ---------------- #

@app.route("/download")
def download():
    global leaderboard_data

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer)

    data = [["Rank", "Candidate", "Final Score", "Status"]]

    for _, row in leaderboard_data.iterrows():
        data.append([
            row["Rank"],
            row["Candidate"],
            round(row["Final_Score"], 2),
            row["Status"]
        ])

    table = Table(data)

    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 1, colors.black)
    ]))

    doc.build([table])
    buffer.seek(0)

    return send_file(buffer, as_attachment=True,
                     download_name="Screenly_Report.pdf",
                     mimetype="application/pdf")

# ---------------- RUN ---------------- #

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)