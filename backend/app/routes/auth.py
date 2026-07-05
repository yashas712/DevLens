from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
import httpx

from app.config import settings
from app.database import get_db
from app.models.user import User

router = APIRouter()

@router.get("/auth/login")
def login():
    github_url = (
        "https://github.com/login/oauth/authorize"
        f"?client_id={settings.github_client_id}"
        "&scope=read:user,repo"
    )
    return RedirectResponse(github_url)


@router.get("/auth/callback")
async def callback(code: str = None, error: str = None, db: Session = Depends(get_db)):
    # Case 1: user clicked "Cancel" on GitHub's authorize screen
    if error:
        raise HTTPException(
            status_code=400,
            detail=f"GitHub authorization was declined: {error}"
        )

    if not code:
        raise HTTPException(
            status_code=400,
            detail="No authorization code received from GitHub."
        )

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            # Step A: exchange the temporary code for a real access token
            token_response = await client.post(
                "https://github.com/login/oauth/access_token",
                headers={"Accept": "application/json"},
                data={
                    "client_id": settings.github_client_id,
                    "client_secret": settings.github_client_secret,
                    "code": code,
                },
            )
            token_data = token_response.json()
            access_token = token_data.get("access_token")

            if not access_token:
                raise HTTPException(
                    status_code=400,
                    detail=f"Failed to obtain access token from GitHub: {token_data.get('error_description', 'unknown error')}"
                )

            # Step B: use that token to fetch the user's GitHub profile
            user_response = await client.get(
                "https://api.github.com/user",
                headers={"Authorization": f"Bearer {access_token}"},
            )

            if user_response.status_code != 200:
                raise HTTPException(
                    status_code=502,
                    detail="Failed to fetch user profile from GitHub."
                )

            github_user = user_response.json()

    except httpx.RequestError as e:
        raise HTTPException(
            status_code=504,
            detail=f"Could not reach GitHub — network or connectivity issue: {str(e)}"
        )

    # Step C: save (or update) this user in our own database
    existing_user = db.query(User).filter(User.github_id == github_user["id"]).first()

    if existing_user:
        existing_user.access_token = access_token
        existing_user.username = github_user["login"]
        existing_user.avatar_url = github_user.get("avatar_url")
    else:
        existing_user = User(
            github_id=github_user["id"],
            username=github_user["login"],
            avatar_url=github_user.get("avatar_url"),
            access_token=access_token,
        )
        db.add(existing_user)

    db.commit()

    return {"status": "logged in", "username": existing_user.username}
