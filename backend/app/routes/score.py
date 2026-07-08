from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.commit import Commit
from app.models.developer_score import DeveloperScore
from app.models.language import Language
from app.models.repository import Repository
from app.models.user import User

router = APIRouter()


@router.post("/score/{user_id}")
def compute_score(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    repo_ids = [
        r.id for r in db.query(Repository).filter(Repository.user_id == user_id).all()
    ]
    if not repo_ids:
        raise HTTPException(
            status_code=400,
            detail="No repositories found — run /sync/repositories first.",
        )

    # --- Activity: total commit count, capped at 100 commits = full score ---
    total_commits = db.query(Commit).filter(Commit.repository_id.in_(repo_ids)).count()
    activity_score = min(total_commits / 100, 1.0) * 100

    # --- Consistency: distinct days with a commit in the last 90 days, capped at 30 days = full score ---
    ninety_days_ago = datetime.utcnow() - timedelta(days=90)
    distinct_days = (
        db.query(func.date(Commit.committed_at))
        .filter(
            Commit.repository_id.in_(repo_ids), Commit.committed_at >= ninety_days_ago
        )
        .distinct()
        .count()
    )
    consistency_score = min(distinct_days / 30, 1.0) * 100

    # --- Growth: stars + forks across all repos, capped at 50 = full score ---
    growth_raw = (
        db.query(
            func.coalesce(func.sum(Repository.stars), 0)
            + func.coalesce(func.sum(Repository.forks), 0)
        )
        .filter(Repository.user_id == user_id)
        .scalar()
    )
    growth_score = min(growth_raw / 50, 1.0) * 100

    # --- Diversity: distinct languages used, capped at 5 languages = full score ---
    distinct_languages = (
        db.query(Language.language)
        .filter(Language.repository_id.in_(repo_ids))
        .distinct()
        .count()
    )
    diversity_score = min(distinct_languages / 5, 1.0) * 100

    # --- Weighted final score ---
    final_score = (
        activity_score * 0.35
        + consistency_score * 0.35
        + growth_score * 0.10
        + diversity_score * 0.20
    )

    breakdown = {
        "activity": round(activity_score, 1),
        "consistency": round(consistency_score, 1),
        "growth": round(growth_score, 1),
        "diversity": round(diversity_score, 1),
        "weights": {
            "activity": 0.35,
            "consistency": 0.35,
            "growth": 0.10,
            "diversity": 0.20,
        },
    }

    score_entry = DeveloperScore(
        user_id=user_id,
        score=round(final_score, 2),
        breakdown_json=breakdown,
    )
    db.add(score_entry)
    db.commit()

    return {
        "status": "computed",
        "score": round(final_score, 2),
        "breakdown": breakdown,
    }
