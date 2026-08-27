from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.database.database import get_db
from app.models.resume import Resume
from app.models.user import User

router = APIRouter(
    prefix="/resumes",
    tags=["Resumes"]
)

UPLOAD_DIR = Path("app/uploads/resumes")
ALLOWED_EXTENSIONS = {".pdf",".dox"}

@router.post("/upload")
def upload_resume(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    file_extension = Path(file.filename).suffix.lower()

    if file_extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDF and DOCX files are allowed.")


    user_upload_dir = UPLOAD_DIR / str(current_user.id)
    user_upload_dir.mkdir(parents=True, exist_ok=True)

    file_path = user_upload_dir / file.filename

    with file_path.open("wb") as buffer:
        buffer.write(file.file.read())

    resume = Resume(
        user_id = current_user.id,
        filename=file.filename,
        file_path=str(file_path)
    )

    db.add(resume)
    db.commit()
    db.refresh(resume)

    return {
        "message": "Resume uploaded successfully",
        "resume_id": resume.id,
        "filename": resume.filename,
    }


