# score.py
from fastapi import APIRouter
from decimal import Decimal, ROUND_HALF_UP
from model import StudentRequest, StudentResponse
from typing import List

score_router = APIRouter()

GRADE_POINTS = {
    'A+': Decimal('4.5'),
    'A0': Decimal('4.0'),
    'B+': Decimal('3.5'),
    'B0': Decimal('3.0'),
    'C+': Decimal('2.5'),
    'C0': Decimal('2.0'),
    'F': Decimal('0.0'),
}

@score_router.post("/student_summary", response_model=StudentResponse)
async def summarize(request: StudentRequest):
    total_credits = sum(c.credits for c in request.courses)
    weighted_sum = sum(
        Decimal(c.credits) * GRADE_POINTS.get(c.grade, Decimal('0.0'))
        for c in request.courses
    )
    if total_credits == 0:
        gpa = Decimal('0.00')
    else:
        raw = weighted_sum / Decimal(total_credits)
        gpa = raw.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    return {
        "student_summary": {
            "student_id": request.student_id,
            "name":       request.name,
            "gpa":        float(gpa),
            "total_credits": total_credits
        }
    }

# 선택: 과거 저장된 점수를 보여주는 GET 핸들러
score_list: List[dict] = []

@score_router.get("/student_summary")
async def retrieve_scores():
    return { "scores": score_list }
