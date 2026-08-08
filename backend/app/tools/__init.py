from app.tools.job_fetcher import fetch_job_posting


TOOL_SHCEMAS = [
    {
        "name": "fetch_job__posting",
        "description": "Fetches a job posting from a URL and returns it's clean text content.",
        "input-schema": {
            "type": "object",
            "properties":{
                "url": {"type": "string", "description": "URL of the job posting"}
            },
            "required": ["url"],
        },
    },
]

TOOL_FUNCTIONS = {
    "fetch_job_posting": fetch_job_posting,
}