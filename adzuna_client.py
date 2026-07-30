import requests
import pydantic
from dotenv import load_dotenv
import os
import json
from extractor import JobSearchParams, extract_job_search_params

from typing import Optional

class JobListing(pydantic.BaseModel):
    title: str
    company: Optional[str] = None
    location: Optional[str] = None
    description: str
    salary_min: Optional[float] = None
    salary_max: Optional[float] = None
    created: str
    redirect_url: str


def parse_jobs(raw_response: dict) -> list[JobListing]:
    jobs = []
    for raw_job in raw_response.get("results", []):
        jobs.append(JobListing(
            title=raw_job.get("title"),
            company=raw_job.get("company", {}).get("display_name"),
            location=raw_job.get("location", {}).get("display_name"),
            description=raw_job.get("description"),
            salary_min=raw_job.get("salary_min"),
            salary_max=raw_job.get("salary_max"),
            created=raw_job.get("created"),
            redirect_url=raw_job.get("redirect_url"),
        ))
    return jobs

def search_jobs(query: str) -> list[JobListing]:
    extracted_params = extract_job_search_params(query)
    auth_params = {"app_id": os.getenv("ADZUNA_APP_ID"), "app_key": os.getenv("ADZUNA_APP_KEY")}
    final_params = {**extracted_params, **auth_params}

    response = requests.get(url="https://api.adzuna.com/v1/api/jobs/in/search/1", params=final_params)
    return parse_jobs(response.json())
