from typing import List, Dict
from openai import OpenAI
from scripts.config import OPENAI_API_KEY, MODEL, PROMPT_TEMPLATE, RESUME_TEXT, INSTRUCTIONS


def analyze_jobs_with_resume(jobs: List[Dict]) -> List[Dict]:
    """Call OpenAI to analyze each job against the resume."""
    client = OpenAI(api_key=OPENAI_API_KEY)
    print(OPENAI_API_KEY)
    analyses = []
    print('hi')
    for job in jobs:
        prompt = PROMPT_TEMPLATE.replace("{JOB_DESCRIPTION}", job["Job Description"])\
                                .replace("{RESUME_TEXT}", RESUME_TEXT)
        
        resp = client.responses.create(
            model=MODEL,
            instructions=INSTRUCTIONS,
            input=prompt,
            temperature=0.1,
            max_output_tokens=600
        )
        
        job_copy = {k: v for k, v in job.items() if k != "Job Description"}
        analyses.append({
            **job_copy,
            "analysis": resp.output[0].content[0].text
        })
        print(analyses)

    return analyses