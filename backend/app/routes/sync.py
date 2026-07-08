import httpx
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.repository import Repository
from app.models.user import User

router = APIRouter()


@router.post("/sync/repositories/{user_id}")
async def sync_repositories(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    synced_count = 0
    page = 1

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            while True:
                response = await client.get(
                    "https://api.github.com/user/repos",
                    headers={"Authorization": f"Bearer {user.access_token}"},
                    params={"per_page": 100, "page": page, "affiliation": "owner"},
                )

                if response.status_code != 200:
                    raise HTTPException(
                        status_code=502,
                        detail=f"GitHub API error while fetching repos: {response.text}",
                    )

                repos = response.json()

                if not repos:
                    break  # no more pages

                for repo in repos:
                    existing = (
                        db.query(Repository)
                        .filter(Repository.github_repo_id == repo["id"])
                        .first()
                    )

                    if existing:
                        existing.name = repo["name"]
                        existing.description = repo.get("description")
                        existing.primary_language = repo.get("language")
                        existing.stars = repo.get("stargazers_count", 0)
                        existing.forks = repo.get("forks_count", 0)
                        existing.is_fork = repo.get("fork", False)
                        existing.pushed_at = repo.get("pushed_at")
                    else:
                        new_repo = Repository(
                            user_id=user.id,
                            github_repo_id=repo["id"],
                            name=repo["name"],
                            description=repo.get("description"),
                            primary_language=repo.get("language"),
                            stars=repo.get("stargazers_count", 0),
                            forks=repo.get("forks_count", 0),
                            is_fork=repo.get("fork", False),
                            created_at=repo.get("created_at"),
                            pushed_at=repo.get("pushed_at"),
                        )
                        db.add(new_repo)

                    synced_count += 1

                page += 1

        db.commit()

    except httpx.RequestError as e:
        raise HTTPException(
            status_code=504, detail=f"Could not reach GitHub — network issue: {str(e)}"
        )

    return {"status": "synced", "repositories_synced": synced_count}
