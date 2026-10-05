from fastapi import APIRouter , Query

from app.job_sources.naukri import NaukriJobSource

router = APIRouter(
    prefix = "/jobs",
    tags=["jobs"]
)

naukri = NaukriJobSource()

@router.get("/search")
def search_jobs(
    job_title: str = Query(...,min_length=2)
):
    jobs = naukri.search_jobs(job_title)

    return {
        "job_title" : job_title,
        "jobs" : jobs
    }