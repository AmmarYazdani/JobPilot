from pydantic import BaseModel, Field

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

