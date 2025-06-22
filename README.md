# LinkedIn Job Matcher

A complete end-to-end tool that:
1. 🔐 Logs into LinkedIn via saved session cookies.
2. 🔎 Scrapes job postings based on your target companies, roles, and filters.
3. 🧹 Cleans and normalizes job descriptions for analysis.
4. 🤖 Uses LLM Model to compare each job against your resume and generate fit insights.
5. 📑 Outputs structured JSON and reader-friendly Markdown reports.

---

## 📂 Directory Structure

```
linkedin-job-matcher/
├── .env                  # OpenAI API key and optional MODEL override
├── cookies/              # Saved LinkedIn session cookies
│   └── linkedin_cookies.pkl
├── data/                 # Generated output files
│   ├── all_jobs.json
│   └── all_job_analysis.md
├── prompts/              # LLM prompt templates
│   └── prompt_template.txt
├── resume/               # Your resume(s) for analysis
│   └── resume.txt
├── scripts/              # Core modules
│   ├── config.py         # Constants and env loader
│   ├── utils.py          # Helper functions (cleaning, delays)
│   ├── scraper.py        # LinkedIn scraping logic
│   ├── llm_analyzer.py   # LLM analysis logic
│   ├── job_parser.py     # JSON/Markdown report generators
│   └── save_cookies.py   # Script to record session cookies
├── main.py               # Entry point orchestration
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation (this file)
```

---

## ⚙️ Configuration (`.env`)

Create a file named `.env` in the project root with:

```ini
OPENAI_API_KEY=sk-...
# Optional: override default model
MODEL=gpt-4o-mini-2024-07-18
```
#### For customization of companies, titles, filters, and search URLs, please check the config/ directory and scripts/config.py.

No other secrets or credentials are required—cookies handle LinkedIn auth.

---

## 📝 Prompt Template (`prompts/prompt_template.txt`)

This template drives the LLM analysis. It defines **placeholders**:
- `{JOB_DESCRIPTION}` → injected raw text from LinkedIn.
- `{RESUME_TEXT}` → your full resume in plain text.

Example snippet:

```
You are an expert technical recruiter.

Job Description:
{JOB_DESCRIPTION}

Candidate Resume:
{RESUME_TEXT}

Please evaluate the fit and list:
1. Core Skills Match
2. Gaps
3. Overall recommendation
```

Customize this prompt to refine analysis style or add scoring criteria.

---

## 📄 Resume Format (`resume/resume.txt`)

- Plain text file, UTF-8 encoded.
- Include all relevant sections: Summary, Skills, Experience, Education.
- Keep it concise (1–2 pages) to limit token usage.

Example structure:
```
John Doe
Backend Engineer

Skills:
- Node.js, Express, TypeScript
- PostgreSQL, MongoDB

Experience:
...
```

---

## 🚀 Usage

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
2. **Save LinkedIn cookies**
   ```bash
   python scripts/save_cookies.py
   ```
3. **Run main pipeline**
   ```bash
   python main.py
   ```
4. **View Results**
   - JSON: `data/all_jobs_urls.json`
   - Markdown report: `data/job_analysis.md`

---

## 📊 Output Example

> See `data/job_analysis.md` for a sample of how each job is evaluated with headings, analysis text, and separators.

---

## 🤝 Contributing

1. Fork the repo
2. Create a feature branch
3. Submit a pull request

---

## 🛡 License

This project is licensed under the MIT License.
