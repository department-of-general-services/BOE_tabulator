base_url = "https://comptroller.baltimorecity.gov/"
minutes_url = base_url + "boe/meetings/minutes"

# If there is no such folder, the script will create one automatically
# folder_location = r'E:\webscraping'
# if not os.path.exists(folder_location):os.mkdir(folder_location)

response = requests.get(minutes_url)
soup = BeautifulSoup(response.text, "html.parser")
root = Path.cwd()
for year in range(2009, 2021):
    link = soup.find("a", href=True, text=str(year))
    annual_url = link["href"]
    print(annual_url)
    annual_response = requests.get(annual_url)
    annual_soup = BeautifulSoup(annual_response.text, "html.parser")
    pdf_links = annual_soup.find_all(name="a", href=re.compile("files"))
    for link in pdf_links:
        pdf_location = link["href"]
        pdf_url = base_url + pdf_location
        pdf_file = requests.get(pdf_url)
        try:
            pdf_name = (
                re.search(pattern=r"[^\/]+(?=\.[^\/.]*$)", string=pdf_location)[0]
                + ".pdf"
            )
            save_path = root / "pdf_files" / pdf_name
            with open(save_path, "wb") as f:
                f.write(pdf_file.content)
        except:
            print(f"an error occurred with path {pdf_location}")


def confirm_meeting_date():
    pass


def create_dateframes():
    meetings = pd.DataFrame(
        columns=[
            "date",
            "president",
            "mayor",
            "no_of_protests",
            "no_of_settlements",
            "no_of_mous",
        ]
    )
    return meetings


def read_pdf(path):
    pdf_paths = list(pdf_dir.rglob("*.pdf"))

    for pdf_path in pdf_paths:
        pdfFileObj = open(pdf_path, "rb")
        pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
        for page in pdfReader.pages:
            print(page.extractText())
        break


read_pdf(pdf_dir)
