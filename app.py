@app.route("/analyze", methods=["GET", "POST"])
def analyze():
    global leaderboard_data, model

    # 🚨 HANDLE GET REQUEST (VERY IMPORTANT)
    if request.method == "GET":
        return render_template("index.html")

    # 🚨 LOAD MODEL ASYNC (CRITICAL FIX)
    if model is None:
        from sentence_transformers import SentenceTransformer
        import threading

        def load_model():
            global model
            model = SentenceTransformer('all-MiniLM-L6-v2')

        threading.Thread(target=load_model).start()

        return render_template("index.html",
            error="⏳ Model loading first time... please wait 20 seconds and try again")

    # ---------------- NORMAL FLOW ---------------- #

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

    # -------- AI SCORING -------- #
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
            status = "Shortlisted"
        elif final >= 0.4:
            status = "Review"
        else:
            status = "Rejected"

        status_list.append(status)
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