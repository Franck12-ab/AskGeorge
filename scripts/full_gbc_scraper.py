import os
import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime

base_url = "https://www.georgebrown.ca"
log_file = 'logs/metadata.csv'

# Setup folders and log
os.makedirs("raw_data", exist_ok=True)
os.makedirs("logs", exist_ok=True)

if not os.path.isfile(log_file):
    with open(log_file, mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['filename', 'url', 'category', 'date_downloaded'])

def download_pdfs_from_page(full_url, category):
    try:
        response = requests.get(full_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        pdf_links = [a['href'] for a in soup.find_all('a', href=True) if a['href'].endswith('.pdf')]

        for pdf_link in pdf_links:
            pdf_url = pdf_link if pdf_link.startswith("http") else base_url + pdf_link
            filename = pdf_url.split("/")[-1]

            print(f"📥 Downloading {filename} from {pdf_url}")

            try:
                pdf_response = requests.get(pdf_url)
                with open(f"raw_data/{filename}", "wb") as f:
                    f.write(pdf_response.content)
                print(f"✅ Saved: {filename}")

                with open(log_file, mode='a', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow([filename, pdf_url, category, datetime.now().isoformat()])
            except Exception as e:
                print(f"❌ Failed to download {filename} | {e}")
    except Exception as e:
        print(f"⚠️ Failed to access {full_url} | {e}")

# === SECTION 1: /about subpages ===
about_url = f"{base_url}/about"
print(f"🌐 Scanning ABOUT page: {about_url}")
try:
    response = requests.get(about_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    about_links = [a['href'] for a in soup.select('a[href^="/about/"]')]

    for rel_link in about_links:
        full_url = base_url + rel_link
        category = rel_link.split('/')[-1].replace('-', ' ').title()
        print(f"\n📂 Visiting /about: {full_url} [Category: {category}]")
        download_pdfs_from_page(full_url, category)
except Exception as e:
    print(f"❌ Failed to scrape /about | {e}")

# === SECTION 2: /business main page ===
business_url = f"{base_url}/business"
print(f"\n🌐 Scanning BUSINESS page: {business_url}")
download_pdfs_from_page(business_url, "Centre for Business")

# === SECTION 3: /current-students subpages ===
students_url = f"{base_url}/current-students"
print(f"\n🌐 Scanning CURRENT STUDENTS page: {students_url}")
try:
    response = requests.get(students_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    student_links = [a['href'] for a in soup.select('a[href^="/current-students/"]')]

    for rel_link in student_links:
        full_url = base_url + rel_link
        category = rel_link.split('/')[-1].replace('-', ' ').title()
        print(f"\n📂 Visiting /current-students: {full_url} [Category: {category}]")
        download_pdfs_from_page(full_url, category)
except Exception as e:
    print(f"❌ Failed to scrape /current-students | {e}")

# === SECTION 4: /programs subpages ===
programs_url = f"{base_url}/programs"
print(f"\n🌐 Scanning PROGRAMS page: {programs_url}")
try:
    response = requests.get(programs_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    program_links = set([a['href'] for a in soup.select('a[href^="/programs/"]')])

    for rel_link in program_links:
        full_url = base_url + rel_link
        print(f"\n📂 Visiting /programs: {full_url} [Category: Program Page]")
        download_pdfs_from_page(full_url, "Program Page")
except Exception as e:
    print(f"❌ Failed to scrape /programs | {e}")

# === SECTION 5: Direct Co-op / FAQ / Continuing Ed Pages ===
faq_pages = [
    # Main Co-op and FAQ pages
    # ("https://www.georgebrown.ca/programs/co-op-education", "Co-op"),
    ("https://www.georgebrown.ca/ask-george-brown", "FAQ"),
    
    # Continuing education content
    ("https://coned.georgebrown.ca/courses-and-programs", "ConEd Courses"),
    ("https://coned.georgebrown.ca/registration-information", "ConEd Registration"),
    ("https://coned.georgebrown.ca/policies", "ConEd Policies"),
    ("https://coned.georgebrown.ca/student-resources", "ConEd Resources"),
    ("https://coned.georgebrown.ca/about-us", "ConEd About"),
    ("https://coned.georgebrown.ca/contact-us", "ConEd Contact")
]

for url, category in faq_pages:
    print(f"\n📂 Visiting Direct Page: {url} [Category: {category}]")
    download_pdfs_from_page(url, category)
