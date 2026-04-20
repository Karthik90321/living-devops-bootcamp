# app.py - simple Flask "about me" page
# Living DevOps Bootcamp - Day 06

from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    # Change these to your actual info
    context = {
        "name": "Karthik",
        "tagline": "Application Support Engineer → DevOps",
        "location": "Hyderabad, India",
        "bootcamp": "Living DevOps Bootcamp (Jan 2026 batch)",
        "github": "https://github.com/Karthik90321/living-devops-bootcamp",
        "skills": [
            "AWS (EC2, VPC, Route 53, ACM)",
            "Linux administration (WSL, Amazon Linux 2023)",
            "Bash scripting",
            "Nginx reverse proxy",
            "Python / Flask / Gunicorn",
            "Git + GitHub",
        ],
        "currently_learning": [
            "ECS Fargate + Docker",
            "Terraform (IaC)",
            "CI/CD with GitHub Actions",
        ],
    }
    return render_template("index.html", **context)


@app.route("/health")
def health():
    # Simple health-check endpoint for monitoring later
    return {"status": "ok"}, 200


if __name__ == "__main__":
    # Only runs in development. Production uses Gunicorn.
    app.run(host="0.0.0.0", port=8000, debug=False)