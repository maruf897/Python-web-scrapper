from bs4 import BeautifulSoup
import requests
from datetime import datetime

now = datetime.now()
date_time = now.strftime("%m_%d_%Y_%H_%M_%S")
url = "https://stackoverflow.com/jobs"  # enter desired url
req = requests.get(url)
soup = BeautifulSoup(req.text, "lxml")
soup.prettify()
# i couldnt make file with ":"and "/" present in the link, so replaced them
filename = url.replace("/", "_").replace(":", "_") + date_time + "_1730897.txt"
print(filename)
body = soup.body
# to check if we found any thing if not then a general solution for other website
no_match_flag = True
# for mofa gov link
press = body.find("ul", {"class": "meganizr"})

if press is not None:
    no_match_flag = False

    lis = press.find_all("li")

    with open(filename, "w", encoding="utf-8") as file1:
        file1.write("Navigation \n")
        for li in lis:

            file1.writelines("Menu Item" + li.a.text)
            file1.writelines(" Link: " + li.a["href"])
            file1.write("\n")
# for table data if present
table = body.find("table")

if table is not None:
    table_body = table.tbody
    data = []
    rows = table_body.find_all("tr")

    with open(filename, "a", encoding="utf-8") as file1:
        file1.write("Table Data \n")
        for row in rows:
            cols = row.find_all("td")

            for td in cols:
                file1.write(td.text + ",")
                file1.write("\n")
# for mofa gov link
footer = body.find("div", id="footer-menu")
if footer is not None:
    no_match_flag = False

    footer = footer.ul
    lis = footer.find_all("li")
    with open(filename, "a", encoding="utf-8") as file1:
        file1.write("Footer \n")
        for li in lis:

            file1.writelines("Menu Item " + li.a.text)
            file1.writelines(" Link: " + li.a["href"])
            file1.write("\n")
# for downloading any content
links = body.find_all("a", {"href": True})

accepted_format = (".pdf", ".docx", ".mp3", ".mp4", ".png", ".jpeg")
for link in links:
    if link["href"] is not None:
        doc_link = link["href"]

        if doc_link.endswith((accepted_format)):
            r = requests.get(doc_link)
            doc_name = doc_link.rsplit("/", 1)[1]
            with open(doc_name, "wb") as file2:
                file2.write(r.content)
# for stackover flow link
jobs = body.find_all("div", {"class": "-job"})

if len(jobs) > 0:
    no_match_flag = False
    print(no_match_flag)
    print(jobs)
    for job in jobs:

        with open(filename, "a", encoding="utf-8") as file1:
            file1.write("Job \n")

            file1.writelines("Job Title: " + job.find("a", {"class": "s-link"}).text)
            file1.writelines("\nLink: " + job.find("a", {"class": "s-link"})["href"])
            temp = job.find("h3", {"class": "fs-body1"})
            file1.writelines("\nCompany: " + temp.find("span").text.strip())
            file1.writelines(
                "\nLocation: "
                + temp.find("span", {"class": "fc-black-500"}).text.strip()
            )
            file1.writelines("\nSkills:")
            for skill in job.find_all("a", {"class": "s-tag"}):
                file1.writelines(skill.text + ", ")
            file1.writelines("\nFeatures:")
            for feature in job.find_all("li"):
                file1.writelines(feature.text + ", ")

            file1.write("\n")
# for any form data, i am not sure how to get category so using place holder to indentify
forms = body.find_all("input", {"placeholder": True, "value": True})
if forms is not None:
    with open(filename, "a", encoding="utf-8") as file1:
        file1.write("Form Data \n")
        for form in forms:
            file1.writelines(form["placeholder"] + ":" + form["value"] + "\n")
# for general case
if no_match_flag:
    with open(filename, "a", encoding="utf-8") as file1:
        file1.write("Body Text: \n")
        file1.write(body.text.strip())
