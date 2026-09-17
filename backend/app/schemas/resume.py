from pydantic import BaseModel, Field
from datetime import datetime


class ProjectData(BaseModel):
    title: str
    technologies: list[str] = Field(default_factory=list)
    year: str | None = None
    description: list[str] = Field(default_factory=list)


class ResumeData(BaseModel):
    name: str | None = None
    email: str | None = None
    phone: str | None = None

    skills: list[str] = Field(default_factory=list)
    education: list[str] = Field(default_factory=list)
    experience: list[str] = Field(default_factory=list)
    projects: list[ProjectData] = Field(default_factory=list)
    certifications: list[str] = Field(default_factory=list)

class ResumeResponse(BaseModel):
    id : int
    filename : str
    parsed_data : ResumeData | None = None
    created_at : datetime
    updated_at : datetime

    class Config:
        from_attributes = True
