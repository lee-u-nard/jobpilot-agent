from flask import Blueprint, jsonify, request
from app.agent import run_agent

main = Blueprint("main", __name__)

@main.route("/health")
def health():
    return jsonify(status="ok", service="jobpilot-agent")


@main.route("/agent/analyze", methods=["POST"])
def analyze():
    data = request.get_json(silent=True) or {}
    job_url = data.get("job_url")

    if not job_url:
        return jsonify(error="job_url is required"), 400
    
    result = run_agent(f"Analyze this job posting: {job_url}")
    return jsonify(result)