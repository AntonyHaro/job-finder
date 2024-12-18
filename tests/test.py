import http.client
import json
from dotenv import load_dotenv
import os

load_dotenv()

conn = http.client.HTTPSConnection("fresh-linkedin-profile-data.p.rapidapi.com")

# Updated JSON payload with correct double quotes and valid data
payload = {
    "keywords": "marketing",
    "geo_code": 92000000,
    "date_posted": "Any time",
    "experience_levels": [],
    "company_ids": [1035],
    "title_ids": [],
    "onsite_remotes": [],
    "functions": [],
    "industries": [],
    "job_types": [],
    "sort_by": "Most relevant",
    "easy_apply": "false",
    "under_10_applicants": "false",
    "start": 0,
}

headers = {
    "x-rapidapi-key": os.getenv("RAPID_API_TEST_KEY"),  # Replace with your actual RapidAPI key
    "x-rapidapi-host": "fresh-linkedin-profile-data.p.rapidapi.com",
    "Content-Type": "application/json",
}

# Convert the Python dictionary to a JSON string
payload = json.dumps(payload)

conn.request("POST", "/search-jobs", payload, headers)

res = conn.getresponse()
data = res.read()

# Print the response from the API
print(data.decode("utf-8"))
