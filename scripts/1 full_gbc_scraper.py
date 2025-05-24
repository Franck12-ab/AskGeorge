# George Brown College Full Content Scraper

import os
import csv
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import urljoin

# === SETUP ===
base_url = "https://www.georgebrown.ca"
coned_base = "https://coned.georgebrown.ca"
os.makedirs("logs", exist_ok=True)
os.makedirs("raw_data", exist_ok=True)
os.makedirs("raw_programs", exist_ok=True)
os.makedirs("raw_html", exist_ok=True)
os.makedirs("raw_coned", exist_ok=True)

# === Load static URLs to crawl ===
STATIC_URLS = [
    # Admissions & International
    "https://www.georgebrown.ca/admissions",
    "https://www.georgebrown.ca/admissions/international",
    "https://www.georgebrown.ca/international-students",

    # Tuition
    "https://www.georgebrown.ca/tuition",
    "https://www.georgebrown.ca/admissions/tuition-fees",
    "https://www.georgebrown.ca/financial-aid",

    # Student Life
    "https://www.georgebrown.ca/current-students",
    "https://www.georgebrown.ca/current-students/student-life",
    "https://www.georgebrown.ca/current-students/student-services",
    "https://www.georgebrown.ca/current-students/orientation",

    # D2L / Brightspace
    "https://www.georgebrown.ca/d2l",
    "https://www.georgebrown.ca/current-students/brightspace",

    # Co-op & Career
    "https://www.georgebrown.ca/current-students/co-op",
    "https://www.georgebrown.ca/current-students/field-education",
    "https://www.georgebrown.ca/careerservices",

    # Accessibility
    "https://www.georgebrown.ca/accessibility-services",
    "https://www.georgebrown.ca/aoda",
    "https://www.georgebrown.ca/about/policies",

    # FAQ & About
    "https://www.georgebrown.ca/ask-george-brown",
    "https://www.georgebrown.ca/contact",
    "https://www.georgebrown.ca/about"
]

PDF_LOG = "logs/metadata.csv"
PROGRAM_LOG = "logs/program_urls.csv"
HTML_LOG = "logs/static_html.csv"
CONED_LOG = "logs/coned_html.csv"

# === Log Headers ===
def init_logs():
    for log_file, header in [
        (PDF_LOG, ['filename', 'url', 'category', 'date_downloaded']),
        (PROGRAM_LOG, ['title', 'program_code', 'url', 'status', 'category', 'scraped_at']),
        (HTML_LOG, ['url', 'category', 'date_scraped']),
        (CONED_LOG, ['url', 'category', 'date_scraped'])
    ]:
        if not os.path.isfile(log_file):
            with open(log_file, mode='w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(header)

# === 1. Scrape PDF Links ===
def download_pdfs_from_page(full_url, category):
    try:
        response = requests.get(full_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        pdf_links = [a['href'] for a in soup.find_all('a', href=True) if a['href'].endswith('.pdf')]

        for pdf_link in pdf_links:
            pdf_url = urljoin(base_url, pdf_link)
            filename = pdf_url.split("/")[-1]

            try:
                r = requests.get(pdf_url)
                with open(f"raw_data/{filename}", "wb") as f:
                    f.write(r.content)
                with open(PDF_LOG, mode='a', newline='') as f:
                    csv.writer(f).writerow([filename, pdf_url, category, datetime.now().isoformat()])
                print(f"✅ PDF saved: {filename}")
            except Exception as e:
                print(f"❌ Failed to download {filename}: {e}")
    except Exception as e:
        print(f"⚠️ Failed to access {full_url}: {e}")

# === 2. Scrape Structured Program Pages ===
def scrape_program_pages():
    availability_url = f"{base_url}/programs/program-availability?year=2025&availability=domestic"
    try:
        response = requests.get(availability_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        rows = soup.select("table tbody tr")

        for row in rows:
            cols = row.find_all('td')
            if len(cols) < 3:
                continue
            link_tag = cols[0].find('a', href=True)
            if not link_tag:
                continue

            title = link_tag.get_text(strip=True)
            href = link_tag['href']
            full_url = urljoin(base_url, href)
            code = href.split('-')[-1].upper()
            status = cols[-1].get_text(strip=True)

            try:
                r = requests.get(full_url)
                s = BeautifulSoup(r.text, 'html.parser')
                content = "\n".join(el.get_text(strip=True) for el in s.select('h1, h2, p, li'))
                with open(f"raw_programs/{code}.txt", "w", encoding="utf-8") as f:
                    f.write(content)
                with open(PROGRAM_LOG, mode='a', newline='') as f:
                    csv.writer(f).writerow([title, code, full_url, status, "Program Page", datetime.now().isoformat()])
                print(f"📘 Program saved: {title} ({code})")
            except Exception as e:
                print(f"❌ Failed to scrape program {code}: {e}")
    except Exception as e:
        print(f"❌ Failed to load program availability: {e}")

# === 3. Scrape Static HTML Pages ===
def scrape_static_html():
    for url in STATIC_URLS:
        category = url.split("/")[-1].replace("-", " ").title()
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            content = "\n".join(el.get_text(strip=True) for el in soup.select('h1, h2, p, li'))
            filename = category.replace(" ", "_").lower() + ".txt"
            with open(f"raw_html/{filename}", "w", encoding="utf-8") as f:
                f.write(content)
            with open(HTML_LOG, mode='a', newline='') as f:
                csv.writer(f).writerow([url, category, datetime.now().isoformat()])
            print(f"🌐 Static HTML saved: {url}")
        except Exception as e:
            print(f"❌ Failed to scrape static URL: {url} | {e}")

# === 4. Scrape ConEd Sitemap Pages ===
def scrape_coned_pages():
    sitemap_url = f"{coned_base}/about-us/site-map"
    try:
        res = requests.get(sitemap_url)
        soup = BeautifulSoup(res.text, 'html.parser')
        links = [a['href'] for a in soup.select('a[href^="/courses-and-programs/"]')] + [
            "/courses-and-programs", "/registration-information", "/policies", "/student-resources", "/about-us", "/contact-us"
        ]
        links = set(urljoin(coned_base, href) for href in links)

        for url in links:
            category = url.split("/")[-1].replace("-", " ").title()
            try:
                r = requests.get(url)
                s = BeautifulSoup(r.text, 'html.parser')
                content = "\n".join(el.get_text(strip=True) for el in s.select('h1, h2, p, li'))
                filename = category.replace(" ", "_").lower() + ".txt"
                with open(f"raw_coned/{filename}", "w", encoding="utf-8") as f:
                    f.write(content)
                with open(CONED_LOG, mode='a', newline='') as f:
                    csv.writer(f).writerow([url, category, datetime.now().isoformat()])
                print(f"📘 ConEd saved: {url}")
            except Exception as e:
                print(f"❌ Failed to scrape ConEd URL: {url} | {e}")
    except Exception as e:
        print(f"❌ Failed to load ConEd sitemap: {e}")

# === MAIN ===
if __name__ == "__main__":
    print("📦 Initializing GBC full content scraper...")
    init_logs()
    scrape_static_html()
    scrape_program_pages()
    scrape_coned_pages()
    for url in STATIC_URLS:
        download_pdfs_from_page(url, category=url.split("/")[-1].title())
    print("✅ All scraping complete.")
