import groq
import os
import json
import re
from dotenv import load_dotenv

load_dotenv()

client = groq.Groq(api_key=os.getenv("GROQ_API_KEY"))

def analyze_with_llm(report_text: str) -> str:
    prompt = f"""
    Analyze this medical report and return ONLY a valid JSON object. 
    No explanation, no markdown, no code blocks. Just raw JSON.
    
    Return exactly this structure:
    {{
        "summary": "2-3 line simple summary of overall health",
        "conditions": ["condition1", "condition2"],
        "abnormal_values": {{"test_name": "value - reason why abnormal"}},
        "recommendations": ["recommendation1", "recommendation2"],
        "see_doctor": true
    }}
    
    Medical Report:
    {report_text[:3000]}
    """
    
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}]
        )
        raw = response.choices[0].message.content
        
        
        match = re.search(r'\{.*\}', raw, re.DOTALL)
        if match:
            return match.group()
        
        return raw
        
    except Exception as e:
        raise Exception(f"LLM analysis failed: {str(e)}")