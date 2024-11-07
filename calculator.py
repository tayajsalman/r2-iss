from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class CalculatorResults:
    iss_stage: str
    iss_points: float
    ldh_points: float
    cytogenetic_points: float
    total_points: float
    r2_iss_stage: str
    breakdown_messages: List[str]

def calculate_iss_stage(b2m: str, albumin: str) -> Tuple[str, float]:
    if b2m == "< 3.5 mg/L" and albumin == "≥ 3.5 g/dL":
        return "I", 0.0
    elif b2m == "≥ 5.5 mg/L":
        return "III", 1.5
    else:
        return "II", 1.0

def calculate_ldh_points(ldh: str) -> float:
    if ldh == "Normal (< 240 U/L)":
        return 0.0
    else:
        return 1.0

def calculate_cytogenetic_points(del17p: bool, t414: bool, gain1q: bool) -> float:
    points = 0.0
    if del17p:
        points += 1.0
    if t414:
        points += 1.0
    if gain1q:
        points += 0.5
    return points

def determine_r2_iss_stage(total_points: float) -> str:
    if total_points == 0:
        return "R2-ISS I (Low Risk)"
    elif 0.5 <= total_points <= 1.0:
        return "R2-ISS II (Low-Intermediate Risk)"
    elif 1.5 <= total_points <= 2.5:
        return "R2-ISS III (Intermediate-High Risk)"
    else:
        return "R2-ISS IV (High Risk)"

def generate_breakdown(iss_stage: str, iss_points: float, ldh: str, ldh_points: float,
                      del17p: bool, t414: bool, gain1q: bool) -> List[str]:
    messages = []
    
    if iss_stage == "I":
        messages.append("ISS Stage I: 0 points (β2M < 3.5 mg/L and Albumin ≥ 3.5 g/dL)")
    elif iss_stage == "II":
        messages.append("ISS Stage II: 1 point")
    else:
        messages.append("ISS Stage III: 1.5 points (β2M ≥ 5.5 mg/L)")
    
    if ldh == "Normal (< 240 U/L)":
        messages.append("LDH Normal: 0 points")
    else:
        messages.append("LDH Elevated: Added 1 point")
    
    if del17p:
        messages.append("High-risk cytogenetics - del(17p): Added 1 point")
    if t414:
        messages.append("High-risk cytogenetics - t(4;14): Added 1 point")
    if gain1q:
        messages.append("High-risk cytogenetics - 1q gain: Added 0.5 points")
    
    return messages

def calculate_r2_iss(b2m: str, albumin: str, ldh: str, 
                     del17p: bool, t414: bool, gain1q: bool) -> CalculatorResults:
    iss_stage, iss_points = calculate_iss_stage(b2m, albumin)
    ldh_points = calculate_ldh_points(ldh)
    cytogenetic_points = calculate_cytogenetic_points(del17p, t414, gain1q)
    total_points = iss_points + ldh_points + cytogenetic_points
    r2_iss_stage = determine_r2_iss_stage(total_points)
    breakdown = generate_breakdown(iss_stage, iss_points, ldh, ldh_points,
                                 del17p, t414, gain1q)
    
    return CalculatorResults(
        iss_stage=iss_stage,
        iss_points=iss_points,
        ldh_points=ldh_points,
        cytogenetic_points=cytogenetic_points,
        total_points=total_points,
        r2_iss_stage=r2_iss_stage,
        breakdown_messages=breakdown
    ) 
