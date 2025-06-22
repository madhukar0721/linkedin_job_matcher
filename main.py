from scripts.scraper import scrape_all_jobs  # Scrapes job listings from LinkedIn
from scripts.llm_analyzer import analyze_jobs_with_resume  # Analyzes listings vs. your resume
from scripts.job_parser import save_results_json, save_results_markdown  # Output functions
from scripts.utils import save_json, load_json

def main():
    """
    Entry point: scrapes jobs, runs LLM analysis, and writes outputs.
    """
    try:
        jobs = scrape_all_jobs()
        print(f"[+] Scraped {len(jobs)} jobs.")

        analyses = analyze_jobs_with_resume(jobs)
        save_results_json(analyses)
        save_results_markdown(analyses)
        print("[✓] Analysis saved to JSON and Markdown.")
    except Exception as e:
        print(f"[!] Pipeline error: {e}")


if __name__ == "__main__":
    main()