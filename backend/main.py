from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from services.pdf_parser import extract_text_from_pdf
from services.llm import analyze_with_llm
from services.analyzer import detect_conditions, calculate_risk_score
import json
import os
import re

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze")
async def analyze_report(file: UploadFile = File(...)):
    try:
        file_bytes = await file.read()
        report_text = extract_text_from_pdf(file_bytes)

        if not report_text.strip():
            return {"error": "Could not extract text from PDF. It may be a scanned image."}

        llm_response = analyze_with_llm(report_text)

        try:
            clean = llm_response.strip()
            clean = re.sub(r'```json|```', '', clean).strip()
            result = json.loads(clean)
        except json.JSONDecodeError as e:
            return {"error": f"Parse error: {str(e)}", "raw": llm_response}

        abnormal_count = len(result.get("abnormal_values", {}))
        conditions = result.get("conditions", [])
        risk_score = calculate_risk_score(abnormal_count, conditions)
        result["risk_score"] = risk_score

        return result

    except Exception as e:
        return {"error": str(e)}