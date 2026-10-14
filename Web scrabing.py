
import pandas as pd
import requests
from bs4 import BeautifulSoup
from pathlib import Path

url = "https://realpython.github.io/fake-jobs/"

headers = {
    "User-Agent": "Mozilla/5.0"
}

# Step 1: Fetch website HTML
response = requests.get(url, headers=headers, timeout=15)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

# Step 2: Find job container
job_container = soup.find("div", id="ResultsContainer")

if not job_container:
    print("Jobs container not found")
    raise SystemExit

# Step 3: Find all job cards
jobs = job_container.find_all("div", class_="card")

print("Jobs found:", len(jobs))

# Step 4: Store raw HTML
job_info = []

for job in jobs:
    job_info.append(" ".join(job.prettify().split()))

# Step 5: Create raw DataFrame
raw_df = pd.DataFrame(job_info, columns=["Info"])
raw_df = raw_df.dropna(subset=["Info"])

# Step 6: Save raw data
output_folder = Path("jobportalws")
output_folder.mkdir(parents=True, exist_ok=True)

raw_df.to_csv(r"C:\Users\bavad\OneDrive\Documents\Stock_Bava\Job portal\jobs_info_raw.csv", index=False)

print("Raw Data Stored Successfully")

# Step 7: Extract job details
job_titles = []
companies = []
locations = []
job_urls = []

for element in raw_df["Info"].values:

    job_soup = BeautifulSoup(str(element), "html.parser")

    # Extract job title
    title_tag = job_soup.find("h2", class_="title")
    job_titles.append(
        title_tag.get_text(strip=True) if title_tag else "-"
    )

    # Extract company name
    company_tag = job_soup.find("h3", class_="company")
    companies.append(
        company_tag.get_text(strip=True) if company_tag else "-"
    )

    # Extract location
    location_tag = job_soup.find("p", class_="location")
    locations.append(
        location_tag.get_text(strip=True) if location_tag else "-"
    )

    # Extract job URL
    link_tag = job_soup.select_one("a.card-footer-item")

    if link_tag and link_tag.get("href"):
        job_urls.append(
            requests.compat.urljoin(url, link_tag["href"])
        )
    else:
        job_urls.append("-")

# Step 8: Create final DataFrame
job_df = pd.DataFrame({
    "Job Title": job_titles,
    "Company": companies,
    "Location": locations,
    "Job URL": job_urls
})

# Step 9: Save cleaned job data
job_df.to_csv(r"C:\Users\bavad\OneDrive\Documents\Stock_Bava\Job portal\job_posts.csv", index=False)

print(job_df)
print("Total jobs extracted:", len(job_df))
print("Job Data Stored Successfully")