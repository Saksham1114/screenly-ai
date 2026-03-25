#  Screenly – AI Resume Screener & ATS Analyzer

An AI-powered web application that analyzes resumes, ranks candidates, and provides intelligent feedback using NLP and ATS-based scoring.

---

## 🌟 Features

* 🤖 **AI Resume Matching (SBERT)**
* 📊 **Hybrid Scoring System (AI + ATS)**
* 🎯 **Shortlisting System (Shortlisted / Review / Rejected)**
* 🧠 **Skill Gap Analysis**
* 💡 **AI Suggestions for Improvement**
* 📈 **Interactive Dashboard with Charts**
* 📄 **PDF Report Generation**

---

## 🛠️ Tech Stack

* **Backend:** Flask (Python)
* **AI/NLP:** Sentence Transformers (SBERT)
* **ML:** Scikit-learn (Cosine Similarity)
* **Frontend:** HTML, CSS, Chart.js
* **PDF:** ReportLab

---

## 🧠 How It Works

1. Upload resumes (PDF/DOCX)
2. Enter job description
3. System performs:

   * Semantic similarity (AI score)
   * ATS scoring (skills + structure)
4. Generates:

   * Final score (70% AI + 30% ATS)
   * Skill gap analysis
   * Improvement suggestions
5. Displays results in dashboard + downloadable report

---

## 📊 Scoring Logic

* **AI Score:** Semantic similarity using SBERT
* **ATS Score:** Based on:

  * Skill matching
  * Resume length
  * Section presence
* **Final Score:**

```
Final Score = 0.7 * AI Score + 0.3 * ATS Score
```

---

## 📸 Screenshots

> <img width="978" height="799" alt="Screenshot 2026-03-26 003058" src="https://github.com/user-attachments/assets/15896a29-c406-4399-9be4-43d225acb79f" />
> <img width="1829" height="648" alt="Screenshot 2026-03-26 003131" src="https://github.com/user-attachments/assets/f48342c6-614f-49f5-9022-38d098fe75d2" />
> <img width="1842" height="829" alt="Screenshot 2026-03-26 003140" src="https://github.com/user-attachments/assets/dad15225-e2af-40e9-927a-ea616214b24c" />




---

## 🚀 Run Locally

```bash
git clone https://github.com/Saksham/screenly-ai.git
cd screenly-ai

pip install -r requirements.txt
python app.py
```

---

## 🎯 Future Improvements

* 🧠 LLM-based resume suggestions
* 🔐 Authentication system
* 📊 Advanced analytics dashboard
* 🌍 Multi-language support

---

## 👨‍💻 Author

Saksham 

Computer Science Engineering Student

---

## ⭐ Show some love

If you like this project, give it a ⭐ on GitHub!
