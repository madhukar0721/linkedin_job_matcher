from pathlib import Path
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Base directories and files
BASE_DIR = Path(__file__).parent.parent
BASE_URL = "https://www.linkedin.com"
COOKIES_PATH = BASE_DIR / "cookies" / "linkedin_cookies.pkl"
COMPANIES_FILE = BASE_DIR / "config" / "company_names.json"
TITLES_FILE = BASE_DIR / "config" / "title.json"
OUTPUT_FILE = BASE_DIR / "data" / "all_jobs.json"
MARKDOWN_FILE = BASE_DIR / "data" / "all_job_analysis.md"

# LinkedIn search filters
GEO_ID_INDIA = "102713980"
EXPERIENCE_LEVELS = [2, 3]
TIME_RANGE = "r86400"
FILTER_FUNCTIONAL = ["eng", "it"]

# LLM configuration
PROMPT_TEMPLATE_PATH = BASE_DIR / "prompts" / "prompt_template.txt"
RESUME_PATH = BASE_DIR / "resume" / "resume.txt"
PROMPT_TEMPLATE = PROMPT_TEMPLATE_PATH.read_text(encoding="utf-8")
RESUME_TEXT = RESUME_PATH.read_text(encoding="utf-8")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL = os.getenv("MODEL", "gpt-4o-mini-2024-07-18")

INSTRUCTIONS = """
You are a helpful assistant that analyzes job descriptions and compares them to a resume.
You will be given a job description and a resume.
You will need to analyze the job description and compare it to the resume.
You will need to return a score for the job description based on how well it matches the resume.
"""