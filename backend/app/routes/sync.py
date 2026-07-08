import httpx
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.commit import Commit
from app.models.language import Language
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


@router.post("/sync/languages/{user_id}")
async def sync_languages(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    repos = db.query(Repository).filter(Repository.user_id == user_id).all()
    if not repos:
        raise HTTPException(
            status_code=400,
            detail="No repositories found — run /sync/repositories first.",
        )

    synced_count = 0

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            for repo in repos:
                response = await client.get(
                    f"https://api.github.com/repositories/{repo.github_repo_id}/languages",
                    headers={"Authorization": f"Bearer {user.access_token}"},
                )

                if response.status_code != 200:
                    continue  # skip this repo, don't kill the whole sync

                language_data = response.json()  # e.g. {"Python": 45000, "HTML": 3000}

                for language, byte_count in language_data.items():
                    existing = (
                        db.query(Language)
                        .filter(
                            Language.repository_id == repo.id,
                            Language.language == language,
                        )
                        .first()
                    )

                    if existing:
                        existing.bytes = byte_count
                    else:
                        db.add(
                            Language(
                                repository_id=repo.id,
                                language=language,
                                bytes=byte_count,
                            )
                        )
                    synced_count += 1

        db.commit()

    except httpx.RequestError as e:
        raise HTTPException(
            status_code=504, detail=f"Could not reach GitHub — network issue: {str(e)}"
        )

    return {"status": "synced", "languages_synced": synced_count}


@router.post("/sync/commits/{user_id}")
async def sync_commits(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    repos = db.query(Repository).filter(Repository.user_id == user_id).all()
    if not repos:
        raise HTTPException(
            status_code=400,
            detail="No repositories found — run /sync/repositories first.",
        )

    synced_count = 0

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            for repo in repos:
                response = await client.get(
                    f"https://api.github.com/repositories/{repo.github_repo_id}/commits",
                    headers={"Authorization": f"Bearer {user.access_token}"},
                    params={"per_page": 100},
                )

                if response.status_code != 200:
                    continue  # e.g. empty repo with no commits yet — skip, don't fail whole sync

                commits = response.json()

                for c in commits:
                    sha = c.get("sha")
                    commit_info = c.get("commit", {})
                    author_info = commit_info.get("author", {})

                    existing = (
                        db.query(Commit)
                        .filter(Commit.repository_id == repo.id, Commit.sha == sha)
                        .first()
                    )

                    if existing:
                        continue  # commits are immutable — no need to update, just skip

                    db.add(
                        Commit(
                            repository_id=repo.id,
                            sha=sha,
                            author_name=author_info.get("name"),
                            author_email=author_info.get("email"),
                            message=commit_info.get("message"),
                            committed_at=author_info.get("date"),
                        )
                    )
                    synced_count += 1

        db.commit()

    except httpx.RequestError as e:
        raise HTTPException(
            status_code=504, detail=f"Could not reach GitHub — network issue: {str(e)}"
        )

    return {"status": "synced", "commits_synced": synced_count}
