import re

from app.schemas.resume import ResumeData, ProjectData



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

    skills = extract_skills(text)

    return ResumeData(
        name=extract_name(text),
        email=extract_email(text),
        phone=extract_phone(text),
        skills=skills,
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
        projects=extract_projects(
            text, skills),
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

def extract_projects(
    text: str,
    skills: list[str]
) -> list[ProjectData]:

    lines = text.splitlines()

    projects = []
    in_projects = False
    current_project = None

    section_headers = {
        "professional summary",
        "education",
        "technical skills",
        "skills",
        "experience",
        "work experience",
        "professional experience",
        "certifications",
        "certificates",
        "achievements",
        "summary",
        "profile",
    }

    for line in lines:
        clean_line = line.strip()

        if not clean_line:
            continue

        if clean_line.lower() == "projects":
            in_projects = True
            continue

        if in_projects and clean_line.lower() in section_headers:
            break

        if not in_projects:
            continue

        clean_line = clean_line.lstrip("•- ").strip()

        # A new project heading ends with a year.
        year_match = re.search(r"\b(20\d{2})\s*$", clean_line)

        if year_match:
            year = year_match.group(1)

            # Remove the year.
            project_text = clean_line[:year_match.start()].strip()

            technologies = []

            # Split the project heading by commas.
            parts = [
                part.strip()
                for part in project_text.split(",")
                if part.strip()
            ]

            # First part contains the project title
            # and possibly the first technology.
            title_part = parts[0] if parts else project_text

            # Check the remaining parts against detected skills.
            for part in parts[1:]:
                for skill in sorted(skills, key=len, reverse=True):
                    if part.lower() == skill.lower():
                        technologies.append(skill)
                        break

            # Check whether a technology is attached
            # to the end of the project title.
            for skill in sorted(skills, key=len, reverse=True):
                pattern = r"\s+" + re.escape(skill) + r"$"

                if re.search(pattern, title_part, re.IGNORECASE):
                    technologies.insert(0, skill)

                    title_part = re.sub(
                        pattern,
                        "",
                        title_part,
                        flags=re.IGNORECASE
                    ).strip()

                    break

            # Clean leftover commas and spaces.
            title = re.sub(r"\s*,\s*", " ", title_part)
            title = re.sub(r"\s{2,}", " ", title)
            title = title.strip(" :-,")

            current_project = ProjectData(
                title=title,
                technologies=technologies,
                year=year,
                description=[]
            )

            projects.append(current_project)

        elif current_project:
            current_project.description.append(clean_line)

    return projects