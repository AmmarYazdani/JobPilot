from abc import ABC, abstractmethod


class JobSource(ABC):

    @abstractmethod
    def search_jobs(self, job_title: str) -> list[dict]:
        pass

    @abstractmethod
    def apply_to_job(self, job: dict) -> dict:
        pass
    


