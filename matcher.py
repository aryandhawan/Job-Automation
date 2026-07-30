import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from typing import Optional
import yaml
load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")

config=yaml.safe_load(open("config.yaml"))

class JobRelevance(BaseModel):
    matching_indices: list[int] = Field(..., description="Index numbers of listings that are genuine matches")

prompt=ChatPromptTemplate.from_messages([
    ("system","""You are a job relevance judge. You will be given a person's original job search request,
followed by a numbered list of job listings. Your job is to identify which listings are
genuine, substantive matches — not just keyword overlap.

The person's original request: {original_query}

Job listings:
{numbered_list_of_jobs}

For each listing, consider whether it actually matches the role, seniority, location, and
any other explicit constraints the person stated — not just whether keywords from the
request appear in the title.

Return the index numbers (as they appear in the numbered list above) of ONLY the listings
that are genuine matches. Exclude anything that superficially mentions the right skill but
is clearly a different type of role, wrong location when one was specified, or otherwise
doesn't actually fit what was asked for.""")
])


llm=ChatGroq(model=config["llm"]["model_name"], temperature=config["llm"]["temperature"], api_key=groq_api_key)

chain=prompt | llm.with_structured_output(JobRelevance)


def judge_job_relevance(original_query: str, numbered_list_of_jobs: list) -> JobRelevance:
    """
    Judges the relevance of job listings based on the original query.

    Args:
        original_query (str): The user's original job search query.
        numbered_list_of_jobs (list): A list of job listings to evaluate.

    Returns:
        JobRelevance: A Pydantic model indicating the indices of relevant job listings.
    """
    formatted_list = "\n".join(numbered_list_of_jobs)  

    response = chain.invoke({
        "original_query": original_query,
        "numbered_list_of_jobs": formatted_list
    })

    matching_indices = response.model_dump()["matching_indices"]

    return [numbered_list_of_jobs[i - 1] for i in matching_indices] 
if __name__ == "__main__":
    # Example usage
    original_query = "find me operations manager jobs in ahmedabad above 1000"
    numbered_list = [
        "1. Operations Manager at XYZ Corp in Ahmedabad",
        "2. Marketing Manager at ABC Inc in Mumbai"
    ]
    judged_relevance = print(judge_job_relevance(original_query, numbered_list))