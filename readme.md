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

> <img width="1114" height="736" alt="image" src="https://github.com/user-attachments/assets/322667e1-faff-4d85-9daa-64d0ce7f5fab" />
> <img width="1806" height="852" alt="image" src="https://github.com/user-attachments/assets/9e6e5c6a-f42e-4216-9c01-bfddc8a23261" />
> <img width="1795" height="506" alt="image" src="https://github.com/user-attachments/assets/b8493d24-36ab-40b0-a65f-5ae6c6587778" />




---

## 🚀 Run Locally

```bash
git clone https://github.com/Saksham/screenly-ai.git
cd screenly-ai

pip install -r requirements.txt
python app.py
```

---

## 🌐 Deployment

Deployed using **Render**
👉 (Add your live link here after deployment)

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
