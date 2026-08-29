import re

from app.schemas.resume import ResumeData


def extract_email(text: str) -> str | None:
    match = re.search(
        r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
        text
    )

    return match.group(0) if match else None


def extract_phone(text: str) -> str | None:
    match = re.search(
        r"(?:\+91[\s-]?)?[6-9]\d{4}[\s-]?\d{5}",
        text
    )

    return match.group(0) if match else None


def extract_name(text: str) -> str | None:
    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    if not lines:
        return None

    return lines[0]


def extract_section(
    text: str,
    section_names: list[str]
) -> list[str]:

    lines = text.splitlines()
    start_index = None

    for i, line in enumerate(lines):
        clean_line = line.strip().lower()

        if clean_line in section_names:
            start_index = i + 1
            break

    if start_index is None:
        return []

    section_lines = []

    section_headers = [
        "skills",
        "technical skills",
        "education",
        "experience",
        "work experience",
        "professional experience",
        "projects",
        "certifications",
        "certificates",
        "achievements",
        "summary",
        "profile"
    ]

    for line in lines[start_index:]:

        clean_line = line.strip().lower()

        if clean_line in section_headers:
            break

        if line.strip():
            section_lines.append(line.strip())

    return section_lines


def parse_resume(text: str) -> ResumeData:

    return ResumeData(
        name=extract_name(text),
        email=extract_email(text),
        phone=extract_phone(text),
        skills=extract_skills(text),
        education=extract_section(
            text,
            ["education", "academic background"]
        ),
        experience=extract_section(
            text,
            [
                "experience",
                "work experience",
                "professional experience"
            ]
        ),
        projects=extract_section(
            text,
            ["projects", "personal projects"]
        ),
        certifications=extract_section(
            text,
            ["certifications", "certificates"]
        )
    )

def extract_skills(text: str) -> list[str]:
    lines = text.splitlines()

    skills = []

    in_skills = False

    section_headers = [
        "education",
        "experience",
        "work experience",
        "professional experience",
        "projects",
        "certifications",
        "certificates",
        "achievements",
        "summary",
        "profile"
    ]

    for line in lines:
        clean_line = line.strip()

        if clean_line.lower() == "technical skills":
            in_skills = True
            continue

        if in_skills and clean_line.lower() in section_headers:
            break

        if in_skills and clean_line:
            clean_line = clean_line.lstrip("•- ")

            if ":" in clean_line:
                _, skill_text = clean_line.split(":", 1)
            else:
                skill_text = clean_line

            skill_items = skill_text.split(",")

            for skill in skill_items:
                skill = skill.strip()

                if skill:
                    skills.append(skill)

    return skills