"""
Streamlit interface for the Career Bot.
Run with: streamlit run app.py
"""

import streamlit as st
from extractor import extract_job_search_params
from adzuna_client import search_jobs
from matcher import judge_job_relevance

st.set_page_config(page_title="Career Bot", page_icon="💼", layout="centered")

st.title("💼 Career Bot")
st.write("Describe the job you're looking for in plain language — I'll find genuinely matching listings.")

query = st.text_input(
    "What are you looking for?",
    placeholder="e.g. find me python developer jobs in bangalore above 8 lakhs"
)

search_clicked = st.button("Search", type="primary")

if search_clicked:
    if not query.strip():
        st.warning("Type a query first.")
    else:
        with st.spinner("Understanding your request..."):
            extracted_params = extract_job_search_params(query)

        with st.spinner("Searching listings..."):
            jobs = search_jobs(query)  # adjust if search_jobs expects extracted_params directly instead of raw query

        if not jobs:
            st.info("No listings found for that search.")
        else:
            with st.spinner(f"Judging relevance of {len(jobs)} listings..."):
                # matcher expects a numbered list of job strings — build that from the JobListing objects
                numbered_list = [
                    f"{i+1}. {job.title} at {job.company} in {job.location}"
                    for i, job in enumerate(jobs)
                ]
                matched_descriptions = judge_job_relevance(query, numbered_list)

            # Map matched description strings back to their full JobListing objects
            matched_jobs = [
                job for job, desc in zip(jobs, numbered_list) if desc in matched_descriptions
            ]

            if not matched_jobs:
                st.info("Found listings, but none were a genuine match for your request.")
            else:
                st.success(f"Found {len(matched_jobs)} matching job(s)")

                for job in matched_jobs:
                    with st.container(border=True):
                        st.subheader(job.title)
                        st.write(f"**{job.company}** — {job.location}")

                        if job.salary_min or job.salary_max:
                            salary_text = ""
                            if job.salary_min:
                                salary_text += f"₹{job.salary_min:,.0f}"
                            if job.salary_max:
                                salary_text += f" – ₹{job.salary_max:,.0f}"
                            st.write(f"💰 {salary_text}")

                        st.write(job.description[:300] + "..." if len(job.description) > 300 else job.description)
                        st.link_button("View & Apply", job.redirect_url)