# 🏥 Medical Report Analyzer AI

An AI-powered application that analyzes medical report PDFs and turns them into simple, easy-to-understand health insights using Large Language Models (LLMs) and NLP-based analysis.

> ⚠️ **Educational use only.** This project does not provide medical advice, diagnosis, or treatment. See the [Disclaimer](#-disclaimer).

---

## 📑 Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [How It Works](#-how-it-works)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
- [Usage](#-usage)
- [API Reference](#-api-reference)
- [Limitations](#-limitations)
- [Privacy & Security](#-privacy--security)
- [Roadmap](#-roadmap)
- [Contributing](#-contributing)
- [License](#-license)
- [Disclaimer](#-disclaimer)

---

## ✨ Features

- 📄 **PDF upload**: upload medical reports (blood tests, lipid profiles, etc.) in PDF format
- 🔍 **Text extraction**: pull text and tables from reports using `pdfplumber`
- 🤖 **LLM analysis**: interpret report contents in plain language
- 🚨 **Abnormal value detection**: flag results outside standard reference ranges
- 🩺 **Possible condition insights**: highlight health conditions the values may be associated with
- 📊 **Health risk score**: get an overall, easy-to-read risk indicator
- 📝 **Summary & recommendations**: receive an AI-generated summary and general lifestyle suggestions

---

## 🛠 Tech Stack

| Layer | Technology |
|-------|------------|
| Language | Python 3.10+ |
| Frontend | Streamlit |
| Backend API | FastAPI |
| PDF parsing | pdfplumber |
| AI / NLP | Large Language Models (LLMs), NLP-based analysis |

---

## ⚙️ How It Works

```
┌──────────┐   PDF   ┌───────────┐  text  ┌──────────────┐  prompt  ┌─────┐
│ Streamlit│ ──────▶ │  FastAPI  │ ─────▶ │ Preprocessing │ ──────▶ │ LLM │
│    UI    │         │  backend  │        │ & extraction  │         └──┬──┘
└────▲─────┘         └───────────┘        └──────────────┘            │
     │                                                                 │
     └──────── summary · abnormalities · risk score · tips ◀───────────┘
```

1. The user uploads a medical report PDF through the Streamlit interface.
2. The FastAPI backend extracts text and tables using `pdfplumber`.
3. Extracted values are cleaned, structured, and compared against reference ranges.
4. The data is sent to an LLM for interpretation.
5. The app displays a summary, flagged abnormalities, possible conditions, a risk score, and recommendations.

---

## 📁 Project Structure

```
medical-report-analyzer/
├── backend/
│   ├── services/
│   │   ├── analyzer.py    # Abnormal value detection, risk score & analysis logic
│   │   ├── llm.py         # LLM client and prompt handling
│   │   └── pdf_parser.py  # PDF text extraction (pdfplumber)
│   └── main.py            # FastAPI entry point
├── frontend/
│   └── app.py             # Streamlit user interface
├── .gitignore
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10 or higher
- An API key for your chosen LLM provider

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/<your-username>/medical-report-analyzer.git
cd medical-report-analyzer

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install fastapi uvicorn streamlit pdfplumber python-multipart requests python-dotenv
# Also install the SDK for your LLM provider (e.g., openai, google-generativeai)
```

> 💡 Tip: run `pip freeze > requirements.txt` once everything works, so others can install with `pip install -r requirements.txt`.

### Configuration

Create a `.env` file in the project root:

```env
LLM_API_KEY=your_api_key_here
LLM_MODEL=your_model_name
BACKEND_URL=http://localhost:8000
```

---

## ▶️ Usage

Start the backend (from the project root):

```bash
uvicorn backend.main:app --reload --port 8000
```

In a second terminal, start the frontend:

```bash
streamlit run frontend/app.py
```

Then open **http://localhost:8501**, upload a PDF report, and click **Analyze**.

---

## 🔌 API Reference

Interactive docs are available at `http://localhost:8000/docs` when the backend is running.

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/analyze` | Upload a PDF and receive the full analysis |
| `GET`  | `/health`  | Check that the API is running |

**Example request**

```bash
curl -X POST "http://localhost:8000/analyze" \
  -F "file=@sample_report.pdf"
```

**Example response**

```json
{
  "summary": "Most values are within range. Cholesterol is mildly elevated.",
  "abnormal_values": [
    { "test": "Total Cholesterol", "value": 235, "unit": "mg/dL", "reference": "< 200", "status": "High" }
  ],
  "possible_conditions": ["Elevated cardiovascular risk"],
  "risk_score": 42,
  "recommendations": [
    "Consider reducing saturated fat intake",
    "Discuss these results with your doctor"
  ]
}
```

---

## ⚠️ Limitations

- Accuracy depends on PDF quality. **Scanned or image-based PDFs** may not extract correctly without OCR.
- Reference ranges vary by lab, age, sex, and region; the app may not always apply the right one.
- LLMs can make mistakes or "hallucinate"; always verify results with a qualified professional.
- The risk score is an **illustrative estimate**, not a clinical measurement.

---

## 🔒 Privacy & Security

Medical data is sensitive. If you deploy or extend this project:

- Do **not** commit real patient reports to the repository.
- Avoid logging extracted report text.
- Be aware that report content is sent to the configured LLM provider; review their data-handling policy.
- Use HTTPS and access controls in any shared deployment.
- Consider compliance requirements (e.g., HIPAA, GDPR) before handling real patient data.

---

## 🗺 Roadmap

- [ ] OCR support for scanned reports
- [ ] Support for more report types (imaging, pathology, discharge summaries)
- [ ] Trend tracking across multiple reports
- [ ] Multi-language support
- [ ] Export analysis as PDF
- [ ] Unit tests and CI pipeline
- [ ] Docker setup

---

## 🤝 Contributing

Contributions are welcome!

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m "Add your feature"`
4. Push the branch: `git push origin feature/your-feature`
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## 📢 Disclaimer

This application provides AI-generated insights for **educational purposes only** and is **not a substitute for professional medical advice, diagnosis, or treatment**. Always seek the advice of a qualified healthcare provider with any questions about a medical condition. Never disregard professional medical advice or delay seeking it because of information from this application.
