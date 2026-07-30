import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from typing import Optional
from dotenv import load_dotenv
import os
import yaml

config=yaml.safe_load(open("config.yaml"))

load_dotenv()

class JobSearchParams(BaseModel):
    what: str = Field(description="The core role/keywords to search for, e.g. 'python developer'. Required — always extract something here.")
    where: Optional[str] = Field(default=None, description="Location mentioned, e.g. 'Bangalore'. Null if not mentioned or user said 'remote' with no city.")
    salary_min: Optional[int] = Field(default=None, description="Minimum salary mentioned, converted to a plain number in the local currency (e.g. '8 lakhs' -> 800000). Null if not mentioned.")
    full_time: Optional[bool] = Field(default=None, description="True if user specifically wants full-time roles, False if they specifically want part-time/contract, null if not mentioned.")
    salary_max: Optional[int] = Field(default=None, description="Maximum salary mentioned, converted to a plain number in the local currency. Null if not mentioned.")

llm =ChatGroq(
    model=config["llm"]["model_name"],
    temperature=config["llm"]["temperature"],
    api_key=os.getenv("GROQ_API_KEY")
)

prompt = ChatPromptTemplate.from_messages([
    ("system", """You extract structured job search parameters from a person's natural-language request.
 
Only extract what is actually stated or clearly implied — never invent a location, salary,
or employment type the person didn't mention. If something isn't mentioned, leave it null.
 
Examples:
- "find me python developer jobs in bangalore" -> what="python developer", where="Bangalore", everything else null
- "remote react roles paying above 10 lakhs" -> what="react developer", where=null, salary_min=1000000, salary_max=null
- "marketing jobs" -> what="marketing", everything else null"""),
    ("human", "{query}")
])

chain=prompt | llm.with_structured_output(JobSearchParams)

def extract_job_search_params(query: str) -> JobSearchParams:
    """
    Extracts structured job search parameters from a natural-language query.

    Args:
        query (str): The user's natural-language job search query.

    Returns:
        JobSearchParams: A Pydantic model containing the extracted parameters.
    """
    response = chain.invoke(input=query)

    return response.model_dump(exclude_none=True)


if __name__ == "__main__":
    # Example usage
    query = "find me python developer jobs in bangalore below 200000"
    params = extract_job_search_params(query)
    print(params)
    