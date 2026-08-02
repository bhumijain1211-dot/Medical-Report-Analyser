def detect_conditions(parameters: dict) -> list:
    conditions = []
    
    hb = parameters.get("hemoglobin")
    hba1c = parameters.get("hba1c")
    wbc = parameters.get("wbc")
    ldl = parameters.get("ldl")
    
    if hb and float(hb) < 12:
        conditions.append("Anemia")
    if hba1c and float(hba1c) > 6.5:
        conditions.append("Diabetes")
    if wbc and float(wbc) > 11000:
        conditions.append("Possible Infection")
    if ldl and float(ldl) > 160:
        conditions.append("High Cholesterol")
        
    return conditions

def calculate_risk_score(abnormal_count: int, conditions: list) -> int:
    score = 0
    score += abnormal_count * 10
    score += len(conditions) * 15
    return min(score, 100)