from flask import Flask, render_template, request, jsonify
import os
import requests
from dotenv import load_dotenv
from utils.format_utils import format_datetime

load_dotenv()

app = Flask(__name__)

# localidades remotas - Estados Unidos, Europa etc
# estados brasileiros


def search_jobs(
    keywords,
    geo_code=106057199,
    date_posted="Any time",
    start=0,
    company_ids=None,
    experience_levels=None,
    onsite_remotes=None,
):
    url = "https://fresh-linkedin-profile-data.p.rapidapi.com/search-jobs"

    headers = {
        "Content-Type": "application/json",
        "x-rapidapi-host": "fresh-linkedin-profile-data.p.rapidapi.com",
        "x-rapidapi-key": os.getenv("RAPID_API_TEST_KEY"),
    }

    payload = {
        "keywords": keywords,
        "geo_code": geo_code,
        "date_posted": date_posted,
        "experience_levels": experience_levels if experience_levels else [],
        "company_ids": company_ids if company_ids else [],
        "title_ids": [],
        "onsite_remotes": onsite_remotes if onsite_remotes else [],
        "functions": [],
        "industries": [],
        "job_types": [],
        "sort_by": "Most relevant",
        "easy_apply": "false",
        "under_10_applicants": "false",
        "start": start,
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        return response.json() or {}
    except Exception as e:
        return {"error": str(e)}


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")


@app.route("/api", methods=["POST"])
def api():
    if request.method == "POST":
        keywords = request.form.get("keywords", "")
        experience = request.form.get("experience", "")
        work_type = request.form.get("work_type", "")
        date_posted = request.form.get("date_posted", "")
        company_filter = request.form.get("company_filter", "")

        experience_options = {
            "": [],
            "Estágio": ["INTERNSHIP"],
            "Júnior": ["ENTRY_LEVEL"],
            "Pleno": ["MID_SENIOR"],
            "Sênior": ["SENIOR"],
            "Diretor": ["DIRECTOR"],
        }
        work_type_options = {
            "": [],
            "Presencial": ["ONSITE"],
            "Remoto": ["REMOTE"],
            "Híbrido": ["HYBRID"],
        }
        date_options = {
            "Qualquer período": "Any time",
            "Última 24 horas": "Past 24 hours",
            "Última semana": "Past week",
            "Último mês": "Past month",
        }

        experience_levels = experience_options[experience]
        onsite_remotes = work_type_options[work_type]
        company_ids = [1035] if company_filter.lower() == "microsoft" else []

        results = search_jobs(
            keywords=keywords,
            date_posted=date_options[date_posted],
            experience_levels=experience_levels,
            onsite_remotes=onsite_remotes,
            company_ids=company_ids,
        )

        if "data" in results:
            vagas = results["data"]
            return jsonify({"jobs": vagas})
        else:
            return jsonify({"error": "Erro ao fazer a requisição"})


if __name__ == "__main__":
    app.run(debug=True)
