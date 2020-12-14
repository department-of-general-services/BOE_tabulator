import PyPDF2
import datetime as dt
import pandas as pd
import re
from datetime import datetime

from common.utils import replace_chars

REPLACEMENTS = [
    ("Œ", "-"),
    ("ﬁ", '"'),
    ("ﬂ", '"'),
    ("™", "'"),
    ("Ł", "•"),
    ("Š", "-"),
    ("€", " "),
    ("¬", "-"),
    ("–", "…"),
    ("‚", "'"),
    ("Ž", "™"),
    ("˚", "fl"),
    ("˜", "fi"),
    ("˛", "ff"),
    ("˝", "ffi"),
    ("š", "—"),
    ("ü", "ti"),
    ("î", "í"),
    ("è", "c"),
    ("ë", "e"),
    ("Ð", "–"),
    ("Ò", '"'),
    ("Ó", '"'),
    ("Õ", "'"),
]


def parse_pdf(pdf_path):
    """Parses the pdf of the minutes from a BOE meeting and cleans the text

    Args:
        pdf_path (pathlib.Path): The path to the pdf to parse
    Returns:
        minutes (Minutes): An instance of the Minutes class
    """
    try:
        minutes = Minutes(pdf_path)
        minutes.parse_and_clean_pages()
    except (ValueError, FileNotFoundError) as e:
        print(f"The following error occurred parsing file '{pdf_path}': {e}")
        raise e
    return minutes


def store_pdf_text_to_df(path):
    """Finds .pdf files stored at the given url and stores them within the
    repository for later analysis.

    Args:
        base_url (str): The main url for the Comptroller of Baltimore's webiste
        minutes_url (str): The url where the function can find links to pages of
        pdf files organized by year
    Returns:
        None: This is a void function.
    """
    pdf_paths = list(path.rglob("*.pdf"))
    text_df = pd.DataFrame(columns=["date", "page_number", "minutes"])
    for pdf_path in pdf_paths:
        # print(f"Parsing file: {pdf_path.name}")
        minutes = ""
        pdfFileObj = open(pdf_path, "rb")
        try:
            pdfReader = PyPDF2.PdfFileReader(pdfFileObj, strict=False)
        except ValueError:
            print(f"An error occurred reading file {pdf_path}")
        for page in pdfReader.pages:
            minutes += page.extractText().strip()

        date_string = pdf_path.stem
        date = datetime.strptime(date_string, "%Y_%m_%d").date()
        page_number = re.findall(r"(^[0-9]+)", minutes)
        if page_number:
            page_number = page_number[0]
        else:
            page_number = ""
        try:
            row = {"date": date, "page_number": page_number, "minutes": minutes.strip()}
            text_df = text_df.append(row, ignore_index=True)
        except ValueError:
            print(f"No date found for file {pdf_path}")
    print(f"Wrote {len(text_df)} rows to the table of minutes.")
    return text_df


class Minutes:
    """Creates an object that represents the minutes for an individual BOE
    meeting. This object contains the methods used to parse the pdf and
    stores the outputs of that parsing as a set of attributes"""

    def __init__(self, pdf_path):

        self.pdf_path = pdf_path
        self.reader = self.read_pdf(pdf_path)
        self.page_count = self.reader.getNumPages()
        self.raw_text = None
        self.clean_text = None
        self.date = self.parse_date(pdf_path)
        self.meeting_date = self.date.strftime("%Y-%m-%d")
        self.agreements = []

    def read_pdf(self, pdf_path):
        """Initializes a PdfFileReader instance from the PyPDF2 library that
        will be called in subsequent methods and attributes

        Args:
            pdf_path (pathlib.Path): The path to the pdf file to read
        Returns:
            reader (PyPDF2.PdfFileReader): Returns an instance of PdfFileReader
            that will be stored in self.reader
        """
        file = open(pdf_path, "rb")
        reader = PyPDF2.PdfFileReader(file, strict=False)
        return reader

    def parse_date(self, pdf_path):
        """Parses a datetime object from the path to the pdf file for use
        in self.meeting_date and self.year

        Args:
            pdf_path (pathlib.Path): Path to pdf ending in */YYYY_MM_DD.pdf
        Returns:
            date (datetime.datetime): Returns a datetime object of the
            date parsed from the pdf_path that will be stored in self.date
        """
        date_str = pdf_path.stem
        date = dt.datetime.strptime(date_str, "%Y_%m_%d")
        return date

    def parse_and_clean_pages(self, page_range=None):
        """Extracts text from pdf pages and stores it in self.raw_text then
        cleans the parsed text and stores the result in self.clean_text

        Args:
            self: Uses the self.reader object created by self.read_pdf()
        Returns:
            N/A: Void function
        """

        # extract the raw text
        text_raw = ""
        if page_range:
            for num in page_range:
                page = self.reader.getPage(num)
                text_raw += page.extractText().strip()
        else:
            for page in self.reader.pages:
                text_raw += page.extractText().strip()
        self.raw_text = text_raw

        # clean the raw text
        clean_text = " ".join(self.raw_text.split())  # remove double spaces
        clean_text = replace_chars(clean_text, REPLACEMENTS)
        self.clean_text = clean_text

    def get_agreements(self):

        pass
